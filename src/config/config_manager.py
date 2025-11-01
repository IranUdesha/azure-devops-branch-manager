"""
Configuration Manager for Azure DevOps Branch Creator
Supports both Python config files and environment variables
"""

import os
import logging
from typing import Any, Dict, Optional


class ConfigManager:
    """Configuration manager that supports multiple configuration sources"""
    
    def __init__(self, use_env_vars: bool = False, env_file_path: Optional[str] = None):
        self.use_env_vars = use_env_vars
        self.env_file_path = env_file_path
        self._config = {}
        self._load_configuration()
    
    def _load_configuration(self):
        """Load configuration from the appropriate source"""
        if self.use_env_vars:
            self._load_from_env()
        else:
            self._load_from_config_file()
    
    def _load_from_config_file(self):
        """Load configuration from config.py file"""
        try:
            import sys
            import os
            # Add parent directory to path to import config
            parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            if parent_dir not in sys.path:
                sys.path.insert(0, parent_dir)
            
            # Import the config module from parent directory
            import importlib.util
            config_path = os.path.join(parent_dir, 'config.py')
            spec = importlib.util.spec_from_file_location("config_file", config_path)
            config_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(config_module)
            
            AZURE_CONFIG = config_module.AZURE_CONFIG
            LOGGING_CONFIG = config_module.LOGGING_CONFIG
            
            self._config = {
                "azure": AZURE_CONFIG,
                # "repository": REPOSITORY_CONFIG,
                "logging": LOGGING_CONFIG,
            }
        except ImportError as e:
            raise ImportError(f"Could not import configuration: {e}")
    
    def _load_from_env(self):
        """Load configuration from environment variables"""
        if self.env_file_path and os.path.exists(self.env_file_path):
            self._load_env_file()
        
        self._config = {
            "azure": {
                "organization": os.getenv("AZURE_ORGANIZATION", ""),
                "project": os.getenv("AZURE_PROJECT", ""),
                "pat": os.getenv("AZURE_PAT", "")
            },
            "repository": {
                "repository": os.getenv("TARGET_REPOSITORY") or None,
                "source_branch": os.getenv("SOURCE_BRANCH", "main"),
                "new_branch": os.getenv("NEW_BRANCH", "feature/branch01")
            },
            "logging": {
                "log_level": os.getenv("LOG_LEVEL", "INFO"),
                "log_to_file": os.getenv("LOG_TO_FILE", "true").lower() == "true",
                "log_to_console": os.getenv("LOG_TO_CONSOLE", "true").lower() == "true",
                "log_dir": os.getenv("LOG_DIR", "logs"),
                "log_filename": os.getenv("LOG_FILENAME", "branch_lock_unlock")
            },
            "pipeline": {
                "run_pipeline_after_branch_creation": os.getenv("RUN_PIPELINE_AFTER_BRANCH_CREATION", "true").lower() == "true"
            }
        }
    
    def _load_env_file(self):
        """Load environment variables from .env file"""
        try:
            with open(self.env_file_path, 'r') as file:
                for line in file:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        key, value = line.split('=', 1)
                        os.environ[key] = value
        except Exception as e:
            print(f"Warning: Could not load .env file: {e}")
    
    def get(self, section: str, key: str, default: Any = None) -> Any:
        """Get a configuration value"""
        return self._config.get(section, {}).get(key, default)
    
    def get_section(self, section: str) -> Dict[str, Any]:
        """Get an entire configuration section"""
        return self._config.get(section, {})
    
    def get_azure_config(self) -> Dict[str, str]:
        """Get Azure DevOps configuration"""
        return self.get_section("azure")
    
    def get_logging_config(self) -> Dict[str, Any]:
        """Get logging configuration"""
        return self.get_section("logging")
    
    def validate_config(self) -> bool:
        """Validate that required configuration is present and valid"""
        errors = []
        
        # Validate Azure configuration
        azure_config = self.get_azure_config()
        azure_required = ["organization", "project", "pat"]
        
        for field in azure_required:
            value = azure_config.get(field)
            if not value or (isinstance(value, str) and value.strip() == ""):
                errors.append(f"Azure config: '{field}' is required and cannot be empty")
        
        # Validate PAT format (basic check)
        pat = azure_config.get("pat", "")
        if pat and (len(pat) < 20 or not pat.replace("-", "").replace("_", "").isalnum()):
            errors.append("PAT format appears invalid. Ensure you're using a valid Azure DevOps Personal Access Token")
        
        # Validate logging configuration
        logging_config = self.get_logging_config()
        valid_log_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        log_level = logging_config.get("log_level", "").upper()
        if log_level not in valid_log_levels:
            errors.append(f"Invalid log level '{log_level}'. Valid options: {valid_log_levels}")
        
        # Print errors if any
        if errors:
            print("❌ Configuration Validation Failed:")
            for i, error in enumerate(errors, 1):
                print(f"   {i}. {error}")
            print("\n💡 Please fix the above issues in your configuration and try again.")
            return False
        
        print("✅ Configuration validation passed")
        return True
    
    def print_config_summary(self):
        """Print a summary of the current configuration (excluding sensitive data)"""
        print("📋 Configuration Summary:")
        print(f"   Organization: {self.get('azure', 'organization')}")
        print(f"   Project: {self.get('azure', 'project')}")
        print(f"   Log Level: {self.get('logging', 'log_level')}")


# Convenience function to create config manager
def get_config_manager(use_env_vars: bool = False, env_file: str = ".env") -> ConfigManager:
    """Create and return a configuration manager"""
    env_file_path = env_file if use_env_vars else None
    return ConfigManager(use_env_vars=use_env_vars, env_file_path=env_file_path)