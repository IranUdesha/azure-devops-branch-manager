# Azure DevOps Branch Lock/Unlock Tool

A Python command-line tool for locking and unlocking branches in Azure DevOps repositories. This tool allows you to manage branch protection across single or multiple repositories in your Azure DevOps projects.

## 🎯 Purpose

This tool is designed to help DevOps teams and developers manage branch protection in Azure DevOps by:

- **Locking branches** to prevent commits and force changes through pull requests
- **Unlocking branches** to allow direct commits when needed
- **Bulk operations** across multiple repositories
- **Automated logging** for audit trails and troubleshooting

## ✨ Features

- Lock/unlock branches in single or multiple Azure DevOps repositories
- Support for all repositories in a project with a single command
- Comprehensive logging with file and console output
- Environment variable support for secure credential management
- Detailed operation summaries and error reporting
- Command-line interface with intuitive arguments

## 📋 Prerequisites

Before running this tool, you need:

### 1. Azure DevOps Setup
- **Azure DevOps Organization** and **Project** access
- **Personal Access Token (PAT)** with the following permissions:
  - `Code (read & write)` - Required for repository access
  - `Project and team (read)` - Required for project operations

### 2. Python Environment
- **Python 3.7 or higher**
- Required Python packages (see Installation section)

### 3. Network Access
- Internet connection to reach Azure DevOps APIs (`dev.azure.com`)
- Corporate firewall configurations may need to allow HTTPS traffic

## 🚀 Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd azure-devops-branch-manager
   ```

2. **Install required dependencies:**
   ```bash
   pip install requests
   ```

3. **Configure the application:**
   
   **Option A: Using config.py (Default)**
   ```python
   # Edit src/config.py
   AZURE_CONFIG = {
       "organization": "your-organization-name",
       "project": "your-project-name", 
       "pat": "your-personal-access-token"
   }
   ```

   **Option B: Using Environment Variables (Recommended for production)**
   ```bash
   # Windows (PowerShell)
   $env:AZURE_ORGANIZATION="your-organization-name"
   $env:AZURE_PROJECT="your-project-name"
   $env:AZURE_PAT="your-personal-access-token"

   # Linux/macOS
   export AZURE_ORGANIZATION="your-organization-name"
   export AZURE_PROJECT="your-project-name"
   export AZURE_PAT="your-personal-access-token"
   ```

## 🔧 Configuration

### Configuration Files

- **`src/config.py`** - Main configuration file with Azure DevOps settings
- **`src/config/config_manager.py`** - Configuration management logic
- **`src/utils/logger_config.py`** - Logging configuration

### Configuration Options

| Setting | Description | Default |
|---------|-------------|---------|
| `organization` | Azure DevOps organization name | Required |
| `project` | Azure DevOps project name | Required |
| `pat` | Personal Access Token | Required |
| `log_level` | Logging level (DEBUG, INFO, WARNING, ERROR) | `DEBUG` |
| `log_to_file` | Enable file logging | `True` |
| `log_to_console` | Enable console logging | `True` |
| `log_dir` | Log files directory | `logs` |

## 📖 Usage

### Basic Commands

Navigate to the `src` directory before running commands:

```bash
cd src
```

**Lock a branch in a specific repository:**
```bash
python main.py --action lock --branch main --repo my-repository
```

**Unlock a branch in a specific repository:**
```bash
python main.py --action unlock --branch feature/test --repo my-repository
```

**Lock a branch in multiple repositories:**
```bash
python main.py --action lock --branch main --repo repo1,repo2,repo3
```

**Lock a branch in ALL repositories in the project:**
```bash
python main.py --action lock --branch main --repo "*"
```

### Command Line Arguments

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `--action` | ✅ | Action to perform: `lock` or `unlock` | `--action lock` |
| `--branch` | ✅ | Branch name to lock/unlock | `--branch main` |
| `--repo` | ✅ | Repository name(s) or `"*"` for all repos | `--repo my-repo` or `--repo "repo1,repo2"` |

### Examples

```bash
# Lock main branch in a single repository
python main.py --action lock --branch main --repo web-app

# Unlock development branch in multiple repositories  
python main.py --action unlock --branch development --repo api-service,web-app,database

# Lock release branch in all repositories
python main.py --action lock --branch release/v2.0 --repo "*"

# Unlock feature branch with special characters
python main.py --action unlock --branch "feature/user-auth" --repo auth-service
```

## 📁 Project Structure

```
src/
├── main.py                 # Main application entry point
├── config.py              # Configuration settings
├── classes/
│   └── devops_repos.py    # Azure DevOps API client
├── config/
│   ├── __init__.py
│   └── config_manager.py  # Configuration management
├── utils/
│   ├── __init__.py
│   └── logger_config.py   # Logging utilities
└── logs/                  # Log files (created automatically)
```

## 🔐 Security Best Practices

1. **Never commit PAT tokens to version control**
2. **Use environment variables for credentials in production**
3. **Limit PAT permissions to minimum required scope**
4. **Regularly rotate Personal Access Tokens**
5. **Review logs for unauthorized access attempts**

## 🐛 Troubleshooting

### Common Issues

**Authentication Errors:**
- Verify PAT token has correct permissions
- Check organization and project names are correct
- Ensure PAT token hasn't expired

**Branch Not Found:**
- Verify branch name spelling and case sensitivity
- Check if branch exists in the target repository
- Use full branch path (e.g., `refs/heads/main` becomes `main`)

**Network Errors:**
- Check internet connectivity
- Verify corporate firewall settings
- Ensure access to `dev.azure.com`

### Logging

Logs are automatically created in the `logs/` directory with detailed information about:
- Configuration validation
- API requests and responses  
- Success and error messages
- Operation summaries

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section above
2. Review log files for detailed error messages
3. Create an issue in the repository with:
   - Error message
   - Command used
   - Log file contents (remove sensitive information)

## 🏷️ Version History

- **v1.0.0** - Initial release with basic lock/unlock functionality
- Support for single and multiple repository operations
- Comprehensive logging and error handling