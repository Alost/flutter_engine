#!/bin/bash

set -euv
set -o pipefail

export ROOT_DIR="${ROOT_DIR:-$PWD}"

source $ROOT_DIR/scripts/common.sh

cd $ROOT_DIR/flutter/engine/src
rm -rf lib.tar.gz
tar -czvf lib.tar.gz lib
