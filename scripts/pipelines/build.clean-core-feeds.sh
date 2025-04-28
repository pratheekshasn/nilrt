#!/bin/bash

SCRIPT_ROOT=$(realpath $(dirname $BASH_SOURCE))

. "${SCRIPT_ROOT}/build.common.sh"

echo "INFO: Cleaning and building the core package feed."
bitbake -c cleanall packagefeed-ni-core
bitbake -c cleanall package-index
bitbake -c cleanall linux-nilrt

echo "INFO: Building the core package feed."
bitbake packagefeed-ni-core
bitbake package-index
bitbake linux-nilrt