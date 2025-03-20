from Shell_commands import *
import time

def Test():
    # Step 1: Start the VM using VBoxManage
    print("Starting the VM...")
    start = run_command('VBoxManage startvm "NILRTAgain" --type headless')
    if start[0] != 0:
        return start
    print(start)    
    time.sleep(5)

    # Step 2: Copy the image to the target machine using SCP
    print("Copying image to target machine...")
    copy = run_command("scp /home/tonks/dev/nilrt/build/tmp-glibc/deploy/images/x64/nilrt-base-system-image-x64.tar admin@10.152.8.225:/home/admin")
    if copy[0] != 0:
        return copy 
    
    print(copy)

    # Step 3: SSH into the machine and extract the image
    print("Extracting image on target machine...")
    first_cmd = run_command('ssh admin@10.152.8.225 "tar xf /home/admin/nilrt-base-system-image-x64.tar"')
    if first_cmd[0] != 0:
        return first_cmd
    print(first_cmd)
    second_cmd = run_command('ssh admin@10.152.8.225 "tar xf data.tar.gz -C /mnt/userfs && ./postinst"')
    if second_cmd[0] != 0:
        return second_cmd
    print(second_cmd)

    # Step 4: Reboot the machine
    print("Rebooting the machine...")
    reboot = run_command('ssh admin@10.152.8.225 "reboot"')
    if reboot[0] != 0:
        return reboot
    print(reboot)

    time.sleep(90)
    
    # Step 5: Verify OS version
    print("Verifying OS version...")
    os_version = run_command('ssh admin@10.152.8.225 "cat /etc/os-release"')
    if os_version[0] != 0:
        return os_version
    print(os_version)
    

    #Step 6: Power off the VM
    print("Powering off the VM...")
    poweroff = run_command('VBoxManage controlvm "NILRTAgain" poweroff')
    if poweroff[0] != 0:
        return poweroff
    print(poweroff)
    
    # Step 6: Restore snapshot using VBoxManage
    print("Restoring to Clean_SSHEnabled snapshot...")
    restore = run_command('VBoxManage snapshot "NILRTAgain" restore Clean_SSHEnabled')
    if restore[0] != 0:
        print(restore)
        return restore
    print(restore)

    return (0, None)

if __name__ == "__main__":
    Test()
