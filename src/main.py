
import sys
import argparse
from classes.devops_repos import az_devops
from utils import setup_logging, get_logger
from config import get_config_manager


# Initialize configuration manager
# Set use_env_vars=True to use environment variables instead of config.py
config_manager = get_config_manager(use_env_vars=False)

# Validate configuration
if not config_manager.validate_config():
    exit(1)

# Get configuration sections
azure_config = config_manager.get_azure_config()
logging_config = config_manager.get_logging_config()


# Initialize logger with configuration
logger = setup_logging(
    log_level=logging_config['log_level'],
    log_to_file=logging_config['log_to_file'],
    log_to_console=logging_config['log_to_console'],
    log_dir=logging_config['log_dir'],
    log_filename=logging_config.get('log_filename')
)

# Extract variables for backward compatibility
organization = azure_config['organization']
project = azure_config['project']
PAT = azure_config['pat']    

# Lock a specific branch in an Azure DevOps repository
def lock_branch_in_repository(organization: str, project: str, pat: str, repository: str, branch_name: str) -> bool:
    """Lock a specific branch in the given Azure DevOps repository"""
    try:
        client = az_devops(organization, project, repository, pat)
        
        logger.info(f"Locking branch '{branch_name}' in repository '{repository}'")
        result = client.modify_branch(branch_name, lock=True)
        
        # Check if the result is an exception (in case modify_branch returns exceptions)
        if isinstance(result, Exception):
            raise result
        
        logger.info(f"Successfully locked branch '{branch_name}' in repository '{repository}'")
        return True
        
    except Exception as e:
        logger.error(f"An error occurred while locking branch '{branch_name}' in repository '{repository}': {e}")
        return False


# Unlock a specific branch in an Azure DevOps repository
def unlock_branch_in_repository(organization: str, project: str, pat: str, repository: str, branch_name: str) -> bool:
    """Unlock a specific branch in the given Azure DevOps repository"""
    try:
        client = az_devops(organization, project, repository, pat)
        
        logger.info(f"Unlocking branch '{branch_name}' in repository '{repository}'")
        result = client.modify_branch(branch_name, lock=False)
        
        # Check if the result is an exception (in case modify_branch returns exceptions)
        if isinstance(result, Exception):
            raise result
            
        logger.info(f"Successfully unlocked branch '{branch_name}' in repository '{repository}'")
        return True
        
    except Exception as e:
        logger.error(f"An error occurred while unlocking branch '{branch_name}' in repository '{repository}': {e}")
        return False


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description='Azure DevOps Branch Lock/Unlock Tool',
        epilog='''
Examples:
  python branch.py --action lock --branch main --repo my-repo
  python branch.py --action unlock --branch feature/test --repo repo1,repo2,repo3
  python branch.py --action lock --branch main --all-repos
        ''',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--action', 
        choices=['lock', 'unlock'], 
        required=True,
        help='Action to perform on the branch (lock or unlock)'
    )
    
    parser.add_argument(
        '--branch', 
        required=True,
        help='Name of the branch to lock/unlock'
    )
    
    # Repository selection - mutually exclusive group
    repo_group = parser.add_mutually_exclusive_group(required=True)
    repo_group.add_argument(
        '--repo', 
        help='Repository name(s). Use comma-separated list for multiple repos. If omitted, all repositories in the project will be processed.'
    )

    return parser.parse_args()


def get_repositories_list(client, args):
    """Get the list of repositories to process based on arguments"""
    
    # If --repo is not provided, fetch all repositories
    if not args.repo or args.repo == "*":
        logger.info("Fetching all repositories in the project...")
        repos_response = client.get_all_repositories()
        if repos_response and 'value' in repos_response:
            repos = [repo['name'] for repo in repos_response['value']]
            logger.info(f"Found {len(repos)} repositories: {', '.join(repos)}")
            return repos
        else:
            logger.error("Failed to fetch repositories or no repositories found")
            return []
    else:
        # Parse comma-separated repository list
        repos = [repo.strip() for repo in args.repo.split(',') if repo.strip()]
        logger.info(f"Target repositories: {', '.join(repos)}")
        return repos


def process_repositories(args, organization, project, pat):
    """Process the lock/unlock action for specified repositories"""
    # Create a client to get repository list if needed
    temp_client = az_devops(organization, project, "", pat)
    
    # Get the list of repositories to process
    repositories = get_repositories_list(temp_client, args)

    if not repositories:
        logger.error("No repositories to process")
        return False
    
    success_count = 0
    total_count = len(repositories)
    
    for repo_name in repositories:
        logger.info(f"\n{'='*60}")
        logger.info(f"Processing repository: {repo_name}")
        logger.info(f"Action: {args.action.upper()} branch '{args.branch}'")
        
        try:
            if args.action == 'lock':
                success = lock_branch_in_repository(organization, project, pat, repo_name, args.branch)
            elif args.action == 'unlock':
                success = unlock_branch_in_repository(organization, project, pat, repo_name, args.branch)
            else:
                logger.error(f"Unknown action '{args.action}'")
                success = False
            if success:
                success_count += 1
                
        except Exception as e:
            logger.error(f"Failed to {args.action} branch '{args.branch}' in repository '{repo_name}': {e}")
    
    # Summary
    logger.info(f"\n{'='*60}")
    logger.info(f"SUMMARY: {success_count}/{total_count} repositories processed successfully")
    
    return success_count == total_count    


def main():
    """Main function to handle command line arguments and execute branch operations"""
    
    # Parse command line arguments
    args = parse_arguments()
    
    # Display configuration summary
    logger.info("Azure DevOps Branch Lock/Unlock Tool")
    logger.info("=" * 50)
    config_manager.print_config_summary()
    logger.info("")
    
    # Display operation details
    logger.info("Operation Details:")
    logger.info(f"   Action: {args.action.upper()}")
    logger.info(f"   Branch: {args.branch}")
    if args.repo:
        repos_list = [repo.strip() for repo in args.repo.split(',')]
        logger.info(f"   Repositories: {', '.join(repos_list)}")
    else:
        logger.info("   Repositories: ALL repositories in project")
        
    # Execute the operation
    success = process_repositories(args, organization, project, PAT)
    
    if success:
        logger.info("SUCCESS: All operations completed successfully!")
        sys.exit(0)
    else:
        logger.error("ERROR: Some operations failed. Check the logs for details.")
        sys.exit(1)




if __name__ == "__main__":
    main()