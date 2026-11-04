#!/usr/bin/env bash
# Boots AA Linux in QEMU. To exit: type "poweroff", or press Ctrl-A, then X.
set -euo pipefail
cd "$(dirname "$0")/.."

if [ "$(uname -s)" = Darwin ] && [ "$(uname -m)" = arm64 ]; then
  ACCEL=(-accel hvf -cpu host)   # Apple Silicon: hardware virtualization, near-native speed
else
  ACCEL=(-accel tcg -cpu max)    # anywhere else: software emulation, slow but works
fi

exec qemu-system-aarch64 -M virt "${ACCEL[@]}" -m 512M -nographic \
  -kernel out/Image -initrd out/initramfs.cpio.gz \
  -append "console=ttyAMA0"
