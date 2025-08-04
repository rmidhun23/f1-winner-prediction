# Security Policy

## About This Project

This is a personal learning project for F1 race prediction using machine learning. While it's primarily educational, I take security seriously for any code that might be deployed or used by others.

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| main    | ✅ Yes             |
| develop | ⚠️ Development only |

## Reporting a Vulnerability

### For Security Issues

If you discover a security vulnerability, please report it privately:

1. **GitHub Security Advisories** (preferred): [Create a security advisory](https://github.com/rmidhun23/f1-winner-prediction/security/advisories/new)
2. **Direct contact**: Create an issue and mention it's security-related

### What to Include

- Description of the vulnerability
- Steps to reproduce (if applicable)
- Potential impact
- Suggested fix (if you have one)

### Response Timeline

As this is a personal project with limited time:
- **Initial response**: Within 2-3 weeks
- **Status update**: Within 4-6 weeks
- **Fix timeline**: 1-3 months depending on severity and complexity

*Note: I work on this project in my spare time, so please be patient. Critical security issues will be prioritized.*

### Security Considerations

This project includes:
- **Flask API** - Potential for injection attacks
- **File uploads/downloads** - Path traversal risks
- **Model loading** - Pickle deserialization concerns
- **Docker deployment** - Container security

### Not Security Issues

These are **not** considered security vulnerabilities:
- Incorrect F1 predictions (it's ML, not perfect!)
- Performance issues
- Missing features
- Documentation gaps

## Security Best Practices

If you're deploying this project:
- Use HTTPS in production
- Validate all API inputs
- Run in isolated containers
- Keep dependencies updated
- Don't expose internal endpoints

## Acknowledgments

Security researchers who help improve this project will be acknowledged in the README (with permission).

Thanks for helping keep this F1 prediction project secure! 🏎️
