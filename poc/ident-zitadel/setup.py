#!/usr/bin/env python3
"""PoC Ident (EduKSX-Architektur #25): Mandanten, Rollen und Clients in Zitadel per API anlegen.

Nur erfundene Testdaten. Schreibt die erzeugten IDs und Zugangsdaten nach state.json (nicht ins Repository).
Aufruf: python3 setup.py   (Zitadel läuft unter http://localhost:8080, Admin-Token in pat/admin.pat)
"""

import json
import pathlib
import sys

import requests

BASE = "http://localhost:8080"
ROOT = pathlib.Path(__file__).parent
TOKEN = (ROOT / "pat" / "admin.pat").read_text().strip()
S = requests.Session()
S.trust_env = False  # localhost nicht über den Proxy
S.headers.update({"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"})


def call(method: str, path: str, body: dict | None = None, org: str | None = None) -> dict:
    headers = {"x-zitadel-orgid": org} if org else {}
    r = S.request(method, BASE + path, json=body, headers=headers)
    if r.status_code >= 300:
        sys.exit(f"{method} {path} → {r.status_code}: {r.text}")
    return r.json() if r.text else {}


state: dict = {}
me = call("GET", "/auth/v1/users/me")
platform_org = me["user"]["details"]["resourceOwner"]
state["platform_org"] = platform_org

# 1 Mandanten: Organisationen je Schule bzw. Schulgemeinde (erfunden)
orgs = {}
for key, name in [("musterhausen", "Sekundarschule Musterhausen"), ("beispielthal", "Schulgemeinde Beispielthal")]:
    orgs[key] = call("POST", "/v2/organizations", {"name": name})["organizationId"]
state["orgs"] = orgs

# 2 Projekt je Modul mit Rollen (Modulschlüssel als Präfix), Rollen im Token
project = call("POST", "/management/v1/projects", {
    "name": "glossary", "projectRoleAssertion": True, "projectRoleCheck": True, "hasProjectCheck": False,
}, org=platform_org)["id"]
state["project"] = project
roles = [("glossary.reader", "Lesen"), ("glossary.editor", "Redaktion"), ("glossary.admin", "Administration")]
call("POST", f"/management/v1/projects/{project}/roles/_bulk", {
    "roles": [{"key": k, "displayName": d, "group": "glossary"} for k, d in roles],
}, org=platform_org)
# Plattformrolle Super-Admin (DB-E6) als eigenes Projekt «platform»
platform_project = call("POST", "/management/v1/projects", {"name": "platform", "projectRoleAssertion": True}, org=platform_org)["id"]
call("POST", f"/management/v1/projects/{platform_project}/roles", {"roleKey": "platform.super_admin", "displayName": "Super-Admin"}, org=platform_org)
state["platform_project"] = platform_project

# 3 Projekt-Freigabe an die Schulen: dürfen ihren Konten Glossary-Rollen geben (nicht admin)
grants = {}
for key, org_id in orgs.items():
    grants[key] = call("POST", f"/management/v1/projects/{project}/grants", {
        "grantedOrgId": org_id, "roleKeys": ["glossary.reader", "glossary.editor"],
    }, org=platform_org)["grantId"]
state["project_grants"] = grants

# 4 OIDC-Client für das Glossary (Code-Flow mit PKCE und Secret, JWT-Access-Token, Rollen im ID-Token)
app = call("POST", f"/management/v1/projects/{project}/apps/oidc", {
    "name": "glossary-web",
    "redirectUris": ["http://localhost:8000/auth/callback"],
    "postLogoutRedirectUris": ["http://localhost:8000/"],
    "responseTypes": ["OIDC_RESPONSE_TYPE_CODE"],
    "grantTypes": ["OIDC_GRANT_TYPE_AUTHORIZATION_CODE", "OIDC_GRANT_TYPE_REFRESH_TOKEN"],
    "appType": "OIDC_APP_TYPE_WEB",
    "authMethodType": "OIDC_AUTH_METHOD_TYPE_BASIC",
    "accessTokenType": "OIDC_TOKEN_TYPE_JWT",
    "accessTokenRoleAssertion": True,
    "idTokenRoleAssertion": True,
    "idTokenUserinfoAssertion": True,
    "devMode": True,  # nur PoC: http://localhost erlaubt
}, org=platform_org)
state["oidc_app"] = {"client_id": app["clientId"], "client_secret": app["clientSecret"], "app_id": app["appId"]}

# 5 Testkonten in den Schulen (erfunden) mit Rollen
def human(org_id: str, user: str, given: str, family: str) -> str:
    return call("POST", "/v2/users/human", {
        "username": user,
        "organization": {"orgId": org_id},
        "profile": {"givenName": given, "familyName": family, "preferredLanguage": "de"},
        "email": {"email": user, "isVerified": True},
        "password": {"password": "Poc-Test-2026!", "changeRequired": False},
    })["userId"]

users = {
    "lehrperson": human(orgs["musterhausen"], "lehrperson@musterhausen.example", "Lea", "Lehrerin"),
    "redaktion": human(orgs["beispielthal"], "redaktion@beispielthal.example", "Remo", "Redaktor"),
}
call("POST", f"/management/v1/users/{users['lehrperson']}/grants", {
    "projectId": project, "projectGrantId": grants["musterhausen"], "roleKeys": ["glossary.reader"],
}, org=orgs["musterhausen"])
call("POST", f"/management/v1/users/{users['redaktion']}/grants", {
    "projectId": project, "projectGrantId": grants["beispielthal"], "roleKeys": ["glossary.editor"],
}, org=orgs["beispielthal"])
state["users"] = users

# 6 Dienstkonto für Dienst-zu-Dienst (S2): Client Credentials, Rolle reader
sa = call("POST", "/management/v1/users/machine", {
    "userName": "intranet-sync", "name": "Intranet Synchronisation", "accessTokenType": "ACCESS_TOKEN_TYPE_JWT",
}, org=platform_org)["userId"]
secret = call("PUT", f"/management/v1/users/{sa}/secret", {}, org=platform_org)
call("POST", f"/management/v1/users/{sa}/grants", {"projectId": project, "roleKeys": ["glossary.reader"]}, org=platform_org)
state["service_account"] = {"user_id": sa, "client_id": secret["clientId"], "client_secret": secret["clientSecret"]}

(ROOT / "state.json").write_text(json.dumps(state, indent=2))
print(json.dumps({k: v for k, v in state.items() if k not in ("oidc_app", "service_account")}, indent=2))
print("Clients angelegt: glossary-web, intranet-sync (Zugangsdaten in state.json)")
