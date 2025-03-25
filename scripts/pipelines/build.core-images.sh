#!/bin/bash

SCRIPT_ROOT=$(realpath $(dirname $BASH_SOURCE))

. "${SCRIPT_ROOT}/build.common.sh"

echo "INFO: Building safemode rootfs and base system image and Building recovery media."
bitbake nilrt-safemode-rootfs
bitbake nilrt-base-system-image
bitbake nilrt-recovery-media
