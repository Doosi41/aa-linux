# AA Linux

A small Linux distribution built from scratch: the Linux kernel, BusyBox and our own boot scripts. We're building it to learn how a Linux system works, from the moment the kernel starts to the shell prompt.

**Status:** early work. The build scripts are written, and the first boot in QEMU (arm64) is being tested. There is no package manager and no installation to disk yet.

## What's inside

- **Linux 6.18 LTS**, built with the stock arm64 config and no modules
- **BusyBox 1.38**: one static binary that provides the shell, `init` and the core commands
- **initramfs**: the whole system is loaded into RAM at boot
- **`rootfs/`**: our own files (init configuration, boot script, `os-release`)

## How it boots

1. QEMU loads the kernel (`out/Image`) and the root filesystem (`out/initramfs.cpio.gz`) into memory.
2. The kernel unpacks the initramfs and runs `/init`, which is BusyBox `init`.
3. `init` reads [`/etc/inittab`](rootfs/etc/inittab) and runs [`/etc/init.d/rcS`](rootfs/etc/init.d/rcS), which mounts `/proc`, `/sys` and `/dev`.
4. `init` starts a shell on the console.

## Build and run

### macOS (Apple Silicon)

```sh
brew install qemu lima
./scripts/build-macos.sh
./scripts/run-qemu.sh
```

macOS can't build the Linux kernel, so `build-macos.sh` runs the build inside a Debian VM called `aa-builder` (created by [Lima](https://lima-vm.io) on the first run) and copies the result to `out/`.

### Linux (arm64, Debian or Ubuntu)

```sh
sudo apt install build-essential bc bison flex libssl-dev libelf-dev cpio curl xz-utils bzip2 qemu-system-arm
./scripts/build.sh
./scripts/run-qemu.sh
```

To leave QEMU, type `poweroff`, or press `Ctrl-A` and then `X`.

## Repository layout

| Path | What it is |
| --- | --- |
| `scripts/build.sh` | Downloads and checksums the sources, builds the kernel and BusyBox, packs the initramfs |
| `scripts/build-macos.sh` | Runs `build.sh` inside a Lima VM on macOS |
| `scripts/run-qemu.sh` | Boots the result in QEMU |
| `rootfs/` | Files copied into the root filesystem as they are |

## Authors

- Altai Abdurahim
- Atay Mahmudov

## License

[MIT](LICENSE)
