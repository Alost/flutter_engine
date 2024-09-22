#!/bin/bash

source ${ROOT_DIR:-$PWD}/scripts/set_env.sh

cd $ROOT_DIR/flutter/engine

python3 $ROOT_DIR/scripts/modify_source.py

log "modify source finish"
