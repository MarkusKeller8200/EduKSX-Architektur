"""Erzeugt die SVG-Grafik «Wie die Module zusammenarbeiten» (Quelle: docs/MODULE-UEBERSICHT.md §2–4)."""
import math

W, H = 1130, 700
NW, NH = 166, 52

# key: (x, y, Name, Untertitel, Art)  Art: modul | hub | extern
NODES = {
    "intranet": (300, 60, "Intranet", "Zugang intern", "modul"),
    "portal": (820, 60, "Portal", "Zugang extern", "modul"),
    "glossary": (100, 190, "Glossary", "Begriffe", "modul"),
    "codex": (100, 350, "Codex", "Rechtssammlung", "modul"),
    "sign": (300, 270, "Sign", "Unterschriften", "modul"),
    "flow": (560, 230, "Flow", "Abläufe, Termine", "modul"),
    "planner": (560, 335, "Planner", "Jahresplanung", "modul"),
    "shop": (1035, 190, "Shop", "Bestellungen", "modul"),
    "licence": (1035, 300, "Licence", "Lizenzen, Zugänge", "modul"),
    "timetable": (1035, 410, "Timetable", "Stundenplan", "modul"),
    "staffing": (1035, 520, "Staffing", "Einsatzplanung", "modul"),
    "connect": (820, 440, "Connect", "Stammdaten, Sync", "hub"),
    "extern": (560, 440, "Fremdsysteme", "M365, ASM, Escola, CMI …", "extern"),
    "time": (560, 540, "Time", "Zeiterfassung", "modul"),
    "ops": (100, 480, "Ops", "Leitstand", "modul"),
}
# (von, nach, Art, Text für die Liste)  Art: daten | dienst | plugin | offen
EDGES = [
    ("connect", "licence", "daten", "Connect liefert Personen und Klassen an Licence"),
    ("connect", "timetable", "daten", "Connect liefert Personen und Klassen an Timetable"),
    ("connect", "staffing", "daten", "Connect liefert Personen an Staffing"),
    ("connect", "portal", "daten", "Connect liefert Personen an Portal"),
    ("connect", "extern", "daten", "Connect gleicht IDs und Stammdaten mit Fremdsystemen ab (M365/Entra, Google, Apple School Manager, Escola, CMI, LMVZ, MDM)"),
    ("connect", "ident", "daten", "Connect versorgt Ident als Zielsystem mit Konten"),
    ("shop", "licence", "dienst", "Shop übergibt gekaufte Lizenzen an Licence zur Zuweisung"),
    ("intranet", "sign", "dienst", "Intranet nutzt Sign für Unterschriften"),
    ("portal", "sign", "dienst", "Portal nutzt Sign für Unterschriften"),
    ("codex", "sign", "dienst", "Codex nutzt Sign für Unterschriften"),
    ("intranet", "glossary", "plugin", "Intranet bindet Glossary als Plugin ein"),
    ("intranet", "codex", "plugin", "Intranet bindet Codex als Plugin ein"),
    ("planner", "flow", "offen", "Planner und Flow: Abgrenzung des Jahreskalenders offen"),
    ("timetable", "staffing", "offen", "Timetable und Staffing: Stellvertretungen offen"),
]
FARBE = {"daten": "var(--brand-orange)", "dienst": "var(--brand-blue)", "plugin": "var(--brand-violet)",
         "offen": "var(--muted-foreground)"}
BANDS = [("ident", 590, "Ident", "Anmeldung für alle Module – optional, lokales Login ist Standard"),
         ("core", 645, "eduksx/core", "gemeinsame Bausteine in jedem Modul")]
BAND_X, BAND_W, BAND_H = 17, 1096, 42


def rand(cx, cy, w, h, tx, ty):
    """Punkt auf dem Rand des Rechtecks (cx, cy, w, h) in Richtung (tx, ty)."""
    dx, dy = tx - cx, ty - cy
    if dx == 0 and dy == 0:
        return cx, cy
    s = min((w / 2) / abs(dx) if dx else math.inf, (h / 2) / abs(dy) if dy else math.inf)
    return cx + dx * s, cy + dy * s


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;")


def svg(icon):
    out = [f'<svg class="graph" viewBox="0 0 {W} {H}" role="img" aria-labelledby="g-titel g-desc">',
           '<title id="g-titel">Wie die EduKSX-Module zusammenarbeiten</title>',
           '<desc id="g-desc">Connect liefert Stammdaten an Licence, Timetable, Staffing, Portal und Ident und gleicht sie mit '
           'Fremdsystemen ab. Shop übergibt Lizenzen an Licence. Intranet, Portal und Codex nutzen Sign. Intranet bindet '
           'Glossary und Codex als Plugins ein. Alle Module nutzen Core und optional Ident. Die Liste unter der Grafik '
           'nennt alle Verbindungen.</desc>', '<defs>']
    for art, f in FARBE.items():
        out.append(f'<marker id="m-{art}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
                   f'orient="auto-start-reverse"><path d="M0 0 10 5 0 10z" fill="{f}"/></marker>')
    out.append("</defs>")
    for key, y, name, sub in BANDS:
        out.append(f'<g class="node band" data-k="{key}"><rect x="{BAND_X}" y="{y}" width="{BAND_W}" height="{BAND_H}" rx="10"/>'
                   f'{icon(key, BAND_X + 14, y + 9, 24)}<text x="{BAND_X + 50}" y="{y + 26}"><tspan class="t">{name}</tspan>'
                   f'<tspan class="s" dx="10">{esc(sub)}</tspan></text></g>')
    for a, b, art, _ in EDGES:
        ax, ay = NODES[a][:2]
        if b in ("ident",):
            bx, by = ax, BANDS[0][1]
            x1, y1 = rand(ax, ay, NW + 14, NH + 12, bx, by)
            x2, y2 = bx, by
        else:
            bx, by = NODES[b][:2]
            wa = NW + 14 if NODES[a][4] == "hub" else NW
            ha = NH + 12 if NODES[a][4] == "hub" else NH
            wb = NW + 14 if NODES[b][4] == "hub" else (210 if NODES[b][4] == "extern" else NW)
            x1, y1 = rand(ax, ay, wa + 8, ha + 8, bx, by)
            x2, y2 = rand(bx, by, wb + 8, NH + 8, ax, ay)
        dash = ' stroke-dasharray="6 5"' if art == "offen" else ""
        start = f' marker-start="url(#m-{art})"' if art == "offen" else ""
        out.append(f'<line class="edge {art}" data-a="{a}" data-b="{b}" x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" '
                   f'stroke="{FARBE[art]}"{dash}{start} marker-end="url(#m-{art})"/>')
    for key, (cx, cy, name, sub, art) in NODES.items():
        w = NW + 14 if art == "hub" else (210 if art == "extern" else NW)
        h = NH + 12 if art == "hub" else NH
        x, y = cx - w / 2, cy - h / 2
        ico = "" if art == "extern" else icon(key, x + 12, cy - 12, 24)
        tx = x + 14 if art == "extern" else x + 46
        out.append(f'<g class="node {art}" data-k="{key}" tabindex="0" role="button" aria-label="{name}: Verbindungen hervorheben">'
                   f'<rect x="{x:.0f}" y="{y:.0f}" width="{w}" height="{h}" rx="10"/>{ico}'
                   f'<text x="{tx:.0f}" y="{cy - 3:.0f}" class="t">{name}</text>'
                   f'<text x="{tx:.0f}" y="{cy + 14:.0f}" class="s">{esc(sub)}</text></g>')
    out.append("</svg>")
    return "".join(out)


def liste():
    gruppen = {"daten": "Stammdaten", "dienst": "Dienst über API", "plugin": "Plugin", "offen": "Abgrenzung offen"}
    li = []
    for art, titel in gruppen.items():
        punkte = "".join(f"<li>{esc(t)}</li>" for a, b, k, t in EDGES if k == art)
        li.append(f'<div><h3><i class="ln {art}"></i>{titel}</h3><ul>{punkte}</ul></div>')
    return "".join(li)
