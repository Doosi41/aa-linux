#!/usr/bin/env bash
# Builds the AA Linux kernel and initramfs. Runs on arm64 Linux (Debian/Ubuntu).
# Result: out/Image (kernel) and out/initramfs.cpio.gz (root filesystem).
set -euo pipefail

KERNEL_VERSION=6.18.60
KERNEL_SHA256=3c2f44ef6acc021a7ad444d9a2e6ec1ef488ff09368793d0004a6080f69d621e
BUSYBOX_VERSION=1.38.0
BUSYBOX_SHA256=34f9ea6ff8636f2c9241153b9114eefa9e65674a45318ae1ef95bb5f31c53bb2

ROOT=$(cd "$(dirname "$0")/.." && pwd)
BUILD=$ROOT/build
OUT=$ROOT/out
JOBS=$(nproc)

mkdir -p "$BUILD" "$OUT"
cd "$BUILD"

# Download a tarball once, verify its checksum, unpack it.
fetch() {
  local url=$1 sha256=$2 file=${1##*/}
  [ -f "$file" ] || curl -fL -o "$file" "$url"
  echo "$sha256  $file" | sha256sum -c -
  [ -d "${file%.tar.*}" ] || tar -xf "$file"
}

fetch "https://cdn.kernel.org/pub/linux/kernel/v6.x/linux-$KERNEL_VERSION.tar.xz" "$KERNEL_SHA256"
fetch "https://busybox.net/downloads/busybox-$BUSYBOX_VERSION.tar.bz2" "$BUSYBOX_SHA256"

# Kernel: the stock arm64 config already supports QEMU's "virt" machine.
# Only the kernel image is built, no modules.
make -C "linux-$KERNEL_VERSION" defconfig
make -C "linux-$KERNEL_VERSION" -j"$JOBS" Image
cp "linux-$KERNEL_VERSION/arch/arm64/boot/Image" "$OUT/"

# BusyBox: one static binary that provides sh, init, mount, ls and ~300 other commands.
make -C "busybox-$BUSYBOX_VERSION" defconfig
sed -i 's/^# CONFIG_STATIC is not set$/CONFIG_STATIC=y/' "busybox-$BUSYBOX_VERSION/.config"
# The tc applet does not compile against kernel headers 6.8+ (CBQ was removed).
sed -i 's/^CONFIG_TC=y$/# CONFIG_TC is not set/' "busybox-$BUSYBOX_VERSION/.config"
make -C "busybox-$BUSYBOX_VERSION" -j"$JOBS"

# Root filesystem: BusyBox plus our files from rootfs/, packed as a cpio archive.
rm -rf initramfs
make -C "busybox-$BUSYBOX_VERSION" CONFIG_PREFIX="$BUILD/initramfs" install
cp -a "$ROOT/rootfs/." initramfs/
mkdir -p initramfs/dev initramfs/proc initramfs/sys initramfs/tmp initramfs/root
ln -s bin/busybox initramfs/init   # the kernel runs /init first; BusyBox acts as init
(cd initramfs && find . | cpio -o -H newc -R 0:0 --quiet | gzip -9) > "$OUT/initramfs.cpio.gz"

echo "Done: $OUT/Image $OUT/initramfs.cpio.gz"
