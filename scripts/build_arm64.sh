#!/bin/bash

source ${ROOT_DIR:-$PWD}/scripts/set_env.sh

log "build start"

cd $ROOT_DIR/flutter/engine/src

# rm -rf out/android_release_arm64

flutter/tools/gn ${GN_OPTS:-} --no-prebuilt-dart-sdk --android --runtime-mode release --android-cpu arm64
ninja -C out/android_release_arm64

mkdir -p lib/arm64-v8a/
cp out/android_release_arm64/lib.stripped/libflutter.so lib/arm64-v8a/

log "build finish"
