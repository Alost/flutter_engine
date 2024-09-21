#!/bin/bash

source ${ROOT_DIR:-$PWD}/scripts/set_env.sh

# CPU性能从高到低排序：7763,8370C,8272CL,8171M,E5系列
cat /proc/cpuinfo | grep 'model name'
lscpu | grep 'Model name'

uname -a
df -hT .
df -hT
free -h

nproc
lscpu
cat /proc/cpuinfo
hostnamectl
lsb_release -a
cat /etc/os-release
lshw -short
ifconfig
swapon --show

sudo apt-get install -y ninja-build pkg-config openjdk-21-jdk

sudo fallocate -l 6G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
sudo sysctl vm.swappiness=25
