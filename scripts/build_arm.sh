#!/bin/bash

set -euv
set -o pipefail

export ROOT_DIR="${ROOT_DIR:-$PWD}"
export PATH=$ROOT_DIR/flutter/depot_tools:$PATH

source $ROOT_DIR/scripts/common.sh

log "build arm start"

cd $ROOT_DIR/flutter/engine/src

GN_OPTS = --no-goma --no-build-embedder-examples --no-enable-unittests --no-dart-version-git-info --unoptimized --no-lto --no-clang-static-analyzer
flutter/tools/gn $GN_OPTS --no-prebuilt-dart-sdk --android --runtime-mode release --android-cpu arm
ninja -C out/android_release

mkdir -p lib/armeabi-v7a/
cp out/android_release/lib.stripped/libflutter.so lib/armeabi-v7a/

log "build arm finish"
