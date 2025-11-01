#!/usr/bin/env python3
"""
Configuration validation script for Azure DevOps Branch Manager
This script helps users validate their configuration before using the tool.

Usage:
    python validate_config.py
    python validate_config.py --use-env-vars
"""

import sys
import os
import argparse
from pathlib import Path

# Add src directory to path for imports
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

try:
    from config.config_manager import get_config_manager
except ImportError as e:
    print(f"❌ Error importing configuration manager: {e}")
    print("Please ensure you're running this script from the project root directory.")
    sys.exit(1)


def test_azure_connection(config_manager):
    """Test Azure DevOps connection"""
    print("\n🔗 Testing Azure DevOps Connection...")
    
    try:
        azure_config = config_manager.get_azure_config()
        
        # Import here to avoid circular imports
        from classes.devops_repos import az_devops
        
        # Create a test client
        client = az_devops(
            organization=azure_config['organization'],
            project=azure_config['project'],
            repository="",  # Empty repository for basic connection test
            pat=azure_config['pat']
        )
        
        # Try to get repositories (this will test authentication)
        response = client.get_all_repositories()
        
        if response and 'value' in response:
            repo_count = len(response['value'])
            print(f"✅ Connection successful! Found {repo_count} repositories.")
            return True
        else:
            print("❌ Connection failed: Unable to retrieve repositories.")
            return False
            
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False


def main():
    """Main validation function"""
    parser = argparse.ArgumentParser(
        description="Validate Azure DevOps Branch Manager configuration"
    )
    parser.add_argument(
        "--use-env-vars",
        action="store_true",
        help="Use environment variables instead of config.py"
    )
    parser.add_argument(
        "--test-connection",
        action="store_true",
        help="Test Azure DevOps connection (requires valid credentials)"
    )
    
    args = parser.parse_args()
    
    print("🔧 Azure DevOps Branch Manager - Configuration Validator")
    print("=" * 60)
    
    # Configuration method
    config_method = "Environment Variables" if args.use_env_vars else "config.py"
    print(f"📋 Configuration Method: {config_method}")
    
    # Create config manager
    try:
        config_manager = get_config_manager(use_env_vars=args.use_env_vars)
    except Exception as e:
        print(f"❌ Failed to create configuration manager: {e}")
        sys.exit(1)
    
    # Validate configuration
    print("\n🔍 Validating Configuration...")
    if config_manager.validate_config():
        print("✅ Configuration validation passed!")
    else:
        print("❌ Configuration validation failed!")
        sys.exit(1)
    
    # Print configuration summary
    print("\n📊 Configuration Summary:")
    config_manager.print_config_summary()
    
    # Test connection if requested
    if args.test_connection:
        connection_success = test_azure_connection(config_manager)
        if not connection_success:
            sys.exit(1)
    
    print("\n🎉 All validations completed successfully!")
    print("\n💡 Your configuration is ready to use with the Azure DevOps Branch Manager!")
    print("\nNext steps:")
    print("  1. Navigate to the src directory: cd src")
    print("  2. Run the tool: python main.py --help")
    print("  3. Example usage: python main.py --action lock --branch main --repo my-repo")


if __name__ == "__main__":
    main()