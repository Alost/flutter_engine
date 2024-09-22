#!/bin/bash

source ${ROOT_DIR:-$PWD}/scripts/set_env.sh

log "prepare source start"

# depot_tools 工具
mkdir -p $ROOT_DIR/flutter; cd $ROOT_DIR/flutter;
git clone --depth 1 https://chromium.googlesource.com/chromium/tools/depot_tools.git || true

# 下载代码和依赖
mkdir -p $ROOT_DIR/flutter/engine; cd $ROOT_DIR/flutter/engine;
fetch flutter

# gclient sync

# 切换版本
cd $ROOT_DIR/flutter/engine/src/flutter
git checkout $VERSION

# 下载依赖
gclient sync -D --with_branch_heads --with_tags

# 修改代码
($ROOT_DIR/scripts/modify_source.sh "gclient_sync")

log "prepare source finish"
