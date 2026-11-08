from common import *

EMOJI = "'Segoe UI Emoji','Apple Color Emoji','Noto Color Emoji',sans-serif"

# ======================================================== REEL SIMULATION
# exact port of runReelMinigame() in FishingService.server.lua
CFG = dict(TickRate=1 / 20, BarMax=100, BarStart=50, FillRate=28, DrainRate=18, IndicatorRise=55,
           IndicatorFall=40, ZoneMinSize=14, ZoneMaxSize=24, ZoneSpeed=18, ReelTimeLimit=20)


def simulate(fish, seed, delay=6, noise=8, panic=0.03):
    rnd = random.Random(seed)
    d = fish["d"]
    zs = CFG["ZoneMaxSize"] - (CFG["ZoneMaxSize"] - CFG["ZoneMinSize"]) * d
    sp = CFG["ZoneSpeed"] * (1 + d)
    prog = ind = zc = CFG["BarStart"]
    zv = 0
    el = 0
    hist = []
    holding = False
    seen = [zc] * (delay + 1)
    lock = 0
    while True:
        dt = CFG["TickRate"]
        el += dt
        # a (deliberately imperfect) human: delayed perception, noisy aim, occasional panic
        if lock > 0:
            lock -= 1
        elif rnd.random() < panic:
            lock = rnd.randint(8, 22)
            holding = rnd.random() < 0.5
        else:
            holding = ind < seen[0] + rnd.uniform(-noise, noise)
        zv += (rnd.random() * 2 - 1) * sp * dt
        zv = max(-sp, min(sp, zv))
        zc = max(zs / 2, min(100 - zs / 2, zc + zv * dt))
        ind += CFG["IndicatorRise"] * dt if holding else -CFG["IndicatorFall"] * dt
        ind = max(0, min(100, ind))
        inside = zc - zs / 2 <= ind <= zc + zs / 2
        prog += CFG["FillRate"] * dt if inside else -CFG["DrainRate"] * dt
        prog = max(0, min(100, prog))
        seen = seen[1:] + [zc]
        hist.append(dict(t=el, p=prog, i=ind, z=zc, zs=zs, h=holding))
        if prog >= 100:
            return True, hist
        if prog <= 0 or el >= CFG["ReelTimeLimit"]:
            return False, hist


MARLIN = FISH[8]
best = None
for seed in range(20000):
    ok, h = simulate(MARLIN, seed)
    if not ok:
        continue
    dur = h[-1]["t"]
    lowest = min(x["p"] for x in h[20:]) if len(h) > 20 else 100
    if 8 <= dur <= 11 and lowest < 30 and max(x["p"] for x in h[:len(h)//2]) > 70:
        best = (seed, h)
        break
seed, HIST = best
TS = HIST[-1]["t"]
print("reel sim seed", seed, "duration", TS, "ticks", len(HIST))
POP = 3.6
C = TS + POP + 0.6          # whole cycle
START = 0.6                  # small lead-in

W, H = 1200, 600
p = [svg_open(W, H)]
p.append(f'''<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#060f22"/><stop offset="1" stop-color="#0b1730"/></linearGradient>
<linearGradient id="pf" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#2fae55"/><stop offset="1" stop-color="#6dff8f"/></linearGradient>
<filter id="gl" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<filter id="gl2" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="10" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40,0 H0 V40" fill="none" stroke="#38e8ff" stroke-opacity="0.06"/></pattern>
<linearGradient id="leg" x1="0" x2="1"><stop offset="0" stop-color="#ffaa28"/><stop offset="1" stop-color="#ffe08a"/></linearGradient>
</defs>''')
p.append(f'<rect x="2" y="2" width="{W-4}" height="{H-4}" rx="24" fill="url(#bg)" stroke="#1d3557" stroke-width="2"/>')
p.append(f'<rect x="2" y="2" width="{W-4}" height="{H-4}" rx="24" fill="url(#grid)"/>')


def kt_vals(series, fn, hold_end=None):
    """Build keyTimes/values for a cycle of length C with series sampled over [START, START+TS]."""
    kts, vals = [0.0], [fn(series[0], True)]
    for k, s in enumerate(series):
        kts.append((START + s["t"]) / C)
        vals.append(fn(s, False))
    kts.append(1.0)
    vals.append(hold_end if hold_end is not None else vals[-1])
    return ";".join(f"{k:.4f}" for k in kts), ";".join(str(v) for v in vals)


# ---- game UI replica (left)
RX, RY, RW, RH = 150, 120, 84, 400
p.append(f'<text x="{RX+RW/2}" y="{RY-40}" text-anchor="middle" font-family="{SANS}" font-size="18" font-weight="800" fill="#fff" stroke="#000" stroke-opacity="0.5" stroke-width="3" paint-order="stroke">Tahan klik buat narik!</text>')
p.append(f'<rect x="{RX-8}" y="{RY-8}" width="{RW+16}" height="{RH+16}" rx="14" fill="#141414" fill-opacity="0.85" stroke="#2a3b55" stroke-width="2"/>')
p.append(f'<rect x="{RX}" y="{RY}" width="{RW}" height="{RH}" rx="4" fill="#3c3c3c"/>')
# progress fill (from bottom)
k, v = kt_vals(HIST, lambda s, f0: fmt(RH * (50 if f0 else s["p"]) / 100), fmt(RH * 0.5))
k2, v2 = kt_vals(HIST, lambda s, f0: fmt(RY + RH - RH * (50 if f0 else s["p"]) / 100), fmt(RY + RH * 0.5))
p.append(f'<rect x="{RX}" width="{RW}" fill="url(#pf)" y="{RY+RH/2}" height="{RH/2}">'
         f'<animate attributeName="height" keyTimes="{k}" values="{v}" dur="{C:.2f}s" repeatCount="indefinite"/>'
         f'<animate attributeName="y" keyTimes="{k2}" values="{v2}" dur="{C:.2f}s" repeatCount="indefinite"/></rect>')
# zone
zs = HIST[0]["zs"]
k, v = kt_vals(HIST, lambda s, f0: fmt(RY + RH * (1 - ((50 if f0 else s["z"]) + zs / 2) / 100)), fmt(RY + RH * (1 - (50 + zs / 2) / 100)))
p.append(f'<rect x="{RX-14}" width="{RW+28}" height="{fmt(RH*zs/100)}" rx="5" fill="#e6c83c" fill-opacity="0.72" stroke="#fff3a6" stroke-width="2" y="0">'
         f'<animate attributeName="y" keyTimes="{k}" values="{v}" dur="{C:.2f}s" repeatCount="indefinite"/></rect>')
# indicator
k, v = kt_vals(HIST, lambda s, f0: fmt(RY + RH * (1 - (50 if f0 else s["i"]) / 100) - 4), fmt(RY + RH * 0.5 - 4))
p.append(f'<rect x="{RX-22}" width="{RW+44}" height="8" rx="4" fill="#fff" filter="url(#gl)" y="0">'
         f'<animate attributeName="y" keyTimes="{k}" values="{v}" dur="{C:.2f}s" repeatCount="indefinite"/></rect>')
# scale ticks
for q in range(0, 101, 25):
    y = RY + RH * (1 - q / 100)
    p.append(f'<line x1="{RX+RW+14}" y1="{y}" x2="{RX+RW+24}" y2="{y}" stroke="#6f8db3"/><text x="{RX+RW+30}" y="{y+4}" font-family="{MONO}" font-size="11" fill="#6f8db3">{q}</text>')
p.append(f'<text x="{RX+RW/2}" y="{RY+RH+44}" text-anchor="middle" font-family="{MONO}" font-size="12" fill="#6f8db3">ReelFrame · 1:1 replika UI</text>')
# legend
for i, (c, lab) in enumerate([("#6dff8f", "progress"), ("#e6c83c", "zona ikan"), ("#ffffff", "indikator")]):
    p.append(f'<rect x="{40}" y="{RY+60+i*26}" width="14" height="14" rx="3" fill="{c}"/><text x="{60}" y="{RY+72+i*26}" font-family="{SANS}" font-size="13" fill="#cfe1f5">{lab}</text>')

# ---- telemetry chart (right)
GX, GY, GW, GH = 400, 120, 740, 300
p.append(f'<text x="{GX}" y="{GY-48}" font-family="{BLACK}" font-weight="900" font-size="22" fill="#e9fdff">TELEMETRI SERVER</text>'
         f'<text x="{GX}" y="{GY-24}" font-family="{MONO}" font-size="13" fill="#6f8db3">ReelUpdate @ 20Hz · ikan: Ikan Marlin (d=0.72) · zona {zs:.1f} · seed {seed}</text>')
p.append(f'<rect x="{GX}" y="{GY}" width="{GW}" height="{GH}" rx="10" fill="#050b18" stroke="#1d3557"/>')
for q in (25, 50, 75):
    y = GY + GH * (1 - q / 100)
    p.append(f'<line x1="{GX}" y1="{y}" x2="{GX+GW}" y2="{y}" stroke="#1d3557" stroke-dasharray="4 6"/>')
for s in range(0, int(TS) + 1):
    x = GX + GW * s / TS
    p.append(f'<line x1="{x}" y1="{GY+GH}" x2="{x}" y2="{GY+GH+6}" stroke="#6f8db3"/><text x="{x}" y="{GY+GH+20}" text-anchor="middle" font-family="{MONO}" font-size="11" fill="#6f8db3">{s}s</text>')
X = lambda t: GX + GW * t / TS
Y = lambda v: GY + GH * (1 - v / 100)
top = " ".join(f"{fmt(X(s['t']))},{fmt(Y(s['z']+s['zs']/2))}" for s in HIST)
bot = " ".join(f"{fmt(X(s['t']))},{fmt(Y(s['z']-s['zs']/2))}" for s in reversed(HIST))
ind_line = " ".join(f"{fmt(X(s['t']))},{fmt(Y(s['i']))}" for s in HIST)
pro_line = " ".join(f"{fmt(X(s['t']))},{fmt(Y(s['p']))}" for s in HIST)
pro_area = f"{GX},{GY+GH} " + pro_line + f" {fmt(X(TS))},{GY+GH}"
p.append(f'<clipPath id="rev"><rect x="{GX}" y="{GY-10}" width="0" height="{GH+90}">'
         f'<animate attributeName="width" values="0;0;{GW};{GW};0" keyTimes="0;{START/C:.4f};{(START+TS)/C:.4f};0.985;1" dur="{C:.2f}s" repeatCount="indefinite"/></rect></clipPath>')
p.append(f'<g clip-path="url(#rev)">')
p.append(f'<polygon points="{pro_area}" fill="#6dff8f" opacity="0.10"/>')
p.append(f'<polygon points="{top} {bot}" fill="#e6c83c" opacity="0.35"/>')
p.append(f'<polyline points="{ind_line}" fill="none" stroke="#ffffff" stroke-width="1.6" opacity="0.85"/>')
p.append(f'<polyline points="{pro_line}" fill="none" stroke="#6dff8f" stroke-width="3.2" filter="url(#gl)"/>')
# HOLD input lane
LY = GY + GH + 34
runs = []
cur = None
for s in HIST:
    if s["h"] and cur is None:
        cur = s["t"] - 0.05
    if not s["h"] and cur is not None:
        runs.append((cur, s["t"] - 0.05)); cur = None
if cur is not None:
    runs.append((cur, TS))
for a, b in runs:
    p.append(f'<rect x="{fmt(X(a))}" y="{LY}" width="{fmt(max(1.5, X(b)-X(a)))}" height="16" rx="2" fill="#38e8ff" opacity="0.85"/>')
p.append('</g>')
p.append(f'<text x="{GX-10}" y="{LY+13}" text-anchor="end" font-family="{MONO}" font-size="12" fill="#38e8ff">HOLD</text>')
p.append(f'<rect x="{GX}" y="{LY}" width="{GW}" height="16" rx="3" fill="none" stroke="#1d3557"/>')
# playhead
p.append(f'<line x1="{GX}" y1="{GY-6}" x2="{GX}" y2="{LY+22}" stroke="#ffd166" stroke-width="2" filter="url(#gl)">'
         f'<animateTransform attributeName="transform" type="translate" values="0,0;0,0;{GW},0;{GW},0;0,0" keyTimes="0;{START/C:.4f};{(START+TS)/C:.4f};0.985;1" dur="{C:.2f}s" repeatCount="indefinite"/></line>')
# keycap that lights while holding
kts = [0.0] + [(START + s["t"]) / C for s in HIST] + [1.0]
vals = ["0"] + ["1" if s["h"] else "0" for s in HIST] + ["0"]
KX, KY = GX, LY + 44
p.append(f'<g font-family="{SANS}" font-weight="800">'
         f'<rect x="{KX}" y="{KY}" width="200" height="46" rx="10" fill="#0f1d36" stroke="#2a4570" stroke-width="2"/>'
         f'<rect x="{KX}" y="{KY}" width="200" height="46" rx="10" fill="#38e8ff" opacity="0" filter="url(#gl)">'
         f'<animate attributeName="opacity" keyTimes="{";".join(f"{k:.4f}" for k in kts)}" values="{";".join(vals)}" calcMode="discrete" dur="{C:.2f}s" repeatCount="indefinite"/></rect>'
         f'<text x="{KX+100}" y="{KY+29}" text-anchor="middle" font-size="16" fill="#e9fdff" letter-spacing="4">SPACE</text>'
         f'<text x="{KX+230}" y="{KY+29}" font-size="16" fill="#6f8db3">atau</text>'
         f'<rect x="{KX+282}" y="{KY-4}" width="38" height="54" rx="19" fill="#0f1d36" stroke="#2a4570" stroke-width="2"/>'
         f'<path d="M{KX+282},{KY+20} H{KX+320} M{KX+301},{KY-4} V{KY+20}" stroke="#2a4570" stroke-width="2"/>'
         f'<path d="M{KX+301},{KY-3} A18,18 0 0 0 {KX+283},{KY+15} V{KY+19} H{KX+300}Z" fill="#38e8ff" opacity="0">'
         f'<animate attributeName="opacity" keyTimes="{";".join(f"{k:.4f}" for k in kts)}" values="{";".join(vals)}" calcMode="discrete" dur="{C:.2f}s" repeatCount="indefinite"/></path>'
         f'<text x="{KX+340}" y="{KY+20}" font-size="14" fill="#cfe1f5">tahan = indikator naik (+55/s)</text>'
         f'<text x="{KX+340}" y="{KY+40}" font-size="14" fill="#cfe1f5">lepas = indikator turun (−40/s)</text>'
         f'</g>')
# time-limit ring
TX, TY = GX + GW - 40, KY + 22
circ = 2 * math.pi * 22
p.append(f'<circle cx="{TX}" cy="{TY}" r="22" fill="none" stroke="#1d3557" stroke-width="6"/>'
         f'<circle cx="{TX}" cy="{TY}" r="22" fill="none" stroke="#ff8a3d" stroke-width="6" stroke-linecap="round" transform="rotate(-90 {TX} {TY})" stroke-dasharray="{fmt(circ)} {fmt(circ)}">'
         f'<animate attributeName="stroke-dashoffset" values="0;0;{fmt(circ*TS/20)};{fmt(circ*TS/20)};0" keyTimes="0;{START/C:.4f};{(START+TS)/C:.4f};0.985;1" dur="{C:.2f}s" repeatCount="indefinite"/></circle>'
         f'<text x="{TX}" y="{TY+4}" text-anchor="middle" font-family="{MONO}" font-size="11" fill="#ff8a3d">20s</text>'
         f'<text x="{TX-34}" y="{TY+5}" text-anchor="end" font-family="{SANS}" font-size="13" fill="#6f8db3">batas waktu</text>')

# ---- catch popup at end
a = (START + TS) / C
b = a + 0.04
e = (START + TS + POP) / C
p.append(f'<g opacity="0"><animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="0;{a:.4f};{a+0.01:.4f};{e-0.02:.4f};{e:.4f};1" dur="{C:.2f}s" repeatCount="indefinite"/>'
         f'<rect width="{W}" height="{H}" rx="24" fill="#02060f" opacity="0.65"/>'
         f'<g transform="translate({W/2},{H/2})"><g>'
         f'<animateTransform attributeName="transform" type="scale" values="0.2;0.2;1.12;1;1" keyTimes="0;{a:.4f};{b:.4f};{b+0.03:.4f};1" dur="{C:.2f}s" repeatCount="indefinite"/>')
rays = "".join(f'<polygon points="0,0 {fmt(400*math.cos(math.radians(t-5)))},{fmt(400*math.sin(math.radians(t-5)))} {fmt(400*math.cos(math.radians(t+5)))},{fmt(400*math.sin(math.radians(t+5)))}" fill="#ffaa28"/>' for t in range(0, 360, 24))
p.append(f'<g opacity="0.18">{rays}<animateTransform attributeName="transform" type="rotate" values="0;360" dur="10s" repeatCount="indefinite"/></g>')
p.append(f'<rect x="-230" y="-120" width="460" height="240" rx="26" fill="#14100a" stroke="url(#leg)" stroke-width="4" filter="url(#gl2)"/>'
         f'<g transform="translate(-130,0)">{fish_svg("marlin", 170, 40, MARLIN["col"], wag_dur=0.18)}</g>'
         f'<text x="40" y="-46" font-family="{SANS}" font-size="15" font-weight="800" letter-spacing="4" fill="#ffaa28">LEGENDARY</text>'
         f'<text x="40" y="-6" font-family="{BLACK}" font-weight="900" font-size="32" fill="#fff">Ikan Marlin</text>'
         f'<text x="40" y="36" font-family="{BLACK}" font-weight="900" font-size="30" fill="#6dff8f" filter="url(#gl)">+250 uang</text>'
         f'<text x="40" y="70" font-family="{MONO}" font-size="13" fill="#b9a27a">ditangkap dalam {TS:.2f} detik</text>')
p.append('</g></g>')
rnd = random.Random(3)
for _ in range(40):
    ang = rnd.uniform(0, 2 * math.pi)
    dist = rnd.uniform(150, 420)
    col = rnd.choice(["#ffaa28", "#ffd166", "#6dff8f", "#38e8ff", "#ff3c5a", "#fff"])
    x1, y1 = W / 2 + math.cos(ang) * dist, H / 2 + math.sin(ang) * dist * 0.7
    p.append(f'<rect x="{W/2}" y="{H/2}" width="8" height="12" rx="2" fill="{col}">'
             f'<animate attributeName="x" values="{W/2};{W/2};{fmt(x1)};{fmt(x1)}" keyTimes="0;{a:.4f};{a+0.06:.4f};1" calcMode="spline" keySplines="0 0 1 1;0.1 0.9 0.2 1;0 0 1 1" dur="{C:.2f}s" repeatCount="indefinite"/>'
             f'<animate attributeName="y" values="{H/2};{H/2};{fmt(y1)};{fmt(y1+120)}" keyTimes="0;{a:.4f};{a+0.06:.4f};1" calcMode="spline" keySplines="0 0 1 1;0.1 0.9 0.2 1;0.5 0 1 1" dur="{C:.2f}s" repeatCount="indefinite"/>'
             f'<animateTransform attributeName="transform" type="rotate" values="0 {fmt(x1)} {fmt(y1)};720 {fmt(x1)} {fmt(y1)}" dur="1.5s" repeatCount="indefinite"/></rect>')
p.append('</g>')
p.append('</svg>')
save("reel-sim.svg", "".join(p))

# ======================================================== GAME LOOP
W, H = 1200, 360
p = [svg_open(W, H)]
p.append(f'''<defs><filter id="gl" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#060f22"/><stop offset="1" stop-color="#0b1730"/></linearGradient>
<linearGradient id="ln" x1="0" x2="1"><stop offset="0" stop-color="#38e8ff"/><stop offset="0.5" stop-color="#ffd166"/><stop offset="1" stop-color="#6dff8f"/></linearGradient></defs>''')
p.append(f'<rect x="2" y="2" width="{W-4}" height="{H-4}" rx="24" fill="url(#bg)" stroke="#1d3557" stroke-width="2"/>')
STEPS = [("LEMPAR", "CastRod", "#38e8ff", "klik tombol\nLempar Pancing"),
         ("TUNGGU", "2 – 8 detik", "#46a0ff", "server roll\nwaktu gigitan"),
         ("STRIKE!", "FishBite", "#ffd166", "pickFish()\nberbobot"),
         ("TARIK", "ReelInput ⇄ Update", "#ff8a3d", "jaga indikator\ndi zona"),
         ("CUAN", "CatchResult", "#6dff8f", "+uang, simpan\nke DataStore")]
N = len(STEPS)
CY = 150
xs = [150 + i * 225 for i in range(N)]
LOOPD = 10.0
path = f"M{xs[0]},{CY} " + " ".join(f"L{x},{CY}" for x in xs[1:]) + f" C{xs[-1]+105},{CY} {xs[-1]+105},{CY+150} {xs[-1]},{CY+150} L{xs[0]},{CY+150} C{xs[0]-105},{CY+150} {xs[0]-105},{CY} {xs[0]},{CY}"
p.append(f'<path d="{path}" fill="none" stroke="#1d3557" stroke-width="6" stroke-linecap="round"/>')
p.append(f'<path d="{path}" fill="none" stroke="url(#ln)" stroke-width="3" stroke-dasharray="10 14"><animate attributeName="stroke-dashoffset" values="0;-240" dur="4s" repeatCount="indefinite"/></path>')
p.append(f'<text x="{W/2}" y="{CY+182}" text-anchor="middle" font-family="{MONO}" font-size="14" fill="#6f8db3">session.state :  idle → casting → waiting → reeling → idle   (ulang terus sampai bosen)</text>')
# traveling comet
for k in range(6):
    p.append(f'<circle r="{9-k*1.3:.1f}" fill="#fff" opacity="{1-k*0.15:.2f}" filter="url(#gl)"><animateMotion path="{path}" dur="{LOOPD}s" begin="{-k*0.06:.2f}s" repeatCount="indefinite"/></circle>')
# total path len approx -> highlight timings
seglen = 225
total = 4 * seglen + 2 * (math.pi * 75 + 0) + 4 * seglen  # approx
for i, (title, remote, col, desc) in enumerate(STEPS):
    x = xs[i]
    tfrac = (i * seglen) / total
    hk = f"0;{max(0,tfrac-0.001):.3f};{tfrac+0.01:.3f};{tfrac+0.09:.3f};1"
    p.append(f'<circle cx="{x}" cy="{CY}" r="50" fill="#08142a" stroke="{col}" stroke-width="3"/>')
    p.append(f'<circle cx="{x}" cy="{CY}" r="50" fill="{col}" opacity="0.12"><animate attributeName="r" values="50;50;70;50;50" keyTimes="{hk}" dur="{LOOPD}s" repeatCount="indefinite"/>'
             f'<animate attributeName="opacity" values="0.12;0.12;0.5;0.12;0.12" keyTimes="{hk}" dur="{LOOPD}s" repeatCount="indefinite"/></circle>')
    p.append(f'<circle cx="{x}" cy="{CY}" r="56" fill="none" stroke="{col}" stroke-width="1.5" stroke-dasharray="4 8" opacity="0.6"><animateTransform attributeName="transform" type="rotate" values="0 {x} {CY};{360 if i%2 else -360} {x} {CY}" dur="12s" repeatCount="indefinite"/></circle>')
    # icons
    if i == 0:
        icon = (f'<g><animateTransform attributeName="transform" type="rotate" values="-30 {x-18} {CY+22};20 {x-18} {CY+22};-30 {x-18} {CY+22}" dur="1.6s" repeatCount="indefinite"/>'
                f'<path d="M{x-18},{CY+22} L{x+18},{CY-26}" stroke="#c9a77a" stroke-width="5" stroke-linecap="round"/><circle cx="{x-10}" cy="{CY+12}" r="6" fill="#556"/>'
                f'<path d="M{x+18},{CY-26} Q{x+30},{CY} {x+24},{CY+18}" stroke="#e8f8ff" stroke-width="1.5" fill="none"/></g>')
    elif i == 1:
        icon = (f'<g><animateTransform attributeName="transform" type="translate" values="0,0;0,-4;0,0" dur="1.2s" repeatCount="indefinite"/>'
                f'<circle cx="{x}" cy="{CY}" r="13" fill="#ff3c5a"/><path d="M{x-13},{CY} a13,13 0 0 0 26,0Z" fill="#f4f4f4"/><line x1="{x}" y1="{CY-13}" x2="{x}" y2="{CY-26}" stroke="#ddd" stroke-width="2"/></g>'
                f'<ellipse cx="{x}" cy="{CY+16}" rx="18" ry="4" fill="none" stroke="#bff6ff"><animate attributeName="rx" values="14;34" dur="1.6s" repeatCount="indefinite"/><animate attributeName="opacity" values="1;0" dur="1.6s" repeatCount="indefinite"/></ellipse>')
    elif i == 2:
        icon = (f'<g><animateTransform attributeName="transform" type="rotate" values="-8 {x} {CY};8 {x} {CY};-8 {x} {CY}" dur="0.25s" repeatCount="indefinite"/>'
                f'<text x="{x}" y="{CY+22}" text-anchor="middle" font-family="{BLACK}" font-weight="900" font-size="64" fill="{col}" filter="url(#gl)">!</text></g>')
    elif i == 3:
        icon = (f'<rect x="{x-9}" y="{CY-30}" width="18" height="60" rx="4" fill="#3c3c3c"/>'
                f'<rect x="{x-9}" width="18" rx="4" fill="#6dff8f" y="{CY}" height="30"><animate attributeName="height" values="10;55;10" dur="2.4s" repeatCount="indefinite"/><animate attributeName="y" values="{CY+20};{CY-25};{CY+20}" dur="2.4s" repeatCount="indefinite"/></rect>'
                f'<rect x="{x-14}" y="{CY-10}" width="28" height="14" rx="3" fill="#e6c83c" opacity="0.75"><animate attributeName="y" values="{CY-20};{CY+6};{CY-12};{CY-20}" dur="1.9s" repeatCount="indefinite"/></rect>'
                f'<rect x="{x-17}" y="{CY}" width="34" height="4" rx="2" fill="#fff"><animate attributeName="y" values="{CY-16};{CY+10};{CY-8};{CY-16}" dur="1.7s" repeatCount="indefinite"/></rect>')
    else:
        icon = (f'<g><animateTransform attributeName="transform" type="translate" values="0,0;0,-6;0,0" dur="1s" repeatCount="indefinite"/>'
                f'<circle cx="{x}" cy="{CY}" r="20" fill="#ffd166" stroke="#e0a019" stroke-width="3"/>'
                f'<text x="{x}" y="{CY+8}" text-anchor="middle" font-family="{BLACK}" font-weight="900" font-size="22" fill="#a06a00">$</text></g>')
    p.append(icon)
    p.append(f'<text x="{x}" y="{CY-72}" text-anchor="middle" font-family="{BLACK}" font-weight="900" font-size="22" fill="{col}" letter-spacing="1">{title}</text>')
    p.append(f'<rect x="{x-82}" y="{CY+62}" width="164" height="26" rx="13" fill="{col}" fill-opacity="0.12" stroke="{col}" stroke-opacity="0.5"/>'
             f'<text x="{x}" y="{CY+80}" text-anchor="middle" font-family="{MONO}" font-size="13" fill="{col}">{remote}</text>')
    p.append(f'<text x="{x}" y="{CY+112}" text-anchor="middle" font-family="{SANS}" font-size="12.5" fill="#9fb8d6">{desc.replace(chr(10), " · ")}</text>')
p.append('</svg>')
save("game-loop.svg", "".join(p))
