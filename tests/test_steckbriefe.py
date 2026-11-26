"""Modul-Steckbriefe der Übersichtsseite (scripts/site/steckbriefe.py).

- Jedes Modul aus dem Register (ausser «reserviert») hat einen Steckbrief mit «Macht» und «Nicht».
- Die gebaute Seite site/index.html enthält für jedes dieser Module einen Steckbrief.
"""

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts/site"))

import steckbriefe  # noqa: E402


class Steckbriefe(unittest.TestCase):
    def test_jedes_modul_hat_steckbrief(self) -> None:
        reg = {k for k, v in steckbriefe.register().items() if not v["status"].startswith("reserviert")}
        daten = {m["key"]: m for m in steckbriefe.daten()}
        self.assertEqual(reg, set(daten), "Register und Modulübersicht passen nicht zusammen")
        for key, m in daten.items():
            felder = m.get("felder", {})
            self.assertIn("Macht", felder, f"{key}: «Macht» fehlt in MODULE-UEBERSICHT §3")
            self.assertIn("Nicht", felder, f"{key}: «Nicht» fehlt in MODULE-UEBERSICHT §3")

    def test_seite_enthaelt_steckbriefe(self) -> None:
        seite = (ROOT / "site/index.html").read_text(encoding="utf-8")
        for m in steckbriefe.daten():
            self.assertIn(f'id="steckbrief-{m["key"]}"', seite, f"Steckbrief {m['key']} fehlt – Seite neu bauen")


if __name__ == "__main__":
    unittest.main()
