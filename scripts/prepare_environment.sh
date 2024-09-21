#!/bin/bash

set -eux
set -o pipefail

free -h
df -h
df -h .
nproc
cat /proc/cpuinfo

sudo apt clean all
sudo apt update
sudo apt install -y ninja-build pkg-config openjdk-21-jdk
