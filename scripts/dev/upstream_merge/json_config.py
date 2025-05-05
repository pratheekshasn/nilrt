class json_config:
    def __init__(self, NILRT_branch, conf_file, force_checkout, upstream_repo_name, merge_branch_name, username, fork_name, email_from, email_to, email_log_level, log_level, work_item_id, vm_name, snapshot_name):
        self.NILRT_branch = NILRT_branch
        self.conf_file = conf_file
        self.force_checkout = force_checkout
        self.upstream_repo_name = upstream_repo_name
        self.merge_branch_name = merge_branch_name
        self.username = username
        self.fork_name = fork_name
        self.email_from = email_from
        self.email_to = email_to
        self.email_log_level = email_log_level
        self.log_level = log_level
        self.work_item_id = work_item_id
        self.vm_name = vm_name
        self.snapshot_name = snapshot_name