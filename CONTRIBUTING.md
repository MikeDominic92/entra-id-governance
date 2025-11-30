# Contributing to Entra ID Governance Toolkit

Thank you for your interest in contributing! This document provides guidelines for contributing to this project.

## Code of Conduct

- Be respectful and professional
- Focus on constructive feedback
- Welcome newcomers and help them learn

## How to Contribute

### Reporting Bugs

1. Check if the issue already exists
2. Use the issue template
3. Provide detailed reproduction steps
4. Include environment details (Python version, OS, etc.)

### Suggesting Features

1. Open an issue with the "enhancement" label
2. Describe the use case clearly
3. Explain the expected behavior
4. Consider implementation complexity

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Write/update tests
5. Ensure tests pass (`pytest`)
6. Format code (`black src/`)
7. Commit your changes (`git commit -m 'Add amazing feature'`)
8. Push to branch (`git push origin feature/amazing-feature`)
9. Open a Pull Request

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/entra-id-governance.git
cd entra-id-governance

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install development dependencies
pip install -r requirements.txt
pip install black flake8 mypy pytest-cov

# Run tests
pytest --cov=src
```

## Code Style

- Follow PEP 8
- Use type hints where possible
- Write docstrings for all public functions
- Keep functions focused and small
- Use Black for formatting: `black src/`

## Testing

- Write tests for new features
- Maintain test coverage above 80%
- Use pytest fixtures for common setups
- Mock external API calls

## Documentation

- Update README.md for user-facing changes
- Add docstrings to new functions/classes
- Update relevant documentation in `docs/`

## Commit Messages

Follow conventional commits:

```
feat: add support for named locations in CA policies
fix: resolve token caching issue
docs: update API documentation
test: add tests for PIM analyzer
refactor: simplify graph client retry logic
```

## Review Process

1. Maintainer will review PR within 7 days
2. Address review comments
3. Once approved, maintainer will merge

## Questions?

Open an issue with the "question" label.

Thank you for contributing!
