from Shell_commands import *
import time

def test(VM_name):
    print("Starting the VM...")
    start = execute(f"VBoxManage startvm \"{VM_name}\" --type headless")
    if start[0] != 0:
        print(start)    
        return start
    time.sleep(5)

    print("Copying image to target machine...")
    copy = execute("scp /home/tonks/dev/nilrt/build/tmp-glibc/deploy/images/x64/nilrt-base-system-image-x64.tar admin@NI-cRIO-903x-VM-27108694:/home/admin")
    if copy[0] != 0:
        print(copy)
        return copy 
    
    print("Extracting image on target machine...")
    first_cmd = execute('ssh admin@NI-cRIO-903x-VM-27108694 "tar xf /home/admin/nilrt-base-system-image-x64.tar"')
    if first_cmd[0] != 0:
        print(first_cmd)
        return first_cmd

    second_cmd = execute('ssh admin@NI-cRIO-903x-VM-27108694 "tar xf data.tar.gz -C /mnt/userfs && ./postinst"')
    if second_cmd[0] != 0:
        print(second_cmd)
        return second_cmd

    print("Rebooting the machine...")
    reboot = execute('ssh admin@NI-cRIO-903x-VM-27108694 "reboot"')
    if reboot[0] != 0:
        print(reboot)
        return reboot

    time.sleep(90)
    
    print("Verifying OS version...")
    os_version = execute('ssh admin@NI-cRIO-903x-VM-27108694 "cat /etc/os-release"')
    if os_version[0] != 0:
        print(os_version)
        return os_version
    
    
    print("Powering off the VM...")
    poweroff = execute(f"VBoxManage controlvm \"{VM_name}\" poweroff")
    if poweroff[0] != 0:
        print(poweroff)
        return poweroff
    
    print("Restoring to Clean_SSHEnabled snapshot...")
    restore = execute('VBoxManage snapshot "NILRTAgain" restore Clean_SSHEnabled')
    if restore[0] != 0:
        print(restore)
        return restore

    return (0, None)