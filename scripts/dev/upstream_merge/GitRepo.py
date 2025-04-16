from git_commands import *

class GitRepo:
    def __init__(self, local_repo=None, upstream_repo_url=None, upstream_branch=None, local_base_branch=None,upstream_repo_name=None,fork_name=None,fork_url=None):
        self.local_repo = local_repo
        self.local_base_branch = local_base_branch
        self.upstream_branch = upstream_branch
        self.upstream_repo_url = upstream_repo_url
        self.upstream_repo_name = upstream_repo_name
        self.fork_name = fork_name
        self.fork_url = fork_url

    def get_current_commit(self):
        """
        Get the current HEAD commit hash.
        :param capture_output: Whether to capture the command output.
        :return: The current commit hash.
        """
        return run_command("git rev-parse HEAD")[1]
    
    def branch_exists(self, branch_name, fork_name = None, remote=False, capture_output=True):
        """
        Check if a branch exists locally.
        :param branch_name: Name of the branch to check.
        :param capture_output: Whether to capture the command output.
        :return: True if the branch exists, False otherwise.
        """
        if remote:
            if fork_name is None:
                fork_name = self.upstream_repo_name
            result = run_command(f"git ls-remote --heads {fork_name} {branch_name}", capture_output)
            if result[0] == 0:
                return result != (0,'')
            return  False
        
        return run_command(f"git rev-parse --verify {branch_name}", capture_output)[0] == 0
    
    def checkout_branch(self, branch_name, create = False, force_checkout = False):
        """Switch to the given branch."""
        return git_checkout(branch_name, create, force_checkout)

    def delete_branch(self,branch_name):
        """Delete a local branch."""
        return git_branch(branch_name,delete=True)

    def fetch_branch(self, upstream_repo_name = None, repo_branch = None):
        """Fetch a remote branch."""
        if upstream_repo_name is None:
            upstream_repo_name = self.upstream_repo_name
        if repo_branch is  None:
            repo_branch = self.upstream_branch
        return git_fetch(upstream_repo_name, repo_branch)

    def merge_branch(self, branch_name, message = "Merge"):
        """Merge a remote branch into the current branch."""
        return git_merge(branch_name,message,signoff=True, capture_output=True)

    def add_remote(self, upstream_repo_name = None, repo_url = None):
        """Add a new remote."""
        if upstream_repo_name is None:
            upstream_repo_name = self.upstream_repo_name
        if repo_url is None:
            repo_url = self.upstream_repo_url

        existing_remotes = git_remote(capture_output=True)[1].splitlines()

        if upstream_repo_name in existing_remotes:
            git_remote(upstream_repo_name,remove=True)

        return git_remote(upstream_repo_name, repo_url)

    def diff(self):
        """Check if there are differences in the last merge."""
        return git_diff(compare_with="HEAD~1", capture_output=True)

    def pull_latest(self, branch_name = None, upstream_repo_name = None):
        """Pull latest changes from the current branch's remote tracking branch."""
        return git_pull(remote=upstream_repo_name, branch=branch_name,capture_output=True)

    def push(self, branch_name, upstream_repo_name = None, force = False, delete = False):
        """Push a branch to the remote repository."""
        if upstream_repo_name is None:
            upstream_repo_name = self.upstream_repo_name 

        return git_push(upstream_repo_name, branch_name, force, delete)

    def create_pull_request(self, title, body="", base_branch="main", head_branch=None):
        """Create a pull request on GitHub using the GitHub CLI (gh)."""

        if head_branch is None:
            head_branch = self.local_base_branch
        
        return git_pull_request(title, body, base_branch, head_branch, capture_output=True)
