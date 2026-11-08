from common import *

EMOJI = "'Segoe UI Emoji','Apple Color Emoji','Noto Color Emoji',sans-serif"

# ---------------------------------------------------------------- headers
HEADERS = [
    ("01", "about", "TENTANG GAME", "apa sih Catch &amp; Clash itu?", "🎣", "#38e8ff", "#5dffb0"),
    ("02", "loop", "CARA MAIN", "lempar → tunggu → strike → tarik → cuan", "🕹️", "#5dffb0", "#ffd166"),
    ("03", "reel", "MINIGAME REEL", "simulasi asli dari Config.lua, frame per frame", "⚡", "#ffd166", "#ff8a3d"),
    ("04", "codex", "FISH CODEX", "10 penghuni kolam, dari Lele sampai Naga", "📖", "#46a0ff", "#af50e6"),
    ("05", "drop", "DROP RATE", "matematika di balik keberuntunganmu", "🎲", "#af50e6", "#ff3c5a"),
    ("06", "map", "PETA KOLAM", "BuildPondTerrain.lua dilihat dari atas &amp; samping", "🗺️", "#5dffb0", "#38e8ff"),
    ("07", "arch", "ARSITEKTUR", "server-authoritative, client cuma pegang tombol", "🛡️", "#38e8ff", "#46a0ff"),
    ("08", "tree", "STRUKTUR PROJECT", "peta folder ala Rojo", "🗂️", "#ffd166", "#5dffb0"),
    ("09", "install", "INSTALASI", "dari clone sampai mancing dalam 5 langkah", "🚀", "#ff8a3d", "#ff3c5a"),
    ("10", "config", "KONFIGURASI", "semua kenop yang bisa kamu putar", "🎛️", "#46a0ff", "#38e8ff"),
    ("11", "model", "MODEL 3D", "joran prosedural dari RodTool.lua", "🧊", "#af50e6", "#46a0ff"),
    ("12", "faq", "FAQ &amp; TROUBLESHOOT", "kalau ada yang nyangkut di kail", "🧰", "#ff3c5a", "#ffd166"),
]


def header(num, slug, title, sub, emo, c1, c2):
    W, H = 1200, 130
    rnd = random.Random(sum(map(ord, slug)))
    p = [svg_open(W, H)]
    p.append(f'''<defs>
<linearGradient id="hg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient>
<linearGradient id="shine" x1="0" y1="0" x2="1" y2="0">
 <stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="0.5" stop-color="#fff" stop-opacity="0.85"/><stop offset="1" stop-color="#fff" stop-opacity="0"/>
</linearGradient>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#071226"/><stop offset="1" stop-color="#0b1f3d"/></linearGradient>
<clipPath id="tclip"><text x="170" y="74" font-family="{BLACK}" font-size="52" font-weight="900" letter-spacing="3">{title}</text></clipPath>
<clipPath id="card"><rect x="2" y="2" width="{W-4}" height="{H-4}" rx="22"/></clipPath>
<filter id="gl" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>''')
    p.append(f'<rect x="2" y="2" width="{W-4}" height="{H-4}" rx="22" fill="url(#bg)"/>')
    p.append('<g clip-path="url(#card)">')
    # grid + glow blobs
    for x in range(0, W, 40):
        p.append(f'<line x1="{x}" y1="0" x2="{x}" y2="{H}" stroke="{c1}" stroke-opacity="0.05"/>')
    for y in range(0, H, 40):
        p.append(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}" stroke="{c1}" stroke-opacity="0.05"/>')
    p.append(f'<circle cx="1050" cy="20" r="140" fill="{c2}" opacity="0.12"><animate attributeName="cx" values="1050;900;1050" dur="9s" repeatCount="indefinite"/></circle>')
    p.append(f'<circle cx="200" cy="140" r="120" fill="{c1}" opacity="0.10"><animate attributeName="cx" values="200;380;200" dur="11s" repeatCount="indefinite"/></circle>')
    # big outline number
    p.append(f'<text x="{W-30}" y="118" text-anchor="end" font-family="{BLACK}" font-size="130" font-weight="900" fill="none" stroke="{c1}" stroke-opacity="0.18" stroke-width="2">{num}</text>')
    # wave bottom
    p.append(f'<g opacity="0.5"><path d="{wave_path(W+240, H-12, 4, 120, H)}" fill="{c1}" fill-opacity="0.25"><animateTransform attributeName="transform" type="translate" values="0,0;-120,0" dur="4s" repeatCount="indefinite"/></path></g>')
    # small fish crossing
    f = rnd.choice(FISH[:8])
    p.append(f'<g opacity="0.7"><animateMotion path="M-80,{H-26} C300,{H-40} 700,{H-12} {W+80},{H-28}" dur="{rnd.uniform(9,14):.1f}s" repeatCount="indefinite" rotate="auto"/>{fish_svg(f["kind"], 44, 18, f["col"], wag_dur=0.3)}</g>')
    p.append(bubbles(rnd, 10, 120, W - 200, H - 10, 10, 1.5, 3.5, c1))
    p.append('</g>')
    # border with running light
    p.append(f'<rect x="2" y="2" width="{W-4}" height="{H-4}" rx="22" fill="none" stroke="url(#hg)" stroke-opacity="0.35" stroke-width="2"/>')
    per = 2 * (W - 4 + H - 4)
    p.append(f'<rect x="2" y="2" width="{W-4}" height="{H-4}" rx="22" fill="none" stroke="url(#hg)" stroke-width="3" stroke-dasharray="220 {per-220}" filter="url(#gl)">'
             f'<animate attributeName="stroke-dashoffset" values="0;{-per}" dur="6s" repeatCount="indefinite"/></rect>')
    # icon badge
    p.append(f'<g><animateTransform attributeName="transform" type="translate" values="0,0;0,-5;0,0" dur="3s" repeatCount="indefinite"/>'
             f'<circle cx="92" cy="62" r="44" fill="url(#hg)" opacity="0.18"/>'
             f'<circle cx="92" cy="62" r="44" fill="none" stroke="url(#hg)" stroke-width="3" stroke-dasharray="8 6">'
             f'<animateTransform attributeName="transform" type="rotate" values="0 92 62;360 92 62" dur="14s" repeatCount="indefinite"/></circle>'
             f'<text x="92" y="78" text-anchor="middle" font-family="{EMOJI}" font-size="44">{emo}</text></g>')
    # title
    p.append(f'<text x="170" y="74" font-family="{BLACK}" font-size="52" font-weight="900" letter-spacing="3" fill="url(#hg)" filter="url(#gl)">{title}</text>')
    p.append(f'<g clip-path="url(#tclip)"><rect x="-300" y="0" width="240" height="{H}" fill="url(#shine)" transform="skewX(-20)">'
             f'<animate attributeName="x" values="-300;-300;1200" keyTimes="0;0.55;1" dur="5s" repeatCount="indefinite"/></rect></g>')
    p.append(f'<text x="174" y="104" font-family="{MONO}" font-size="17" fill="#9fc6e6"><tspan fill="{c1}">{num} ▸</tspan> {sub}</text>')
    p.append('</svg>')
    save(f"h-{num}-{slug}.svg", "".join(p))


for h in HEADERS:
    header(*h)

# ---------------------------------------------------------------- divider
W, H = 1200, 46
rnd = random.Random(5)
p = [svg_open(W, H), '<defs><linearGradient id="dg" x1="0" x2="1"><stop offset="0" stop-color="#38e8ff" stop-opacity="0"/><stop offset="0.2" stop-color="#38e8ff"/><stop offset="0.5" stop-color="#ffd166"/><stop offset="0.8" stop-color="#ff3c5a"/><stop offset="1" stop-color="#ff3c5a" stop-opacity="0"/></linearGradient></defs>']
d = f"M0,23 " + " ".join(f"q30,-10 60,0 t60,0" for _ in range(12))
p.append(f'<g><path d="{d}" fill="none" stroke="url(#dg)" stroke-width="2.5" stroke-linecap="round"><animateTransform attributeName="transform" type="translate" values="0,0;-120,0" dur="3s" repeatCount="indefinite"/></path></g>')
for i in range(3):
    f = FISH[[2, 6, 8][i]]
    p.append(f'<g><animateMotion path="M-60,23 C300,8 900,38 {W+60},23" dur="{8+i*3}s" begin="-{i*3}s" repeatCount="indefinite" rotate="auto"/>{fish_svg(f["kind"], 34, 14, f["col"], wag_dur=0.25)}</g>')
p.append('</svg>')
save("divider.svg", "".join(p))

# ---------------------------------------------------------------- terminal typing
W, H = 1000, 330
FS = 19
CW = FS * 0.6
LINES = [
    [("#5dffb0", "player@kolam"), ("#9fc6e6", ":~$ "), ("#e9fdff", "rojo serve default.project.json")],
    [("#38e8ff", "▸ "), ("#e9fdff", "[Lempar Pancing] "), ("#9fc6e6", "Melempar kail...")],
    [("#38e8ff", "▸ "), ("#9fc6e6", "menunggu gigitan "), ("#ffd166", "(2.0 - 8.0 detik)"), ("#9fc6e6", " ...")],
    [("#ff3c5a", "!! STRIKE !! "), ("#e9fdff", "Tahan klik buat narik!")],
    [("#38e8ff", "▸ "), ("#5dffb0", "[██████████████░░░░] "), ("#ffd166", "78%"), ("#9fc6e6", "  zona=16.8  speed=31.0")],
    [("#ffaa28", "★ LEGENDARY ★ "), ("#e9fdff", "Ikan Marlin "), ("#5dffb0", "+250 uang"), ("#9fc6e6", "  (peluang 2.17%)")],
]
CYCLE = 16.0
p = [svg_open(W, H)]
p.append(f'''<defs><linearGradient id="tb" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0a1426"/><stop offset="1" stop-color="#050a14"/></linearGradient>
<filter id="tg"><feGaussianBlur stdDeviation="1.4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="2" fill="#fff" opacity="0.025"/></pattern></defs>''')
p.append(f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="16" fill="url(#tb)" stroke="#1d3557" stroke-width="2"/>')
p.append(f'<rect x="1" y="1" width="{W-2}" height="40" rx="16" fill="#0f1e38"/><rect x="1" y="26" width="{W-2}" height="15" fill="#0f1e38"/>')
for i, c in enumerate(["#ff5f57", "#febc2e", "#28c840"]):
    p.append(f'<circle cx="{26+i*22}" cy="21" r="7" fill="{c}"/>')
p.append(f'<text x="{W/2}" y="26" text-anchor="middle" font-family="{MONO}" font-size="14" fill="#6f8db3">catch-and-clash — fishing.log — 120×24</text>')
y0 = 82
t = 0.4
for li, segs in enumerate(LINES):
    text = "".join(s for _, s in segs)
    n = len(text)
    speed = 0.035 if li else 0.06
    start = t
    end = start + n * speed
    t = end + (1.1 if li in (2, 3) else 0.55)
    y = y0 + li * 38
    cid = f"lc{li}"
    # keyframes for width (discrete)
    kts, vals = ["0"], ["0"]
    steps = min(n, 40)
    for k in range(steps + 1):
        tt = start + (end - start) * k / steps
        kts.append(f"{tt/CYCLE:.4f}")
        vals.append(f"{fmt(n*CW*k/steps)}")
    kts += [f"{(CYCLE-0.6)/CYCLE:.4f}", "1"]
    vals += [fmt(n * CW), "0"]
    p.append(f'<clipPath id="{cid}"><rect x="40" y="{y-22}" width="0" height="32">'
             f'<animate attributeName="width" values="{";".join(vals)}" keyTimes="{";".join(kts)}" calcMode="discrete" dur="{CYCLE}s" repeatCount="indefinite"/></rect></clipPath>')
    tsp = "".join(f'<tspan fill="{c}">{s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")}</tspan>' for c, s in segs)
    p.append(f'<text x="40" y="{y}" font-family="{MONO}" font-size="{FS}" textLength="{fmt(n*CW)}" lengthAdjust="spacingAndGlyphs" clip-path="url(#{cid})" filter="url(#tg)" xml:space="preserve">{tsp}</text>')
    # cursor for this line: visible only while typing / until next line
    nxt = t
    p.append(f'<rect x="40" y="{y-17}" width="{CW:.1f}" height="22" fill="#5dffb0" opacity="0">'
             f'<animate attributeName="x" values="{";".join(str(40+float(v)) for v in vals)}" keyTimes="{";".join(kts)}" calcMode="discrete" dur="{CYCLE}s" repeatCount="indefinite"/>'
             f'<animate attributeName="opacity" values="0;0.9;0" keyTimes="0;{start/CYCLE:.4f};{min(nxt, CYCLE-0.7)/CYCLE:.4f}" calcMode="discrete" dur="{CYCLE}s" repeatCount="indefinite"/></rect>')
    if li == 3:
        p.append(f'<rect x="20" y="{y-26}" width="{W-40}" height="36" rx="6" fill="#ff3c5a" opacity="0">'
                 f'<animate attributeName="opacity" values="0;0;0.25;0;0.2;0" keyTimes="0;{start/CYCLE:.4f};{(start+0.1)/CYCLE:.4f};{(start+0.3)/CYCLE:.4f};{(start+0.4)/CYCLE:.4f};{(start+0.7)/CYCLE:.4f}" dur="{CYCLE}s" repeatCount="indefinite"/></rect>')
p.append(f'<rect x="1" y="41" width="{W-2}" height="{H-42}" fill="url(#scan)"/>')
p.append('</svg>')
save("terminal.svg", "".join(p))

# ---------------------------------------------------------------- odometer stats
W, H = 1200, 190
STATS = [("10", "JENIS IKAN", "#38e8ff"), ("5", "TIER RARITY", "#af50e6"), ("20", "TICK / DETIK", "#5dffb0"),
         ("1386", "BARIS LUAU", "#ffd166"), ("0.43", "% NAGA LAUT", "#ff3c5a")]
DH = 64
p = [svg_open(W, H)]
p.append(f'<defs><filter id="og"><feGaussianBlur stdDeviation="4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
         f'<linearGradient id="fade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#071226"/><stop offset="0.25" stop-color="#071226" stop-opacity="0"/><stop offset="0.75" stop-color="#071226" stop-opacity="0"/><stop offset="1" stop-color="#071226"/></linearGradient></defs>')
tw = W / len(STATS)
for i, (num, label, col) in enumerate(STATS):
    x0 = i * tw + 10
    p.append(f'<rect x="{x0}" y="10" width="{tw-20}" height="{H-20}" rx="20" fill="#071226" stroke="{col}" stroke-opacity="0.45" stroke-width="2"/>')
    p.append(f'<rect x="{x0}" y="10" width="{tw-20}" height="{H-20}" rx="20" fill="{col}" opacity="0.06"><animate attributeName="opacity" values="0.04;0.14;0.04" dur="3s" begin="{i*0.4}s" repeatCount="indefinite"/></rect>')
    cw = 40
    total = sum(cw if ch.isdigit() else 18 for ch in num)
    cx = x0 + (tw - 20) / 2 - total / 2
    ytop = 32
    cid = f"oc{i}"
    p.append(f'<clipPath id="{cid}"><rect x="{x0}" y="{ytop}" width="{tw-20}" height="{DH+8}"/></clipPath><g clip-path="url(#{cid})" filter="url(#og)">')
    di = 0
    for ch in num:
        if ch.isdigit():
            tgt = int(ch) + 10
            strip = "".join(f'<text x="{fmt(cx+cw/2)}" y="{fmt(ytop+DH-6+k*DH)}" text-anchor="middle" font-family="{BLACK}" font-size="62" font-weight="900" fill="{col}">{k%10}</text>' for k in range(21))
            delay = 0.2 + di * 0.25 + i * 0.15
            dur = 2.2 + di * 0.4
            T = 10.0
            k1, k2 = delay / T, (delay + dur) / T
            p.append(f'<g>{strip}<animateTransform attributeName="transform" type="translate" values="0,0;0,0;0,{-tgt*DH};0,{-tgt*DH};0,0" '
                     f'keyTimes="0;{k1:.3f};{k2:.3f};0.97;1" calcMode="spline" keySplines="0 0 1 1;0.15 0.8 0.2 1;0 0 1 1;0 0 1 1" dur="{T}s" repeatCount="indefinite"/></g>')
            cx += cw
            di += 1
        else:
            p.append(f'<text x="{fmt(cx+9)}" y="{ytop+DH-6}" text-anchor="middle" font-family="{BLACK}" font-size="62" fill="{col}">{ch}</text>')
            cx += 18
    p.append('</g>')
    p.append(f'<text x="{x0+(tw-20)/2}" y="{H-36}" text-anchor="middle" font-family="{SANS}" font-size="15" font-weight="800" letter-spacing="3" fill="#cfe8ff">{label}</text>')
    p.append(f'<rect x="{x0+(tw-20)/2-30}" y="{H-28}" width="60" height="3" rx="1.5" fill="{col}"><animate attributeName="width" values="10;60;10" dur="3s" repeatCount="indefinite"/>'
             f'<animate attributeName="x" values="{x0+(tw-20)/2-5};{x0+(tw-20)/2-30};{x0+(tw-20)/2-5}" dur="3s" repeatCount="indefinite"/></rect>')
p.append('</svg>')
save("stats.svg", "".join(p))
