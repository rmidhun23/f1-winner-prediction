# Contributing to F1 Winner Prediction

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Getting Started

### Prerequisites
- Python 3.10+
- Git
- Virtual environment tool

### Setup Development Environment

```bash
# Fork and clone the repository
git clone https://github.com/yourusername/f1-winner-prediction.git
cd f1-winner-prediction

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install development dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install

# Run tests to verify setup
pytest
```

## Development Workflow

### 1. Create a Branch
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/issue-description
```

### 2. Make Changes
- Write clean, readable code
- Follow existing code style
- Add tests for new functionality
- Update documentation as needed

### 3. Test Your Changes
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run pre-commit checks
pre-commit run --all-files

# Test API manually
python -m src.api
```

### 4. Commit Changes
```bash
git add .
git commit -m "feat: add new prediction feature"
```

**Commit Message Format:**
- `feat:` new feature
- `fix:` bug fix
- `docs:` documentation changes
- `test:` adding tests
- `refactor:` code refactoring

### 5. Push and Create PR
```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub.

## Code Standards

### Python Style
- Follow PEP 8
- Use Black for formatting
- Use isort for import sorting
- Maximum line length: 88 characters

### Testing
- Write tests for all new functionality
- Maintain minimum 80% code coverage
- Use descriptive test names
- Mock external dependencies

### Documentation
- Update README.md for user-facing changes
- Add docstrings to new functions/classes
- Update API documentation if needed

## Pull Request Guidelines

### Before Submitting
- [ ] Tests pass locally
- [ ] Pre-commit hooks pass
- [ ] Code coverage maintained
- [ ] Documentation updated
- [ ] Self-review completed

### PR Description
- Clearly describe the changes
- Link related issues
- Include screenshots if UI changes
- List breaking changes if any

## Issue Guidelines

### Bug Reports
- Use the bug report template
- Include reproduction steps
- Provide environment details
- Attach relevant logs/screenshots

### Feature Requests
- Use the feature request template
- Explain the problem being solved
- Describe proposed solution
- Consider alternatives

## Code Review Process

1. **Automated Checks**: All CI checks must pass
2. **Code Owner Review**: Required for all changes
3. **Discussion**: Address feedback and questions
4. **Approval**: Code owner approves changes
5. **Merge**: Squash and merge to main

## Project Structure

```
├── src/                 # Source code
│   ├── api.py          # Flask API
│   ├── predict_winner.py # ML prediction logic
│   └── data_utils.py   # Utility functions
├── tests/              # Test files
├── notebooks/          # Jupyter notebooks
├── data/               # Data files (gitignored)
├── models/             # Trained models (gitignored)
└── deploy/             # Deployment configs
```

## Getting Help

- **Questions**: Use GitHub Discussions
- **Bugs**: Create an issue with bug report template
- **Features**: Create an issue with feature request template
- **Security**: Use private security advisory

## Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- GitHub contributors page

Thank you for contributing to F1 Winner Prediction! 🏎️
