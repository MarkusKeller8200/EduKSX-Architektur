"""Erzeugt die Modul-Steckbriefe für site/index.html.

Quellen (keine eigenen Inhalte, damit nichts auseinanderläuft):
- docs/MODULE-UEBERSICHT.md §1 (Name, Kurzbeschreibung, Personendaten) und §3 (Macht, Nicht, OFFEN)
- docs/REGISTER-MODULE.md (Betriebsart, Repo, Status)
- module_graph.EDGES (Verbindungen)
"""
import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BLOB = "https://github.com/MarkusKeller8200/EduKSX-Architektur/blob/main/docs/"
GH = "https://github.com/MarkusKeller8200/"


def zeilen(tabelle_text):
    """Zeilen einer Markdown-Tabelle als Zellenlisten (ohne Kopf und Trenner)."""
    out = []
    for z in tabelle_text.splitlines():
        if not z.startswith("|") or re.match(r"^\|\s*-", z) or re.match(r"^\|[\s|:-]+\|$", z):
            continue
        out.append([c.strip() for c in z.strip().strip("|").split("|")])
    return out


def inline(t):
    """Wenig Markdown → HTML: `code`, **fett**, [Text](Ziel)."""
    t = html.escape(t, quote=False)

    def link(m):
        text, ziel = m.group(1), m.group(2)
        if not ziel.startswith("http"):
            ziel = BLOB + ziel
        return f'<a href="{html.escape(ziel)}">{text}</a>'

    t = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", link, t)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", t)
    return t


def uebersicht():
    text = (ROOT / "docs/MODULE-UEBERSICHT.md").read_text(encoding="utf-8")
    kopf = text.split("## 1. Auf einen Blick", 1)[1].split("\n## ", 1)[0]
    module = {}
    for z in zeilen(kopf):
        if len(z) < 6 or not z[2].startswith("`"):
            continue
        key = z[2].strip("`")
        kurz = re.sub(r"\s*\(Icon [^)]*\)", "", z[3]).replace(" ()", "")
        module[key] = {"name": z[1], "kurz": kurz, "personendaten": z[4]}
    teil3 = text.split("## 3. Module und Systemgrenzen", 1)[1].split("\n## ", 1)[0]
    for block in re.split(r"^### ", teil3, flags=re.M)[1:]:
        titel, _, rumpf = block.partition("\n")
        key = titel.split(" ", 1)[0]
        felder, aktuell = {}, None
        for z in rumpf.splitlines():
            m = re.match(r"^- \*\*(Macht|Nicht|Stack|OFFEN):\*\*\s*(.*)", z)
            if m:
                aktuell = m.group(1)
                felder[aktuell] = [[m.group(2), []]]
            elif aktuell and re.match(r"^  - ", z):
                felder[aktuell][-1][1].append(z[4:])
            elif aktuell and z.startswith("    ") and felder[aktuell][-1][1]:
                felder[aktuell][-1][1][-1] += " " + z.strip()
            elif aktuell and z.startswith("  ") and z.strip():
                felder[aktuell][-1][0] += " " + z.strip()
            elif z.strip():
                aktuell = None
        module.setdefault(key, {})["titel"] = titel.split("–", 1)[-1].strip()
        module[key]["felder"] = felder
    return module


def register():
    text = (ROOT / "docs/REGISTER-MODULE.md").read_text(encoding="utf-8")
    teil = text.split("## Register", 1)[1].split("\n## ", 1)[0]
    reg = {}
    for z in zeilen(teil):
        if len(z) >= 6 and z[0].startswith("`"):
            reg[z[0].strip("`")] = {"repo": z[3], "betrieb": z[4], "status": z[5]}
    return reg


def daten():
    """Alle Module mit Steckbrief, in der Reihenfolge der Modulübersicht; `services` (reserviert) entfällt."""
    mod, reg = uebersicht(), register()
    out = []
    for key, m in mod.items():
        if key not in reg or reg[key]["status"].startswith("reserviert"):
            continue
        out.append({"key": key, **m, **reg[key]})
    return out


def _absatz(felder, name):
    if name not in felder:
        return ""
    teile = []
    for text, unter in felder[name]:
        teile.append(f"<p>{inline(text)}</p>")
        if unter:
            teile.append("<ul>" + "".join(f"<li>{inline(u)}</li>" for u in unter) + "</ul>")
    return "".join(teile)


def html_steckbriefe(icon, edges):
    namen = {}
    out = []
    for m in daten():
        key = m["key"]
        namen[key] = m["name"]
        repo = m["repo"]
        if repo and repo != "–" and repo.startswith("EduKSX-"):
            repo_html = f'<a href="{GH}{repo}">{html.escape(repo)}</a>'
        elif repo and repo != "–":
            repo_html = f"{html.escape(repo)} (privat)"
        else:
            repo_html = "noch keines"
        verb = [t for a, b, _k, t in edges if key in (a, b)]
        f = m.get("felder", {})
        badge = "ok" if m["status"].startswith("aktiv") else "plan"
        status_kurz = "✓ aktiv" if badge == "ok" else m["status"].split(" ")[0]
        teile = [
            f'<details class="sb" id="steckbrief-{key}">',
            f'<summary>{icon(key)}<span class="t"><strong>{inline(m["name"])}</strong>'
            f'<span>{inline(m["kurz"])}</span></span><span class="badge {badge}">{html.escape(status_kurz)}</span></summary>',
            '<div class="sbbody"><dl>',
            f"<dt>Schlüssel</dt><dd><code>{key}</code></dd>",
            f"<dt>Betriebsart</dt><dd>{'noch offen' if m['betrieb'] == 'offen' else inline(m['betrieb'])}</dd>",
            f"<dt>Personendaten</dt><dd>{inline(m.get('personendaten', '–'))}</dd>",
            f"<dt>Status</dt><dd>{inline(m['status'])}</dd>",
            f"<dt>Repo</dt><dd>{repo_html}</dd>",
            "</dl><div class=\"sbtext\">",
        ]
        if "Macht" in f:
            teile.append(f"<h4>Macht</h4>{_absatz(f, 'Macht')}")
        if "Nicht" in f:
            teile.append(f"<h4>Macht nicht</h4>{_absatz(f, 'Nicht')}")
        if "Stack" in f:
            teile.append(f"<h4>Stack</h4>{_absatz(f, 'Stack')}")
        if verb:
            teile.append("<h4>Verbindungen</h4><ul>" + "".join(f"<li>{html.escape(v)}</li>" for v in verb) + "</ul>")
        if "OFFEN" in f:
            teile.append(f'<h4>Offen</h4><div class="offen">{_absatz(f, "OFFEN")}</div>')
        teile.append("</div></div></details>")
        out.append("".join(teile))
    return "".join(out)


if __name__ == "__main__":
    for m in daten():
        print(m["key"], m["betrieb"], m["status"], sorted(m.get("felder", {})))
