#!/bin/bash

source ${ROOT_DIR:-$PWD}/scripts/set_env.sh

export ENGINE_DIR=$ROOT_DIR/flutter/engine

cd $ENGINE_DIR

python3 $ROOT_DIR/scripts/modify_source.py

echo "========================================Diff Start======================================"
find . -type d -name ".git" -execdir sh -c 'git diff --exit-code >/dev/null || (git diff && echo "Changes in $(pwd)\n")' \;
echo "========================================Diff End======================================"

log "modify source finish"
