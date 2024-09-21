#!/bin/bash

set -euv
set -o pipefail

export ROOT_DIR="${ROOT_DIR:-$PWD}"
export PATH=$ROOT_DIR/flutter/depot_tools:$PATH

source $ROOT_DIR/scripts/common.sh

log "build arm start"

cd $ROOT_DIR/flutter/engine/src
flutter/tools/gn --no-goma --no-prebuilt-dart-sdk --unoptimized --no-lto --android --runtime-mode release --android-cpu arm
ninja -C out/android_release

mkdir -p lib/armeabi-v7a/
cp out/android_release/lib.stripped/libflutter.so lib/armeabi-v7a/

log "build arm finish"
