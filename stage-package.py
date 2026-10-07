"""Assemble only native target artifacts; never include host proc-macro libraries."""
import argparse
from pathlib import Path
import shutil
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument("--source", type=Path, required=True)
parser.add_argument("--cargo", type=Path, required=True)
parser.add_argument("--rustdoc", type=Path, required=True)
parser.add_argument("--output", type=Path, required=True)
args = parser.parse_args()
target = "aarch64-unknown-haiku"
native = args.source / "build" / target / "stage2"
standard = args.source / "build/aarch64-unknown-linux-gnu/stage2/lib/rustlib" / target / "lib"
assert list(standard.glob("libstd-*.rlib")), "missing target standard library"
driver, = native.glob("lib/librustc_driver-*.so")
for binary in (native / "bin/rustc", driver, args.cargo, args.rustdoc):
    assert binary.is_file(), binary
    header = subprocess.check_output([
        "/opt/haiku/cross-tools-arm64/bin/aarch64-unknown-haiku-readelf", "-h", str(binary)
    ], text=True)
    assert "AArch64" in header, binary
    dynamic = subprocess.check_output([
        "/opt/haiku/cross-tools-arm64/bin/aarch64-unknown-haiku-readelf", "-d", str(binary)
    ], text=True)
    assert "[libroot.so]" in dynamic and "[libc.so.6]" not in dynamic, binary

args.output.mkdir(parents=True, exist_ok=False)
(args.output / "bin").mkdir()
(args.output / "lib").mkdir()
for name, source in (("rustc", native / "bin/rustc"), ("cargo", args.cargo), ("rustdoc", args.rustdoc)):
    shutil.copy2(source, args.output / "bin" / name)
shutil.copy2(driver, args.output / "lib" / driver.name)
shutil.copytree(standard, args.output / "lib/rustlib" / target / "lib")
documentation = args.output / "documentation/packages/rust"
documentation.mkdir(parents=True)
for name in ("LICENSE-MIT", "LICENSE-APACHE", "COPYRIGHT"):
    shutil.copy2(args.source / name, documentation / name)
shutil.copy2(Path(__file__).with_name("PackageInfo"), args.output / ".PackageInfo")
print(args.output)
