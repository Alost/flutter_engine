#!/bin/bash

source ${ROOT_DIR:-$PWD}/scripts/set_env.sh

log "build start"

cd $ROOT_DIR/flutter/engine/src

# rm -rf out/android_release

# flutter/tools/gn ${GN_OPTS:-} --no-prebuilt-dart-sdk --android --runtime-mode release --android-cpu arm
flutter/tools/gn --android --runtime-mode release --android-cpu arm
ninja -C out/android_release

mkdir -p lib/armeabi-v7a/
cp out/android_release/lib.stripped/libflutter.so lib/armeabi-v7a/

log "build finish"
