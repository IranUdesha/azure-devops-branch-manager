import requests
import logging

logger = logging.getLogger(__name__)

class az_devops:
    def __init__(self, organization, project, repository, pat):
        self.organization = organization
        self.project = project
        self.repository = repository
        self.pat = pat
        self.session = requests.Session()
        self.session.auth = ("", pat)
        self.session.headers.update({"Content-Type": "application/json"})
        # Use preview API for ref updates to support isLocked operations
        self.api_version = '7.0'

    def get_all_repositories(self):
        url = f"https://dev.azure.com/{self.organization}/{self.project}/_apis/git/repositories?api-version={self.api_version}"
        response = self.session.get(url, timeout=30)
        response.raise_for_status()
        return response.json()
    
    def list_branches(self):
        url = f"https://dev.azure.com/{self.organization}/{self.project}/_apis/git/repositories/{self.repository}/refs?api-version={self.api_version}"
        
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            branches = response.json()  # All branches data in JSON format
            return branches['value']
        except requests.HTTPError as exc:
            
            logger.error(f"Error listing branches: {exc}")
            return None

    def modify_branch(self, branch_name, lock=True):

        lock_url = f"https://dev.azure.com/{self.organization}/{self.project}/_apis/git/repositories/{self.repository}/refs"

        body = {
            "isLocked": lock
        } 
        
        params = {
            "filter": f"heads/{branch_name}",
            "api-version": "6.0"
        }
        try:
            response = requests.patch(lock_url, json=body, params=params, timeout=30, auth=("", self.pat), headers={"Content-Type": "application/json"})
            response.raise_for_status()
            action = "locked" if lock else "unlocked"
            logger.info(f"Branch '{branch_name}' {action} successfully.")
            return True
        except requests.HTTPError as exc:
            logger.error(f"Error {'locking' if lock else 'unlocking'} branch '{branch_name}': {exc}")
            raise exc  # Re-raise the exception so it can be caught by the caller
        