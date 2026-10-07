#!/bin/bash
set -euo pipefail
cd /work
sha256sum -c openssl-3.5.4.tar.gz.sha256
cd openssl-3.5.4
perl Configure --config=/exchange/rust-port/openssl-haiku.conf haiku-aarch64 \
    --cross-compile-prefix=/opt/haiku/cross-tools-arm64/bin/aarch64-unknown-haiku- \
    --prefix=/opt/haiku/openssl-3.5.4 --libdir=lib \
    --openssldir=/boot/system/data/ssl shared no-tests
make -j8 build_libs
make install_dev
