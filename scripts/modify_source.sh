#!/bin/bash

source ${ROOT_DIR:-$PWD}/scripts/set_env.sh

export ENGINE_DIR=$ROOT_DIR/flutter/engine

cd $ENGINE_DIR

python3 $ROOT_DIR/scripts/modify_source.py

log "modify source finish"
