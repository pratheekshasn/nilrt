from Shell_commands import *
from Git_commands import *

class GitRepo:
    def __init__(self, local_repo, upstream_repo_url, upstream_branch, local_base_branch,remote_repo_name,myfork_name,myfork_url):
        self.local_repo = local_repo
        self.local_base_branch = local_base_branch
        self.upstream_branch = upstream_branch
        self.upstream_repo_url = upstream_repo_url
        self.remote_repo_name = remote_repo_name
        self.myfork_name = myfork_name
        self.myfork_url = myfork_url
    
    
    def get_current_commit(self):
        """Get the current HEAD commit hash."""
        return run_command("git rev-parse HEAD", capture_output=True)[1]
    
    def branch_exists(self,branch_name):
        """Check if a branch exists locally."""
        return run_command(f"git rev-parse --verify {branch_name}")[0] == 0
    
    def checkout_branch(self,branch_name):
        """Switch to the given branch."""
        return git_checkout(branch_name)

    def delete_branch(self,branch_name):
        """Delete a local branch."""
        return git_branch(branch_name,delete=True)

    def fetch_branch(self, remote_repo_name = None, repo_branch = None):
        """Fetch a remote branch."""
        if remote_repo_name is None:
            remote_repo_name = self.remote_repo_name
        if repo_branch is  None:
            repo_branch = self.upstream_branch
        return git_fetch(remote_repo_name, repo_branch)

    def merge_branch(self, branch_name, message = "Merge latest upstream"):
        """Merge a remote branch into the current branch."""
        return git_merge(branch_name,message,signoff=True, capture_output=True)

    def add_remote(self, remote_repo_name = None, repo_url = None):
        """Add a new remote."""
        if remote_repo_name is None:
            remote_repo_name = self.remote_repo_name
        if repo_url is None:
            repo_url = self.upstream_repo_url

        existing_remotes = git_remote(capture_output=True)[1].splitlines()

        if remote_repo_name in existing_remotes:
            git_remote(remote_repo_name,remove=True)

        return git_remote(remote_repo_name, repo_url)

    def diff(self):
        """Check if there are differences in the last merge."""
        return git_diff(compare_with="HEAD~1", capture_output=True)

    def pull_latest(self, branch_name = None, remote_repo_name = None):
        """Pull latest changes from the current branch's remote tracking branch."""
        return git_pull(remote=remote_repo_name, branch=branch_name,capture_output=True)

    def push(self, branch_name, remote_repo_name = None, delete = False):
        """Push a branch to the remote repository."""
        if remote_repo_name is None:
            remote_repo_name = self.remote_repo_name 

        return git_push(remote_repo_name, branch_name,delete)

    def create_pull_request(self, title, body="", base_branch="main", head_branch=None):
        """Create a pull request on GitHub using the GitHub CLI (gh)."""

        if head_branch is None:
            head_branch = self.local_base_branch
        
        return git_pull_request(title, body, base_branch, head_branch, capture_output=True)
