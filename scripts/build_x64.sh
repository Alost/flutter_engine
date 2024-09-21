#!/bin/bash

set -euv
set -o pipefail

export ROOT_DIR="${ROOT_DIR:-$PWD}"
export PATH=$ROOT_DIR/flutter/depot_tools:$PATH

source $ROOT_DIR/scripts/common.sh

log "build x64 start"

cd $ROOT_DIR/flutter/engine/src
flutter/tools/gn --android --runtime-mode release --android-cpu x64
ninja -C out/android_release_x64

mkdir -p lib/x86_64/
cp out/android_release/lib.stripped/libflutter.so lib/x86_64/

log "build x64 finish"
