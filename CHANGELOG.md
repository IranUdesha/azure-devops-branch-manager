# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial repository setup for GitHub

## [1.0.0] - 2024-11-01

### Added
- Azure DevOps branch lock/unlock functionality
- Support for single and multiple repository operations
- Command-line interface with argument parsing
- Comprehensive logging system with file and console output
- Configuration management with environment variable support
- Error handling and validation
- Detailed documentation and examples
- Security best practices implementation

### Features
- Lock branches to prevent direct commits
- Unlock branches to allow direct commits
- Process all repositories in a project with wildcard support
- Configurable logging levels and output destinations
- PAT token authentication with Azure DevOps
- Detailed operation summaries and progress tracking

### Security
- Environment variable support for credentials
- Proper .gitignore configuration
- Security warnings and documentation
- No hardcoded secrets in source code

## [0.1.0] - 2024-10-15

### Added
- Initial project structure
- Basic Azure DevOps API integration
- Core branch modification functionality

---

## Release Notes

### v1.0.0
This is the first stable release of the Azure DevOps Branch Manager. The tool provides a complete solution for managing branch protection across Azure DevOps repositories with enterprise-grade security and logging capabilities.

**Breaking Changes:** None (initial release)

**Migration Guide:** None required (initial release)

**Known Issues:** 
- None at this time

**Compatibility:**
- Python 3.7+
- Azure DevOps Server 2019+
- Azure DevOps Services (cloud)