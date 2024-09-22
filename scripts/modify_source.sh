#!/bin/bash

source ${ROOT_DIR:-$PWD}/scripts/set_env.sh

# 会进来两次，要根据对应代码路径是否存在来修改，默认是第二次调用
# 第一次是 git clone 后
# 第二次是 gclient sync 后

remove_text_line() {
    local filename="\$1"
    local pattern="\$2"
    sed -i "|$pattern|d" "$filename"
}

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
    git checkout $VERSION
    
    log "checkout source finish"
    exit 0
fi

cd $ROOT_DIR/flutter/engine

# 去掉 android 的单元测试
remove_text_line "src/flutter/BUILD.gn" "//flutter/impeller/toolkit/android:apk_unittests"
remove_text_line "src/flutter/BUILD.gn" "//flutter/impeller/toolkit/android:unittests"
remove_text_line "src/flutter/BUILD.gn" "//flutter/shell/platform/android:flutter_shell_native_unittests"

log "modify source finish"
