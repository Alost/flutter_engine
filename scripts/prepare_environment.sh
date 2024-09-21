#!/bin/bash

set -eux
set -o pipefail

apt clean all
apt update
apt install -y ninja-build pkg-config openjdk-21-jdk
