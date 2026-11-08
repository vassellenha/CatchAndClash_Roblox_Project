from common import *

EMOJI = "'Segoe UI Emoji','Apple Color Emoji','Noto Color Emoji',sans-serif"

LORE = {
    "lele": "Penghuni dasar kolam. Kumisnya lebih panjang dari kesabaranmu.",
    "mujair": "Ikan sejuta umat. Gampang ditarik, gampang dilupakan.",
    "nila": "Garis-garisnya rapi, mentalnya juga. Favorit pemula.",
    "gurame": "Bongsor dan kalem. Biasanya sudah dipesan warung sebelah.",
    "kakap": "Merah merona, tarikannya lumayan bikin pegel jempol.",
    "kerapu": "Totol-totol, paling sering nongol di antara yang Rare.",
    "tuna": "Torpedo biru. Zona tangkapnya mulai mengecil, fokus!",
    "hiu": "Bukan hiu beneran (katanya). Tetap jangan dipeluk.",
    "marlin": "Si layar biru. Zona sempit, gerak liar, cuan besar.",
    "naga": "Konon cuma 1 dari 230 lemparan. Zona 14.8, kecepatan 34.6.",
}
TIER = {r: i + 1 for i, r in enumerate(ORDER)}


def card(idx, f):
    W, H = 600, 340
    r = RARITY[f["rarity"]]
    c, c2 = r["c"], r["c2"]
    rnd = random.Random(idx * 13 + 1)
    myth = f["rarity"] == "Mythical"
    leg = f["rarity"] == "Legendary"
    p = [svg_open(W, H)]
    p.append(f'''<defs>
<linearGradient id="bg" x1="0" y1="0" x2="0.4" y2="1"><stop offset="0" stop-color="#0b1a33"/><stop offset="1" stop-color="#030812"/></linearGradient>
<radialGradient id="aura" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="{c}" stop-opacity="0.55"/><stop offset="1" stop-color="{c}" stop-opacity="0"/></radialGradient>
<linearGradient id="bd" x1="0" y1="0" x2="1" y2="1">
 {"".join(f'<stop offset="{k/6:.2f}" stop-color="{col}"/>' for k, col in enumerate(["#ff3c5a","#ffaa28","#ffe14a","#5dffb0","#38e8ff","#af50e6","#ff3c5a"])) if myth else f'<stop offset="0" stop-color="{c}"/><stop offset="1" stop-color="{c2}"/>'}
 {'<animateTransform attributeName="gradientTransform" type="rotate" values="0 0.5 0.5;360 0.5 0.5" dur="4s" repeatCount="indefinite"/>' if myth else ''}
</linearGradient>
<linearGradient id="shine" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="0.5" stop-color="#fff" stop-opacity="0.22"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<clipPath id="cc"><rect x="4" y="4" width="{W-8}" height="{H-8}" rx="24"/></clipPath>
<filter id="gl" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>''')
    p.append(f'<rect x="4" y="4" width="{W-8}" height="{H-8}" rx="24" fill="url(#bg)"/>')
    p.append('<g clip-path="url(#cc)">')
    # water area top
    p.append(f'<rect x="4" y="4" width="{W-8}" height="196" fill="{c}" opacity="0.07"/>')
    for i in range(5):
        x = 60 + i * 120
        p.append(f'<polygon points="{x},4 {x+40},4 {x+90},200 {x-10},200" fill="{c}" opacity="0.05"><animate attributeName="opacity" values="0.02;0.1;0.02" dur="{3+i*0.7:.1f}s" repeatCount="indefinite"/></polygon>')
    p.append(f'<ellipse cx="{W/2}" cy="108" rx="{170 if not myth else 220}" ry="80" fill="url(#aura)"><animate attributeName="rx" values="150;{200 if not myth else 250};150" dur="2.6s" repeatCount="indefinite"/></ellipse>')
    if f["rarity"] in ("Legendary", "Mythical", "UltraRare"):
        # rotating light rays
        rays = "".join(f'<polygon points="{W/2},108 {fmt(W/2+260*math.cos(math.radians(a-4)))},{fmt(108+260*math.sin(math.radians(a-4)))} {fmt(W/2+260*math.cos(math.radians(a+4)))},{fmt(108+260*math.sin(math.radians(a+4)))}" fill="{c}"/>' for a in range(0, 360, 30))
        p.append(f'<g opacity="0.13">{rays}<animateTransform attributeName="transform" type="rotate" values="0 {W/2} 108;360 {W/2} 108" dur="{18 if not myth else 9}s" repeatCount="indefinite"/></g>')
    p.append(bubbles(rnd, 14, 20, W - 20, 200, 10, 1.5, 4, c))
    # fish
    L, Hh = {"marlin": (250, 58), "hiu": (240, 66), "naga": (300, 110), "tuna": (210, 70), "gurame": (190, 88)}.get(f["id"], (190, 76))
    p.append(f'<g transform="translate({W/2+ (20 if f["id"]=="naga" else 0)},108)"><g><animateTransform attributeName="transform" type="translate" values="-10,-6;10,4;-10,-6" dur="{3.5+rnd.uniform(0,1.5):.1f}s" repeatCount="indefinite"/>'
             f'<g><animateTransform attributeName="transform" type="rotate" values="-3;3;-3" dur="2.4s" repeatCount="indefinite"/>{fish_svg(f["kind"], L, Hh, f["col"], wag_dur=0.32 if f["d"]>0.4 else 0.5)}</g></g></g>')
    # sparkles
    if f["rarity"] in ("Legendary", "Mythical", "UltraRare"):
        for _ in range(12 if myth else 8):
            sx, sy = rnd.uniform(40, W - 40), rnd.uniform(20, 190)
            s = rnd.uniform(5, 11)
            d = rnd.uniform(1.2, 2.6)
            p.append(f'<path d="M{fmt(sx)},{fmt(sy-s)} Q{fmt(sx)},{fmt(sy)} {fmt(sx+s)},{fmt(sy)} Q{fmt(sx)},{fmt(sy)} {fmt(sx)},{fmt(sy+s)} Q{fmt(sx)},{fmt(sy)} {fmt(sx-s)},{fmt(sy)} Q{fmt(sx)},{fmt(sy)} {fmt(sx)},{fmt(sy-s)}Z" fill="#fff" opacity="0">'
                     f'<animate attributeName="opacity" values="0;1;0" dur="{d:.1f}s" begin="-{rnd.uniform(0,3):.1f}s" repeatCount="indefinite"/></path>')
    # divider wave
    p.append(f'<g><path d="{wave_path(W+120, 200, 4, 60, H)}" fill="#050c18"><animateTransform attributeName="transform" type="translate" values="0,0;-60,0" dur="3s" repeatCount="indefinite"/></path></g>')
    p.append(f'<rect x="4" y="206" width="{W-8}" height="{H-210}" fill="#050c18"/>')
    # rarity pill + stars
    pw = len(r["name"]) * 11 + 34
    p.append(f'<rect x="24" y="22" width="{pw}" height="30" rx="15" fill="{c}" fill-opacity="0.2" stroke="{c}" stroke-width="1.6"/>'
             f'<text x="{24+pw/2}" y="42" text-anchor="middle" font-family="{SANS}" font-size="14" font-weight="800" letter-spacing="2" fill="{c}">{r["name"]}</text>')
    for k in range(5):
        on = k < TIER[f["rarity"]]
        sx = 24 + pw + 18 + k * 22
        star = f"M{sx},29 l3.2,6.6 7.2,1 -5.2,5 1.3,7.2 -6.5,-3.4 -6.5,3.4 1.3,-7.2 -5.2,-5 7.2,-1Z"
        p.append(f'<path d="{star}" fill="{c if on else "#22324d"}">' + (f'<animate attributeName="opacity" values="1;0.5;1" dur="1.4s" begin="{k*0.15}s" repeatCount="indefinite"/>' if on else '') + '</path>')
    p.append(f'<text x="{W-26}" y="44" text-anchor="end" font-family="{MONO}" font-size="16" font-weight="700" fill="#6f8db3">#{idx:02d}</text>')
    # name
    p.append(f'<text x="28" y="246" font-family="{BLACK}" font-size="30" font-weight="900" fill="{"url(#bd)" if myth else "#f2f8ff"}" letter-spacing="1">{f["name"].upper()}</text>')
    lore = LORE[f["id"]]
    p.append(f'<text x="28" y="270" font-family="{SANS}" font-size="13.5" font-style="italic" fill="#8fb0d4">{lore}</text>')
    # stats
    stats = [("PELUANG", f"{f['pct']:.2f}%"), ("NILAI", f"+{f['value']}"), ("ZONA", f"{f['zone']:.1f}")]
    for k, (lab, val) in enumerate(stats):
        x = 28 + k * 118
        p.append(f'<text x="{x}" y="298" font-family="{SANS}" font-size="11" font-weight="800" letter-spacing="2" fill="#5f7fa6">{lab}</text>'
                 f'<text x="{x}" y="322" font-family="{MONO}" font-size="20" font-weight="800" fill="{c}">{val}</text>')
    # difficulty bar
    bx, bw = 390, 182
    p.append(f'<text x="{bx}" y="298" font-family="{SANS}" font-size="11" font-weight="800" letter-spacing="2" fill="#5f7fa6">KESULITAN</text>'
             f'<text x="{bx+bw}" y="298" text-anchor="end" font-family="{MONO}" font-size="12" font-weight="800" fill="{c}">{f["d"]:.2f}</text>'
             f'<rect x="{bx}" y="307" width="{bw}" height="14" rx="7" fill="#13233d"/>')
    for k in range(10):
        p.append(f'<rect x="{bx+k*bw/10+1}" y="309" width="{bw/10-2}" height="10" rx="3" fill="#1b2f50"/>')
    p.append(f'<rect x="{bx}" y="307" width="0" height="14" rx="7" fill="url(#bd)" filter="url(#gl)">'
             f'<animate attributeName="width" values="0;{fmt(bw*f["d"])};{fmt(bw*f["d"])};0" keyTimes="0;0.25;0.92;1" calcMode="spline" keySplines="0.2 0.8 0.2 1;0 0 1 1;0 0 1 1" dur="6s" repeatCount="indefinite"/></rect>')
    # shine sweep
    p.append(f'<rect x="-200" y="0" width="160" height="{H}" fill="url(#shine)" transform="skewX(-18)"><animate attributeName="x" values="-300;-300;{W+200}" keyTimes="0;0.7;1" dur="{5+idx*0.3:.1f}s" repeatCount="indefinite"/></rect>')
    p.append('</g>')
    # border
    per = 2 * (W - 8 + H - 8)
    p.append(f'<rect x="4" y="4" width="{W-8}" height="{H-8}" rx="24" fill="none" stroke="url(#bd)" stroke-width="2" stroke-opacity="0.55"/>')
    if f["rarity"] != "Common":
        p.append(f'<rect x="4" y="4" width="{W-8}" height="{H-8}" rx="24" fill="none" stroke="url(#bd)" stroke-width="{5 if myth or leg else 3}" stroke-dasharray="{300 if myth else 180} {per-(300 if myth else 180)}" filter="url(#gl)">'
                 f'<animate attributeName="stroke-dashoffset" values="0;{-per}" dur="{2.5 if myth else 4 if leg else 6}s" repeatCount="indefinite"/></rect>')
    if myth:
        p.append(f'<rect x="4" y="4" width="{W-8}" height="{H-8}" rx="24" fill="none" stroke="url(#bd)" stroke-width="5" stroke-dasharray="300 {per-300}" stroke-dashoffset="{per/2}" filter="url(#gl)">'
                 f'<animate attributeName="stroke-dashoffset" values="{-per/2};{-per*1.5}" dur="2.5s" repeatCount="indefinite"/></rect>')
    p.append('</svg>')
    save(f"fish-{idx:02d}-{f['id']}.svg", "".join(p))


for i, f in enumerate(FISH, 1):
    card(i, f)

# ---------------------------------------------------------------- drop chart
W, H = 1200, 600
p = [svg_open(W, H)]
p.append(f'<defs><filter id="gl" x="-20%" y="-50%" width="140%" height="200%"><feGaussianBlur stdDeviation="4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
         f'<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#071226"/><stop offset="1" stop-color="#0d0a24"/></linearGradient>'
         + "".join(f'<linearGradient id="g{r}" x1="0" x2="1"><stop offset="0" stop-color="{RARITY[r]["c2"]}"/><stop offset="1" stop-color="{RARITY[r]["c"]}"/></linearGradient>' for r in ORDER) +
         '</defs>')
p.append(f'<rect x="2" y="2" width="{W-4}" height="{H-4}" rx="24" fill="url(#bg)" stroke="#1d3557" stroke-width="2"/>')
p.append(f'<text x="40" y="54" font-family="{BLACK}" font-size="26" fill="#e9fdff">PELUANG PER IKAN</text>'
         f'<text x="40" y="80" font-family="{MONO}" font-size="14" fill="#6f8db3">P(ikan) = weight / {TOTAL_W}   ·   diambil dari FishData.lua</text>')
T = 9.0
bx0, bmax = 200, 470
srt = sorted(FISH, key=lambda f: -f["weight"])
maxp = srt[0]["pct"]
for i, f in enumerate(srt):
    y = 112 + i * 46
    col = RARITY[f["rarity"]]["c"]
    w = bmax * f["pct"] / maxp
    d0 = 0.05 + i * 0.03
    p.append(f'<text x="{bx0-14}" y="{y+20}" text-anchor="end" font-family="{SANS}" font-size="16" font-weight="700" fill="#dce9f7">{f["name"]}</text>')
    p.append(f'<rect x="{bx0}" y="{y}" width="{bmax}" height="28" rx="8" fill="#0f1d36"/>')
    p.append(f'<rect x="{bx0}" y="{y}" width="0" height="28" rx="8" fill="url(#g{f["rarity"]})" filter="url(#gl)">'
             f'<animate attributeName="width" values="0;0;{fmt(max(w,6))};{fmt(max(w,6))};0" keyTimes="0;{d0:.2f};{d0+0.18:.2f};0.94;1" calcMode="spline" keySplines="0 0 1 1;0.2 0.9 0.2 1;0 0 1 1;0 0 1 1" dur="{T}s" repeatCount="indefinite"/></rect>')
    p.append(f'<text x="{bx0+max(w,6)+10}" y="{y+20}" font-family="{MONO}" font-size="15" font-weight="800" fill="{col}" opacity="0">{f["pct"]:.2f}%'
             f'<animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;{d0+0.15:.2f};{d0+0.2:.2f};0.94;1" dur="{T}s" repeatCount="indefinite"/></text>')
# donut by rarity
cx, cy, R = 950, 330, 150
circ = 2 * math.pi * R
p.append(f'<text x="{cx}" y="54" text-anchor="middle" font-family="{BLACK}" font-size="26" fill="#e9fdff">PER TIER</text>'
         f'<text x="{cx}" y="80" text-anchor="middle" font-family="{MONO}" font-size="14" fill="#6f8db3">total weight per rarity</text>')
p.append(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="#0f1d36" stroke-width="46"/>')
acc = 0
tiers = []
for r in ORDER:
    pct = sum(f["pct"] for f in FISH if f["rarity"] == r)
    tiers.append((r, pct))
for k, (r, pct) in enumerate(tiers):
    seg = circ * pct / 100
    off = -circ * acc / 100
    b = 0.08 + k * 0.08
    p.append(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="{RARITY[r]["c"]}" stroke-width="46" transform="rotate(-90 {cx} {cy})" '
             f'stroke-dasharray="0 {fmt(circ)}" stroke-dashoffset="{fmt(off)}" filter="url(#gl)">'
             f'<animate attributeName="stroke-dasharray" values="0 {fmt(circ)};0 {fmt(circ)};{fmt(max(seg-2,1.5))} {fmt(circ)};{fmt(max(seg-2,1.5))} {fmt(circ)};0 {fmt(circ)}" keyTimes="0;{b:.2f};{b+0.12:.2f};0.94;1" dur="{T}s" repeatCount="indefinite"/></circle>')
    acc += pct
p.append(f'<circle cx="{cx}" cy="{cy}" r="{R-23}" fill="#08142a"/>')
p.append(f'<g><animateTransform attributeName="transform" type="rotate" values="0 {cx} {cy};360 {cx} {cy}" dur="20s" repeatCount="indefinite"/>'
         f'<circle cx="{cx}" cy="{cy}" r="{R+34}" fill="none" stroke="#38e8ff" stroke-opacity="0.35" stroke-dasharray="2 10"/></g>')
p.append(f'<text x="{cx}" y="{cy-6}" text-anchor="middle" font-family="{BLACK}" font-size="44" fill="#e9fdff">{TOTAL_W}</text>'
         f'<text x="{cx}" y="{cy+22}" text-anchor="middle" font-family="{SANS}" font-size="13" font-weight="800" letter-spacing="3" fill="#6f8db3">TOTAL WEIGHT</text>')
for k, (r, pct) in enumerate(tiers):
    y = cy + R + 50 + (k // 3) * 26
    x = cx - 210 + (k % 3) * 150
    p.append(f'<circle cx="{x}" cy="{y-5}" r="6" fill="{RARITY[r]["c"]}"/><text x="{x+12}" y="{y}" font-family="{SANS}" font-size="13" font-weight="700" fill="#cfe1f5">{RARITY[r]["name"].title()} <tspan fill="{RARITY[r]["c"]}" font-family="{MONO}">{pct:.2f}%</tspan></text>')
p.append('</svg>')
save("drop-chart.svg", "".join(p))

# ---------------------------------------------------------------- footer
W, H = 1280, 300
rnd = random.Random(99)
p = [svg_open(W, H)]
p.append(f'''<defs><linearGradient id="w" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0f5f86"/><stop offset="1" stop-color="#020d1c"/></linearGradient>
<linearGradient id="tg" x1="0" x2="1"><stop offset="0" stop-color="#38e8ff"/><stop offset="0.5" stop-color="#ffd166"/><stop offset="1" stop-color="#ff3c5a"/>
<animateTransform attributeName="gradientTransform" type="translate" values="-0.5 0;0.5 0;-0.5 0" dur="6s" repeatCount="indefinite"/></linearGradient>
<filter id="gl" x="-20%" y="-50%" width="140%" height="200%"><feGaussianBlur stdDeviation="5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>''')
S = 150
for lay, (amp, per, col, op, dur, dy) in enumerate([(10, 260, "#0b4a6c", 0.6, 9, -14), (8, 180, "#0f6f99", 0.6, 6, -4), (6, 140, "url(#w)", 1, 4, 6)]):
    p.append(f'<g opacity="{op}"><path d="{wave_path(W+per*2, S+dy, amp, per, H)}" fill="{col}"><animateTransform attributeName="transform" type="translate" values="0,0;{-per},0" dur="{dur}s" repeatCount="indefinite"/></path></g>')
# jumping fish (marlin) arc with splash
J = 6.0
jx0, jx1 = 300, 580
p.append(f'<g opacity="0"><animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.4;0.41;1" dur="{J}s" repeatCount="indefinite"/><g>'
         f'<animateMotion path="M{jx0},{S+30} Q{(jx0+jx1)/2},{S-190} {jx1},{S+30}" keyTimes="0;0.4;1" keyPoints="0;1;1" calcMode="linear" dur="{J}s" repeatCount="indefinite" rotate="auto"/>'
         f'{fish_svg("marlin", 130, 30, FISH[8]["col"], wag_dur=0.2)}</g></g>')
for sx, b in ((jx0, 0.02), (jx1, 0.38)):
    k1 = b + 0.12
    for k in range(8):
        ang = math.radians(-165 + k * 21)
        dx, dy = math.cos(ang) * 45, math.sin(ang) * 55
        p.append(f'<circle cx="{sx}" cy="{S}" r="4" fill="#bff6ff" opacity="0">'
                 f'<animate attributeName="cx" values="{sx};{sx};{fmt(sx+dx)};{fmt(sx+dx)}" keyTimes="0;{b};{k1:.2f};1" dur="{J}s" repeatCount="indefinite"/>'
                 f'<animate attributeName="cy" values="{S};{S};{fmt(S+dy)};{S+14};{S+14}" keyTimes="0;{b};{b+0.06:.2f};{k1:.2f};1" dur="{J}s" repeatCount="indefinite"/>'
                 f'<animate attributeName="opacity" values="0;0;1;0;0" keyTimes="0;{b};{b+0.01:.2f};{k1:.2f};1" dur="{J}s" repeatCount="indefinite"/></circle>')
    p.append(f'<ellipse cx="{sx}" cy="{S+4}" rx="6" ry="2" fill="none" stroke="#bff6ff" stroke-width="2" opacity="0">'
             f'<animate attributeName="rx" values="6;6;80;80" keyTimes="0;{b};{b+0.2:.2f};1" dur="{J}s" repeatCount="indefinite"/>'
             f'<animate attributeName="ry" values="2;2;14;14" keyTimes="0;{b};{b+0.2:.2f};1" dur="{J}s" repeatCount="indefinite"/>'
             f'<animate attributeName="opacity" values="0;0;1;0;0" keyTimes="0;{b};{b+0.01:.2f};{b+0.2:.2f};1" dur="{J}s" repeatCount="indefinite"/></ellipse>')
p.append(bubbles(rnd, 26, 0, W, H, S + 10, 2, 5))
p.append(f'<text x="{W*0.68}" y="{S+80}" text-anchor="middle" font-family="{BLACK}" font-size="46" fill="url(#tg)" filter="url(#gl)" letter-spacing="2">SELAMAT MANCING!</text>'
         f'<text x="{W*0.68}" y="{S+116}" text-anchor="middle" font-family="{MONO}" font-size="16" fill="#9fd8ef">semoga Naga Laut nyangkut di kailmu  ~  0.43% itu bukan nol</text>')
p.append('</svg>')
save("footer.svg", "".join(p))
