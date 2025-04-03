automation_conf.json
//It is passed as argument while running upstream_merge.py


upstream_merge.py
main():
    parse_args(): //It handles automation_conf.json

    merge_submodules_with_upstream():
    //for each sub-module it calls merge_upstream 
        merge_upstream():
            merge_prepare():
                switch_to_base_branch_and_pull():
                fetch_upstream():
                create_merge_branch():
            //merges it with upstream and compares it with previous commit and produces diff if any
    
    Build_and_Test()://It is called if Submodule_merge_Flag
        build()://It is present in Build.py 
        test()://It is present in Test.py 
    
    write_log_and_send_email():
        format_merge_report():
            push_and_PR()://Incase of ... OK the branch is pushed to your repository and then a PR is created
        write_email_addresses():
        write_log():
        send_email():

Shell_commands.py
It is used to run any Shell command

Git_commands.py
It has various git function which uses Shell_commands functions

GitRepo.py
It has GitRepo class with local_repo,local_base_branch,upstream_branch,upstream_repo_name,upstream_repo_url,myfork_name,myfork_url as data members and has various member functions specific to a git repository

Build.py
It builds the images

Test.py
it tests the image on a VM