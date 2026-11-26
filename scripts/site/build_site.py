"""Baut site/index.html aus scripts/site/index.template.html: Tokens (EduKSX-UI tokens.json) als CSS-Variablen, Icons inline.

Aufruf: python3 scripts/site/build_site.py ../EduKSX-UI scripts/site/index.template.html site/index.html <EduKSX-UI-Commit>
"""
import json
import re
import sys
from pathlib import Path

UI = Path(sys.argv[1])          # EduKSX-UI
VORLAGE = Path(sys.argv[2])     # index.template.html
ZIEL = Path(sys.argv[3])        # site/index.html
UI_STAND = sys.argv[4]

tokens = json.loads((UI / "tokens/tokens.json").read_text(encoding="utf-8"))
hell, dunkel = [], []
for name, t in tokens["color"].items():
    if not isinstance(t, dict) or "$value" not in t:
        continue
    hell.append(f"--{name}:{t['$value']};")
    d = t.get("$extensions", {}).get("ch.eduksx", {}).get("dark")
    if d:
        dunkel.append(f"--{name}:{d};")
css = (
    ":root{" + "".join(hell) + "}"
    ":root[data-theme=dark]{" + "".join(dunkel) + "}"
    "@media (prefers-color-scheme:dark){:root:not([data-theme=light]){" + "".join(dunkel) + "}}"
)


def icon(key: str) -> str:
    svg = (UI / f"icons/svg/eduksx-{key}.svg").read_text(encoding="utf-8")
    svg = re.sub(r"<title>.*?</title>\s*", "", svg, flags=re.S)
    svg = svg.replace('role="img"', 'aria-hidden="true" focusable="false" class="ico"')
    return re.sub(r">\s+<", "><", svg.strip())


def gicon(key, x, y, size):
    s = icon(key).replace('class="ico"', f'class="gi" x="{x:.0f}" y="{y:.0f}" width="{size}" height="{size}"', 1)
    return s


sys.path.insert(0, str(Path(__file__).parent))
import module_graph  # noqa: E402
import steckbriefe  # noqa: E402

html = VORLAGE.read_text(encoding="utf-8")
html = html.replace("{{graph}}", module_graph.svg(gicon)).replace("{{graphlist}}", module_graph.liste())
html = html.replace("{{steckbriefe}}", steckbriefe.html_steckbriefe(icon, module_graph.EDGES))
html = re.sub(r'(<div class="mod">\{\{icon:([a-z]+)\}\}<div><h3>)([^<]+?) <span',
              r'\1<a class="sbl" href="#steckbrief-\2">\3</a> <span', html)
html = html.replace("/*TOKENS*/", css).replace("{{UI_STAND}}", UI_STAND)
html = re.sub(r"\{\{icon:([a-z]+)\}\}", lambda m: icon(m.group(1)), html)
ZIEL.write_text(html, encoding="utf-8")
print("geschrieben:", ZIEL, len(html), "Zeichen")
