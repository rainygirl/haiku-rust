#!/bin/bash
set -euo pipefail
cd /work/rustc-1.90.0-src
python3 /exchange/rust-port/prepare.py "$PWD"
export BOOTSTRAP_SKIP_TARGET_SANITY=1
export CARGO_NET_OFFLINE=true
export AARCH64_UNKNOWN_HAIKU_OPENSSL_DIR=/opt/haiku/openssl-3.5.4
export AARCH64_UNKNOWN_HAIKU_OPENSSL_STATIC=0
export CFLAGS_aarch64_unknown_haiku=-I/opt/haiku/zlib-1.2.13/include
python3 x.py build --stage 2 compiler/rustc library/std src/tools/cargo src/tools/rustdoc
