#!/bin/bash

source ${ROOT_DIR:-$PWD}/scripts/set_env.sh

log "build start"

cd $ROOT_DIR/flutter/engine/src

# rm -rf out/android_release_x64

flutter/tools/gn ${GN_OPTS:-} --no-prebuilt-dart-sdk --android --runtime-mode release --android-cpu x64
ninja -C out/android_release_x64

mkdir -p lib/x86_64/
cp out/android_release_x64/lib.stripped/libflutter.so lib/x86_64/

log "build finish"
