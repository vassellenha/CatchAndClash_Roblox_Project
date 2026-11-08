"""Regenerate every animated SVG + the STL in assets/readme, then rebuild README.md.

    python tools/readme-gen/build.py
"""
import os, sys, runpy

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..")
os.chdir(HERE)
sys.path.insert(0, HERE)
for name in ("hero", "assets2", "assets3", "assets4", "assets5", "stl"):
    runpy.run_path(os.path.join(HERE, name + ".py"), run_name="__main__")

tpl = open(os.path.join(HERE, "README.template.md"), encoding="utf-8").read()
tpl = tpl.replace("&logo=shield&logoColor=black", "").replace("&logo=blender&logoColor=black", "").replace("&logo=rust&logoColor=white", "")
stl = open(os.path.join(ROOT, "assets", "readme", "fishing-rod.stl"), encoding="utf-8").read().strip()
open(os.path.join(ROOT, "README.md"), "w", encoding="utf-8").write(tpl.replace("%%STL%%", stl))
print("README.md rebuilt")
