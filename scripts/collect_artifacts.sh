#!/bin/bash

source ${ROOT_DIR:-$PWD}/scripts/set_env.sh

log "collect artifacts start"

cd $ROOT_DIR/flutter/engine/src
rm -rf lib.tar.gz
tar -czvf lib.tar.gz lib

log "collect artifacts finish"
