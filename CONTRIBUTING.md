# Contributing to Azure DevOps Branch Manager

Thank you for your interest in contributing to this project! We welcome contributions from the community.

## 🚀 Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/azure-devops-branch-manager.git
   cd azure-devops-branch-manager
   ```
3. **Create a new branch** for your feature or bugfix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## 📝 Development Guidelines

### Code Style
- Follow [PEP 8](https://pep8.org/) Python style guidelines
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and single-purpose

### Testing
- Add tests for new features
- Ensure existing tests pass
- Test with multiple Azure DevOps scenarios

### Logging
- Include appropriate logging for new operations
- Use existing logger configuration
- Log errors with sufficient detail for debugging

## 🔧 Setting Up Development Environment

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Azure DevOps access:**
   - Set up environment variables or config.py
   - Ensure you have appropriate PAT permissions

3. **Test your changes:**
   ```bash
   cd src
   python main.py --help
   ```

## 📋 Pull Request Process

1. **Update documentation** if you're changing functionality
2. **Add or update tests** as appropriate
3. **Update CHANGELOG.md** with your changes
4. **Ensure your code follows the style guidelines**
5. **Submit a pull request** with:
   - Clear description of changes
   - Screenshots if UI changes
   - Test results
   - Any breaking changes noted

## 🐛 Bug Reports

When reporting bugs, please include:
- **Operating system** and Python version
- **Azure DevOps organization/project setup** (without sensitive info)
- **Complete error message** and stack trace
- **Steps to reproduce** the issue
- **Expected vs actual behavior**

## 💡 Feature Requests

For feature requests, please:
- **Check existing issues** to avoid duplicates
- **Describe the use case** and problem you're solving
- **Provide examples** of how the feature would be used
- **Consider implementation complexity** and breaking changes

## 🔒 Security

- **Never commit secrets** or PAT tokens
- **Use environment variables** for credentials
- **Report security issues** privately before public disclosure

## 📄 Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help newcomers to the project
- Follow professional communication standards

## ❓ Questions

If you have questions about contributing:
- Check the [README.md](README.md) for documentation
- Review existing issues and pull requests
- Create an issue for discussion

Thank you for contributing! 🎉