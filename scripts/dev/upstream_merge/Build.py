from Shell_commands import *
import os

def build():
    print("Starting Docker setup...")
    for line in execute("bash ./docker/create-build-nilrt.sh"):
        print(line)
    print("Docker setup completed.")
    
    print("Sourcing OE environment...")
    for line in execute("bash -c '. ni-oe-init-build-env --org'"):
        print(line)
    print("OE environment sourced.")
    
    os.chdir(os.getcwd() + "/build")

    print("Building core feeds...")
    for line in execute("bash ../scripts/pipelines/build.core-feeds.sh"):
        print(line)
    print("Core feeds build completed.")
    
    print("Building safemode rootfs...")
    for line in execute("bitbake nilrt-safemode-rootfs"):
        print(line)
    print("Safemode rootfs build completed.")

    print("Building base system image...")
    for line in execute("bitbake nilrt-base-system-image"):
        print(line)
    print("Base system image build completed.")

    print("Building recovery media...")
    for line in execute("bitbake nilrt-recovery-media"):
        print(line)
    print("Recovery media build completed.")

    return (0, None)

if __name__ == "__main__":
    build()