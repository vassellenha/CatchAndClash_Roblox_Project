from common import *

W, H = 1280, 680
SURF = 300
rnd = random.Random(42)
BX = 190

p = [svg_open(W, H)]
p.append(f'''<defs>
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#02040c"/><stop offset="0.55" stop-color="#0a1633"/><stop offset="1" stop-color="#1a2f5c"/>
</linearGradient>
<linearGradient id="water" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#0f5f86"/><stop offset="0.35" stop-color="#083b5e"/><stop offset="1" stop-color="#020d1c"/>
</linearGradient>
<linearGradient id="sand" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#3a3320"/><stop offset="1" stop-color="#14110a"/>
</linearGradient>
<linearGradient id="title" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="#38e8ff"/><stop offset="0.35" stop-color="#e9fdff"/>
  <stop offset="0.65" stop-color="#ffd166"/><stop offset="1" stop-color="#ff3c5a"/>
  <animateTransform attributeName="gradientTransform" type="translate" values="-0.5 0;0.5 0;-0.5 0" dur="8s" repeatCount="indefinite"/>
</linearGradient>
<linearGradient id="ray" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#bff6ff" stop-opacity="0.35"/><stop offset="1" stop-color="#bff6ff" stop-opacity="0"/>
</linearGradient>
<radialGradient id="moonglow"><stop offset="0" stop-color="#fff6d6" stop-opacity="0.55"/><stop offset="1" stop-color="#fff6d6" stop-opacity="0"/></radialGradient>
<radialGradient id="vign" cx="0.5" cy="0.45" r="0.75"><stop offset="0.6" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity="0.65"/></radialGradient>
<filter id="glow" x="-20%" y="-50%" width="140%" height="200%"><feGaussianBlur stdDeviation="6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<filter id="soft"><feGaussianBlur stdDeviation="2.2"/></filter>
<filter id="softer"><feGaussianBlur stdDeviation="4"/></filter>
<filter id="caustic" x="0" y="0" width="100%" height="100%">
  <feTurbulence type="fractalNoise" baseFrequency="0.012 0.03" numOctaves="2" seed="3" result="n">
    <animate attributeName="baseFrequency" values="0.012 0.03;0.016 0.026;0.012 0.03" dur="12s" repeatCount="indefinite"/>
  </feTurbulence>
  <feColorMatrix in="n" type="matrix" values="0 0 0 0 0.7  0 0 0 0 0.95  0 0 0 0 1  0 0 0 9 -5"/>
</filter>
<clipPath id="uw"><rect x="0" y="{SURF}" width="{W}" height="{H-SURF}"/></clipPath>
</defs>''')

# sky
p.append(f'<rect width="{W}" height="{SURF+10}" fill="url(#sky)"/>')
p.append(stars(rnd, 110, W, H, SURF - 60))
# shooting stars
for i, (x, y, b) in enumerate([(200, 40, 1), (700, 20, 5.5), (420, 70, 9)]):
    p.append(f'<line x1="{x}" y1="{y}" x2="{x-90}" y2="{y-30}" stroke="#fff" stroke-width="2" stroke-linecap="round" opacity="0">'
             f'<animateTransform attributeName="transform" type="translate" values="0,0;380,130" dur="1.1s" begin="{b}s;sh{i}.end+{10+i*2}s" id="sh{i}" fill="freeze"/>'
             f'<animate attributeName="opacity" values="0;1;0" dur="1.1s" begin="{b}s;sh{i}.end+{10+i*2}s"/></line>')
# moon
p.append('<circle cx="1190" cy="62" r="80" fill="url(#moonglow)"><animate attributeName="r" values="70;90;70" dur="6s" repeatCount="indefinite"/></circle>'
         '<circle cx="1190" cy="62" r="30" fill="#fff4cf"/><circle cx="1180" cy="55" r="6" fill="#e8dbb0"/>'
         '<circle cx="1200" cy="72" r="7" fill="#e8dbb0"/><circle cx="1199" cy="50" r="3.5" fill="#e8dbb0"/>')
# far hills + trees
hill = f"M0,{SURF} " + " ".join(f"L{x},{SURF-28-18*math.sin(x/120)-10*math.sin(x/37)}" for x in range(0, W + 20, 20)) + f" L{W},{SURF}Z"
p.append(f'<path d="{hill}" fill="#071531"/>')
trees = []
x = -10
while x < W + 20:
    h = rnd.uniform(25, 70)
    w = rnd.uniform(14, 26)
    base = SURF - 10
    trees.append(f"M{fmt(x)},{base} L{fmt(x+w/2)},{fmt(base-h)} L{fmt(x+w)},{base}Z")
    x += rnd.uniform(9, 22)
p.append(f'<path d="{" ".join(trees)}" fill="#030a18"/>')
p.append(f'<rect x="0" y="{SURF-12}" width="{W}" height="14" fill="#030a18"/>')
# fireflies
for _ in range(16):
    fx, fy = rnd.uniform(0, W), rnd.uniform(SURF - 80, SURF - 15)
    d = rnd.uniform(3, 7)
    p.append(f'<circle cx="{fmt(fx)}" cy="{fmt(fy)}" r="2" fill="#e6ff8a" filter="url(#soft)">'
             f'<animate attributeName="opacity" values="0;1;0" dur="{d:.1f}s" begin="-{rnd.uniform(0,7):.1f}s" repeatCount="indefinite"/>'
             f'<animateTransform attributeName="transform" type="translate" values="0,0;{rnd.uniform(-20,20):.0f},{rnd.uniform(-15,5):.0f};0,0" dur="{d*2:.1f}s" repeatCount="indefinite"/></circle>')

# water body
p.append(f'<rect x="0" y="{SURF}" width="{W}" height="{H-SURF}" fill="url(#water)"/>')
p.append(f'<g clip-path="url(#uw)">')
p.append(f'<rect x="0" y="{SURF}" width="{W}" height="{H-SURF}" filter="url(#caustic)" opacity="0.22"/>')
# light rays
for i in range(9):
    x = 80 + i * 145 + rnd.uniform(-30, 30)
    w = rnd.uniform(40, 90)
    d = rnd.uniform(5, 9)
    p.append(f'<polygon points="{fmt(x)},{SURF} {fmt(x+w)},{SURF} {fmt(x+w*2.6-80)},{H} {fmt(x-w*0.8-80)},{H}" fill="url(#ray)">'
             f'<animate attributeName="opacity" values="0.15;0.75;0.15" dur="{d:.1f}s" begin="-{rnd.uniform(0,9):.1f}s" repeatCount="indefinite"/></polygon>')
# moon reflection
for i in range(7):
    p.append(f'<ellipse cx="1190" cy="{SURF+8+i*11}" rx="{60-i*7}" ry="2.5" fill="#fff4cf" opacity="0.5">'
             f'<animate attributeName="rx" values="{60-i*7};{40-i*4};{60-i*7}" dur="{2+i*0.3:.1f}s" repeatCount="indefinite"/></ellipse>')

# deep dragon silhouette
p.append(f'<g opacity="0.28" filter="url(#softer)"><g>'
         f'<animateMotion path="M1500,{H-90} C1100,{H-140} 700,{H-40} 300,{H-110} S-200,{H-80} -400,{H-100}" dur="38s" repeatCount="indefinite"/>'
         f'<g transform="scale(-1,1)">{dragon_svg(380, 90)}</g></g></g>')

# swimming fish
swimmers = [("lele", 300, 0.9, 1, 22), ("nila", 360, 0.8, -1, 18), ("kakap", 420, 1.0, 1, 16), ("gurame", 470, 1.1, -1, 24),
            ("tuna", 520, 1.25, 1, 13), ("mujair", 560, 0.75, 1, 20), ("kerapu", 600, 1.0, -1, 26), ("hiu", 405, 1.5, -1, 21),
            ("marlin", 455, 1.5, 1, 15), ("nila", 590, 0.6, 1, 17), ("lele", 380, 0.6, -1, 25), ("mujair", 500, 0.6, -1, 19)]
FB = {f["id"]: f for f in FISH}
for i, (fid, y, sc, dirn, dur) in enumerate(swimmers):
    f = FB[fid]
    L, Hh = 90 * sc, 38 * sc
    if fid == "marlin":
        L, Hh = 150, 36
    if fid == "hiu":
        L, Hh = 150, 42
    y = y + 10
    begin = -rnd.uniform(0, dur)
    if dirn == 1:
        path = f"M-200,{y} C200,{y-40} 500,{y+40} 800,{y-20} S1200,{y+30} 1500,{y}"
    else:
        path = f"M1500,{y} C1100,{y+40} 800,{y-40} 500,{y+20} S100,{y-30} -200,{y}"
    flip = "" if dirn == 1 else ' transform="scale(-1,1)"'
    op = 0.55 + 0.45 * min(1, sc)
    p.append(f'<g opacity="{op:.2f}"><g><animateMotion path="{path}" dur="{dur}s" begin="{begin:.1f}s" repeatCount="indefinite" rotate="auto"/>'
             f'<g{(" transform=" + chr(34) + "scale(1,-1)" + chr(34)) if dirn == -1 else ""}>{fish_svg(f["kind"], L, Hh, f["col"], wag_dur=0.35 + rnd.uniform(0, 0.3))}</g></g></g>')

p.append(seaweed(rnd, 26, 0, W, H - 30, 60, 150))
# sand floor
floor = f"M0,{H-40} " + " ".join(f"Q{x+40},{H-55-rnd.uniform(0,14):.0f} {x+80},{H-42}" for x in range(0, W, 80)) + f" V{H} H0Z"
p.append(f'<path d="{floor}" fill="url(#sand)"/>')
for _ in range(40):
    p.append(f'<ellipse cx="{rnd.uniform(0,W):.0f}" cy="{rnd.uniform(H-34,H-6):.0f}" rx="{rnd.uniform(3,9):.1f}" ry="{rnd.uniform(2,4):.1f}" fill="#5a4e33" opacity="0.7"/>')
p.append(bubbles(rnd, 45, 0, W, H - 40, SURF + 4))

# fishing line + hook
p.append(f'<path d="M{BX},{SURF} Q{BX+4},{SURF+80} {BX+2},{SURF+150}" stroke="#e8f8ff" stroke-width="1" opacity="0.55" fill="none"/>'
         f'<g><animateTransform attributeName="transform" type="translate" values="0,0;3,2;0,0;-3,1;0,0" dur="3s" repeatCount="indefinite"/>'
         f'<path d="M{BX+2},{SURF+150} v14 a7,7 0 1 1 -12,-4" stroke="#cfd8dc" stroke-width="2.4" fill="none"/>'
         f'<ellipse cx="{BX-4}" cy="{SURF+160}" rx="7" ry="4" fill="#ff7aa0"><animate attributeName="ry" values="4;5;4" dur="0.6s" repeatCount="indefinite"/></ellipse></g>')
p.append('</g>')  # end underwater clip

# surface waves (two layers)
for lay, (amp, per, col, op, dur, dy) in enumerate([(7, 180, "#2a90b8", 0.55, 7, -2), (5, 120, "#58c7e6", 0.45, 4.5, 2)]):
    p.append(f'<g opacity="{op}"><path d="{wave_path(W+per*2, SURF+dy, amp, per, SURF+18)}" fill="{col}">'
             f'<animateTransform attributeName="transform" type="translate" values="0,0;{-per},0" dur="{dur}s" repeatCount="indefinite"/></path></g>')
p.append(f'<g><path d="{wave_path(W+200, SURF, 3, 100, SURF+3)}" fill="none" stroke="#bff6ff" stroke-width="1.6" opacity="0.7">'
         f'<animateTransform attributeName="transform" type="translate" values="0,0;-100,0" dur="3s" repeatCount="indefinite"/></path></g>')

# rod (from left) and line to bobber
p.append(f'<path d="M-20,{SURF-20} Q20,{SURF-140} {BX-80},{SURF-120}" stroke="#2a1d14" stroke-width="7" fill="none" stroke-linecap="round"/>'
         f'<path d="M40,{SURF-95} Q70,{SURF-130} {BX-80},{SURF-120}" stroke="#6b4a2e" stroke-width="3.5" fill="none" stroke-linecap="round"/>'
         f'<circle cx="22" cy="{SURF-62}" r="13" fill="#34383d" stroke="#8a9399" stroke-width="2"><animateTransform attributeName="transform" type="rotate" values="0 22 {SURF-62};360 22 {SURF-62}" dur="4s" repeatCount="indefinite"/></circle>'
         f'<line x1="22" y1="{SURF-75}" x2="22" y2="{SURF-62}" stroke="#cfd8dc" stroke-width="2"><animateTransform attributeName="transform" type="rotate" values="0 22 {SURF-62};360 22 {SURF-62}" dur="4s" repeatCount="indefinite"/></line>')
# bobber with bite cycle (period 8s; bite at 70-82%)
KT = "0;0.15;0.3;0.45;0.6;0.7;0.72;0.75;0.78;0.82;0.9;1"
BV = "0,0;0,-3;0,0;0,-3;0,0;0,-2;0,12;0,4;0,14;0,0;0,-3;0,0"
p.append(f'<path d="M{BX-80},{SURF-120} Q{BX-50},{SURF-60} {BX},{SURF-6}" stroke="#e8f8ff" stroke-width="1.2" fill="none" opacity="0.8">'
         f'<animate attributeName="d" keyTimes="0;0.72;0.75;0.78;0.82;1" values="M{BX-80},{SURF-120} Q{BX-50},{SURF-60} {BX},{SURF-6};M{BX-80},{SURF-120} Q{BX-50},{SURF-60} {BX},{SURF-6};M{BX-80},{SURF-120} Q{BX-40},{SURF-80} {BX},{SURF+8};M{BX-80},{SURF-120} Q{BX-40},{SURF-80} {BX},{SURF+6};M{BX-80},{SURF-120} Q{BX-50},{SURF-60} {BX},{SURF-6};M{BX-80},{SURF-120} Q{BX-50},{SURF-60} {BX},{SURF-6}" dur="8s" repeatCount="indefinite"/></path>')
for k in range(3):
    p.append(f'<ellipse cx="{BX}" cy="{SURF+2}" rx="10" ry="3" fill="none" stroke="#bff6ff" stroke-width="1.5">'
             f'<animate attributeName="rx" values="10;70" dur="2.4s" begin="{k*0.8}s" repeatCount="indefinite"/>'
             f'<animate attributeName="ry" values="3;12" dur="2.4s" begin="{k*0.8}s" repeatCount="indefinite"/>'
             f'<animate attributeName="opacity" values="0.8;0" dur="2.4s" begin="{k*0.8}s" repeatCount="indefinite"/></ellipse>')
p.append(f'<g><animateTransform attributeName="transform" type="translate" keyTimes="{KT}" values="{BV}" dur="8s" repeatCount="indefinite"/>'
         f'<line x1="{BX}" y1="{SURF-24}" x2="{BX}" y2="{SURF-12}" stroke="#ddd" stroke-width="2"/>'
         f'<circle cx="{BX}" cy="{SURF-4}" r="9" fill="#ff3c5a"/><path d="M{BX-9},{SURF-4} a9,9 0 0 0 18,0Z" fill="#f4f4f4"/>'
         f'<circle cx="{BX-3}" cy="{SURF-8}" r="2.5" fill="#fff" opacity="0.8"/></g>')
# BITE popup
p.append(f'<g opacity="0"><animate attributeName="opacity" keyTimes="0;0.7;0.72;0.86;0.9;1" values="0;0;1;1;0;0" dur="8s" repeatCount="indefinite"/>'
         f'<g><animateTransform attributeName="transform" type="translate" keyTimes="0;0.72;0.75;0.78;1" values="0,0;0,0;0,-10;0,0;0,0" dur="8s" repeatCount="indefinite"/>'
         f'<rect x="{BX+14}" y="{SURF-86}" width="110" height="44" rx="12" fill="#ffd166" stroke="#fff" stroke-width="3"/>'
         f'<path d="M{BX+22},{SURF-44} l-8,16 l22,-16Z" fill="#ffd166"/>'
         f'<text x="{BX+69}" y="{SURF-56}" font-family="{BLACK}" font-size="24" font-weight="900" fill="#3a1500" text-anchor="middle">STRIKE!</text></g></g>')

# Title
p.append(f'<g filter="url(#glow)"><animateTransform attributeName="transform" type="translate" values="0,0;0,-6;0,0" dur="5s" repeatCount="indefinite"/>'
         f'<text x="{W/2+40}" y="150" font-family="{BLACK}" font-size="104" font-weight="900" text-anchor="middle" fill="url(#title)" letter-spacing="4" '
         f'stroke="#03111f" stroke-width="2" paint-order="stroke">CATCH <tspan fill="#ffd166">&amp;</tspan> CLASH</text></g>')
p.append(f'<text x="{W/2+40}" y="196" font-family="{SANS}" font-size="20" font-weight="700" text-anchor="middle" fill="#bfe9ff" letter-spacing="9" opacity="0.9">'
         f'ROBLOX  ·  FISHING  ·  LUAU  ·  ROJO</text>')
p.append(f'<g font-family="{SANS}" font-size="15" font-weight="700" text-anchor="middle">')
xs = W / 2 + 40 - 2 * 150
for i, r in enumerate(ORDER):
    x = xs + i * 150
    rr = RARITY[r]
    p.append(f'<g><animateTransform attributeName="transform" type="translate" values="0,0;0,-4;0,0" dur="2s" begin="{i*0.25}s" repeatCount="indefinite"/>'
             f'<rect x="{x-62}" y="214" width="124" height="28" rx="14" fill="{rr["c"]}" fill-opacity="0.18" stroke="{rr["c"]}" stroke-width="1.6"/>'
             f'<text x="{x}" y="233" fill="{rr["c"]}" letter-spacing="2">{rr["name"]}</text></g>')
p.append('</g>')
p.append(f'<rect width="{W}" height="{H}" fill="url(#vign)" pointer-events="none"/>')
p.append('</svg>')
save("hero.svg", "".join(p))
