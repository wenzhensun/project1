# Contributing

Thank you for considering contributing to this project.

## Development Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt -r requirements-dev.txt
   ```
2. Run linters:
   ```bash
   flake8 .
   black --check .
   ```
3. Run tests:
   ```bash
   pytest
   ```

## Pull Request Process

1. Fork the repository and create your branch from `main`.
2. Ensure code passes linting and tests.
3. Submit a pull request with a clear description of changes.
