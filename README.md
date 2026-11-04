<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0f2027,50:203a43,100:2c5364&height=200&section=header&text=AA%20Linux&fontSize=72&fontColor=ffffff&fontAlignY=35&desc=a%20Linux%20distribution%20built%20from%20scratch&descAlignY=56&animation=fadeIn" width="100%" alt="AA Linux" />

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=500&size=20&pause=1000&color=2C9BCB&center=true&vCenter=true&width=560&lines=Linux+kernel+%2B+BusyBox+%2B+initramfs;From+power-on+to+shell+prompt;Made+on+an+M2+MacBook" alt="Linux kernel + BusyBox + initramfs" />

<br/>

<img src="https://img.shields.io/badge/kernel-6.18_LTS-FCC624?style=for-the-badge&logo=linux&logoColor=black" alt="kernel 6.18 LTS" />
<img src="https://img.shields.io/badge/BusyBox-1.38-2C5364?style=for-the-badge" alt="BusyBox 1.38" />
<img src="https://img.shields.io/badge/arch-arm64-0091BD?style=for-the-badge&logo=arm&logoColor=white" alt="arm64" />
<img src="https://img.shields.io/badge/runs_in-QEMU-FF6600?style=for-the-badge&logo=qemu&logoColor=white" alt="QEMU" />
<img src="https://img.shields.io/badge/status-early_work-orange?style=for-the-badge" alt="status: early work" />
<img src="https://img.shields.io/github/license/Doosi41/aa-linux?style=for-the-badge" alt="license" />

</div>

## 🐧 About

AA Linux is a small Linux distribution we're building from scratch: the Linux kernel, BusyBox and our own boot scripts. The goal is to understand every step a Linux system takes, from the moment the kernel starts to the shell prompt.

> **Status:** the build scripts are written, and the first boot in QEMU (arm64) is being tested. There is no package manager and no installation to disk yet.

## 🧩 What's inside

| Part | What it does |
| --- | --- |
| **Linux 6.18 LTS** | The kernel, built with the stock arm64 config and no modules |
| **BusyBox 1.38** | One static binary that provides the shell, `init` and the core commands |
| **initramfs** | The whole system is loaded into RAM at boot |
| **[`rootfs/`](rootfs)** | Our own files: init configuration, boot script, `os-release` |

## 🚀 How it boots

```mermaid
flowchart LR
    A[QEMU] -->|loads| B[Kernel<br/>out/Image]
    B -->|unpacks| C[initramfs]
    C -->|runs /init| D[BusyBox init]
    D -->|reads /etc/inittab| E[rcS<br/>mounts /proc /sys /dev]
    E --> F[Shell]
```

## 🛠 Build and run

**macOS (Apple Silicon)**

```sh
brew install qemu lima
./scripts/build-macos.sh
./scripts/run-qemu.sh
```

macOS can't build the Linux kernel, so `build-macos.sh` runs the build inside a Debian VM called `aa-builder` (created by [Lima](https://lima-vm.io) on the first run) and copies the result to `out/`.

**Linux (arm64, Debian or Ubuntu)**

```sh
sudo apt install build-essential bc bison flex libssl-dev libelf-dev cpio curl xz-utils bzip2 qemu-system-arm
./scripts/build.sh
./scripts/run-qemu.sh
```

To leave QEMU, type `poweroff`, or press `Ctrl-A` and then `X`.

## 📁 Repository layout

| Path | What it is |
| --- | --- |
| [`scripts/build.sh`](scripts/build.sh) | Downloads and checksums the sources, builds the kernel and BusyBox, packs the initramfs |
| [`scripts/build-macos.sh`](scripts/build-macos.sh) | Runs `build.sh` inside a Lima VM on macOS |
| [`scripts/run-qemu.sh`](scripts/run-qemu.sh) | Boots the result in QEMU |
| [`rootfs/`](rootfs) | Files copied into the root filesystem as they are |

## 🗺 Roadmap

- [ ] First boot to a shell in QEMU
- [ ] Our own package manager
- [ ] Boot on real hardware (x86_64 laptop from a USB stick)

## 🧰 Built with

<p align="left">
  <img src="https://skillicons.dev/icons?i=linux,bash,debian,apple" alt="Linux, Bash, Debian, macOS" />
</p>

## 👥 Authors

- **Altai Abdurahim**
- **Atay Mahmudov**

<a href="https://github.com/Doosi41/aa-linux/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=Doosi41/aa-linux" alt="Contributors" />
</a>

## 📄 License

[MIT](LICENSE)

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:2c5364,50:203a43,100:0f2027&height=100&section=footer" width="100%" alt="" />
