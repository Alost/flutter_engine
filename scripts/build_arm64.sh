#!/bin/bash

set -euv
set -o pipefail

export ROOT_DIR="${ROOT_DIR:-$PWD}"
export PATH=$ROOT_DIR/flutter/depot_tools:$PATH

source $ROOT_DIR/scripts/common.sh

log "build arm64 start"

cd $ROOT_DIR/flutter/engine/src
flutter/tools/gn --android --runtime-mode release --android-cpu arm64
ninja -C out/android_release_arm64

mkdir -p lib/arm64-v8a/
cp out/android_release/lib.stripped/libflutter.so lib/arm64-v8a/

log "build arm64 finish"
