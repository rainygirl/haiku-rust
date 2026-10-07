#!/bin/bash
set -euo pipefail
cd /work
if [ ! -f zlib-1.2.13.tar.gz ]; then
    curl -fL --retry 2 https://zlib.net/fossils/zlib-1.2.13.tar.gz -o zlib-1.2.13.tar.gz
fi
tar -xzf zlib-1.2.13.tar.gz
cd zlib-1.2.13
CC=/opt/haiku/cross-tools-arm64/bin/aarch64-unknown-haiku-gcc \
AR=/opt/haiku/cross-tools-arm64/bin/aarch64-unknown-haiku-ar \
RANLIB=/opt/haiku/cross-tools-arm64/bin/aarch64-unknown-haiku-ranlib \
CHOST=aarch64-unknown-haiku ./configure --prefix=/opt/haiku/zlib-1.2.13 --static
make -j8
make install
