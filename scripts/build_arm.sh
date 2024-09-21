#!/bin/bash

source $ROOT_DIR/scripts/set_env.sh

log "build start"

cd $ROOT_DIR/flutter/engine/src

# rm -rf out/android_release
GN_OPTS="--no-goma --no-build-embedder-examples --no-enable-unittests --no-dart-version-git-info --no-clang-static-analyzer"
flutter/tools/gn ${GN_OPTS:-} --no-prebuilt-dart-sdk --android --runtime-mode release --android-cpu arm
ninja -C out/android_release

mkdir -p lib/armeabi-v7a/
cp out/android_release/lib.stripped/libflutter.so lib/armeabi-v7a/

log "build finish"
