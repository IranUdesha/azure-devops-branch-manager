# Azure DevOps Branch Lock/Unlock Tool

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![CI/CD](https://github.com/IranUdesha/azure-devops-branch-manager/workflows/CI/CD%20Pipeline/badge.svg)](https://github.com/IranUdesha/azure-devops-branch-manager/actions)
[![Security Status](https://img.shields.io/badge/security-compliant-green)](https://github.com/IranUdesha/azure-devops-branch-manager/security)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![No Secrets](https://img.shields.io/badge/secrets-none--detected-brightgreen)

A powerful Python automation tool that allows you to lock or unlock Git branches across Azure DevOps repositories. This tool supports both single repository operations and bulk processing across multiple repositories within a project.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)
- [Security Notes](#security-notes)
- [Contributing](#contributing)

## 📖 Overview

This tool provides a command-line interface to lock and unlock Git branches in Azure DevOps repositories. Branch locking is a crucial feature for:

- **Release Management**: Lock release branches to prevent accidental changes
- **Code Freeze**: Temporarily lock branches during critical periods
- **Compliance**: Ensure certain branches remain unchanged during audits
- **Collaboration**: Coordinate team access to specific branches

The tool uses the Azure DevOps REST API to perform branch lock/unlock operations efficiently across single or multiple repositories.

## ✨ Features

- **🔒 Branch Locking/Unlocking**: Lock or unlock branches to control write access
- **📦 Bulk Operations**: Process multiple repositories simultaneously
- **🎯 Flexible Targeting**: Target specific repositories or all repositories in a project
- **📝 Comprehensive Logging**: Detailed logging with configurable output levels
- **⚙️ Configuration Management**: Flexible configuration system
- **🛡️ Error Handling**: Robust error handling with detailed error reporting
- **🔍 Validation**: Input validation for branch names and repository access
- **📊 Progress Tracking**: Real-time progress updates and operation summaries

## 🔧 Prerequisites

Before using this tool, ensure you have the following:

### Software Requirements
- **Python 3.7 or higher**
- **pip** (Python package installer)

### Azure DevOps Requirements
- **Azure DevOps Organization** access
- **Personal Access Token (PAT)** with appropriate permissions:
  - `Code (Read & Write)`: For repository and branch operations
  - `Project and Team (Read)`: For listing repositories

### Network Requirements
- Internet connectivity to reach Azure DevOps services
- Access to `dev.azure.com` domain

## 📦 Installation

### 1. Clone or Download the Project
```bash
git clone <repository-url>
cd branch-lock-unlock
```

### 2. Create Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\\Scripts\\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Verify Installation
```bash
cd src
python main.py --help
```

## ⚙️ Configuration

### 1. Configure Azure DevOps Settings

Edit the `src/config.py` file and update the Azure DevOps configuration:

```python
# Azure DevOps Configuration
AZURE_CONFIG = {
    "organization": "your-organization-name",    # Replace with your Azure DevOps organization
    "project": "your-project-name",              # Replace with your project name
    "pat": "your-personal-access-token"          # Replace with your PAT (see security notes)
}
```

### 2. Configure Logging (Optional)

Adjust logging settings in `src/config.py`:

```python
# Logging Configuration
LOGGING_CONFIG = {
    "log_level": "INFO",          # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
    "log_to_file": True,          # Enable/disable file logging
    "log_to_console": True,       # Enable/disable console logging
    "log_dir": "logs",            # Log directory path
    "log_filename": "branch_lock_unlock"  # Log file prefix
}
```

### 3. Personal Access Token Setup

1. Go to **Azure DevOps** → **User Settings** → **Personal Access Tokens**
2. Click **"+ New Token"**
3. Configure the token:
   - **Name**: `Branch Lock/Unlock Tool`
   - **Expiration**: Choose appropriate duration
   - **Scopes**: Select the following:
     - ✅ **Code (Read & Write)**
     - ✅ **Project and Team (Read)**
4. Click **"Create"**
5. **Copy the token immediately** (you won't see it again)
6. Update the `pat` field in `config.py`

## 🚀 Usage

### Command Line Syntax

```bash
python main.py --action {lock|unlock} --branch BRANCH_NAME --repo REPOSITORY_SPEC
```

### Parameters

| Parameter | Required | Description | Examples |
|-----------|----------|-------------|----------|
| `--action` | ✅ | Action to perform | `lock`, `unlock` |
| `--branch` | ✅ | Branch name to lock/unlock | `main`, `develop`, `feature/my-feature` |
| `--repo` | ✅ | Repository specification | `my-repo`, `repo1,repo2,repo3`, `*` (all repos) |

### Repository Specification Options

- **Single Repository**: `--repo my-repository`
- **Multiple Repositories**: `--repo repo1,repo2,repo3`
- **All Repositories**: `--repo "*"` or `--repo *`

## 💡 Examples

### Example 1: Lock Main Branch in Single Repository
```bash
python main.py --action lock --branch main --repo my-project-repo
```

### Example 2: Unlock Feature Branch in Multiple Repositories
```bash
python main.py --action unlock --branch feature/new-feature --repo web-app,mobile-app,api-service
```

### Example 3: Lock Release Branch in All Repositories
```bash
python main.py --action lock --branch "Releases/Version_10.1000.0" --repo "*"
```

### Example 4: Unlock Development Branch in All Repositories
```bash
python main.py --action unlock --branch develop --repo "*"
```

## 📁 Project Structure

```
branch-lock-unlock/
├── README.md                          # This documentation file
├── requirements.txt                   # Python dependencies
└── src/                              # Source code directory
    ├── main.py                       # Main application entry point
    ├── config.py                     # Configuration settings
    ├── classes/                      # Core business logic
    │   └── devops_repos.py          # Azure DevOps API client
    ├── config/                       # Configuration management
    │   ├── __init__.py
    │   └── config_manager.py        # Configuration utilities
    ├── utils/                        # Utility functions
    │   ├── __init__.py
    │   └── logger_config.py         # Logging configuration
    └── logs/                         # Generated log files (auto-created)
        └── branch_lock_unlock_*.log  # Timestamped log files
```

### Key Components

- **`main.py`**: Entry point with command-line interface and orchestration logic
- **`config.py`**: Central configuration file for Azure DevOps and logging settings
- **`devops_repos.py`**: Azure DevOps REST API client for branch operations
- **`config_manager.py`**: Configuration management and validation utilities
- **`logger_config.py`**: Logging setup and configuration

## 🔍 Sample Output

```
Azure DevOps Branch Lock/Unlock Tool
==================================================
Configuration Summary:
   Organization: my-organization
   Project: my-project
   Log Level: INFO

Operation Details:
   Action: LOCK
   Branch: main
   Repositories: web-app, mobile-app

Target repositories: web-app, mobile-app

============================================================
Processing repository: web-app
Action: LOCK branch 'main'
Branch 'main' locked successfully.
Successfully locked branch 'main' in repository 'web-app'

============================================================
Processing repository: mobile-app
Action: LOCK branch 'main'
Branch 'main' locked successfully.
Successfully locked branch 'main' in repository 'mobile-app'

============================================================
SUMMARY: 2/2 repositories processed successfully
SUCCESS: All operations completed successfully!
```

## 🛠️ Troubleshooting

### Common Issues

#### 1. Authentication Error (401)
```
Error: 401 Client Error: Unauthorized
```
**Solutions:**
- Verify your Personal Access Token is correct and not expired
- Ensure the PAT has the required permissions (`Code (Read & Write)` and `Project and Team (Read)`)
- Check that the organization and project names are correct

#### 2. Repository Not Found (404)
```
Error: 404 Client Error: Not Found
```
**Solutions:**
- Verify the repository name is spelled correctly
- Ensure you have access to the specified repository
- Check that the repository exists in the specified project

#### 3. Branch Not Found
```
Error: Branch 'branch-name' not found
```
**Solutions:**
- Verify the branch name is correct (case-sensitive)
- Ensure the branch exists in the target repository
- Check for typos in the branch name

#### 4. Permission Denied
```
Error: 403 Client Error: Forbidden
```
**Solutions:**
- Verify your PAT has write permissions to the repository
- Ensure you're a member of the project with appropriate permissions
- Contact your Azure DevOps administrator for access

### Enable Debug Logging

For detailed troubleshooting, enable debug logging in `config.py`:

```python
LOGGING_CONFIG = {
    "log_level": "DEBUG",  # Changed from INFO to DEBUG
    # ... other settings
}
```

### Log File Location

Log files are automatically created in the `src/logs/` directory with timestamped filenames:
```
logs/branch_lock_unlock_20231101_143022.log
```

## 🔒 Security Notes

### ⚠️ **CRITICAL: Never commit your Personal Access Token to version control!**

### Best Practices for PAT Security:

1. **Use Environment Variables** (Recommended):
   ```bash
   # Set environment variable
   export AZURE_PAT="your-personal-access-token"
   
   # Update config.py to use environment variable
   "pat": os.getenv("AZURE_PAT", "")
   ```

2. **Use a `.env` file** (Not committed to git):
   ```bash
   # Create .env file
   echo "AZURE_PAT=your-personal-access-token" > .env
   
   # Add .env to .gitignore
   echo ".env" >> .gitignore
   ```

3. **Limit PAT Scope**: Only grant necessary permissions
4. **Set Expiration**: Use the shortest practical expiration time
5. **Regular Rotation**: Rotate PATs regularly

### Configuration Security Checklist:

- [ ] PAT is not hardcoded in `config.py`
- [ ] PAT has minimal required permissions
- [ ] PAT has appropriate expiration date
- [ ] `.env` file is in `.gitignore` (if used)
- [ ] Configuration files are reviewed before commits

## 🤝 Contributing

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/new-feature`
3. **Make your changes** and test thoroughly
4. **Update documentation** if needed
5. **Commit your changes**: `git commit -m "Add new feature"`
6. **Push to the branch**: `git push origin feature/new-feature`
7. **Create a Pull Request**

### Development Guidelines:

- Follow Python PEP 8 style guidelines
- Add appropriate error handling
- Include logging for important operations
- Update documentation for new features
- Test with multiple repositories and scenarios

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues, questions, or contributions:

1. **Check the [Troubleshooting](#troubleshooting) section**
2. **Review existing issues** in the project repository
3. **Create a new issue** with detailed information:
   - Steps to reproduce
   - Expected vs actual behavior
   - Configuration details (without sensitive data)
   - Log file excerpts

---

**Happy Branch Management! 🚀**
