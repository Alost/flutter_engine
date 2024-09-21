#!/bin/bash

set -eux
set -o pipefail

# 会进来两次，要根据对应代码路径是否存在来修改，默认是第二次调用
# 第一次是 git clone 后
# 第二次是 gclient sync 后

export ROOT_DIR="${ROOT_DIR:-$PWD}"

source $ROOT_DIR/scripts/common.sh

replace_lines_with_file() {
    local target_file="$1"
    local start_line="$2"
    local end_line="$3"
    local replace_file="$4"
    
    sed -i "${start_line},${end_line}{ r ${replace_file}
      d
    }" "${target_file}"
}

replace_lines_with_string() {
    local target_file="$1"
    local start_line="$2"
    local end_line="$3"
    local replacement="$4"
    
    local temp_file=$(mktemp)
    echo -e "$replacement" > "$temp_file"

    replace_lines_with_file "$target_file" "$start_line" "$end_line" "$temp_file"

    rm "$temp_file"
}

if [ "$1" == "git_clone" ]; then
    cd $ROOT_DIR/flutter/source/engine
    git checkout 3.22.3

    log "checkout source finish"
    exit 0
fi

log "modify source finish"
