"""Prüfungen der Dokumente (Prüfbefehl: python3 -m unittest discover -s tests).

- Verweise auf Dateien im Repository zeigen auf vorhandene Dateien.
- Keine Geheimnisse oder Zugangsdaten in den Dokumenten (Nichtziel).
- Konzepte, Vorlagen und Prüfaufträge aus Meilenstein 0.2.0 sind vorhanden.
"""

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = [p for p in ROOT.rglob("*.md") if ".git" not in p.parts]

LINK = re.compile(r"\]\(([^)#\s]+)(?:#[^)]*)?\)|<img src=\"([^\"]+)\"")
SECRET = re.compile(
    r"(-----BEGIN [A-Z ]*PRIVATE KEY-----|gls_[A-Za-z0-9]{40}|ghp_[A-Za-z0-9]{36}|"
    r"(?i:password|passwort|secret)\s*[:=]\s*['\"]?[^\s'\"…]{8,})"
)


class Dokumente(unittest.TestCase):
    def test_relative_verweise_existieren(self) -> None:
        fehlend = []
        for doc in DOCS:
            for treffer in LINK.findall(doc.read_text(encoding="utf-8")):
                ziel = treffer[0] or treffer[1]
                if re.match(r"^[a-z]+:", ziel):
                    continue
                if not (doc.parent / ziel).resolve().exists():
                    fehlend.append(f"{doc.relative_to(ROOT)} → {ziel}")
        self.assertEqual([], fehlend, "Verweise ohne Ziel")

    def test_pflichtdokumente_vorhanden(self) -> None:
        pflicht = [
            "docs/KONZEPT-CORE.md", "docs/KONZEPT-IDENT.md", "docs/KONZEPT-MODULVORLAGE.md",
            "docs/vorlagen/DATENSCHUTZ-VERZEICHNIS.md", "docs/vorlagen/DATENSCHUTZ-FOLGENABSCHAETZUNG.md",
            "docs/PRUEFAUFTRAG-RLS.md", "docs/PRUEFAUFTRAG-DPOP-MTLS.md", "spec/README.md", "docs/MODULE-UEBERSICHT.md",
            "docs/KONZEPT-LEITSTAND.md", "docs/KONZEPT-SELBSTHOSTING.md", "docs/KONZEPT-PLUGINS.md",
            "docs/KONZEPT-STACK.md", "docs/KONZEPT-DATENSCHUTZ-ZH.md", "docs/vorlagen/AUFTRAGSBEARBEITUNG-ZH.md",
        ]
        self.assertEqual([], [d for d in pflicht if not (ROOT / d).is_file()], "Dokumente fehlen")

    def test_keine_geheimnisse(self) -> None:
        treffer = []
        for doc in DOCS:
            for nr, zeile in enumerate(doc.read_text(encoding="utf-8").splitlines(), 1):
                if SECRET.search(zeile):
                    treffer.append(f"{doc.relative_to(ROOT)}:{nr}")
        self.assertEqual([], treffer, "Mögliche Geheimnisse in Dokumenten")


if __name__ == "__main__":
    unittest.main()
