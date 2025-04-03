from shell_commands import *

def build_images():
    docker = start_docker_setup()
    if docker[0] != 0:
        return docker
    print("\nDocker setup completed.")
    
    core_feeds = build_core_feeds()
    if core_feeds[0] != 0:
        return core_feeds
    print("\nCore feeds build completed.")   

    core_images = build_core_images()
    if core_images[0] != 0:
        return core_images
    print("\nCore images build completed.")

    return (0, None)

def start_docker_setup():
    print("\nStarting Docker setup...\n")
    return execute("bash ./docker/create-build-nilrt.sh")

def build_core_feeds():
    print("\nBuilding core feeds...\n")
    return execute("bash scripts/pipelines/build.core-feeds.sh")

def build_core_images():
    print("\nBuilding core images...\n")
    return execute("bash scripts/pipelines/build.core-images.sh")
    