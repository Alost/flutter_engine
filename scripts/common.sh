#!/bin/bash

set -euv
set -o pipefail

log_file="script.log"
log() {
    local timestamp=$(date +"%Y-%m-%d %H:%M:%S")
    echo "[$timestamp] $1" | tee -a "$log_file"
}
