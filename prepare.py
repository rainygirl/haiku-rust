"""Prepare the checksum-verified Rust 1.90.0 source for Haiku ARM64."""
from pathlib import Path
import shutil
import sys

source = Path(sys.argv[1])
here = Path(__file__).resolve().parent
assert (source / "src/version").read_text().strip() == "1.90.0"
spec = source / "compiler/rustc_target/src/spec"
shutil.copy2(here / "aarch64_unknown_haiku.rs", spec / "targets/aarch64_unknown_haiku.rs")
registration = spec / "mod.rs"
text = registration.read_text()
if '("aarch64-unknown-haiku",' not in text:
    anchor = '    ("i686-unknown-haiku", i686_unknown_haiku),'
    assert text.count(anchor) == 1
    registration.write_text(text.replace(anchor, '    ("aarch64-unknown-haiku", aarch64_unknown_haiku),\n' + anchor))
shutil.copy2(here / "bootstrap.toml", source / "bootstrap.toml")

# The bootstrap ARM64 repository currently has no downloadable zlib_devel.
# Supply only the conventional linker-name symlink to the VM's real ARM64
# runtime library; do not substitute a Linux library or change system headers.
sysroot = Path("/opt/haiku/cross-tools-arm64/sysroot")
zlib_runtime = sysroot / "boot/system/lib/libz.so.1"
zlib_link = sysroot / "boot/system/develop/lib/libz.so"
assert zlib_runtime.is_file(), "export the guest's installed zlib runtime first"
if not zlib_link.exists():
    zlib_link.symlink_to("../../lib/libz.so.1")
