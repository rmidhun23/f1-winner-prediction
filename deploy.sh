#!/bin/bash

# Configuration
IMAGE_NAME="f1-winner-prediction"
CLUSTER_NAME="f1-prediction-cluster"
TAG="latest"

# Check if cluster exists, create if not
if ! kind get clusters | grep -q "^${CLUSTER_NAME}$"; then
    echo "Creating kind cluster: ${CLUSTER_NAME}..."
    kind create cluster --name ${CLUSTER_NAME}
else
    echo "Using existing kind cluster: ${CLUSTER_NAME}"
fi

# Set kubectl context to kind cluster
kubectl cluster-info --context kind-${CLUSTER_NAME}

echo "Building image with Paketo buildpacks..."

if ! pack build ${IMAGE_NAME}:${TAG} \
    --builder paketobuildpacks/builder:base \
    --trust-builder \
    --verbose \
    --pull-policy if-not-present \
    --env BP_DISABLE_SBOM=true \
    --env BP_CPYTHON_VERSION=3.10.12 \
    --env BP_PIP_VERSION=23.x; then

    echo "Buildpack build failed, falling back to Docker build..."

    # Use existing Dockerfile
    docker build -t ${IMAGE_NAME}:${TAG} .

    # Verify image exists
    if ! docker images | grep -q "${IMAGE_NAME}"; then
        echo "ERROR: Failed to build Docker image"
        exit 1
    fi
fi

# Load image into kind cluster
echo "Loading image into kind cluster..."
kind load docker-image ${IMAGE_NAME}:${TAG} --name ${CLUSTER_NAME}

# Deploy to Kubernetes
echo "Deploying to Kubernetes..."
kubectl apply -f deploy/k8s/namespace.yaml
kubectl apply -f deploy/k8s/pvc.yaml
kubectl apply -f deploy/k8s/deployment.yaml
kubectl apply -f deploy/k8s/service.yaml

echo "Deployment complete!"
echo "To access the service, run: kubectl port-forward svc/f1-api-service 9010:9010 -n f1-ml"
