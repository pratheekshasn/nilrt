from shell_commands import *
import time
import os

def OS_test(VM_name, snapshot_name):
    """
    Perform OS testing on the specified VM.
    Steps:
    1. Restore the VM to a specific snapshot.
    2. Start the VM.
    3. Copy and install the safemode image.
    4. Reboot the machine.
    5. Copy and install the runmode image.
    6. Reboot the machine again.
    7. Verify the OS version.
    8. Power off the VM.
    """
    username="admin"
    target="NI-cRIO-903x-VM-27108694"
    ssh_connection=username+"@"+target

    # Step 1: Restore the VM to the specified snapshot
    restore = restore_snapshot(VM_name, snapshot_name)
    if restore[0] != 0:
        return restore
    
    # Step 2: Start the VM
    start = start_VM(VM_name)
    if start[0] != 0:
        return start
    
    time.sleep(5)  # Wait for the VM to stabilize
    
    # Step 3: Copy and install the safemode image
    copy = copy_image("nilrt-safemode-rootfs-x64.tar.gz" , ssh_connection)
    if copy[0] != 0:
        return copy
    
    extract_and_install = extract_and_install_safemode_image(ssh_connection)
    if extract_and_install[0] != 0:
        return extract_and_install
    
    # Step 4: Reboot the machine
    reboot = reboot_machine(ssh_connection)
    if reboot[0] != 0:
        return reboot

    time.sleep(90)  # Wait for the machine to reboot
    
    # Step 5: Copy and install the runmode image
    copy = copy_image("nilrt-base-system-image-x64.tar" , ssh_connection)
    if copy[0] != 0:
        return copy
    
    extract_and_install = extract_and_install_runmode_image(ssh_connection)
    if extract_and_install[0] != 0:
        return extract_and_install

    # Step 6: Reboot the machine again
    reboot = reboot_machine(ssh_connection)
    if reboot[0] != 0:
        return reboot

    time.sleep(90)  # Wait for the machine to reboot again
    
    # Step 7: Verify the OS version
    os_version = verify_OS_version(ssh_connection)
    if os_version[0] != 0:
        return os_version
    
    # Step 8: Power off the VM
    poweroff = poweroff_VM(VM_name)
    if poweroff[0] != 0:
        return poweroff
    
    return os_version

def restore_snapshot(VM_name, snapshot_name):
    """
    Restore the VM to the specified snapshot.
    """
    print(f"Restoring to {snapshot_name} snapshot...")
    return execute_and_stream_cmd_output(f'VBoxManage snapshot \"{VM_name}\" restore {snapshot_name}')

def start_VM(VM_name):
    """
    Start the VM in headless mode.
    """
    print("Starting the VM...")
    return execute_and_stream_cmd_output(f"VBoxManage startvm \"{VM_name}\" --type headless")

def copy_image(filename ,ssh_connection):
    """
    Copy the image to the target machine.
    """
    print("Copying image to target machine...")
    current_directory = os.getcwd()
    return execute_and_stream_cmd_output(f"scp {current_directory}/build/tmp-glibc/deploy/images/x64/{filename} {ssh_connection}:/home/admin")

def extract_and_install_safemode_image(ssh_connection):
    """
    Extract and install the safemode image on the target machine.
    """
    print("Extracting safemode image on target machine...")
    return execute_and_stream_cmd_output(f'ssh {ssh_connection} "tar xf nilrt-safemode-rootfs-x64.tar.gz -C /boot/.safe/"')

def extract_and_install_runmode_image(ssh_connection):
    """
    Extract and install the runmode image on the target machine.
    """
    print("Extracting runmode image on target machine...")
    first_cmd = execute_and_stream_cmd_output(f'ssh {ssh_connection} "tar xf /home/admin/nilrt-base-system-image-x64.tar"')
    if first_cmd[0] != 0:
        return first_cmd
    
    second_cmd = execute_and_stream_cmd_output(f'ssh {ssh_connection} "tar xf data.tar.gz -C /mnt/userfs && ./postinst"')
    if second_cmd[0] != 0:
        return second_cmd
    return (0, None)

def reboot_machine(ssh_connection):
    """
    Reboot the target machine.
    """
    print("Rebooting the machine...")
    return execute_and_stream_cmd_output(f'ssh {ssh_connection} "reboot"')

def verify_OS_version(ssh_connection):
    """
    Verify the OS version on the target machine.
    """
    print("Verifying OS version...")
    return execute_and_stream_cmd_output(f'ssh {ssh_connection} "cat /etc/os-release"')

def poweroff_VM(VM_name):
    """
    Power off the VM.
    """
    print("Powering off the VM...")
    return execute_and_stream_cmd_output(f"VBoxManage controlvm \"{VM_name}\" poweroff")

if __name__ == "__main__":
    VM_name = "NILRTAgain"
    snapshot_name = "Clean_SSHEnabled"
    
    status_code, message = OS_test(VM_name, snapshot_name)
    
    if status_code == 0:
        print("\nOS test completed successfully.")
    else:
        print(f"\nOS test failed with status code {status_code}. Error: {message}")
