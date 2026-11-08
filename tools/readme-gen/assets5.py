from common import *

# ======================================================== ARCHITECTURE
W, H = 1200, 700
p = [svg_open(W, H)]
p.append(f'''<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#060f22"/><stop offset="1" stop-color="#0b1730"/></linearGradient>
<pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.2" fill="#38e8ff" opacity="0.12"/></pattern>
<filter id="gl" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<marker id="ah" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10Z" fill="#6f8db3"/></marker>
</defs>''')
p.append(f'<rect x="2" y="2" width="{W-4}" height="{H-4}" rx="24" fill="url(#bg)" stroke="#1d3557" stroke-width="2"/><rect x="2" y="2" width="{W-4}" height="{H-4}" rx="24" fill="url(#dots)"/>')


def box(x, y, w, h, title, sub, col, items):
    o = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" fill="#08142a" stroke="{col}" stroke-width="2"/>',
         f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" fill="{col}" opacity="0.05"><animate attributeName="opacity" values="0.03;0.1;0.03" dur="4s" repeatCount="indefinite"/></rect>',
         f'<rect x="{x}" y="{y}" width="{w}" height="46" rx="18" fill="{col}" opacity="0.16"/><rect x="{x}" y="{y+28}" width="{w}" height="18" fill="{col}" opacity="0.0"/>',
         f'<text x="{x+20}" y="{y+30}" font-family="{BLACK}" font-weight="900" font-size="17" fill="{col}" letter-spacing="2">{title}</text>',
         f'<text x="{x+w-18}" y="{y+30}" text-anchor="end" font-family="{MONO}" font-size="11.5" fill="#6f8db3">{sub}</text>']
    for i, (name, desc) in enumerate(items):
        yy = y + 64 + i * 54
        o.append(f'<rect x="{x+14}" y="{yy}" width="{w-28}" height="44" rx="10" fill="#0c1b36" stroke="#1f3a63"/>'
                 f'<text x="{x+28}" y="{yy+19}" font-family="{MONO}" font-size="14" font-weight="700" fill="#e9fdff">{name}</text>'
                 f'<text x="{x+28}" y="{yy+36}" font-family="{SANS}" font-size="12" fill="#8fb0d4">{desc}</text>')
    return "".join(o)


CX, SX, BW = 40, 820, 340
p.append(box(CX, 40, BW, 240, "CLIENT", "StarterPlayerScripts", "#38e8ff", [
    ("FishingClient.client", "UI tombol, ReelFrame, popup tangkapan"),
    ("PondAmbience.client", "10 ikan hias + 6 titik gelembung"),
    ("Input", "MouseButton1 / Space → holding")]))
p.append(box(SX, 40, BW, 240, "SERVER", "ServerScriptService", "#ff8a3d", [
    ("FishingService.server", "loop mancing + minigame 20Hz"),
    ("DataManager", "Cash, FishCaught, leaderstats"),
    ("RodTool", "joran prosedural + animasi")]))
p.append(box(430, 40, 340, 186, "SHARED", "ReplicatedStorage", "#af50e6", [
    ("Config · FishData", "angka balancing &amp; tabel ikan"),
    ("RarityData · Remotes", "warna tier &amp; 5 RemoteEvent")]))
# require arrows
p.append(f'<path d="M430,130 C400,130 400,160 382,160" stroke="#af50e6" stroke-width="2" fill="none" stroke-dasharray="5 5" marker-end="url(#ah)"><animate attributeName="stroke-dashoffset" values="0;-20" dur="1s" repeatCount="indefinite"/></path>')
p.append(f'<path d="M770,130 C800,130 800,160 818,160" stroke="#af50e6" stroke-width="2" fill="none" stroke-dasharray="5 5" marker-end="url(#ah)"><animate attributeName="stroke-dashoffset" values="0;-20" dur="1s" repeatCount="indefinite"/></path>')
p.append(f'<text x="600" y="250" text-anchor="middle" font-family="{MONO}" font-size="12" fill="#af50e6">require() dari kedua sisi</text>')

# remote lanes
LX0, LX1 = CX + BW, SX
lanes = [("CastRod", 1, "( )", "#38e8ff", 1, 3.0),
         ("FishBite", -1, "( )", "#ffd166", 1, 3.4),
         ("ReelInput", 1, "{ holding }", "#38e8ff", 2, 1.6),
         ("ReelUpdate", -1, "{ progress, zoneCenter, zoneSize, indicator }", "#6dff8f", 6, 1.2),
         ("CatchResult", -1, "{ success, fishName, rarity, value }", "#ffaa28", 1, 3.8)]
p.append(f'<rect x="{CX}" y="296" width="{SX+BW-CX}" height="300" rx="18" fill="none" stroke="#1d3557" stroke-dasharray="6 6"/>')
p.append(f'<text x="{W/2}" y="322" text-anchor="middle" font-family="{BLACK}" font-weight="900" font-size="15" letter-spacing="3" fill="#6f8db3">REPLICATEDSTORAGE / FISHINGREMOTES</text>')
for i, (name, dirn, payload, col, npk, dur) in enumerate(lanes):
    y = 360 + i * 48
    p.append(f'<line x1="{CX+20}" y1="{y}" x2="{SX+BW-20}" y2="{y}" stroke="{col}" stroke-opacity="0.25" stroke-width="2"/>')
    p.append(f'<text x="{CX+24}" y="{y-8}" font-family="{MONO}" font-size="13" font-weight="700" fill="{col}">{name}</text>')
    p.append(f'<text x="{SX+BW-24}" y="{y-8}" text-anchor="end" font-family="{MONO}" font-size="11.5" fill="#8fb0d4">{"client → server" if dirn==1 else "server → client"}</text>')
    p.append(f'<text x="{W/2}" y="{y+18}" text-anchor="middle" font-family="{MONO}" font-size="11" fill="#5f7fa6">{payload}</text>')
    a, b = (CX + 20, SX + BW - 20) if dirn == 1 else (SX + BW - 20, CX + 20)
    for k in range(npk):
        p.append(f'<g><animateTransform attributeName="transform" type="translate" values="{a},{y};{b},{y}" dur="{dur}s" begin="{-k*dur/npk:.2f}s" repeatCount="indefinite"/>'
                 f'<rect x="-14" y="-7" width="28" height="14" rx="7" fill="{col}" filter="url(#gl)"/>'
                 f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.08;0.92;1" dur="{dur}s" begin="{-k*dur/npk:.2f}s" repeatCount="indefinite"/></g>')
p.append(f'<text x="{W/2}" y="590" text-anchor="middle" font-family="{SANS}" font-size="12" fill="#5f7fa6">ReelUpdate dikirim tiap tick (TickRate = 1/20)  ·  client hanya mengirim boolean holding</text>')

# exploit attempt bounce
EY = 640
T = 5.0
p.append(f'<text x="{CX+20}" y="{EY-14}" font-family="{SANS}" font-size="12.5" font-weight="700" fill="#ff3c5a">percobaan cheat:</text>')
p.append(f'<g><animateTransform attributeName="transform" type="translate" values="{CX+60},{EY+10};{SX-60},{EY+10};{SX-160},{EY+10}" keyTimes="0;0.6;1" dur="{T}s" repeatCount="indefinite"/>'
         f'<animate attributeName="opacity" values="1;1;0.8;0" keyTimes="0;0.6;0.8;1" dur="{T}s" repeatCount="indefinite"/>'
         f'<rect x="-70" y="-12" width="140" height="24" rx="12" fill="#ff3c5a" fill-opacity="0.2" stroke="#ff3c5a"/>'
         f'<text x="0" y="5" text-anchor="middle" font-family="{MONO}" font-size="12" fill="#ff8a9a">progress = 100</text></g>')
p.append(f'<g transform="translate({SX+10},{EY+8})"><path d="M0,-26 L22,-18 V2 C22,16 10,24 0,28 C-10,24 -22,16 -22,2 V-18Z" fill="#0c1b36" stroke="#6dff8f" stroke-width="2.5" filter="url(#gl)">'
         f'<animate attributeName="stroke-width" values="2.5;2.5;6;2.5;2.5" keyTimes="0;0.58;0.62;0.7;1" dur="{T}s" repeatCount="indefinite"/></path>'
         f'<path d="M-9,1 l6,7 l12,-14" stroke="#6dff8f" stroke-width="3.5" fill="none" stroke-linecap="round"/></g>')
p.append(f'<text x="{SX+44}" y="{EY+4}" font-family="{SANS}" font-size="13" font-weight="700" fill="#6dff8f">ditolak: server menghitung sendiri</text>'
         f'<text x="{SX+44}" y="{EY+22}" font-family="{SANS}" font-size="12" fill="#8fb0d4">payload selain holding diabaikan</text>')
p.append('</svg>')
save("architecture.svg", "".join(p))

# ======================================================== POND MAP
W, H = 1200, 680
rnd = random.Random(11)
p = [svg_open(W, H)]
p.append(f'''<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#060f22"/><stop offset="1" stop-color="#0b1730"/></linearGradient>
<radialGradient id="water" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#1d7fae"/><stop offset="0.8" stop-color="#236a8c"/><stop offset="1" stop-color="#2d8fa8"/></radialGradient>
<pattern id="grass" width="16" height="16" patternUnits="userSpaceOnUse"><rect width="16" height="16" fill="#2f6b2a"/><path d="M3,12 l1,-4 M9,7 l1,-4 M13,14 l1,-4" stroke="#3f8a37" stroke-width="1.5"/></pattern>
<pattern id="sandp" width="10" height="10" patternUnits="userSpaceOnUse"><rect width="10" height="10" fill="#d8c48a"/><circle cx="3" cy="3" r="0.9" fill="#bfa967"/><circle cx="8" cy="7" r="0.9" fill="#bfa967"/></pattern>
<filter id="caus"><feTurbulence type="fractalNoise" baseFrequency="0.03" numOctaves="2" seed="4"><animate attributeName="baseFrequency" values="0.03;0.04;0.03" dur="10s" repeatCount="indefinite"/></feTurbulence>
<feColorMatrix type="matrix" values="0 0 0 0 0.8  0 0 0 0 1  0 0 0 0 1  0 0 0 10 -6"/><feComposite in2="SourceGraphic" operator="in"/></filter>
<filter id="gl" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<clipPath id="mapc"><rect x="30" y="50" width="560" height="600" rx="18"/></clipPath>
<clipPath id="pondc"><circle cx="310" cy="330" r="189"/></clipPath>
</defs>''')
p.append(f'<rect x="2" y="2" width="{W-4}" height="{H-4}" rx="24" fill="url(#bg)" stroke="#1d3557" stroke-width="2"/>')
p.append(f'<text x="40" y="36" font-family="{BLACK}" font-weight="900" font-size="18" letter-spacing="2" fill="#5dffb0">TAMPAK ATAS</text>'
         f'<text x="590" y="36" text-anchor="end" font-family="{MONO}" font-size="12" fill="#6f8db3">1 stud = 4.5 px</text>')
S = 4.5
CXm, CYm = 310, 330
p.append('<g clip-path="url(#mapc)">')
p.append(f'<rect x="30" y="50" width="560" height="600" fill="url(#grass)"/>')
p.append(f'<circle cx="{CXm}" cy="{CYm}" r="{50*S}" fill="url(#sandp)"/>')
p.append(f'<circle cx="{CXm}" cy="{CYm}" r="{42*S}" fill="url(#water)"/>')
p.append(f'<circle cx="{CXm}" cy="{CYm}" r="{42*S}" fill="#fff" opacity="0.5" filter="url(#caus)"/>')
for k in range(3):
    p.append(f'<circle cx="{CXm}" cy="{CYm}" r="{42*S}" fill="none" stroke="#bff6ff" stroke-width="2" opacity="0"><animate attributeName="r" values="{42*S-60};{42*S}" dur="6s" begin="{k*2}s" repeatCount="indefinite"/><animate attributeName="opacity" values="0;0.4;0" dur="6s" begin="{k*2}s" repeatCount="indefinite"/></circle>')
p.append(f'<circle cx="{CXm}" cy="{CYm}" r="{36*S}" fill="none" stroke="#ffd166" stroke-width="2" stroke-dasharray="8 8" opacity="0.8"><animateTransform attributeName="transform" type="rotate" values="0 {CXm} {CYm};360 {CXm} {CYm}" dur="60s" repeatCount="indefinite"/></circle>')
# bubble spots
for i in range(6):
    a = rnd.uniform(0, 2 * math.pi)
    r = rnd.uniform(0, 32) * S
    bx, by = CXm + math.cos(a) * r, CYm + math.sin(a) * r
    for k in range(2):
        p.append(f'<circle cx="{fmt(bx)}" cy="{fmt(by)}" r="3" fill="none" stroke="#e9fdff" stroke-width="1.5"><animate attributeName="r" values="2;14" dur="2s" begin="{k+i*0.3:.1f}s" repeatCount="indefinite"/><animate attributeName="opacity" values="0.9;0" dur="2s" begin="{k+i*0.3:.1f}s" repeatCount="indefinite"/></circle>')
    p.append(f'<circle cx="{fmt(bx)}" cy="{fmt(by)}" r="2.5" fill="#e9fdff"/>')
# ambient fish (wandering loops, top-down = small ellipses)
COLS = ["#ff8c3c", "#e1e1e6", "#ffd75a", "#5aa0ff", "#eb5a5a"]
for i in range(10):
    pts = []
    for k in range(5):
        a = rnd.uniform(0, 2 * math.pi)
        r = math.sqrt(rnd.random()) * 34 * S
        pts.append((CXm + math.cos(a) * r, CYm + math.sin(a) * r))
    d = f"M{fmt(pts[0][0])},{fmt(pts[0][1])} " + " ".join(f"S{fmt((pts[k][0]+pts[(k+1)%5][0])/2)},{fmt((pts[k][1]+pts[(k+1)%5][1])/2)} {fmt(pts[(k+1)%5][0])},{fmt(pts[(k+1)%5][1])}" for k in range(5))
    c = COLS[i % 5]
    p.append(f'<g><animateMotion path="{d}" dur="{rnd.uniform(16,28):.1f}s" repeatCount="indefinite" rotate="auto"/>'
             f'<g clip-path="none"><ellipse cx="0" cy="0" rx="11" ry="4.5" fill="{c}"/><path d="M-9,0 l-7,-5 v10Z" fill="{c}"><animateTransform attributeName="transform" type="rotate" values="-20 -9 0;20 -9 0;-20 -9 0" dur="0.5s" repeatCount="indefinite"/></path>'
             f'<circle cx="6" cy="-1.5" r="1.2" fill="#000"/></g></g>')
# spawn + player
SPY = CYm + 60 * S
p.append(f'<rect x="{CXm-3*S}" y="{SPY-3*S}" width="{6*S}" height="{6*S}" fill="#4bd36a" stroke="#c9ffd6" stroke-width="2"/>'
         f'<circle cx="{CXm}" cy="{SPY}" r="6" fill="#fff"/><path d="M{CXm},{SPY} L{CXm},{SPY-30}" stroke="#c9a77a" stroke-width="3"/>'
         f'<circle cx="{CXm}" cy="{SPY}" r="10" fill="none" stroke="#4bd36a"><animate attributeName="r" values="10;30" dur="1.8s" repeatCount="indefinite"/><animate attributeName="opacity" values="1;0" dur="1.8s" repeatCount="indefinite"/></circle>')
p.append('</g>')
p.append(f'<rect x="30" y="50" width="560" height="600" rx="18" fill="none" stroke="#1d3557" stroke-width="2"/>')
# labels
def label(x1, y1, x2, y2, text, col):
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{col}" stroke-width="1.5"/><circle cx="{x1}" cy="{y1}" r="3.5" fill="{col}"/>'
            f'<rect x="{x2-4}" y="{y2-15}" width="{len(text)*7.6+12}" height="22" rx="6" fill="#050b18" fill-opacity="0.85" stroke="{col}" stroke-opacity="0.6"/>'
            f'<text x="{x2+2}" y="{y2+1}" font-family="{MONO}" font-size="12" fill="{col}">{text}</text>')
p.append(label(CXm + 42 * S * 0.71, CYm - 42 * S * 0.71, 470, 90, "air  r = 42", "#7fd8ff"))
p.append(label(CXm - 50 * S * 0.8, CYm - 50 * S * 0.6, 50, 80, "pasir  r = 50", "#e8d39a"))
p.append(label(CXm + 36 * S * 0.6, CYm + 36 * S * 0.8, 440, 560, "SwimRadius = 36", "#ffd166"))
p.append(label(CXm + 12, SPY, 400, SPY + 14, "Spawn (0, 1, 60)", "#4bd36a"))
# compass
p.append(f'<g transform="translate(548,610)"><circle r="22" fill="#050b18" fill-opacity="0.8" stroke="#6f8db3"/><path d="M0,-16 L5,0 L0,16 L-5,0Z" fill="#ff3c5a"/><text y="-26" text-anchor="middle" font-family="{SANS}" font-size="11" font-weight="800" fill="#cfe1f5">-Z</text></g>')

# ---- cross section
X0, Y0w = 640, 70
p.append(f'<text x="{X0}" y="36" font-family="{BLACK}" font-weight="900" font-size="18" letter-spacing="2" fill="#38e8ff">TAMPAK SAMPING</text>'
         f'<text x="{W-40}" y="36" text-anchor="end" font-family="{MONO}" font-size="12" fill="#6f8db3">potongan melintang lewat X = 0</text>')
SX_ = 4.6   # px per stud horizontal
SY_ = 22    # px per stud vertical
cxs = X0 + 260
def gx(s): return cxs + s * SX_
def gy(s): return 170 - s * SY_   # y=0 at 170
p.append(f'<rect x="{X0}" y="50" width="520" height="380" rx="18" fill="#0a1a33"/>')
p.append(f'<clipPath id="secc"><rect x="{X0}" y="50" width="520" height="380" rx="18"/></clipPath><g clip-path="url(#secc)">')
p.append(f'<rect x="{X0}" y="50" width="520" height="{gy(0)-50}" fill="#0f2147"/>')
p.append(f'<rect x="{X0}" y="{gy(0)}" width="520" height="400" fill="#3a6b2a"/><rect x="{X0}" y="{gy(0)}" width="520" height="6" fill="#4f8f3a"/>')
p.append(f'<rect x="{gx(-50)}" y="{gy(1)}" width="{100*SX_}" height="{3*SY_}" fill="#d8c48a"/>')
p.append(f'<rect x="{gx(-45)}" y="{gy(1)}" width="{90*SX_}" height="{10*SY_}" fill="#0f2147"/>')
p.append(f'<rect x="{gx(-44)}" y="{gy(-7.75)}" width="{88*SX_}" height="{1.5*SY_}" fill="#c9b273"/>')
p.append(f'<rect x="{gx(-42)}" y="{gy(-0.5)}" width="{84*SX_}" height="{8*SY_}" fill="#1d6f9a" opacity="0.92"/>')
p.append(f'<g><path d="{wave_path(84*SX_+80, gy(-0.5), 2.5, 40, gy(-0.5)+6)}" fill="#5fc4e6" opacity="0.8" transform="translate({gx(-42)},0)"><animateTransform attributeName="transform" type="translate" values="{gx(-42)},0;{gx(-42)-40},0" dur="2s" repeatCount="indefinite"/></path></g>')
p.append(f'<rect x="{gx(-42)}" y="{gy(-1.5)}" width="{84*SX_}" height="{5.5*SY_}" fill="none" stroke="#ffd166" stroke-dasharray="6 6" stroke-width="1.5"/>')
# side-view fish in swim band
for i in range(6):
    yv = rnd.uniform(-6.6, -2.0)
    f = FISH[rnd.randint(0, 7)]
    dur = rnd.uniform(8, 14)
    p.append(f'<g><animateMotion path="M{gx(-38)},{gy(yv)} L{gx(38)},{gy(yv)+rnd.uniform(-10,10):.0f} L{gx(-38)},{gy(yv)}" dur="{dur:.1f}s" begin="-{rnd.uniform(0,dur):.1f}s" repeatCount="indefinite" rotate="auto"/>'
             f'<g transform="scale(1,{1})">{fish_svg(f["kind"], 30, 12, f["col"], wag_dur=0.3)}</g></g>')
p.append(bubbles(rnd, 14, gx(-30), gx(30), gy(-7.9), gy(-0.6), 1.5, 3.5))
p.append('</g>')
p.append(f'<rect x="{X0}" y="50" width="520" height="380" rx="18" fill="none" stroke="#1d3557" stroke-width="2"/>')
# axis labels
for yv, lab in [(1, "+1"), (0, "0"), (-0.5, "-0.5"), (-1.5, "-1.5"), (-7, "-7"), (-8.5, "-8.5")]:
    p.append(f'<line x1="{X0+514}" y1="{gy(yv)}" x2="{X0+522}" y2="{gy(yv)}" stroke="#6f8db3"/><text x="{X0+528}" y="{gy(yv)+4}" font-family="{MONO}" font-size="10.5" fill="#6f8db3">{lab}</text>')
# legend for section
LEG = [("#4f8f3a", "Grass  ·  FillBlock 500×20×500"), ("#d8c48a", "Sand ring  ·  r 50"), ("#1d6f9a", "Water  ·  r 42, tinggi 8"),
       ("#c9b273", "Sand floor  ·  r 44"), ("#ffd166", "Zona renang ikan hias (y -7 … -1.5)")]
for i, (c, t) in enumerate(LEG):
    y = 460 + i * 28
    p.append(f'<rect x="{X0}" y="{y}" width="16" height="16" rx="4" fill="{c}"/><text x="{X0+26}" y="{y+13}" font-family="{SANS}" font-size="13.5" fill="#cfe1f5">{t}</text>')
p.append(f'<text x="{X0}" y="{460+5*28+14}" font-family="{MONO}" font-size="12" fill="#6f8db3">WaterColor (35,106,140) · Transparency 0.3 · WaveSpeed 10</text>')
p.append('</svg>')
save("pond-map.svg", "".join(p))
