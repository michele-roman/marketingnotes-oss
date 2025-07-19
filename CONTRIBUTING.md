# Contributing to MarketingNotes.ai

Thank you for your interest in contributing to MarketingNotes.ai! This document provides guidelines and information for contributors.

## 🤝 How to Contribute

### Reporting Issues

Before creating an issue, please:

1. **Search existing issues** to see if your problem has already been reported
2. **Use the issue templates** when available
3. **Provide detailed information** including:
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details (OS, Docker version, etc.)
   - Error messages and logs

### Suggesting Features

We welcome feature suggestions! When suggesting a feature:

1. **Describe the problem** you're trying to solve
2. **Explain your proposed solution**
3. **Consider the impact** on existing users
4. **Think about implementation** complexity

### Code Contributions

#### Getting Started

1. **Fork the repository**
2. **Clone your fork**:
   ```bash
   git clone https://github.com/michele-roman/marketingnotes-oss.git
   cd marketingnotes-oss
   ```

3. **Set up development environment**:
   ```bash
   # Install Python dependencies
   poetry install
   
   # Install Node.js dependencies
   npm install
   
   # Build Tailwind CSS
   npm run build:css
   
   # Run migrations
   poetry run python manage.py migrate
   ```

4. **Create a feature branch**:
   ```bash
   git checkout -b feature/amazing-feature
   ```

#### Development Guidelines

##### Code Style

- **Python**: Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- **JavaScript**: Use consistent formatting
- **HTML/CSS**: Follow existing patterns
- **Django**: Follow Django best practices

##### Commit Messages

Use clear, descriptive commit messages:

```bash
# Good
git commit -m "Add user authentication system"

# Better
git commit -m "feat: add user authentication with JWT tokens

- Implement JWT-based authentication
- Add login/logout endpoints
- Include user profile management
- Add tests for auth functionality"

# Bad
git commit -m "fix stuff"
```

##### Testing

- **Write tests** for new features
- **Update tests** when modifying existing code
- **Ensure all tests pass** before submitting

```bash
# Run tests
poetry run python manage.py test

# Run with coverage
poetry run coverage run --source='.' manage.py test
poetry run coverage report
```

##### Documentation

- **Update README.md** if adding new features
- **Add docstrings** to new functions and classes
- **Update API documentation** if changing endpoints

#### Submitting Changes

1. **Test your changes**:
   ```bash
   # Run tests
   poetry run python manage.py test
   
   # Test with Docker
   docker-compose up --build
   ```

2. **Commit your changes**:
   ```bash
   git add .
   git commit -m "feat: add amazing new feature"
   git push origin feature/amazing-feature
   ```

3. **Create a Pull Request**:
   - Use the PR template
   - Describe your changes clearly
   - Link related issues
   - Include screenshots for UI changes

## 🏗️ Project Structure

```
marketingnotes_oss/
├── app/                    # Main Django application
│   ├── models.py          # Database models
│   ├── views.py           # View logic
│   ├── urls.py            # URL routing
│   ├── agent.py           # AI agent implementations
│   ├── admin.py           # Django admin configuration
│   └── tests.py           # Application tests
├── templates/             # HTML templates
│   ├── base.html          # Base template
│   ├── api_keys.html      # API keys management
│   └── chat/              # Chat templates
├── static/                # Static files
│   ├── input.css          # Tailwind CSS input
│   └── output.css         # Compiled CSS
├── marketingnotes_oss/    # Django project settings
├── tests/                 # Additional tests
├── docs/                  # Documentation
└── scripts/               # Utility scripts
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
poetry run python manage.py test

# Run specific app tests
poetry run python manage.py test app

# Run with coverage
poetry run coverage run --source='.' manage.py test
poetry run coverage report
poetry run coverage html  # Generate HTML report
```

### Test Guidelines

- **Unit tests** for individual functions
- **Integration tests** for API endpoints
- **Frontend tests** for UI components
- **Docker tests** for container functionality

## 🐳 Docker Development

### Local Development with Docker

```bash
# Start development environment
docker-compose up -d

# View logs
docker-compose logs -f web

# Access Django shell
docker-compose exec web poetry run python manage.py shell

# Run tests in container
docker-compose exec web poetry run python manage.py test
```

### Building for Production

```bash
# Build production image
docker build -t marketingnotes-oss:latest .

# Test production build
docker run -p 8000:8000 marketingnotes-oss:latest
```

## 📝 Documentation

### Code Documentation

- **Docstrings**: Use Google or NumPy style
- **Type hints**: Add type annotations to functions
- **Comments**: Explain complex logic

### API Documentation

- **Endpoint descriptions**: Document all API endpoints
- **Request/response examples**: Include examples
- **Error codes**: Document error responses

## 🔒 Security

### Security Guidelines

- **Never commit secrets** (API keys, passwords, etc.)
- **Use environment variables** for sensitive data
- **Validate user input** to prevent injection attacks
- **Follow OWASP guidelines** for web security

### Reporting Security Issues

For security issues, please:

1. **Don't create public issues**
2. **Email security@yourdomain.com** (replace with actual email)
3. **Include detailed information** about the vulnerability
4. **Allow time for response** before public disclosure

## 🎯 Areas for Contribution

### High Priority

- **Bug fixes** and performance improvements
- **Security enhancements**
- **Documentation improvements**
- **Test coverage** improvements

### Medium Priority

- **New AI service integrations**
- **UI/UX improvements**
- **Additional features**
- **Performance optimizations**

### Low Priority

- **Code refactoring**
- **Style improvements**
- **Minor enhancements**

## 📞 Getting Help

- **GitHub Issues**: For bugs and feature requests
- **GitHub Discussions**: For questions and general discussion
- **Documentation**: Check the wiki and docs folder
- **Code of Conduct**: Please read and follow our CoC

## 🙏 Recognition

Contributors will be recognized in:

- **README.md** contributors section
- **Release notes** for significant contributions
- **GitHub contributors** page

Thank you for contributing to MarketingNotes.ai! 🚀 