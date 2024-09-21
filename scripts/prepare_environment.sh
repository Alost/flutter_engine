#!/bin/bash

set -eux
set -o pipefail

sudo apt clean all
sudo apt update
sudo apt install -y ninja-build pkg-config openjdk-21-jdk

nproc
cat /proc/cpuinfo
free -h
df -h
