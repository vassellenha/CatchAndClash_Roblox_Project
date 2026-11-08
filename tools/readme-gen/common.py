import math, random, os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets", "readme")
os.makedirs(OUT, exist_ok=True)

SANS = "'Segoe UI','Inter','Helvetica Neue',Helvetica,Arial,sans-serif"
BLACK = "'Arial Black','Segoe UI Black','Helvetica Neue',Impact,sans-serif"
MONO = "'JetBrains Mono','Fira Code',Consolas,'DejaVu Sans Mono','Courier New',monospace"

RARITY = {
    "Common":    {"name": "COMMON",     "c": "#bebebe", "c2": "#7d8796"},
    "Rare":      {"name": "RARE",       "c": "#46a0ff", "c2": "#1b5fd1"},
    "UltraRare": {"name": "ULTRA RARE", "c": "#af50e6", "c2": "#6a1fb0"},
    "Legendary": {"name": "LEGENDARY",  "c": "#ffaa28", "c2": "#e0611a"},
    "Mythical":  {"name": "MYTHICAL",   "c": "#ff3c5a", "c2": "#a3155f"},
}
ORDER = ["Common", "Rare", "UltraRare", "Legendary", "Mythical"]

# mirrors src/ReplicatedStorage/Fishing/FishData.lua
FISH = [
    dict(id="lele",   name="Ikan Lele",      rarity="Common",    weight=230, value=5,   d=0.10, kind="catfish", col=("#4a4f45", "#9aa08a")),
    dict(id="mujair", name="Ikan Mujair",    rarity="Common",    weight=220, value=8,   d=0.12, kind="basic",   col=("#3d4a52", "#a9b7bd")),
    dict(id="nila",   name="Ikan Nila",      rarity="Common",    weight=210, value=10,  d=0.15, kind="stripe",  col=("#5b6670", "#d3d9dc")),
    dict(id="gurame", name="Ikan Gurame",    rarity="Rare",      weight=115, value=28,  d=0.30, kind="deep",    col=("#8a6a55", "#f0d2b4")),
    dict(id="kakap",  name="Ikan Kakap",     rarity="Rare",      weight=105, value=35,  d=0.35, kind="basic",   col=("#c2283a", "#ff9a8a")),
    dict(id="kerapu", name="Ikan Kerapu",    rarity="Rare",      weight=150, value=38,  d=0.40, kind="spots",   col=("#6b4a2e", "#d9a06a")),
    dict(id="tuna",   name="Ikan Tuna",      rarity="UltraRare", weight=48,  value=75,  d=0.50, kind="tuna",    col=("#14305e", "#c9d6e8")),
    dict(id="hiu",    name="Ikan Hiu-Hiuan", rarity="UltraRare", weight=42,  value=95,  d=0.55, kind="shark",   col=("#4b5d6e", "#e4ecf1")),
    dict(id="marlin", name="Ikan Marlin",    rarity="Legendary", weight=25,  value=250, d=0.72, kind="marlin",  col=("#0f3f8c", "#bfe3ff")),
    dict(id="naga",   name="Naga Laut",      rarity="Mythical",  weight=5,   value=750, d=0.92, kind="dragon",  col=("#ff3c5a", "#ffd166")),
]
TOTAL_W = sum(f["weight"] for f in FISH)
for f in FISH:
    f["pct"] = f["weight"] / TOTAL_W * 100
    f["zone"] = 24 - (24 - 14) * f["d"]
    f["speed"] = 18 * (1 + f["d"])


def save(name, svg):
    with open(os.path.join(OUT, name), "w") as fh:
        fh.write(svg)
    print("wrote", name, len(svg) // 1024, "KB")


def svg_open(w, h, extra=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'width="{w}" height="{h}" viewBox="0 0 {w} {h}" {extra}>')


def fmt(x):
    return f"{x:.2f}".rstrip("0").rstrip(".")


_uid = [0]
def uid(p="u"):
    _uid[0] += 1
    return f"{p}{_uid[0]}"


def fish_svg(kind, L, H, col, wag=True, wag_dur=0.45, glow=None):
    """Fish facing right centered at 0,0. Returns svg group content (string)."""
    top, belly = col
    g = uid("fg")
    out = [f'<defs><linearGradient id="{g}" x1="0" y1="0" x2="0" y2="1">'
           f'<stop offset="0" stop-color="{top}"/><stop offset="0.55" stop-color="{top}"/>'
           f'<stop offset="1" stop-color="{belly}"/></linearGradient></defs>']
    hl, hh = L / 2, H / 2
    if kind == "dragon":
        return dragon_svg(L, H, wag_dur)
    # body shape
    nose = hl
    if kind in ("tuna", "shark", "marlin"):
        body = (f"M{fmt(nose)},0 C{fmt(hl*0.6)},{fmt(-hh*1.0)} {fmt(-hl*0.4)},{fmt(-hh*0.95)} {fmt(-hl*0.78)},{fmt(-hh*0.12)} "
                f"L{fmt(-hl*0.78)},{fmt(hh*0.12)} C{fmt(-hl*0.4)},{fmt(hh*0.85)} {fmt(hl*0.6)},{fmt(hh*0.9)} {fmt(nose)},0Z")
    elif kind == "deep":
        body = (f"M{fmt(nose)},{fmt(hh*0.1)} C{fmt(hl*0.7)},{fmt(-hh*1.25)} {fmt(-hl*0.5)},{fmt(-hh*1.2)} {fmt(-hl*0.75)},{fmt(-hh*0.2)} "
                f"L{fmt(-hl*0.75)},{fmt(hh*0.2)} C{fmt(-hl*0.5)},{fmt(hh*1.2)} {fmt(hl*0.7)},{fmt(hh*1.15)} {fmt(nose)},{fmt(hh*0.1)}Z")
    elif kind == "catfish":
        body = (f"M{fmt(nose)},{fmt(hh*0.15)} C{fmt(hl*0.95)},{fmt(-hh*0.9)} {fmt(-hl*0.4)},{fmt(-hh*0.8)} {fmt(-hl*0.8)},{fmt(-hh*0.15)} "
                f"L{fmt(-hl*0.8)},{fmt(hh*0.15)} C{fmt(-hl*0.4)},{fmt(hh*0.8)} {fmt(hl*0.95)},{fmt(hh*0.95)} {fmt(nose)},{fmt(hh*0.15)}Z")
    else:
        body = (f"M{fmt(nose)},0 C{fmt(hl*0.7)},{fmt(-hh*1.15)} {fmt(-hl*0.45)},{fmt(-hh*1.05)} {fmt(-hl*0.75)},{fmt(-hh*0.15)} "
                f"L{fmt(-hl*0.75)},{fmt(hh*0.15)} C{fmt(-hl*0.45)},{fmt(hh*1.05)} {fmt(hl*0.7)},{fmt(hh*1.1)} {fmt(nose)},0Z")
    tx = -hl * 0.72
    if kind in ("tuna", "marlin", "shark"):
        tail = (f"M{fmt(tx)},0 L{fmt(tx-hl*0.38)},{fmt(-hh*1.25)} Q{fmt(tx-hl*0.22)},0 {fmt(tx-hl*0.38)},{fmt(hh*1.25)}Z")
    else:
        tail = (f"M{fmt(tx)},0 L{fmt(tx-hl*0.36)},{fmt(-hh*0.85)} Q{fmt(tx-hl*0.26)},0 {fmt(tx-hl*0.36)},{fmt(hh*0.85)}Z")
    wag_anim = (f'<animateTransform attributeName="transform" type="rotate" values="-14 {fmt(tx)} 0;14 {fmt(tx)} 0;-14 {fmt(tx)} 0" '
                f'dur="{wag_dur}s" repeatCount="indefinite"/>') if wag else ""
    out.append(f'<g><path d="{tail}" fill="{top}" opacity="0.95"/>{wag_anim}</g>')
    # dorsal fin
    if kind == "shark":
        out.append(f'<path d="M{fmt(hl*0.05)},{fmt(-hh*0.8)} L{fmt(-hl*0.12)},{fmt(-hh*2.1)} L{fmt(-hl*0.32)},{fmt(-hh*0.72)}Z" fill="{top}"/>')
        out.append(f'<path d="M{fmt(hl*0.1)},{fmt(hh*0.5)} L{fmt(-hl*0.05)},{fmt(hh*1.4)} L{fmt(-hl*0.2)},{fmt(hh*0.55)}Z" fill="{top}" opacity="0.9"/>')
    elif kind == "marlin":
        sail = (f"M{fmt(hl*0.42)},{fmt(-hh*0.7)} C{fmt(hl*0.3)},{fmt(-hh*2.9)} {fmt(-hl*0.15)},{fmt(-hh*2.6)} {fmt(-hl*0.45)},{fmt(-hh*0.6)}Z")
        out.append(f'<path d="{sail}" fill="#2d7dff" opacity="0.92"><animate attributeName="opacity" values="0.75;1;0.75" dur="1.6s" repeatCount="indefinite"/></path>')
        for i in range(5):
            x = hl * (0.32 - i * 0.16)
            out.append(f'<line x1="{fmt(x)}" y1="{fmt(-hh*0.7)}" x2="{fmt(x+hl*0.02)}" y2="{fmt(-hh*2.1+i*hh*0.18)}" stroke="#bfe3ff" stroke-width="1" opacity="0.45"/>')
    elif kind == "tuna":
        out.append(f'<path d="M{fmt(hl*0.12)},{fmt(-hh*0.8)} L{fmt(-hl*0.05)},{fmt(-hh*1.55)} L{fmt(-hl*0.2)},{fmt(-hh*0.75)}Z" fill="{top}"/>')
    else:
        out.append(f'<path d="M{fmt(hl*0.25)},{fmt(-hh*0.85)} Q{fmt(-hl*0.05)},{fmt(-hh*1.55)} {fmt(-hl*0.5)},{fmt(-hh*0.55)} L{fmt(-hl*0.3)},{fmt(-hh*0.6)}Z" fill="{top}" opacity="0.9"/>')
    out.append(f'<path d="{body}" fill="url(#{g})"/>')
    if kind == "marlin":
        out.append(f'<path d="M{fmt(nose-2)},{fmt(-hh*0.06)} L{fmt(nose+hl*0.7)},{fmt(-hh*0.02)} L{fmt(nose-2)},{fmt(hh*0.08)}Z" fill="{top}"/>')
        for i in range(4):
            x = -hl * (0.2 + i * 0.12)
            out.append(f'<path d="M{fmt(x)},{fmt(-hh*0.6)} Q{fmt(x+hl*0.04)},0 {fmt(x)},{fmt(hh*0.55)}" stroke="#9fd0ff" stroke-width="{fmt(max(1,H*0.04))}" fill="none" opacity="0.55"/>')
    if kind == "stripe":
        cp = uid("cp")
        out.append(f'<clipPath id="{cp}"><path d="{body}"/></clipPath><g clip-path="url(#{cp})" opacity="0.35">')
        for i in range(6):
            x = hl * 0.35 - i * hl * 0.2
            out.append(f'<rect x="{fmt(x)}" y="{fmt(-hh*1.2)}" width="{fmt(hl*0.07)}" height="{fmt(H*1.2)}" fill="#1d252c"/>')
        out.append('</g>')
    if kind == "spots":
        cp = uid("cp")
        rnd = random.Random(7)
        out.append(f'<clipPath id="{cp}"><path d="{body}"/></clipPath><g clip-path="url(#{cp})">')
        for i in range(22):
            out.append(f'<circle cx="{fmt(rnd.uniform(-hl*0.7, hl*0.6))}" cy="{fmt(rnd.uniform(-hh, hh*0.6))}" r="{fmt(rnd.uniform(H*0.03, H*0.07))}" fill="#3a2414" opacity="0.7"/>')
        out.append('</g>')
    if kind == "tuna":
        for i in range(5):
            x = -hl * (0.35 + i * 0.08)
            out.append(f'<path d="M{fmt(x)},{fmt(-hh*0.42+i*hh*0.05)} l{fmt(-hl*0.04)},{fmt(-hh*0.25)} l{fmt(-hl*0.02)},{fmt(hh*0.22)}Z" fill="#ffd23a"/>')
            out.append(f'<path d="M{fmt(x)},{fmt(hh*0.4-i*hh*0.05)} l{fmt(-hl*0.04)},{fmt(hh*0.25)} l{fmt(-hl*0.02)},{fmt(-hh*0.22)}Z" fill="#ffd23a"/>')
        out.append(f'<path d="M{fmt(hl*0.6)},{fmt(-hh*0.05)} C{fmt(hl*0.1)},{fmt(-hh*0.25)} {fmt(-hl*0.4)},{fmt(-hh*0.15)} {fmt(-hl*0.7)},0" stroke="#7fb6ff" stroke-width="{fmt(H*0.05)}" fill="none" opacity="0.6"/>')
    # pectoral fin
    out.append(f'<path d="M{fmt(hl*0.18)},{fmt(hh*0.25)} q{fmt(-hl*0.18)},{fmt(hh*0.25)} {fmt(-hl*0.3)},{fmt(hh*0.55)} q{fmt(hl*0.15)},{fmt(-hh*0.05)} {fmt(hl*0.3)},{fmt(-hh*0.55)}Z" fill="{top}" opacity="0.8">'
               f'<animateTransform attributeName="transform" type="rotate" values="0 {fmt(hl*0.18)} {fmt(hh*0.25)};-18 {fmt(hl*0.18)} {fmt(hh*0.25)};0 {fmt(hl*0.18)} {fmt(hh*0.25)}" dur="{wag_dur*1.6:.2f}s" repeatCount="indefinite"/></path>')
    # gill + highlight
    out.append(f'<path d="M{fmt(hl*0.42)},{fmt(-hh*0.55)} Q{fmt(hl*0.3)},0 {fmt(hl*0.42)},{fmt(hh*0.55)}" stroke="#000" stroke-opacity="0.25" stroke-width="{fmt(max(1,H*0.04))}" fill="none"/>')
    out.append(f'<ellipse cx="{fmt(hl*0.05)}" cy="{fmt(-hh*0.45)}" rx="{fmt(hl*0.45)}" ry="{fmt(hh*0.14)}" fill="#fff" opacity="0.18"/>')
    # eye
    ex = hl * (0.62 if kind != "catfish" else 0.7)
    out.append(f'<circle cx="{fmt(ex)}" cy="{fmt(-hh*0.18)}" r="{fmt(H*0.11)}" fill="#fff"/>'
               f'<circle cx="{fmt(ex+H*0.03)}" cy="{fmt(-hh*0.18)}" r="{fmt(H*0.065)}" fill="#0b0f14"/>'
               f'<circle cx="{fmt(ex+H*0.05)}" cy="{fmt(-hh*0.24)}" r="{fmt(H*0.025)}" fill="#fff"/>')
    if kind == "catfish":
        for sgn, dy in ((-1, 0.0), (1, 0.15), (1, 0.35)):
            out.append(f'<path d="M{fmt(nose-2)},{fmt(hh*dy)} q{fmt(hl*0.3)},{fmt(hh*0.3*sgn)} {fmt(hl*0.42)},{fmt(hh*(0.9 if sgn>0 else -0.4))}" stroke="{top}" stroke-width="{fmt(max(1,H*0.035))}" fill="none" stroke-linecap="round">'
                       f'<animateTransform attributeName="transform" type="rotate" values="0 {fmt(nose)} 0;{6*sgn} {fmt(nose)} 0;0 {fmt(nose)} 0" dur="1.3s" repeatCount="indefinite"/></path>')
    return "".join(out)


def dragon_svg(L, H, dur=0.45):
    """Serpentine sea dragon facing right, centered."""
    g = uid("dg")
    out = [f'<defs><linearGradient id="{g}" x1="0" y1="0" x2="1" y2="0">'
           f'<stop offset="0" stop-color="#7a1fd1"/><stop offset="0.45" stop-color="#ff3c5a"/>'
           f'<stop offset="1" stop-color="#ffb14a"/></linearGradient></defs>']
    hl = L / 2
    amp = H * 0.35

    def wave(phase):
        pts = []
        n = 24
        for i in range(n + 1):
            t = i / n
            x = -hl + t * L * 0.82
            y = math.sin(t * math.pi * 2.2 + phase) * amp * (0.4 + 0.6 * (1 - t))
            pts.append((x, y))
        d = f"M{fmt(pts[0][0])},{fmt(pts[0][1])}"
        for x, y in pts[1:]:
            d += f" L{fmt(x)},{fmt(y)}"
        return d, pts
    frames = [wave(p) for p in [0, math.pi / 2, math.pi, 3 * math.pi / 2, 2 * math.pi]]
    ds = ";".join(f[0] for f in frames)
    dur2 = 1.6
    out.append(f'<path d="{frames[0][0]}" stroke="url(#{g})" stroke-width="{fmt(H*0.34)}" fill="none" stroke-linecap="round" stroke-linejoin="round">'
               f'<animate attributeName="d" values="{ds}" dur="{dur2}s" repeatCount="indefinite"/></path>')
    # dorsal spikes line (dashed stroke offset above)
    out.append(f'<path d="{frames[0][0]}" stroke="#ffd166" stroke-width="{fmt(H*0.1)}" fill="none" stroke-dasharray="{fmt(H*0.06)} {fmt(H*0.1)}" transform="translate(0,{fmt(-H*0.17)})" opacity="0.9">'
               f'<animate attributeName="d" values="{ds}" dur="{dur2}s" repeatCount="indefinite"/></path>')
    out.append(f'<path d="{frames[0][0]}" stroke="#ffe7b0" stroke-width="{fmt(H*0.06)}" fill="none" stroke-dasharray="1 {fmt(H*0.12)}" stroke-linecap="round" opacity="0.6">'
               f'<animate attributeName="d" values="{ds}" dur="{dur2}s" repeatCount="indefinite"/></path>')
    hx, hy = frames[0][1][-1]
    hx += H * 0.05
    # head (static at end; body end y is ~sin(2.2pi)*small)
    out.append(f'<g transform="translate({fmt(hx)},{fmt(hy)})">'
               f'<animateTransform attributeName="transform" type="translate" values="' +
               ";".join(f"{fmt(f[1][-1][0]+H*0.05)},{fmt(f[1][-1][1])}" for f in frames) +
               f'" dur="{dur2}s" repeatCount="indefinite"/>'
               f'<path d="M{fmt(-H*0.2)},{fmt(-H*0.22)} L{fmt(H*0.45)},{fmt(-H*0.12)} L{fmt(H*0.62)},{fmt(H*0.02)} L{fmt(H*0.35)},{fmt(H*0.16)} L{fmt(-H*0.2)},{fmt(H*0.2)}Z" fill="#ff5a6e"/>'
               f'<path d="M{fmt(H*0.05)},{fmt(-H*0.18)} L{fmt(-H*0.25)},{fmt(-H*0.55)} L{fmt(-H*0.05)},{fmt(-H*0.2)}Z" fill="#ffd166"/>'
               f'<path d="M{fmt(H*0.18)},{fmt(-H*0.16)} L{fmt(H*0.0)},{fmt(-H*0.5)} L{fmt(H*0.25)},{fmt(-H*0.17)}Z" fill="#ffd166"/>'
               f'<path d="M{fmt(H*0.55)},{fmt(H*0.04)} q{fmt(H*0.3)},{fmt(H*0.1)} {fmt(H*0.5)},{fmt(H*0.45)}" stroke="#ffd166" stroke-width="{fmt(H*0.03)}" fill="none"/>'
               f'<path d="M{fmt(H*0.5)},{fmt(-H*0.08)} q{fmt(H*0.35)},{fmt(-H*0.05)} {fmt(H*0.6)},{fmt(-H*0.4)}" stroke="#ffd166" stroke-width="{fmt(H*0.03)}" fill="none"/>'
               f'<circle cx="{fmt(H*0.3)}" cy="{fmt(-H*0.05)}" r="{fmt(H*0.06)}" fill="#fff6c2"><animate attributeName="fill" values="#fff6c2;#ffffff;#ffd166;#fff6c2" dur="1.2s" repeatCount="indefinite"/></circle>'
               f'<circle cx="{fmt(H*0.32)}" cy="{fmt(-H*0.05)}" r="{fmt(H*0.025)}" fill="#3a0010"/>'
               f'</g>')
    return "".join(out)


def stars(rnd, n, w, h, ymax):
    s = []
    for _ in range(n):
        x, y = rnd.uniform(0, w), rnd.uniform(0, ymax)
        r = rnd.choice([0.6, 0.8, 1, 1.2, 1.6])
        d = rnd.uniform(1.5, 4.5)
        b = rnd.uniform(0, 4)
        s.append(f'<circle cx="{fmt(x)}" cy="{fmt(y)}" r="{r}" fill="#fff"><animate attributeName="opacity" values="0.2;1;0.2" dur="{d:.2f}s" begin="-{b:.2f}s" repeatCount="indefinite"/></circle>')
    return "".join(s)


def wave_path(width, y, amp, period, bottom):
    d = f"M0,{y}"
    x = 0
    while x <= width + period:
        d += f" q{period/4},{-amp} {period/2},0 t{period/2},0"
        x += period
    d += f" V{bottom} H0Z"
    return d


def bubbles(rnd, n, x0, x1, ybot, ytop, rmin=2, rmax=6, col="#bdf6ff"):
    out = []
    for _ in range(n):
        x = rnd.uniform(x0, x1)
        r = rnd.uniform(rmin, rmax)
        d = rnd.uniform(4, 10)
        b = rnd.uniform(0, 10)
        sway = rnd.uniform(4, 14)
        out.append(f'<g><animateTransform attributeName="transform" type="translate" values="0,0;{fmt(sway)},0;0,0;{fmt(-sway)},0;0,0" dur="{d/2:.2f}s" repeatCount="indefinite"/>'
                   f'<circle cx="{fmt(x)}" cy="{ybot}" r="{fmt(r)}" fill="none" stroke="{col}" stroke-width="1.2" opacity="0">'
                   f'<animate attributeName="cy" values="{ybot};{ytop}" dur="{d:.2f}s" begin="-{b:.2f}s" repeatCount="indefinite"/>'
                   f'<animate attributeName="opacity" values="0;0.8;0.8;0" keyTimes="0;0.1;0.85;1" dur="{d:.2f}s" begin="-{b:.2f}s" repeatCount="indefinite"/></circle>'
                   f'<circle cx="{fmt(x-r*0.3)}" cy="{ybot}" r="{fmt(r*0.25)}" fill="#fff" opacity="0">'
                   f'<animate attributeName="cy" values="{fmt(ybot-r*0.3)};{fmt(ytop-r*0.3)}" dur="{d:.2f}s" begin="-{b:.2f}s" repeatCount="indefinite"/>'
                   f'<animate attributeName="opacity" values="0;0.7;0.7;0" keyTimes="0;0.1;0.85;1" dur="{d:.2f}s" begin="-{b:.2f}s" repeatCount="indefinite"/></circle></g>')
    return "".join(out)


def seaweed(rnd, n, x0, x1, ybot, hmin, hmax):
    out = []
    cols = ["#0f5e4a", "#13785a", "#1a8f63", "#0c4a3f"]
    for _ in range(n):
        x = rnd.uniform(x0, x1)
        h = rnd.uniform(hmin, hmax)
        c = rnd.choice(cols)
        w = rnd.uniform(6, 12)
        d = f"M{fmt(x)},{ybot} C{fmt(x-w*2)},{fmt(ybot-h*0.33)} {fmt(x+w*2)},{fmt(ybot-h*0.66)} {fmt(x)},{fmt(ybot-h)} C{fmt(x+w*2.4)},{fmt(ybot-h*0.66)} {fmt(x-w*1.2)},{fmt(ybot-h*0.33)} {fmt(x+w)},{ybot}Z"
        dur = rnd.uniform(3, 6)
        a = rnd.uniform(4, 9)
        out.append(f'<path d="{d}" fill="{c}" opacity="0.9"><animateTransform attributeName="transform" type="rotate" values="{-a} {fmt(x)} {ybot};{a} {fmt(x)} {ybot};{-a} {fmt(x)} {ybot}" dur="{dur:.2f}s" repeatCount="indefinite"/></path>')
    return "".join(out)
