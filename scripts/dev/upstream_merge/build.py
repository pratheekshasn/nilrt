from shell_commands import *

def build_images():
    """
    Build the required images by performing the following steps:
    1. Set up the Docker environment.
    2. Build the core feeds.
    3. Build the core images.
    :return: A tuple (status_code, message). Returns (0, None) on success.
    """
    # Step 1: Set up the Docker environment
    docker = start_docker_setup()
    if docker[0] != 0:
        return docker
    print("\nDocker setup completed.")
    
    # Step 2: Build the core feeds
    core_feeds = build_core_feeds()
    if core_feeds[0] != 0:
        return core_feeds
    print("\nCore feeds build completed.")   

    # Step 3: Build the core images
    core_images = build_core_images()
    if core_images[0] != 0:
        return core_images
    print("\nCore images build completed.")

    # Return success if all steps are completed
    return (0, None)

def start_docker_setup():
    """
    Start the Docker setup process.
    This script initializes the Docker environment required for building images.
    :return: A tuple (status_code, message). Returns (0, None) on success.
    """
    print("\nStarting Docker setup...\n")
    return execute_and_stream_cmd_output("bash ./docker/create-build-nilrt.sh")

def build_core_feeds():
    """
    Build the core feeds.
    This step involves running the script to build the core feeds required for the images.
    :return: A tuple (status_code, message). Returns (0, None) on success.
    """
    print("\nBuilding core feeds...\n")
    return execute_and_stream_cmd_output("bash scripts/pipelines/build.clean-core-feeds.sh")

def build_core_images():
    """
    Build the core images.
    This step involves running the script to build the core images for the project.
    :return: A tuple (status_code, message). Returns (0, None) on success.
    """
    print("\nBuilding core images...\n")
    return execute_and_stream_cmd_output("bash scripts/pipelines/build.core-images.sh")

if __name__ == "__main__":
    status_code, message = build_images()
    
    if status_code == 0:
        print("\nBuild completed successfully.")
    else:
        print(f"\nBuild failed with status code {status_code}. Error: {message}")
