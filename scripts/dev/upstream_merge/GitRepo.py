from Shell_commands import *

class GitRepo:
    def __init__(self, local_repo, upstream_repo_url, upstream_branch, local_base_branch,remote_repo_name,myfork_name,myfork_url):
        self.local_repo = local_repo
        self.local_base_branch = local_base_branch
        self.upstream_branch = upstream_branch
        self.upstream_repo_url = upstream_repo_url
        self.remote_repo_name = remote_repo_name
        self.myfork_name = myfork_name
        self.myfork_url = myfork_url

    def checkout_branch(self,branch_name):
        """Switch to the given branch."""
        return run_command(f"git checkout {branch_name}")

    def create_branch(self,branch_name):
        """Create a new branch from base_branch."""
        return run_command(f"git checkout -b {branch_name} {self.local_base_branch}")

    def delete_branch(self,branch_name):
        """Delete a local branch."""
        return run_command(f"git branch -D {branch_name}")

    def fetch_branch(self, remote_repo_name = None, repo_branch = None):
        """Fetch a remote branch."""
        if remote_repo_name is None:
            remote_repo_name = self.remote_repo_name
        if repo_branch is None:
            repo_branch = self.upstream_branch

        return run_command(f"git fetch {remote_repo_name} {repo_branch}")

    def merge_branch(self, branch_name, message = "Merge_latest_upstream"):
        """Merge a remote branch into the current branch."""
        return run_command(f"git merge {branch_name} --signoff -m {message}", capture_output=True)

    def add_remote(self, remote_repo_name = None, repo_url = None):
        """Add a new remote."""
        if remote_repo_name is None:
            remote_repo_name = self.remote_repo_name
        if repo_url is None:
            repo_url = self.upstream_repo_url

        existing_remotes = run_command("git remote", capture_output=True)[1].splitlines()

        if remote_repo_name in existing_remotes:
            run_command(f"git remote remove {remote_repo_name}")
        
        return run_command(f"git remote add {remote_repo_name} {repo_url}")
    

    def get_current_commit(self):
        """Get the current HEAD commit hash."""
        return run_command("git rev-parse HEAD", capture_output=True)[1]

    def branch_exists(self,branch_name):
        """Check if a branch exists locally."""
        return run_command(f"git rev-parse --verify {branch_name}")[0] == 0

    def diff(self):
        """Check if there are differences in the last merge."""
        return run_command("git diff HEAD~1 HEAD", capture_output=True)

    def pull_latest(self):
        """Pull latest changes from the current branch's remote tracking branch."""
        return run_command("git pull")

    def push(self, branch_name, remote_repo_name = None):
        """Push a branch to the remote repository."""
        if remote_repo_name is None:
            remote_repo_name = self.remote_repo_name 

        return run_command(f"git push {remote_repo_name} {branch_name}")
    
    def create_pull_request(self, title, body="", base_branch="main", head_branch=None):
        """Create a pull request on GitHub using the GitHub CLI (gh)."""

        if head_branch is None:
            head_branch = self.local_base_branch
        
        return run_command(f"gh pr create --title {title} --body {body} --base {base_branch} --head {head_branch}", capture_output=True)

    
