from Shell_commands import *

def build():
    print("\nStarting Docker setup...\n")
    docker = execute("bash ./docker/create-build-nilrt.sh")
    if docker[0] != 0:
        print(docker)
        return docker
    print("\nDocker setup completed.")
    
    print("\nSourcing OE environment...\n")
    source = execute("bash -c '. ni-oe-init-build-env --org'")
    if source[0] != 0:
        print(source)
        return source
    print("\nOE environment sourced.\n")

    print("\nBuilding core feeds...\n")
    core_feeds = execute("bash scripts/pipelines/build.core-feeds.sh")
    if core_feeds[0] != 0:
        print(core_feeds)
        return core_feeds
    print("\nCore feeds build completed.\n")

    print("\nBuilding safemode rootfs...\n")
    safemode = execute("bitbake nilrt-safemode-rootfs")
    if safemode[0] != 0:
        print(safemode)
        return safemode
    print("\nSafemode rootfs build completed.\n")

    print("\nBuilding base system image...\n")
    BSI = execute("bitbake nilrt-base-system-image")
    if BSI[0] != 0:
        print(BSI)
        return BSI
    print("\nBase system image build completed.\n")

    print("\nBuilding recovery media...\n")
    recovery = execute("bitbake nilrt-recovery-media")
    if recovery[0] != 0:
        print(recovery)
        return recovery
    print("\nRecovery media build completed.\n")

    return (0, None)
