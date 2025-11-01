"""
Config package for Azure DevOps tools.
Contains configuration management modules.
"""

from .config_manager import ConfigManager, get_config_manager

__all__ = ['ConfigManager', 'get_config_manager']