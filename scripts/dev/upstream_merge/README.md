# HOW TO USE THE MERGE SCRIPT

This script automates the process of merging upstream changes, building images, and testing them on a virtual machine (VM). Follow the steps below to use the script effectively.

---

## **Steps to Run the Script**

### **1. Navigate to the `nilrt` Directory**
```bash
cd ~/nilrt
```

### **2. Run the Script**

#### **To Perform a Merge**
This will merge upstream changes, build the images, and test them:
```bash
python3 scripts/dev/upstream_merge/upstream_merge.py -c scripts/dev/upstream_merge/automation_conf.json
```

#### **To Skip the Merge and Only Build and Test**
If you want to skip the merge step and directly proceed with building and testing:
```bash
python3 scripts/dev/upstream_merge/upstream_merge.py -c scripts/dev/upstream_merge/automation_conf.json -skip-merge True
```

---

## **Configuration File: `automation_conf.json`**

The script relies on a configuration file (`automation_conf.json`) to define various parameters. Below is an explanation of the fields in the configuration file:

- **`conf_file_path`**:  
  Path to the configuration file (default: `repos.conf`). This file must be located in the `/scripts/dev/upstream_merge/` folder.

- **`force_checkout`**:  
  Enables forceful checkout to the base branch if set to `True`.

- **`forks`**:  
  A dictionary where the keys are local repository names (as mentioned in `repos.conf`) and the values are the URLs of your forks.

- **`upstream_repo_name`**:  
  The name of the upstream remote repository.

- **`merge_branch_name`**:  
  The name of the branch where the merge will be performed.

- **`email_from`**:  
  The email address from which the merge report will be sent.

- **`email_to`**:  
  The email address to which the merge report will be sent.

- **`email_log_level`**:  
  - `0`: Minimal information will be included in the email.  
  - `1`: Additional detailed information will be included in the email.

- **`log_level`**:  
  Integer representing the logging level:  
  - `10`: DEBUG  
  - `20`: INFO  
  - `30`: WARNING  
  - `40`: ERROR  
  - `50`: CRITICAL  

- **`work_item_id`**:  
  The work item ID associated with the pull request.

- **`vm_name`**:  
  The name of the VM where the images will be tested.

- **`snapshot_name`**:  
  The snapshot of the VM to be restored before testing. This snapshot must have SSH enabled.

---

## **Script Overview**

### **`main()`**
- **`parse_args()`**: Parses command-line arguments, such as the path to the configuration file and whether to skip the merge step.
- **`conf_details()`**: Extracts information from the `automation_conf.json` file.
- **`merge_submodules_with_upstream()`**: Handles merging upstream changes for each submodule:
  - **`merge_upstream()`**:
    - **`merge_prepare()`**:
      - **`switch_to_base_branch_and_pull()`**: Switches to the base branch and pulls the latest changes.
      - **`fetch_upstream()`**: Fetches updates from the upstream repository.
      - **`create_merge_branch()`**: Creates a new branch for the merge.
    - Performs the merge, compares it with the previous commit, and generates a diff if there are changes.
- **`build_and_test()`**:
  - **`build_images()`**: Builds the required images (defined in `build.py`).
  - **`OS_test()`**: Tests the built images on a VM (defined in `test.py`).
- **`push_and_PR_prepare()`**:
  - Prepares and pushes the branch to the fork and creates a pull request if there are any mergeable changes.
- **`write_log_and_send_email()`**:
  - **`format_merge_report()`**: Formats the merge report.
  - **`write_email_addresses()`**: Writes the email addresses for the report.
  - **`write_log()`**: Writes the log data to a file.
  - **`send_email()`**: Sends the email using `git send-email`.

---

## **Supporting Files**

### **`shell_commands.py`**
- Provides utility functions to execute shell commands.  
- Acts as a wrapper for running system commands from Python.

### **`git_commands.py`**
- Contains various Git-related functions that rely on `shell_commands.py`.  
- Includes operations like fetching, pulling, creating branches, and merging.

### **`GitRepo.py`**
- Defines the `GitRepo` class, which encapsulates details and operations for a Git repository.  
-  Data members are:
    - local_repo
    - local_base_branch
    - upstream_branch
    - upstream_repo_name
    - upstream_repo_url
    - fork_name
    - fork_url

### **`build.py`**
- Handles the process of building images.  
- Key steps include:
  - Setting up the Docker environment.
  - Building core feeds.
  - Building core images.

### **`test.py`**
- Manages testing of the built images on a VM.  
- Key steps include:
  - Restoring the VM to a specific snapshot.
  - Installing and testing safemode and runmode images.
  - Verifying the OS version.
  
---
