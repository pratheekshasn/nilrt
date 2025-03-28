from Shell_commands import *
import time
import os

def test(VM_name, snapshot_name):
    restore = restore_snapshot(VM_name, snapshot_name)
    if restore[0] != 0:
        return restore
    
    start = start_VM(VM_name)
    if start[0] != 0:
        return start
    
    time.sleep(5)
    
    copy = copy_image()
    if copy[0] != 0:
        return copy
    
    extract_and_install = extract_and_install_image()
    if extract_and_install_image[0] != 0:
        extract_and_install

    reboot = reboot_machine()
    if reboot[0] != 0:
        return reboot

    time.sleep(90)
    
    os_version = verify_OS_version()
    if os_version[0] != 0:
        return os_version
    
    poweroff = poweroff_VM(VM_name)
    if poweroff[0] != 0:
        return poweroff
    
    return os_version

def restore_snapshot(VM_name, snapshot_name):
    print(f"Restoring to {snapshot_name} snapshot...")
    return execute(f'VBoxManage snapshot \"{VM_name}\" restore {snapshot_name}')

def start_VM(VM_name):
    print("Starting the VM...")
    return execute(f"VBoxManage startvm \"{VM_name}\" --type headless")

def copy_image():
    print("Copying image to target machine...")
    current_directory = os.getcwd()
    return execute(f"scp {current_directory}/build/tmp-glibc/deploy/images/x64/nilrt-base-system-image-x64.tar admin@NI-cRIO-903x-VM-27108694:/home/admin")

def extract_and_install_image():
    print("Extracting image on target machine...")
    first_cmd = execute('ssh admin@NI-cRIO-903x-VM-27108694 "tar xf /home/admin/nilrt-base-system-image-x64.tar"')
    if first_cmd[0] != 0:
        return first_cmd
    
    second_cmd = execute('ssh admin@NI-cRIO-903x-VM-27108694 "tar xf data.tar.gz -C /mnt/userfs && ./postinst"')
    if second_cmd[0] != 0:
        return second_cmd
    return (0, None)

def reboot_machine():
    print("Rebooting the machine...")
    return execute('ssh admin@NI-cRIO-903x-VM-27108694 "reboot"')

def verify_OS_version():
    print("Verifying OS version...")
    return execute('ssh admin@NI-cRIO-903x-VM-27108694 "cat /etc/os-release"')

def poweroff_VM(VM_name):
    print("Powering off the VM...")
    return execute(f"VBoxManage controlvm \"{VM_name}\" poweroff")

if __name__ == "__main__":
    test("NILRTAgain", "Clean_SSHEnabled")