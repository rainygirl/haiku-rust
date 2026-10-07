#!/bin/bash
# Run inside the installed Haiku ARM64 VM, with the candidate toolchain on PATH.
set -euo pipefail
cd "$(dirname "$0")"
test "$(uname -m)" = arm64
rustc -vV
cargo -vV
[[ "$(rustc -vV)" == *"host: aarch64-unknown-haiku"* ]]
rustc --edition=2021 smoke.rs -o smoke-native
./smoke-native
rustc --edition=2021 --crate-type=proc-macro smoke_macro.rs -o libsmoke_macro.so
rustc --edition=2021 smoke_macro_user.rs --extern smoke_macro=libsmoke_macro.so -o smoke-macro-native
./smoke-macro-native
test_root=$(mktemp -d /boot/home/rust-native-test.XXXXXX)
cargo new --vcs none "$test_root/example"
cp smoke.rs "$test_root/example/src/main.rs"
cp smoke_lib.rs "$test_root/example/src/lib.rs"
cargo run --offline --manifest-path "$test_root/example/Cargo.toml"
cargo test --offline --manifest-path "$test_root/example/Cargo.toml"
echo "PASS: rustc and Cargo native build/run/test; artifacts: $test_root"
