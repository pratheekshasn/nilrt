#!/bin/bash

SCRIPT_ROOT=$(realpath $(dirname $BASH_SOURCE))

. "${SCRIPT_ROOT}/build.common.sh"

echo "Current working directory: $(pwd)"
echo 'NILRT_MAIN_FEED_VERSION = "2025Q2"' >> ./conf/local.conf

echo "INFO: Building the core package feed."
bitbake packagefeed-ni-core
bitbake package-index

# AB#2791248: Build the Linux Kernel to ensure CVEs are made available
bitbake linux-nilrt
