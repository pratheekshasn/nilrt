from Shell_commands import *

def build():
    print("\nStarting Docker setup...\n")
    docker = execute("bash ./docker/create-build-nilrt.sh")
    if docker[0] != 0:
        print(docker)
        return docker
    print("\nDocker setup completed.")

    print("\nBuilding core feeds...\n")
    core_feeds = execute("bash scripts/pipelines/build.core-feeds.sh")
    if core_feeds[0] != 0:
        print(core_feeds)
        return core_feeds
    print("\nCore feeds build completed.")

    print("\nBuilding core images...\n")
    core_images = execute("bash scripts/pipelines/build.core-images.sh")
    if core_images[0] != 0:
        print(core_images)
        return core_images
    print("\nCore images build completed.")

    return (0, None)
