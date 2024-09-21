#!/bin/bash

set -eux
set -o pipefail

# 会进来两次，要根据对应代码路径是否存在来修改，默认是第二次调用
# 第一次是 git clone 后
# 第二次是 gclient sync 后

export ROOT_DIR="${ROOT_DIR:-$PWD}"

source $ROOT_DIR/scripts/common.sh

if [ "$1" -eq "git_clone" ]; then
    cd $ROOT_DIR/flutter/source/engine
    git checkout 3.22.3

    log "checkout source finish"
    exit 0
fi

log "modify source finish"
