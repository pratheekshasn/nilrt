import os
import json
class json_config:
    def __init__(self, automation_conf_path, workitemID):
        try:
            with open(automation_conf_path, "r") as file:
                config = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading config file: {e}")
            exit(1)
        self.NILRT_branch = config.get("NILRT_branch")
        self.meta_nilrt_branch = config.get("meta_nilrt_branch")
        self.conf_file = os.getcwd()+f"/{config.get('conf_file_path')}"
        self.force_checkout = config.get("force_checkout")
        self.upstream_repo_name = config.get("upstream_repo_name")
        self.merge_branch_name = config.get("merge_branch_name")
        self.username = config.get("username")
        self.fork_name = config.get("fork_name")
        self.email_from = config.get("email_from")
        self.email_to = config.get("email_to")
        self.email_log_level = config.get("email_log_level")
        self.log_level = config.get("log_level")
        self.work_item_id = workitemID
        self.vm_name = config.get("vm_name")
        self.snapshot_name = config.get("snapshot_name")