#!/usr/bin/env bash
# macOS cannot build the Linux kernel, so this runs scripts/build.sh inside
# a Lima Linux VM and copies the result back to out/.
set -euo pipefail
cd "$(dirname "$0")/.."
VM=aa-builder

if ! limactl list -q 2>/dev/null | grep -qx "$VM"; then
  # No shared folders: kernel sources need a case-sensitive filesystem,
  # so everything is built on the VM's own disk.
  limactl start --name="$VM" --cpus=4 --memory=4 --mount-none --containerd=none --tty=false template:debian-13
  limactl shell --workdir / "$VM" sudo apt-get update
  limactl shell --workdir / "$VM" sudo DEBIAN_FRONTEND=noninteractive apt-get install -y \
    build-essential bc bison flex libssl-dev libelf-dev cpio curl xz-utils bzip2
elif [ "$(limactl list --format '{{.Status}}' "$VM")" != Running ]; then
  limactl start "$VM"
fi

# Copy our sources into the VM. build/ stays there between runs, so rebuilds are fast.
COPYFILE_DISABLE=1 tar --no-xattrs -cf - scripts rootfs |
  limactl shell --workdir / "$VM" sh -c 'mkdir -p ~/aa-linux && cd ~/aa-linux && rm -rf scripts rootfs && tar -xf -'
limactl shell --workdir / "$VM" sh -c '~/aa-linux/scripts/build.sh'

mkdir -p out
limactl shell --workdir / "$VM" sh -c 'cd ~/aa-linux/out && tar -cf - Image initramfs.cpio.gz' | tar -C out -xf -
echo "Copied to out/. Run ./scripts/run-qemu.sh"
