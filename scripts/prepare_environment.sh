#!/bin/bash

set -eux
set -o pipefail

uname -a
df -hT .
cat /etc/os-release
hostnamectl
lsb_release -a
free -h
df -hT
nproc
cat /proc/cpuinfo
lscpu
lshw -short
ifconfig

sudo apt clean all
sudo apt update
sudo apt install -y ninja-build pkg-config openjdk-21-jdk
