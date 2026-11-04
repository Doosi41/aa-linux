#!/usr/bin/env python3
"""Draws the README images in this folder. Run: python3 assets/generate.py"""
import math
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent

MONO = ("ui-monospace, 'SF Mono', SFMono-Regular, Menlo, Consolas, "
        "'JetBrains Mono', 'DejaVu Sans Mono', 'Liberation Mono', monospace")
SANS = ("Inter, 'SF Pro Display', -apple-system, BlinkMacSystemFont, "
        "'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif")

# Dark pastel palette
INK, PANEL, RULE = "#120f1c", "#17141f", "#3b3552"
MUTED, SUBTLE, TEXT = "#6e6a86", "#908caa", "#e0def4"
LOVE, GOLD, ROSE, PINE, FOAM, IRIS = "#eb6f92", "#f6c177", "#ebbcba", "#31748f", "#9ccfd8", "#c4a7e7"

BASE_CSS = """
text { font-family: MONO; }
.sans { font-family: SANS; }
.tw { animation: tw 4.5s ease-in-out infinite; }
@keyframes tw { 50% { opacity: .1; } }
.cur { animation: bl 1.1s steps(1) infinite; }
@keyframes bl { 50% { opacity: 0; } }
@media (prefers-reduced-motion: reduce) { * { animation: none !important; } }
""".replace("MONO", MONO).replace("SANS", SANS)

PASTEL = (f'<linearGradient id="pastel" x1="0" y1="0" x2="1" y2="1">'
          f'<stop offset="0" stop-color="{FOAM}"/><stop offset=".5" stop-color="{IRIS}"/>'
          f'<stop offset="1" stop-color="{LOVE}"/></linearGradient>')


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def text(x, y, s, size=13, fill=TEXT, weight=None, anchor=None, cls=None, extra=""):
    a = f' font-weight="{weight}"' if weight else ""
    a += f' text-anchor="{anchor}"' if anchor else ""
    a += f' class="{cls}"' if cls else ""
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}"{a}{extra} xml:space="preserve">{esc(s)}</text>'


def spans(x, y, parts, size=13, extra=""):
    """One line of text made of (string, color[, weight]) parts."""
    body = "".join(
        f'<tspan fill="{p[1]}"' + (f' font-weight="{p[2]}"' if len(p) > 2 else "") + f">{esc(p[0])}</tspan>"
        for p in parts)
    return f'<text x="{x}" y="{y}" font-size="{size}"{extra} xml:space="preserve">{body}</text>'


def sparkle(x, y, s, delay):
    q = s * .22
    d = f"M0,{-s} L{q},{-q} L{s},0 L{q},{q} L0,{s} L{-q},{q} L{-s},0 L{-q},{-q} Z"
    return (f'<path class="tw" style="animation-delay:{delay:.2f}s" transform="translate({x:.0f},{y:.0f})" '
            f'd="{d}" fill="{GOLD}" opacity=".8"/>')


def wallpaper(w, h, seed, moon, sparkles=True, keep_out=()):
    """Night sky: nebula glow, galaxy swirls, a moon and twinkling stars."""
    rnd = random.Random(seed)
    blobs = [(.80, .15, .30, .20, IRIS, .42), (.15, .90, .30, .22, LOVE, .26),
             (.55, .60, .20, .15, FOAM, .14), (.98, .98, .26, .22, PINE, .50),
             (.02, .05, .22, .16, PINE, .34)]
    blob_svg = "".join(
        f'<ellipse cx="{bx * w:.0f}" cy="{by * h:.0f}" rx="{rx * w:.0f}" ry="{ry * w:.0f}" fill="{c}" opacity="{o}"/>'
        for bx, by, rx, ry, c, o in blobs)

    gx, gy = (moon[0], moon[1]) if moon else (w * .7, h * .3)
    swirls = "".join(
        f'<ellipse cx="{gx:.0f}" cy="{gy:.0f}" rx="{r * 2.4:.0f}" ry="{r * .55:.0f}" fill="none" '
        f'stroke="url(#swirl)" stroke-width="{sw}" opacity="{o}" '
        f'stroke-dasharray="{r * 2.2:.0f} {r * 1.4:.0f}" transform="rotate({rot} {gx:.0f} {gy:.0f})"/>'
        for r, sw, o, rot in ((90, 1.4, .45, -16), (140, 1.0, .35, -12), (200, 1.6, .25, -19),
                              (270, .9, .22, -14), (340, 1.2, .16, -17)))

    moon_svg = ""
    if moon:
        mx, my, mr = moon
        moon_svg = (f'<circle cx="{mx}" cy="{my}" r="{mr * 3}" fill="{IRIS}" opacity=".28" filter="url(#neb)"/>'
                    f'<circle cx="{mx}" cy="{my}" r="{mr}" fill="url(#moon)"/>')

    stars = []
    for _ in range(int(w * h / 6500)):
        x, y = rnd.uniform(0, w), rnd.uniform(0, h)
        r = rnd.choice((.5, .7, .9, 1.1, 1.4))
        tw = rnd.random() < .4
        if any(y0 <= y <= y1 for y0, y1 in keep_out):  # no stars behind text that sits on the wallpaper
            continue
        cls = f' class="tw" style="animation-delay:{rnd.uniform(0, 4.5):.2f}s"' if tw else ""
        stars.append(f'<circle{cls} cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="#fff" opacity="{rnd.uniform(.3, .85):.2f}"/>')
    for _ in range(max(2, int(w * h / 90000)) if sparkles else 0):
        stars.append(sparkle(rnd.uniform(20, w - 20), rnd.uniform(14, h - 14), rnd.uniform(4, 7), rnd.uniform(0, 4)))

    return f"""
<radialGradient id="sky" cx=".28" cy=".15" r="1.1">
  <stop offset="0" stop-color="#1d1535"/><stop offset=".55" stop-color="#0f0c1a"/><stop offset="1" stop-color="#07060c"/>
</radialGradient>
<radialGradient id="moon" cx=".38" cy=".35" r=".7">
  <stop offset="0" stop-color="#ffffff"/><stop offset=".7" stop-color="#f1ecff"/><stop offset="1" stop-color="#d9cff5"/>
</radialGradient>
<linearGradient id="swirl" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="{IRIS}" stop-opacity="0"/><stop offset=".4" stop-color="{IRIS}"/>
  <stop offset=".7" stop-color="{GOLD}"/><stop offset="1" stop-color="{ROSE}" stop-opacity="0"/>
</linearGradient>
<filter id="neb" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="{w * .055:.0f}"/></filter>
<filter id="soft"><feGaussianBlur stdDeviation="1.1"/></filter>
<g id="wall">
  <rect width="{w}" height="{h}" fill="url(#sky)"/>
  <g filter="url(#neb)">{blob_svg}</g>
  <g filter="url(#soft)">{swirls}</g>
  {moon_svg}
  {''.join(stars)}
</g>"""


class Scene:
    """A wallpaper with frosted-glass windows on top."""

    def __init__(self, w, h, seed, moon=None, sparkles=True, keep_out=()):
        self.w, self.h = w, h
        self.defs = [wallpaper(w, h, seed, moon, sparkles, keep_out), PASTEL]
        self.glass, self.shadows, self.items = [], [], []
        self.css = ""

    def window(self, x, y, w, h, rx=14, title=None):
        self.glass.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}"/>')
        self.shadows.append(f'<rect x="{x}" y="{y + 8}" width="{w}" height="{h}" rx="{rx}"/>')
        self.items.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{INK}" '
                          f'fill-opacity=".64" stroke="#fff" stroke-opacity=".10"/>')
        if title is not None:
            self.items.append("".join(f'<circle cx="{x + 22 + i * 20}" cy="{y + 20}" r="6" fill="{c}"/>'
                                      for i, c in enumerate((LOVE, GOLD, FOAM))))
            self.items.append(text(x + w / 2, y + 25, title, 12.5, MUTED, anchor="middle"))
            self.items.append(f'<rect x="{x}" y="{y + 39}" width="{w}" height="1" fill="#fff" opacity=".07"/>')

    def add(self, *parts):
        self.items.extend(parts)

    def render(self, label):
        w, h = self.w, self.h
        return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(label)}">
<style>{BASE_CSS}{self.css}</style>
<defs>{''.join(self.defs)}
<clipPath id="frame"><rect width="{w}" height="{h}" rx="18"/></clipPath>
<clipPath id="glass">{''.join(self.glass)}</clipPath>
<filter id="frost" x="0" y="0" width="100%" height="100%"><feGaussianBlur stdDeviation="14" edgeMode="duplicate"/></filter>
<filter id="shadow" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="10"/></filter>
</defs>
<g clip-path="url(#frame)">
  <use href="#wall"/>
  <g fill="#000" opacity=".5" filter="url(#shadow)">{''.join(self.shadows)}</g>
  <g clip-path="url(#glass)"><use href="#wall" filter="url(#frost)"/></g>
  {''.join(self.items)}
</g>
</svg>
"""


def pill(x, y, label, color, size=10.5, pad=8):
    w = len(label) * size * .6 + pad * 2
    return (f'<rect x="{x}" y="{y}" width="{w:.0f}" height="{size + 7}" rx="{(size + 7) / 2}" fill="{color}" opacity=".16"/>'
            + text(x + pad, y + size + 2, label, size, color)), w


# ---------------------------------------------------------------- hero

LOGO = [
    " █████╗  █████╗ ",
    "██╔══██╗██╔══██╗",
    "███████║███████║",
    "██╔══██║██╔══██║",
    "██║  ██║██║  ██║",
    "╚═╝  ╚═╝╚═╝  ╚═╝",
]


def hero():
    s = Scene(900, 600, seed=7, moon=(806, 282, 30))
    s.css = """
.bar { transform-box: fill-box; transform-origin: 50% 100%; animation: eq 1s ease-in-out infinite alternate; }
@keyframes eq { from { transform: scaleY(.28); } to { transform: scaleY(1); } }
"""
    s.defs.append(f'<linearGradient id="logo" gradientUnits="userSpaceOnUse" x1="36" y1="90" x2="262" y2="240">'
                  f'<stop offset="0" stop-color="{FOAM}"/><stop offset=".5" stop-color="{IRIS}"/>'
                  f'<stop offset="1" stop-color="{LOVE}"/></linearGradient>')
    s.defs.append(f'<linearGradient id="eq" gradientUnits="userSpaceOnUse" x1="0" y1="338" x2="0" y2="258">'
                  f'<stop offset="0" stop-color="{FOAM}"/><stop offset=".55" stop-color="{IRIS}"/>'
                  f'<stop offset="1" stop-color="{LOVE}"/></linearGradient>')

    # top bar
    s.window(12, 12, 876, 32, rx=10)
    s.add(text(28, 33, "AA", 14, "url(#pastel)", 800),
          f'<rect x="58" y="23" width="20" height="10" rx="5" fill="{IRIS}"/>',
          *(f'<circle cx="{90 + i * 16}" cy="28" r="4" fill="none" stroke="{SUBTLE}" stroke-width="1.4"/>' for i in range(3)),
          text(450, 32, "root@aa-linux: ~", 12, SUBTLE, anchor="middle"))
    x_end = 880
    for k, v, c in reversed((("kernel", "6.18.60", IRIS), ("ram", "512M", FOAM), ("cpu", "1 · hvf", GOLD), (None, "22:25", TEXT))):
        label = f"{k} {v}" if k else v
        pw = len(label) * 6.9 + 18
        x = x_end - pw
        parts = [(k + " ", MUTED), (v, c)] if k else [(v, c, "700")]
        s.add(f'<rect x="{x:.0f}" y="19" width="{pw:.0f}" height="18" rx="9" fill="#fff" opacity=".07"/>',
              spans(x + 9, 32, parts, 11.5))
        x_end = x - 6

    # fetch
    s.window(12, 52, 530, 300)
    for i, line in enumerate(LOGO):
        s.add(text(36, 112 + i * 25, line, 23, "url(#logo)"))
    s.add(text(146, 272, "LINUX", 13, SUBTLE, anchor="middle", extra=' letter-spacing="10"'),
          text(146, 292, "from scratch", 11, MUTED, anchor="middle", extra=' letter-spacing="3"'),
          text(36, 333, "~ #", 13, LOVE, 700),
          f'<rect class="cur" x="68" y="321" width="8" height="15" fill="{TEXT}"/>',
          spans(290, 90, [("root", LOVE), ("@", MUTED), ("aa-linux", IRIS)], 15, ' font-weight="700"'),
          text(290, 108, "─" * 28, 13, RULE))
    info = [("OS", "AA Linux 0.1 aarch64"), ("Kernel", "6.18.60 LTS"), ("Init", "BusyBox init"),
            ("Shell", "ash (BusyBox 1.38)"), ("Host", "QEMU virt · hvf"), ("Boot", "0.236s to /init"),
            ("Rootfs", "initramfs 1.1 MiB"), ("Packages", "0 (pkg mgr soon)"), ("Built on", "MacBook M2")]
    for i, (k, v) in enumerate(info):
        s.add(f'<text y="{132 + i * 21}" font-size="13"><tspan x="290" fill="{IRIS}" font-weight="700">{esc(k)}</tspan>'
              f'<tspan x="370" fill="{TEXT}">{esc(v)}</tspan></text>')
    for i, c in enumerate(("#26233a", LOVE, GOLD, ROSE, PINE, FOAM, IRIS, TEXT)):
        s.add(f'<rect x="{290 + i * 24}" y="316" width="18" height="18" rx="5" fill="{c}"/>')

    # boot time, like a big clock widget
    s.window(552, 52, 336, 150)
    s.add(text(572, 80, "POWER-ON → /INIT", 10.5, MUTED, extra=' letter-spacing="2.5"'),
          text(868, 80, "WED 04 NOV", 10.5, MUTED, anchor="end", extra=' letter-spacing="2.5"'),
          f'<text x="572" y="150" font-size="60" font-weight="800" fill="url(#pastel)">0.236'
          f'<tspan font-size="26" fill="{SUBTLE}" dx="6">s</tspan></text>',
          text(572, 182, "kernel 6.18.60 · 512M · 1 cpu", 11, MUTED))

    # visualizer
    s.window(552, 212, 336, 140)
    s.add(spans(572, 238, [("♪ ", LOVE), ("now playing: ", MUTED), ("make -j4 Image", TEXT)], 11))
    rnd = random.Random(3)
    for i in range(24):
        hh = 80 * (.35 + .65 * abs(math.sin(i * .55 + .4)) * rnd.uniform(.6, 1))
        s.add(f'<rect class="bar" style="animation-duration:{rnd.uniform(.55, 1.4):.2f}s;animation-delay:-{rnd.uniform(0, 1.4):.2f}s" '
              f'x="{572 + i * 12.3:.1f}" y="{338 - hh:.1f}" width="8" height="{hh:.1f}" rx="2" fill="url(#eq)"/>')

    # neovim with the file tree and a real file
    s.window(12, 362, 530, 226)
    s.add(f'<rect x="200" y="362" width="1" height="204" fill="#fff" opacity=".08"/>')
    tree = [("", "▾ aa-linux", IRIS), ("  ", "▸ assets", FOAM), ("  ", "▾ rootfs", FOAM),
            ("  │ ", "▾ etc", FOAM), ("  │   ", "▸ init.d", FOAM), ("  │   ", "  inittab", TEXT),
            ("  │   ", "  os-release", TEXT), ("  ", "▾ scripts", FOAM), ("  │ ", "  build.sh", GOLD),
            ("  │ ", "  build-macos.sh", GOLD), ("  │ ", "  run-qemu.sh", GOLD), ("  ", "  LICENSE", SUBTLE),
            ("  ", "  README.md", ROSE)]
    for i, (guide, name, c) in enumerate(tree):
        y = 388 + i * 14
        if name.strip() == "inittab":
            s.add(f'<rect x="18" y="{y - 10}" width="176" height="14" rx="3" fill="{IRIS}" opacity=".18"/>')
        s.add(spans(26, y, [(guide, RULE), (name, c, "700") if i == 0 else (name, c)], 11))
    s.add(f'<rect x="210" y="370" width="84" height="20" rx="5" fill="#fff" opacity=".07"/>',
          f'<rect x="210" y="388" width="84" height="2" fill="{IRIS}"/>',
          text(224, 384, "inittab", 11, TEXT), text(310, 384, "rcS", 11, MUTED), text(350, 384, "build.sh", 11, MUTED))
    code = [
        [("# BusyBox init reads this file at boot.", MUTED)],
        [("::", MUTED), ("sysinit", IRIS), (":", MUTED), ("/etc/init.d/rcS", FOAM)],
        [("::", MUTED), ("respawn", IRIS), (":", MUTED), ("/bin/cttyhack ", FOAM), ("/bin/sh", GOLD)],
        [("::", MUTED), ("ctrlaltdel", IRIS), (":", MUTED), ("/sbin/reboot", FOAM)],
        [("::", MUTED), ("shutdown", IRIS), (":", MUTED), ("/bin/umount", FOAM), (" -a -r", ROSE)],
    ]
    for i, parts in enumerate(code):
        y = 414 + i * 17
        if i == 2:
            s.add(f'<rect x="201" y="{y - 12}" width="341" height="16" fill="#fff" opacity=".05"/>',
                  f'<rect class="cur" x="248" y="{y - 11}" width="7" height="14" fill="{TEXT}" opacity=".9"/>')
        s.add(text(236, y, str(i + 1), 11, GOLD if i == 2 else MUTED, anchor="end"),
              spans(248, y, parts, 11.5, ' font-style="italic"' if i == 0 else ""))
    for i in range(5, 8):
        s.add(text(226, 414 + i * 17, "~", 11.5, PINE))
    # statusline
    s.add(f'<rect x="16" y="568" width="62" height="16" rx="4" fill="{IRIS}"/>',
          text(24, 580, "NORMAL", 10, INK, 800),
          f'<rect x="84" y="568" width="50" height="16" rx="4" fill="#fff" opacity=".08"/>',
          text(92, 580, "main", 10, SUBTLE),
          text(144, 580, "rootfs/etc/inittab", 10, TEXT),
          text(478, 580, "utf-8 · unix", 10, MUTED, anchor="end"),
          f'<rect x="486" y="568" width="46" height="16" rx="4" fill="{FOAM}"/>',
          text(509, 580, "3:1", 10, INK, 800, anchor="middle"))

    # roadmap as a todo list
    s.window(552, 362, 336, 226)
    s.add(text(868, 388, "2026-11-04", 10.5, MUTED, anchor="end"),
          text(574, 400, "roadmap", 24, LOVE, 800, cls="sans"),
          text(574, 424, "v0.1 → v1", 13, IRIS, 600, cls="sans"))
    todo = [("boot to a shell in qemu", True), ("our own package manager", False), ("boot on real hardware", False)]
    for i, (item, done) in enumerate(todo):
        y = 458 + i * 30
        if done:
            s.add(f'<rect x="574" y="{y - 12}" width="15" height="15" rx="4" fill="{GOLD}"/>',
                  f'<path d="M577.5,{y - 4.5} l3.5,3.5 l6,-7" fill="none" stroke="{INK}" stroke-width="2" stroke-linecap="round"/>',
                  text(600, y, item, 13, MUTED),
                  f'<rect x="600" y="{y - 5}" width="{len(item) * 7.8:.0f}" height="1.2" fill="{MUTED}"/>')
        else:
            s.add(f'<rect x="574.75" y="{y - 11.25}" width="13.5" height="13.5" rx="4" fill="none" stroke="{SUBTLE}" stroke-width="1.5"/>',
                  text(600, y, item, 13, TEXT))
    s.add(text(574, 556, "1 / 3 done", 10.5, MUTED),
          '<rect x="574" y="566" width="294" height="6" rx="3" fill="#fff" opacity=".08"/>',
          '<rect x="574" y="566" width="98" height="6" rx="3" fill="url(#pastel)"/>')

    return s.render("AA Linux desktop: system info (AA Linux 0.1, kernel 6.18.60 LTS, BusyBox init, aarch64), "
                    "0.236 s from power-on to /init, a file tree with rootfs/etc/inittab open, "
                    "and a roadmap: boot to a shell in QEMU (done), our own package manager, boot on real hardware")


# ---------------------------------------------------------------- first boot

def boot():
    cut = 100

    def k(ts, msg, color=SUBTLE):
        room = cut - len(ts) - 1
        if len(msg) > room:  # crop like a terminal without wrapping, at a word boundary
            msg = msg[:room].rsplit(" ", 1)[0]
        return [(ts + " ", MUTED), (msg, color)]

    lines = [
        k("[    0.000000]", "Linux version 6.18.60 (qwerty@lima-aa-builder) (gcc (Debian 14.2.0-19) 14.2.0, GNU ld (GNU Binutils for Debian) 2.44)"),
        k("[    0.000000]", "Machine model: linux,dummy-virt"),
        k("[    0.001891]", "smp: Brought up 1 node, 1 CPU"),
        k("[    0.004249]", "Memory: 435620K/524288K available (18368K kernel code, 5442K rwdata, 13220K rodata, 3264K init)"),
        k("[    0.008009]", "9000000.pl011: ttyAMA0 at MMIO 0x9000000 (irq = 13, base_baud = 0) is a PL011 rev1"),
        k("[    0.072327]", "clocksource: Switched to clocksource arch_sys_counter"),
        k("[    0.073204]", "Unpacking initramfs..."),
        [("               ⋮", MUTED)],
        k("[    0.235709]", "Freeing unused kernel memory: 3264K"),
        k("[    0.235865]", "Run /init as init process", FOAM),
        [],
        [("Welcome to AA Linux 0.1", "url(#pastel)", "800")],
        [],
        [("~ # ", LOVE, "700"), ("uname -sr", TEXT)],
        [("Linux 6.18.60", TEXT)],
        [("~ # ", LOVE, "700"), ("cat /etc/os-release", TEXT)],
        [("NAME=", IRIS), ('"AA Linux"', GOLD)],
        [("ID=", IRIS), ("aa-linux", GOLD)],
        [("VERSION_ID=", IRIS), ("0.1", GOLD)],
        [("PRETTY_NAME=", IRIS), ('"AA Linux 0.1"', GOLD)],
        [("~ # ", LOVE, "700"), ("ls /", TEXT)],
        [("bin", FOAM, "700"), ("      ", TEXT), ("etc", FOAM, "700"), ("      ", TEXT), ("linuxrc", ROSE), ("  ", TEXT),
         ("root", FOAM, "700"), ("     ", TEXT), ("sys", FOAM, "700"), ("      ", TEXT), ("usr", FOAM, "700")],
        [("dev", FOAM, "700"), ("      ", TEXT), ("init", ROSE), ("     ", TEXT), ("proc", FOAM, "700"), ("     ", TEXT),
         ("sbin", FOAM, "700"), ("     ", TEXT), ("tmp", FOAM, "700")],
        [("~ # ", LOVE, "700")],
    ]
    step, x0, y0 = 21, 48, 24 + 40 + 28
    h = y0 + (len(lines) - 1) * step + 24 + 24 + 4
    s = Scene(900, h, seed=11, moon=(842, 64, 22))
    s.css = """
.l { animation: in .01s linear backwards; }
@keyframes in { from, to { opacity: 0; } }
.l.cur { animation: in .01s linear backwards, bl 1.1s steps(1) infinite; }
"""
    s.window(24, 24, 852, h - 48, title="qemu-system-aarch64 -M virt -accel hvf — ttyAMA0")

    # Kernel lines appear quickly, then the shell session at typing pace.
    t = .3
    for i, parts in enumerate(lines):
        t += .8 if parts and parts[0][0].startswith("~ #") else .12
        if parts:
            s.add(spans(x0, y0 + i * step, parts, 13, f' class="l" style="animation-delay:{t:.2f}s"'))
    y = y0 + (len(lines) - 1) * step
    s.add(f'<rect class="l cur" style="animation-delay:{t:.2f}s, {t:.2f}s" x="{x0 + 32}" y="{y - 12}" width="8" height="16" fill="{TEXT}"/>')
    return s.render("First boot of AA Linux in QEMU: the kernel log ends with 'Run /init as init process', "
                    "then 'Welcome to AA Linux 0.1' and a shell runs uname -sr, cat /etc/os-release and ls /")


# ---------------------------------------------------------------- what's inside

def icon(kind):
    if kind == "chip":
        pins = "".join(f"M{t},2 V7 M{t},29 V34 M2,{t} H7 M29,{t} H34 " for t in (12, 18, 24))
        return f'<rect x="7" y="7" width="22" height="22" rx="3"/><rect x="13" y="13" width="10" height="10" rx="1.5"/><path d="{pins}"/>'
    if kind == "cube":
        return '<path d="M18,3 L32,10 L32,26 L18,33 L4,26 L4,10 Z M4,10 L18,17 L32,10 M18,17 L18,33"/>'
    if kind == "ram":
        pins = "".join(f"M{x},25 V30 " for x in range(6, 31, 4))
        return (f'<rect x="2" y="9" width="32" height="16" rx="2"/><rect x="6" y="13" width="6" height="8" rx="1"/>'
                f'<rect x="15" y="13" width="6" height="8" rx="1"/><rect x="24" y="13" width="6" height="8" rx="1"/><path d="{pins}"/>')
    return '<path d="M3,9 H14 L17,13 H33 V30 H3 Z M3,17 H33"/>'


def stack():
    s = Scene(900, 270, seed=21)
    s.defs.append(f'<linearGradient id="ic" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="36" y2="36">'
                  f'<stop offset="0" stop-color="{FOAM}"/><stop offset=".5" stop-color="{IRIS}"/>'
                  f'<stop offset="1" stop-color="{LOVE}"/></linearGradient>')
    cards = [
        ("chip", "linux", "6.18.60 LTS", IRIS, ["stock arm64 config,", "built without modules"]),
        ("cube", "busybox", "1.38 · static", LOVE, ["sh, init, mount, ls", "and ~300 more commands", "in one binary"]),
        ("ram", "initramfs", "1.1 MiB · cpio.gz", FOAM, ["the whole system is", "unpacked into RAM", "at boot"]),
        ("folder", "rootfs/", "our files", GOLD, ["inittab, rcS and", "os-release, copied", "into / as they are"]),
    ]
    for i, (kind, name, ver, c, desc) in enumerate(cards):
        x, y = 24 + i * 216, 24
        s.window(x, y, 202, 222)
        p, _ = pill(x + 22, y + 104, ver, c)
        s.add(f'<g transform="translate({x + 22},{y + 24})" fill="none" stroke="url(#ic)" stroke-width="2" '
              f'stroke-linejoin="round" stroke-linecap="round">{icon(kind)}</g>',
              text(x + 182, y + 36, f"0{i + 1}", 11, MUTED, anchor="end"),
              text(x + 22, y + 90, name, 17, TEXT, 800), p,
              *(text(x + 22, y + 150 + j * 17, d, 11.5, SUBTLE) for j, d in enumerate(desc)))
    return s.render("What's inside: Linux 6.18.60 LTS kernel with the stock arm64 config and no modules; "
                    "static BusyBox 1.38 with sh, init and ~300 commands; a 1.1 MiB initramfs; "
                    "rootfs/ with inittab, rcS and os-release")


# ---------------------------------------------------------------- boot chain

def chain():
    s = Scene(900, 200, seed=31, sparkles=False, keep_out=((132, 176),))  # captions sit on the wallpaper
    s.css = """
.flow { animation: flow .9s linear infinite; }
@keyframes flow { to { stroke-dashoffset: -16; } }
"""
    nodes = [("qemu", ["loads Image", "+ initramfs"], None, IRIS),
             ("kernel", ["unpacks the", "initramfs"], "0.000s", LOVE),
             ("/init", ["busybox init,", "pid 1"], "0.236s", FOAM),
             ("inittab", ["what to", "start"], None, GOLD),
             ("rcS", ["mounts /proc", "/sys /dev"], None, ROSE),
             ("sh", ["shell on", "the console"], None, IRIS)]
    for i, (name, cap, ts, c) in enumerate(nodes):
        cx = 95 + i * 142
        s.window(cx - 55, 72, 110, 46, rx=12)
        s.add(text(cx, 101, name, 15, TEXT, 800, anchor="middle"),
              f'<rect x="{cx - 14}" y="110" width="28" height="2.5" rx="1.25" fill="{c}"/>',
              *(text(cx, 146 + j * 16, line, 11, SUBTLE, anchor="middle") for j, line in enumerate(cap)))
        if ts:
            s.add(f'<rect x="{cx - 30}" y="42" width="60" height="18" rx="9" fill="{GOLD}" opacity=".16"/>',
                  text(cx, 55, ts, 10.5, GOLD, anchor="middle"))
        if i < len(nodes) - 1:
            x1, x2 = cx + 61, cx + 142 - 63
            s.add(f'<path class="flow" d="M{x1},95 H{x2 - 4}" stroke="{IRIS}" stroke-width="1.8" '
                  f'stroke-dasharray="4 4" stroke-linecap="round" opacity=".85"/>',
                  f'<path d="M{x2 - 5},90.5 L{x2 + 1},95 L{x2 - 5},99.5 Z" fill="{IRIS}"/>')
    return s.render("Boot chain: qemu loads the kernel and initramfs; the kernel (0.000 s) unpacks the initramfs; "
                    "/init is BusyBox init, pid 1 (0.236 s); init reads inittab; rcS mounts /proc, /sys and /dev; "
                    "a shell starts on the console")


# ---------------------------------------------------------------- crew

def crew():
    s = Scene(900, 260, seed=41, sparkles=False)
    s.defs.append(f'<linearGradient id="num" x1="0" y1="0" x2="1" y2="1">'
                  f'<stop offset="0" stop-color="{FOAM}"/><stop offset=".5" stop-color="{IRIS}"/>'
                  f'<stop offset="1" stop-color="{LOVE}"/></linearGradient>')
    people = [(24, "01", "АЛТАЙ", "АБДУРАХИМ", LOVE), (458, "02", "АТАЙ", "МАХМУДОВ", FOAM)]
    for x, num, first, last, c in people:
        y, w = 24, 418
        s.window(x, y, w, 212, rx=16)
        for j, sc in enumerate((LOVE, IRIS, FOAM)):
            x0 = x + 26 + j * 10
            s.add(f'<polygon points="{x0 + 12},{y + 34} {x0 + 18},{y + 34} {x0 + 6},{y + 178} {x0},{y + 178}" fill="{sc}" opacity=".9"/>')
        s.add(f'<text class="sans" x="{x + w - 22}" y="{y + 182}" font-size="150" font-weight="900" text-anchor="end" '
              f'fill="url(#num)" opacity=".2" letter-spacing="-4">{num}</text>',
              text(x + 74, y + 102, first, 46, TEXT, 800, cls="sans", extra=' letter-spacing="1"'),
              text(x + 76, y + 132, last, 15, SUBTLE, extra=' letter-spacing="6"'),
              f'<rect x="{x + 76}" y="{y + 152}" width="120" height="2" rx="1" fill="{c}"/>',
              text(x + 76, y + 178, "TEAM AA LINUX", 10.5, MUTED, extra=' letter-spacing="3"'))
    return s.render("Crew: 01 Алтай Абдурахим and 02 Атай Махмудов, team AA Linux")


# ---------------------------------------------------------------- footer and section headers

def footer():
    s = Scene(900, 120, seed=51, moon=(846, 30, 12))
    s.window(24, 34, 852, 52, rx=16)
    s.add(text(48, 66, "AA", 16, "url(#pastel)", 800), text(78, 66, "linux", 13, SUBTLE),
          f'<rect x="132" y="56" width="20" height="10" rx="5" fill="{IRIS}"/>',
          *(f'<circle cx="{164 + i * 16}" cy="61" r="4" fill="none" stroke="{SUBTLE}" stroke-width="1.4"/>' for i in range(3)),
          spans(450, 65, [("made by ", MUTED), ("алтай", LOVE, "700"), (" × ", MUTED), ("атай", FOAM, "700")], 12.5,
                ' text-anchor="middle"'),
          text(852, 65, "MIT · 2026", 11.5, MUTED, anchor="end"))
    return s.render("Made by Алтай and Атай, MIT license, 2026")


def header(name):
    pw = 38 + len(name) * 10.2 + 18
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="900" height="56" viewBox="0 0 900 56" role="img" aria-label="{esc(name)}">
<style>{BASE_CSS}</style>
<defs>{PASTEL}
<linearGradient id="ln" gradientUnits="userSpaceOnUse" x1="{pw + 14:.0f}" y1="0" x2="899" y2="0">
  <stop offset="0" stop-color="{IRIS}" stop-opacity=".8"/><stop offset=".6" stop-color="{LOVE}" stop-opacity=".25"/>
  <stop offset="1" stop-color="{LOVE}" stop-opacity="0"/>
</linearGradient>
<filter id="glow" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="3"/></filter>
</defs>
<rect x="1" y="8" width="{pw:.0f}" height="40" rx="12" fill="{PANEL}" stroke="#2a2540"/>
<circle class="tw" cx="22" cy="28" r="6" fill="{IRIS}" filter="url(#glow)"/>
<circle cx="22" cy="28" r="2.6" fill="#fff"/>
<text x="38" y="34" font-size="17" font-weight="800" fill="url(#pastel)">{esc(name)}</text>
<rect x="{pw + 14:.0f}" y="27.25" width="{899 - pw - 14:.0f}" height="1.5" fill="url(#ln)"/>
</svg>
"""


if __name__ == "__main__":
    files = {"hero.svg": hero(), "boot.svg": boot(), "stack.svg": stack(), "chain.svg": chain(),
             "crew.svg": crew(), "footer.svg": footer()}
    for section in ("about", "first-boot", "inside", "boot-chain", "build", "crew"):
        files[f"h-{section}.svg"] = header(f"~/{section}")
    for name, svg in files.items():
        (HERE / name).write_text(svg)
    print("wrote", " ".join(files))
