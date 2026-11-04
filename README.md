<div align="center">

<img src="assets/hero.svg" width="100%" alt="AA Linux desktop: system info (AA Linux 0.1, kernel 6.18.60 LTS, BusyBox init, aarch64), 0.236 s from power-on to /init, a file tree with rootfs/etc/inittab open, and the roadmap" />

<br/><br/>

<img alt="kernel 6.18 LTS" src="https://img.shields.io/badge/kernel-6.18_LTS-c4a7e7?style=flat-square&labelColor=17141f" />
<img alt="BusyBox 1.38" src="https://img.shields.io/badge/busybox-1.38-eb6f92?style=flat-square&labelColor=17141f" />
<img alt="arch aarch64" src="https://img.shields.io/badge/arch-aarch64-9ccfd8?style=flat-square&labelColor=17141f" />
<img alt="status: boots to shell" src="https://img.shields.io/badge/status-boots_to_shell-f6c177?style=flat-square&labelColor=17141f" />
<img alt="license MIT" src="https://img.shields.io/badge/license-MIT-ebbcba?style=flat-square&labelColor=17141f" />

<sub>kernel + busybox + initramfs · built from source on an M2 MacBook · power-on to <code>/init</code> in 0.24 s</sub>

</div>

<br/>

<img src="assets/h-about.svg" width="100%" alt="~/about" />

A tiny Linux distribution we're building by hand: our own kernel build, BusyBox and our own boot scripts. There's no Debian or Arch underneath, nothing we didn't put there ourselves. The point is to understand every step from power-on to the shell prompt.

> [!NOTE]
> **Status:** boots to a shell in QEMU on arm64. No package manager and no disk install yet.

<br/>

<img src="assets/h-first-boot.svg" width="100%" alt="~/first-boot" />

<img src="assets/boot.svg" width="100%" alt="First boot of AA Linux in QEMU: the kernel log ends with 'Run /init as init process', then 'Welcome to AA Linux 0.1' and a shell runs uname -sr, cat /etc/os-release and ls /" />

<sub>Real output of <code>./scripts/run-qemu.sh</code>, kernel log trimmed.</sub>

<br/>

<img src="assets/h-inside.svg" width="100%" alt="~/inside" />

<img src="assets/stack.svg" width="100%" alt="What's inside: Linux 6.18.60 LTS kernel with the stock arm64 config and no modules; static BusyBox 1.38 with sh, init and ~300 commands; a 1.1 MiB initramfs; rootfs/ with inittab, rcS and os-release" />

<br/>

<img src="assets/h-boot-chain.svg" width="100%" alt="~/boot-chain" />

<img src="assets/chain.svg" width="100%" alt="Boot chain: qemu loads the kernel and initramfs; the kernel unpacks the initramfs; /init is BusyBox init, pid 1, at 0.236 s; init reads inittab; rcS mounts /proc, /sys and /dev; a shell starts on the console" />

<br/>

<img src="assets/h-build.svg" width="100%" alt="~/build" />

```sh
# macOS, Apple Silicon
brew install qemu lima
./scripts/build-macos.sh   # the first run sets up a Debian VM, later rebuilds take seconds
./scripts/run-qemu.sh
```

```sh
# Linux, arm64 (Debian / Ubuntu)
sudo apt install build-essential bc bison flex libssl-dev libelf-dev cpio curl xz-utils bzip2 qemu-system-arm
./scripts/build.sh
./scripts/run-qemu.sh
```

To leave: type `poweroff`, or press <kbd>Ctrl</kbd>+<kbd>A</kbd>, then <kbd>X</kbd>.

macOS can't build the Linux kernel, so `build-macos.sh` builds inside a [Lima](https://lima-vm.io) VM called `aa-builder` and copies the result to `out/`. The pictures in this README are drawn by [`assets/generate.py`](assets/generate.py).

<br/>

<img src="assets/h-crew.svg" width="100%" alt="~/crew" />

<img src="assets/crew.svg" width="100%" alt="Crew: 01 Алтай Абдурахим and 02 Атай Махмудов, team AA Linux" />

<br/>

<a href="LICENSE"><img src="assets/footer.svg" width="100%" alt="Made by Алтай and Атай, MIT license, 2026" /></a>
