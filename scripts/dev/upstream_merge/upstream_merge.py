import os
import argparse
import json
from GitRepo import *
from Git_commands import *
from Shell_commands import *
from Test import *
from Build import *

def parse_args():
    parser = argparse.ArgumentParser(description="Automated repository merging script")
    parser.add_argument("-c", type=str, help="Path to configuration file", default="automation_conf.json")
    parser.add_argument("-skip-merge", type=bool, help="Skip merging with upstream", default=False)
    args = parser.parse_args()

    return args

def conf_details(config_file_path):
    try:
        with open(config_file_path, "r") as file:
            config = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading config file: {e}")
        exit(1)
    
    return os.getcwd()+f"/scripts/dev/upstream_merge/{config.get('conf_file_path')}", config.get("force_checkout"), config.get("forks"), config.get("upstream_repo_name"), config.get("merge_branch_name"), config.get("email_from"), config.get("email_to"), config.get("log_file_name"), config.get("log_level"), config.get("work_item_id"), config.get("VM_name"), config.get("snapshot_name")

def switch_to_base_branch_and_pull(git_obj,force_checkout):
    if not force_checkout and not git_obj.branch_exists(git_obj.local_base_branch):
        print(f"\n    Branch {git_obj.local_base_branch} does not exist. Exiting")
        return (1,f"\n    Branch {git_obj.local_base_branch} does not exist. Exiting")
    
    if git_obj.checkout_branch(git_obj.local_base_branch)[0] != 0:
        print(f"\n    Error switching to branch {git_obj.local_base_branch}. Exiting")
        return (1,f"\n    Error switching to branch {git_obj.local_base_branch}. Exiting")
    
    if git_obj.pull_latest()[0] != 0:
        print(f"\n    Error pulling latest on {git_obj.local_base_branch}. Exiting")
        return (1,f"\n    Error pulling latest on {git_obj.local_base_branch}. Exiting")

    return (0,None)
    
def fetch_upstream(git_obj):
    if git_obj.add_remote()[0] != 0:
        print(f"\n    Error adding remote repository {git_obj.upstream_repo_name} using {git_obj.upstream_repo_url}. Exiting")
        return (1,f"\n    Error adding remote repository {git_obj.upstream_repo_name} using {git_obj.upstream_repo_url}. Exiting")

    if git_obj.fetch_branch()[0] != 0:
        print(f"\n    Error fetching {git_obj.upstream_branch} from {git_obj.upstream_repo_name}. Exiting")
        return (1,f"\n    Error fetching {git_obj.upstream_branch} from {git_obj.upstream_repo_name}. Exiting")

    return (0,None)

def create_merge_branch(git_obj,merge_branch_name):
    if git_obj.branch_exists(merge_branch_name):
        git_obj.checkout_branch(git_obj.local_base_branch)
        git_obj.delete_branch(merge_branch_name)

    if git_obj.checkout_branch(merge_branch_name)[0] != 0:
        print(f"\n    Error creating {merge_branch_name}. Exiting")
        return (1,f"\n    Error creating {merge_branch_name}. Exiting")
    
    return (0,None)

def merge_prepare(git_obj, merge_branch_name, force_checkout):
    print(f"{git_obj.local_repo}")

    base_branch_details = switch_to_base_branch_and_pull(git_obj,force_checkout)
    if base_branch_details[0]==1:
        return base_branch_details
    
    fetch_details = fetch_upstream(git_obj)
    
    if fetch_details[0]==1:
        return fetch_details
    
    repo_details = create_merge_branch(git_obj, merge_branch_name)

    if repo_details[0]==1:
        return repo_details
    
    return (0,None)

def merge_upstream(git_obj,force_checkout, merge_branch_name, skip_merge):
    if skip_merge:
        return (0," Has Been Skipped")
    
    merge_prepare_details = merge_prepare(git_obj,merge_branch_name,force_checkout)
    
    if merge_prepare_details[0]==1:
        return merge_prepare_details
    
    commit_before_merge = git_obj.get_current_commit()
    
    merge_result = git_obj.merge_branch(f"{git_obj.upstream_repo_name}/{git_obj.upstream_branch}", "Merge latest upstream")

    if merge_result[0] == 0:        
        diff_output=git_obj.diff()
        
        if (git_obj.get_current_commit() == commit_before_merge) or diff_output == (0,None):
            return (0,None)
        else:
            return (0,diff_output[1])
    else:
        return (1,merge_result[1])

def push_and_PR(git_obj,merge_branch_name,work_item_id):
    if git_obj.add_remote(git_obj.fork_name, git_obj.fork_url)[0] != 0:
        print(f"\n    Error adding remote repository {git_obj.fork_name} using {git_obj.fork_url}. Exiting")
        return (1,f"\n    Error adding remote repository {git_obj.fork_name} using {git_obj.fork_url}. Exiting")
    
    if git_obj.push(merge_branch_name, git_obj.fork_name, delete=True)[0] != 0:
        print(f"\n    Failed to delete branch {merge_branch_name} on {git_obj.fork_name}")
        return (1, f"\n    Failed to delete branch {merge_branch_name} on {git_obj.fork_name}")
    
    if git_obj.push(merge_branch_name, git_obj.fork_name)[0] != 0:
        print(f"\n    Failed to push branch {merge_branch_name} to {git_obj.fork_name}")
        return (1, f"\n    Failed to push branch {merge_branch_name} to {git_obj.fork_name}")
    
    #if git_obj.create_pull_request("Automated Merge PR",
#       f"""Merge latest from upstream. No conflicts.
 
    # #AB{work_item_id}
    
    # - [ ] bitbake packagefeed-ni-core
    # - [ ] bitbake packagegroup-ni-desirable
    # - [ ] bitbake package-index && bitbake nilrt-base-system-image
    # - [ ] Reimaged a cRIO with the new base image and successfully booted it""",git_obj.local_base_branch,f"Shreejit-03:{merge_branch_name}")[0] != 0:
    #     print("\n    Error creating the pull request.")
    #     return (1,"\n    Error creating the pull request.")

    return (0,None)
    
def write_email_addresses(log_file_name, email_from, email_to):
    with open(log_file_name, "w") as log:
        log.write(f"From: {email_from}\n")
        log.write(f"To: {email_to}\n")
        log.write("Subject: Merge Details\n\n")

def format_status(status, message):
        if status == 1:
            return " ... ERRORS", f" ... ERRORS\n    {message or ''}\n"
        elif message is None:
            return " ... OK (no changes)", " ... OK (no changes)\n"
        else:
            return " ... OK", f" ... OK\n    {message}\n"
        
def format_merge_report(merge_report, log_level):
    min_detail = ""
    additional_detail = ""

    build_and_test_detail = merge_report.pop("Build and Test")
    push_and_PR_details = merge_report.pop("Push and PR")

    for git_obj, (status, message) in merge_report.items():
        min_line, additional_line = format_status(status, message)
        min_detail += f"{git_obj.local_repo}\n{min_line}\n"
        additional_detail += f"{git_obj.local_repo}\n{additional_line}"
        if status == 0 and message is not None:
            git_obj_push_details = push_and_PR_details[git_obj]
            if git_obj_push_details[0] == 0:
                min_detail += "     Push and PR ... OK\n"
                additional_detail += f" Push and PR ... OK\n    {message or ''}\n"
            else:
                min_detail += "     Push and PR ... ERRORS\n"
                additional_detail += f" Push and PR ... ERRORS\n    {message}\n"
    
    min_detail += "\nBuild and Test\n"
    if build_and_test_detail and build_and_test_detail[0] == 0:
        min_detail += " ... OK\n"
        additional_detail += f"\nBuild and Test\n ... OK\n    {build_and_test_detail[1]}\n"
    else:
        min_detail += " ... ERRORS\n"
        additional_detail += f"\nBuild and Test\n ... ERRORS\n    {build_and_test_detail[1]}\n"

    if log_level == 0:
        return min_detail
    return min_detail + "\n\n" + additional_detail

def merge_submodules_with_upstream(merge_report, conf_file, force_checkout, forks, upstream_repo_name, merge_branch_name, skip_merge):
    current_directory = os.getcwd()

    # Merge each submodule with upstream
    with open(conf_file, "r") as file:
        for line in file:
            if line.startswith("#"):
                continue
            parts = line.split()
            git_obj=GitRepo(local_repo=parts[0],
                            upstream_repo_url=parts[1],
                            upstream_branch=parts[2],
                            local_base_branch=parts[3],
                            upstream_repo_name=upstream_repo_name,
                            fork_name="myfork",
                            fork_url=forks[parts[0]])
            os.chdir(git_obj.local_repo)
            merge_report[git_obj] = merge_upstream(git_obj, force_checkout, merge_branch_name, skip_merge)
            os.chdir(current_directory)
    return merge_report

def write_log(log_file_name, contents):
    with open(log_file_name, "a") as log:
        log.write(contents)

def write_log_and_send_email(log_file_name, email_from, email_to, merge_report, log_level):
    formatted_report_string = format_merge_report(merge_report,log_level)
    write_email_addresses(log_file_name, email_from, email_to)
    write_log(log_file_name, formatted_report_string)
    send_email(to=email_to, subject="Merge Details", file=log_file_name)

def Build_and_Test(vm_name, snapshot_name):
    success=build()
    if success[0] != 0:
        return success
    success=test(vm_name, snapshot_name)
    return success

def main():
    args = parse_args()
    skip_merge = args.skip_merge
    config_file_path = args.c

    conf_file, force_checkout, forks, upstream_repo_name, merge_branch_name, email_from, email_to, log_file_name, log_level, work_item_id, vm_name, snapshot_name = conf_details(config_file_path)
    
    merge_report = {}
    merge_report = merge_submodules_with_upstream(merge_report, conf_file, force_checkout, forks, upstream_repo_name, merge_branch_name, skip_merge)
    
    merge_has_errors = False
    
    for git_obj, (status, message) in merge_report.items():
        if status == 1:
            merge_has_errors = True
            break

    if merge_has_errors == False:
        Build_and_Test_details = Build_and_Test(vm_name, snapshot_name)
        push_and_PR_results = {}

        if Build_and_Test_details[0] == 0:
            for git_obj, (status, message) in list(merge_report.items()):
                if status == 0 and message is not None:
                    current_directory = os.getcwd()
                    os.chdir(git_obj.local_repo)
                    push_and_PR_results[git_obj] = push_and_PR(git_obj, merge_branch_name, work_item_id)
                    os.chdir(current_directory)

            merge_report["Push and PR"] = push_and_PR_results

        merge_report["Build and Test"] = Build_and_Test_details


    # Build the base-system-image
    # If not successful, do not push, and send an email about the build failure
    # Test the new image
    # success = success and test()
    # If not successful, do not push, and send an email about the test failure
    # If both are successful, push branch, create PR, send email with diff.
    
    write_log_and_send_email(log_file_name, email_from, email_to, merge_report, log_level)
    
if __name__ == "__main__":
    main()
