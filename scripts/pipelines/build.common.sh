#!/bin/bash
set -e

SCRIPT_ROOT=$(realpath $(dirname $BASH_SOURCE))

. "${SCRIPT_ROOT}/../../ni-oe-init-build-env" $@

echo "Current working directory: $(pwd)"
echo 'NILRT_MAIN_FEED_VERSION = "2025Q2"' >> ./conf/local.conf

bitbake --version
#printenv | grep -i ^PYREX

export PS1="[bb] $PS1"

echo "INFO: Entered bitbake environment."
