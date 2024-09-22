#!/bin/bash

source ${ROOT_DIR:-$PWD}/scripts/set_env.sh

log "prepare source start"

# depot_tools 工具
mkdir -p $ROOT_DIR/flutter; cd $ROOT_DIR/flutter;
git clone --depth 1 https://chromium.googlesource.com/chromium/tools/depot_tools.git || true

# flutter engine 代码
mkdir -p $ROOT_DIR/flutter/source; cd $ROOT_DIR/flutter/source
git clone https://github.com/flutter/engine.git || true

# 切换版本
($ROOT_DIR/scripts/modify_source.sh "git_clone")
git config --global user.email "flutter@example.com" && git config --global user.name "flutter"
git add . && git commit -am "modify"

# 同步依赖
mkdir -p $ROOT_DIR/flutter/engine; cd $ROOT_DIR/flutter/engine;
cat <<EOL > .gclient
solutions = [
  {
    "custom_deps": {},
    "deps_file": "DEPS",
    "managed": False,
    "name": "src/flutter",
    "safesync_url": "",
    "url": "$ROOT_DIR/flutter/source/engine",
  },
]
EOL
# gclient sync
gclient sync -D --with_branch_heads --with_tags

# 修改代码
($ROOT_DIR/scripts/modify_source.sh "gclient_sync")

log "prepare source finish"
