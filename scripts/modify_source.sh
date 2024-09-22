#!/bin/bash

source ${ROOT_DIR:-$PWD}/scripts/set_env.sh

# 会进来两次，要根据对应代码路径是否存在来修改，默认是第二次调用
# 第一次是 git clone 后
# 第二次是 gclient sync 后

if [ "$1" == "git_clone" ]; then
    cd $ROOT_DIR/flutter/source/engine
    git checkout $VERSION
    
    log "checkout source finish"
    exit 0
fi

cd $ROOT_DIR/flutter/engine

python3 $ROOT_DIR/scripts/modify_source.py

log "modify source finish"
