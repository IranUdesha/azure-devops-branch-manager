"""
Logging configuration module for Azure DevOps branch creation script.
This module provides centralized logging setup and utilities.
"""

import os
import sys
import logging
from datetime import datetime


def setup_logging(log_level, log_to_file=True, log_to_console=True, log_dir='logs', log_filename='branch_creation'):
    """
    Setup logging configuration with customizable options.
    
    Args:
        log_level: Logging level (logging.DEBUG, logging.INFO, etc.)
        log_to_file: Whether to log to file
        log_to_console: Whether to log to console
    
    Returns:
        logger: Configured logger instance
    """
    level_map = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL,
    }
    log_level = level_map.get(str(log_level).upper(), logging.INFO)
                
    # Create logs directory if it doesn't exist
    log_dir = log_dir
    if log_to_file and not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Create log filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_filename = os.path.join(log_dir, f'{log_filename}_{timestamp}.log') if log_to_file else None
    
    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    
    # Get logger
    logger = logging.getLogger('azure_devops_branch_creator')
    logger.setLevel(log_level)
    
    # Clear any existing handlers
    logger.handlers.clear()
    
    # Add handlers based on configuration
    if log_to_file and log_filename:
        file_handler = logging.FileHandler(log_filename)
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    if log_to_console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(log_level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    if log_to_file and log_filename:
        logger.info(f"Logging initialized. Log Level: {log_level}. Log file: {log_filename}")
    else:
        logger.info("Logging initialized (console only)")
    
    return logger


def get_logger():
    """
    Get the configured logger instance.
    If not already configured, will setup with default settings.
    
    Returns:
        logger: Logger instance
    """
    logger = logging.getLogger('azure_devops_branch_creator')
    
    # If logger has no handlers, set it up with defaults
    if not logger.handlers:
        logger = setup_logging()
    
    return logger


class LoggerMixin:
    """
    Mixin class to add logging capabilities to any class.
    Usage: class MyClass(LoggerMixin): ...
    Then use self.logger.info("message") in the class methods.
    """
    
    @property
    def logger(self):
        if not hasattr(self, '_logger'):
            self._logger = get_logger()
        return self._logger


# Convenience functions for different log levels
def log_info(message):
    """Log info message"""
    get_logger().info(message)


def log_error(message):
    """Log error message"""
    get_logger().error(message)


def log_warning(message):
    """Log warning message"""
    get_logger().warning(message)


def log_debug(message):
    """Log debug message"""
    get_logger().debug(message)