#!/bin/bash

source ${ROOT_DIR:-$PWD}/scripts/set_env.sh

cd $ROOT_DIR/flutter/engine/src
rm -rf lib.tar.gz
tar -czvf lib.tar.gz lib
