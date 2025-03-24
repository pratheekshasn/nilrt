import os
import argparse
import json
from GitRepo import *
from Git_commands import *
from Shell_commands import *
from Test import *
from Build import *

Submodule_merge_Flag = False
Build_Flag = False
Test_Flag = False

def parse_args():
    parser = argparse.ArgumentParser(description="Automated repository merging script")
    parser.add_argument("-c", type=str, help="Path to configuration file", default="automation_conf.json")
    args = parser.parse_args()

    try:
        with open(args.c, "r") as file:
            config = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading config file: {e}")
        exit(1)
    
    return config.get("conf_file_path"), config.get("force_checkout"), config.get("forks"), config.get("upstream_repo_name"), config.get("merge_branch_name"), config.get("email_from"), config.get("email_to"), config.get("log_file_name"), config.get("log_level"), config.get("work_item_id"), config.get("VM_name")

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

def merge_upstream(git_obj,force_checkout, merge_branch_name):
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
    if git_obj.add_remote(git_obj.myfork_name, git_obj.myfork_url)[0] != 0:
        print(f"\n    Error adding remote repository {git_obj.myfork_name} using {git_obj.myfork_url}. Exiting")
        return (1,f"\n    Error adding remote repository {git_obj.myfork_name} using {git_obj.myfork_url}. Exiting")
    
    if git_obj.push(merge_branch_name, git_obj.myfork_name,delete=True)[0] != 0:
        print(f"\n    Failed to delete branch {merge_branch_name} on {git_obj.myfork_name}")
        return (1, f"\n    Failed to delete branch {merge_branch_name} on {git_obj.myfork_name}")
    
    if git_obj.push(merge_branch_name, git_obj.myfork_name)[0] != 0:
        print(f"\n    Failed to push branch {merge_branch_name} to {git_obj.myfork_name}")
        return (1, f"\n    Failed to push branch {merge_branch_name} to {git_obj.myfork_name}")
    
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

def format_merge_report(merge_report,log_level, merge_branch_name, work_item_id):
    min_detail = ""
    additional_detail = ""
    build_and_test_detail = merge_report.pop("Build_and_Test")
    for git_obj, (status, message) in merge_report.items():
        min_detail += f"{git_obj.local_repo}\n"
        additional_detail += f"{git_obj.local_repo}\n"
        if status==1:
            min_detail += " ... ERRORS\n"
            additional_detail += f" ... ERRORS\n    {message}\n"
        else:
            if message == None:
                min_detail += " ... OK (no changes)\n"
                additional_detail += " ... OK (no changes)\n"
            else:
                min_detail += " ... OK\n"
                additional_detail += f" ... OK\n    {message}\n"
                if Build_Flag and Test_Flag:
                    current_directory = os.getcwd()
                    os.chdir(git_obj.local_repo)
                    push_and_PR_result = push_and_PR(git_obj,merge_branch_name,work_item_id)
                    os.chdir(current_directory)
                    if push_and_PR_result[0] == 1:
                        min_detail += " ... ERRORS\n"
                        additional_detail += f" ... ERRORS\n    {push_and_PR_result[1]}\n"
                    else:
                        min_detail += " ... PUSH SUCCESSFUL\n"
                        additional_detail += f" ... PUSH SUCCESSFUL\n    {push_and_PR_result[1]}\n"

    min_detail += f"\nBuild and Test\n"
    if build_and_test_detail[0] == 0:
        min_detail += " ... OK\n"
    else:
        min_detail += " ... ERRORS\n"
        additional_detail += f"\nBuild and Test\n ... ERRORS\n    {build_and_test_detail[1]}\n"
    if log_level == 0:
        return min_detail
    return min_detail + "\n\n" + additional_detail

def merge_submodules_with_upstream(conf_file, force_checkout, forks, upstream_repo_name, merge_branch_name):
    current_directory = os.getcwd()

    # Merge each submodule
    merge_report = {}
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
                            myfork_name="myfork",
                            myfork_url=forks[parts[0]])
            os.chdir(git_obj.local_repo)
            merge_report[git_obj] = merge_upstream(git_obj, force_checkout, merge_branch_name)
            if merge_report[git_obj][0] == 1:
                Submodule_merge_Flag = True 
            os.chdir(current_directory)
    return merge_report

def write_log(log_file_name, contents):
    with open(log_file_name, "a") as log:
        log.write(contents)

def write_log_and_send_email(log_file_name, email_from, email_to, merge_report, log_level, merge_branch_name, work_item_id):
    formatted_report_string = format_merge_report(merge_report,log_level, merge_branch_name, work_item_id)
    write_email_addresses(log_file_name, email_from, email_to)
    write_log(log_file_name, formatted_report_string)
    send_email(to=email_to, subject="Merge Details", file=log_file_name)

def Build_and_Test(vm_name):
    success=build()
    if success[0] != 0:
        return success
    Build_Flag = True
    success=test(vm_name)
    if success[0] != 0:
        return success
    Test_Flag = True
    return (0,None)

def main():
    conf_file, force_checkout, forks, upstream_repo_name, merge_branch_name, email_from, email_to, log_file_name, log_level, work_item_id, vm_name = parse_args()
    merge_report = merge_submodules_with_upstream(conf_file, force_checkout, forks, upstream_repo_name, merge_branch_name)
    
    if Submodule_merge_Flag == False:
        details = Build_and_Test(vm_name)
        if details[0] != 0:
            merge_report["Build_and_Test"] = details
        else:
            merge_report["Build_and_Test"] = (0,"Build and Test successful")
    # Build the base-system-image
    # If not successful, do not push, and send an email about the build failure
    # Test the new image
    # success = success and test()
    # If not successful, do not push, and send an email about the test failure
    # If both are successful, push branch, create PR, send email with diff.

    write_log_and_send_email(log_file_name, email_from, email_to, merge_report, log_level, merge_branch_name, work_item_id)
    

if __name__ == "__main__":
    main()
