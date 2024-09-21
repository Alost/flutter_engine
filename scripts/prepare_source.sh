#!/bin/bash

set -eux
set -o pipefail

export ROOT_DIR="${ROOT_DIR:-$PWD}"

source $ROOT_DIR/scripts/common.sh

log "prepare source start"

# depot_tools 工具
mkdir $ROOT_DIR/flutter; cd $ROOT_DIR/flutter;
git clone --depth 1 https://chromium.googlesource.com/chromium/tools/depot_tools.git
echo "export PATH=$ROOT_DIR/flutter/depot_tools:$PATH" >> ~/.bashrc
source ~/.bashrc
export PATH=$ROOT_DIR/flutter/depot_tools:$PATH
echo "export PATH=$ROOT_DIR/flutter/depot_tools:\$PATH" >> $GITHUB_ENV # github actions 共享环境变量

# flutter engine 代码
mkdir $ROOT_DIR/flutter/source; cd $ROOT_DIR/flutter/source
git clone --depth 1 https://github.com/flutter/engine.git

# 切换版本
($ROOT_DIR/scripts/modify_source.sh "1")
git config --global user.email "flutter@example.com" && git config --global user.name "flutter"
git add . && git commit -am "modify"

# 同步依赖
mkdir $ROOT_DIR/flutter/engine; cd $ROOT_DIR/flutter/engine;
cat <<EOL > .gclient
solutions = [
  {
    "custom_deps": {},
    "deps_file": "DEPS",
    "managed": False,
    "name": "src/flutter",
    "safesync_url": "",
    "url": "$ROOT_DIR/source/engine",
  },
]
EOL
gclient sync

# 修改代码
($ROOT_DIR/scripts/modify_source.sh "2")

log "prepare source finish"
