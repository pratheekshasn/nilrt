from shell_commands import *

def git_clone(repo, directory=None, depth=None, capture_output=True):
    command = f"git clone {repo} {directory}" if directory else f"git clone {repo}"
    if depth:
        command += f" --depth {depth}"
    return run_command(command, capture_output)

def git_commit(message, amend=False, capture_output=True):
    if amend:
        command = "git commit --amend -m \"{message}\"" 
    else:
        command = f"git commit -m \"{message}\""
    return run_command(command, capture_output)

def get_current_commit(capture_output=True):
    """Get the current HEAD commit hash."""
    return run_command("git rev-parse HEAD", capture_output)[1]

def branch_exists(branch_name, capture_output=True):
    """Check if a branch exists locally."""
    return run_command(f"git rev-parse --verify {branch_name}", capture_output)[0] == 0

def git_push(remote_repo_name="origin", branch="main", force=False, delete=False, capture_output=True):
    if delete:
        command = f"git push {remote_repo_name} --delete {branch}"
    else:
        command = f"git push {remote_repo_name} {branch}"
        if force:
            command += " --force"
    return run_command(command, capture_output)

def git_pull(remote=None, branch=None, rebase=False, capture_output=True):
    """Pull latest changes from the specified remote and branch."""
    command = "git pull"
    if rebase:
        command += " --rebase"
    if remote is not None and branch is not None:
        command += f" {remote} {branch}"
    return run_command(command, capture_output)

def git_branch(branch_name,show_current=False, create=False, delete=False, capture_output=True):
    """Handles branch operations: create, delete, or list."""
    if show_current:
        command = "git branch --show-current"
    elif create:
        command = f"git branch {branch_name}"
    elif delete:
        command = f"git branch -D {branch_name}"
    else:
        command = "git branch"
    return run_command(command, capture_output)

def git_checkout(branch_name, force_checkout = False, capture_output=True):
    if not branch_exists(branch_name):
        git_branch(branch_name,create=True)
    if force_checkout:
        command = f"git checkout -f {branch_name}"
    else:
        command = f"git checkout {branch_name}"
    return run_command(command, capture_output)

def git_fetch(remote=None, branch=None):
    """Fetch latest changes from a specified remote repository and branch."""
    command = "git fetch"
    if remote:
        command += f" {remote}"
    if branch:
        command += f" {branch}"
    return run_command(command, capture_output=True)

def git_remote(name=None, url=None, remove=False, capture_output=True):
    """Handle listing, adding, and removing remote repositories."""
    if name is not None and url is not None:
        return run_command(f"git remote add {name} {url}", capture_output)
    elif name is not None and remove:
        return run_command(f"git remote remove {name}", capture_output)
    else:
        return run_command("git remote", capture_output)

def git_merge(branch_name, message="Merge latest upstream", no_ff=False, signoff=False, capture_output=True):
    command = f"git merge {branch_name} --signoff -m \"{message}\"" if signoff else f"git merge {branch_name} -m \"{message}\""
    if no_ff:
        command += " --no-ff"
    return run_command(command, capture_output)

def git_diff(target="HEAD", compare_with=None, staged=False, capture_output=True):
    """Show differences between commits or working directory."""
    if compare_with:
        command = f"git diff {target} {compare_with}"
    else:
        command = "git diff --staged" if staged else "git diff"
    return run_command(command, capture_output)

def git_pull_request(title, body="", base_branch="main", head_branch=None, capture_output=True):
    if head_branch is None:
        head_branch =run_command("git rev-parse --abbrev-ref HEAD", capture_output=True)
    command = f"gh pr create --title \"{title}\" --body \"{body}\" --base {base_branch} --head {head_branch}"
    return run_command(command, capture_output)

def send_email(to, subject, file):
    """ Send Mail """
    return run_command(f"git send-email --to {to} --subject \"{subject}\" {file}")