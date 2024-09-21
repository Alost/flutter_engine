#!/bin/bash

set -eux
set -o pipefail

export ROOT_DIR="${ROOT_DIR:-$PWD}"

echo $PATH
export PATH=$ROOT_DIR/flutter/depot_tools:$PATH

source $ROOT_DIR/scripts/common.sh

log "build arm start"

cd $ROOT_DIR/flutter/engine/src
flutter/tools/gn --android --runtime-mode release --android-cpu arm
ninja -C out/android_release

mkdir -p lib/armeabi-v7a/
cp out/android_release/lib.stripped/libflutter.so lib/armeabi-v7a/

log "build arm finish"
