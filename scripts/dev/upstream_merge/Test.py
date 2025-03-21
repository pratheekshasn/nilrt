from Shell_commands import *
import time

def Test():
    print("Starting the VM...")
    start = execute('VBoxManage startvm "NILRTAgain" --type headless')
    if start[0] != 0:
        print(start)    
        return start
    time.sleep(5)

    print("Copying image to target machine...")
    copy = execute("scp /home/tonks/dev/nilrt/build/tmp-glibc/deploy/images/x64/nilrt-base-system-image-x64.tar admin@10.152.8.225:/home/admin")
    if copy[0] != 0:
        print(copy)
        return copy 
    
    print("Extracting image on target machine...")
    first_cmd = execute('ssh admin@10.152.8.225 "tar xf /home/admin/nilrt-base-system-image-x64.tar"')
    if first_cmd[0] != 0:
        print(first_cmd)
        return first_cmd

    second_cmd = execute('ssh admin@10.152.8.225 "tar xf data.tar.gz -C /mnt/userfs && ./postinst"')
    if second_cmd[0] != 0:
        print(second_cmd)
        return second_cmd

    print("Rebooting the machine...")
    reboot = execute('ssh admin@10.152.8.225 "reboot"')
    if reboot[0] != 0:
        print(reboot)
        return reboot

    time.sleep(90)
    
    print("Verifying OS version...")
    os_version = execute('ssh admin@10.152.8.225 "cat /etc/os-release"')
    if os_version[0] != 0:
        print(os_version)
        return os_version
    
    
    print("Powering off the VM...")
    poweroff = execute('VBoxManage controlvm "NILRTAgain" poweroff')
    if poweroff[0] != 0:
        print(poweroff)
        return poweroff
    
    print("Restoring to Clean_SSHEnabled snapshot...")
    restore = execute('VBoxManage snapshot "NILRTAgain" restore Clean_SSHEnabled')
    if restore[0] != 0:
        print(restore)
        return restore

    return (0, None)

if __name__ == "__main__":
    Test()
