"""Prüfungen der Schnittstellen-Schemas unter spec/ (#3).

- Jedes JSON Schema ist gültig nach Draft 2020-12 und hat eine $id unter https://docs.eduksx.ch/spec/v<n>/.
- Jede OpenAPI-Beschreibung ist OpenAPI 3.1 mit eindeutigen operationId; ihre Schemas sind gültige JSON Schemas.
- Zu jedem Schema gibt es mindestens ein gültiges und ein ungültiges Beispiel; beide werden geprüft.

Benötigt das Paket «jsonschema» (requirements-pruefung.txt).
"""

import json
import re
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012

ROOT = Path(__file__).resolve().parent.parent
SPEC = ROOT / "spec"
VERSIONS = sorted(p for p in SPEC.glob("v*") if p.is_dir())
FORMATS = FormatChecker()


def laden(pfad: Path):
    return json.loads(pfad.read_text(encoding="utf-8"))


def beispiele(ordner: Path, art: str) -> list[Path]:
    return sorted((ordner / art).glob("*.json"))


class Schemas(unittest.TestCase):
    def test_versionen_vorhanden(self) -> None:
        self.assertTrue(VERSIONS, "spec/v1 fehlt")
        for v in VERSIONS:
            self.assertRegex(v.name, r"^v[1-9][0-9]*$")

    def test_json_schemas_gueltig_und_mit_beispielen(self) -> None:
        for v in VERSIONS:
            for datei in sorted(v.glob("*.schema.json")):
                name = datei.name.removesuffix(".schema.json")
                with self.subTest(schema=f"{v.name}/{datei.name}"):
                    schema = laden(datei)
                    Draft202012Validator.check_schema(schema)
                    self.assertEqual(
                        f"https://docs.eduksx.ch/spec/{v.name}/{datei.name}", schema.get("$id"), "$id passt nicht"
                    )
                    validator = Draft202012Validator(schema, format_checker=FORMATS)
                    self._pruefe_beispiele(validator, v / "examples" / name)

    def test_openapi_gueltig_und_mit_beispielen(self) -> None:
        for v in VERSIONS:
            for datei in sorted(v.glob("*.openapi.json")):
                name = datei.name.removesuffix(".openapi.json")
                with self.subTest(openapi=f"{v.name}/{datei.name}"):
                    doc = laden(datei)
                    self.assertRegex(doc.get("openapi", ""), r"^3\.1\.\d+$")
                    for feld in ("title", "version", "license", "x-eduksx-module", "x-eduksx-api-standard"):
                        self.assertIn(feld, doc.get("info", {}), f"info.{feld} fehlt")
                    self._pruefe_operationen(doc)
                    schemas = doc.get("components", {}).get("schemas", {})
                    for sname, s in schemas.items():
                        Draft202012Validator.check_schema(s)
                    uri = f"https://docs.eduksx.ch/spec/{v.name}/{datei.name}"
                    registry = Registry().with_resource(uri, Resource.from_contents(doc, DRAFT202012))
                    ordner = v / "examples" / name
                    self.assertTrue(ordner.is_dir(), f"Beispiele fehlen: {ordner.relative_to(ROOT)}")
                    for sname in sorted(p.name for p in ordner.iterdir() if p.is_dir()):
                        self.assertIn(sname, schemas, f"Beispiele für unbekanntes Schema {sname}")
                        validator = Draft202012Validator(
                            {"$ref": f"{uri}#/components/schemas/{sname}"}, registry=registry, format_checker=FORMATS
                        )
                        self._pruefe_beispiele(validator, ordner / sname)
                    # Beispiele in der Beschreibung selbst
                    for pfad, op in self._operationen(doc):
                        body = op.get("requestBody", {}).get("content", {}).get("application/json", {})
                        if "example" in body:
                            ref = body["schema"]["$ref"]
                            Draft202012Validator(
                                {"$ref": f"{uri}{ref}"}, registry=registry, format_checker=FORMATS
                            ).validate(body["example"])

    def test_keine_echten_adressen_in_beispielen(self) -> None:
        erlaubt = re.compile(r"@[a-z0-9.-]+\.example\b")
        for datei in SPEC.rglob("*.json"):
            for treffer in re.findall(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+", datei.read_text(encoding="utf-8")):
                with self.subTest(datei=str(datei.relative_to(ROOT)), adresse=treffer):
                    self.assertRegex(treffer, erlaubt, "nur erfundene Adressen unter .example")

    # Hilfen

    def _pruefe_beispiele(self, validator: Draft202012Validator, ordner: Path) -> None:
        gueltig, ungueltig = beispiele(ordner, "valid"), beispiele(ordner, "invalid")
        rel = ordner.relative_to(ROOT)
        self.assertTrue(gueltig, f"kein gültiges Beispiel in {rel}/valid")
        self.assertTrue(ungueltig, f"kein ungültiges Beispiel in {rel}/invalid")
        for b in gueltig:
            fehler = [e.message for e in validator.iter_errors(laden(b))]
            self.assertEqual([], fehler, f"{b.relative_to(ROOT)} sollte gültig sein")
        for b in ungueltig:
            self.assertFalse(validator.is_valid(laden(b)), f"{b.relative_to(ROOT)} sollte ungültig sein")

    @staticmethod
    def _operationen(doc: dict):
        for pfad, eintrag in doc.get("paths", {}).items():
            for methode, op in eintrag.items():
                if methode in {"get", "put", "post", "delete", "patch", "head", "options", "trace"}:
                    yield pfad, op

    def _pruefe_operationen(self, doc: dict) -> None:
        ids = []
        for pfad, op in self._operationen(doc):
            self.assertTrue(pfad.startswith("/api/v"), f"Pfad ohne Version: {pfad}")
            self.assertRegex(op.get("operationId", ""), r"^[a-z][a-zA-Z0-9]+$", f"operationId in {pfad}")
            self.assertIn("security", op, f"security fehlt in {pfad}")
            ids.append(op["operationId"])
        self.assertTrue(ids, "keine Operationen")
        self.assertEqual(len(ids), len(set(ids)), "operationId doppelt")


if __name__ == "__main__":
    unittest.main()
