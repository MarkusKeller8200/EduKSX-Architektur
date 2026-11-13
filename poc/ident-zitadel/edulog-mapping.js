/**
 * PoC P5 (#36): Edulog-Attribute (Leitfaden IdP 1.2.1) auf das Zitadel-Konto abbilden.
 * Mehrwertige Attribute kommen als mehrere Werte ODER mit ## getrennt (Entra ID) – beides wird gelesen.
 * Rollen und Institutionen landen als Metadaten (edulog_*); die Ident-Brücke leitet daraus Vorschläge ab.
 */
function edulogMapping(ctx, api) {
  let info = ctx.v1.providerInfo;
  if (!info || !info.attributes) { return; }
  let a = info.attributes;
  let werte = function (name) {
    let v = a[name];
    if (v === undefined || v === null) { return []; }
    if (!Array.isArray(v)) { v = [v]; }
    let out = [];
    v.forEach(function (x) { String(x).split('##').forEach(function (y) { y = y.trim(); if (y !== '') { out.push(y); } }); });
    return out;
  };
  let eins = function (name) { let w = werte(name); return w.length > 0 ? w[0] : ''; };
  // Kein Konto für Lernende, Erziehungsberechtigte, «other» und unbekannte Rolle (KONZEPT-IDENT 2.1, Datensparsamkeit)
  let erlaubt = ['teacher', 'administration', 'principal', 'technician'];
  if (!werte('EdulogPersonRole').some(function (r) { return erlaubt.indexOf(r) >= 0; })) {
    throw 'Für diese Rolle ist EduKSX noch nicht freigegeben.';
  }
  api.setFirstName(eins('givenName'));
  api.setLastName(eins('sn'));
  api.setDisplayName(eins('givenName') + ' ' + eins('sn'));
  api.setEmail(eins('mail'));
  api.setEmailVerified(true);
  api.setPreferredUsername(eins('mail'));
  let lang = eins('preferredLanguage');
  if (lang !== '') { api.setPreferredLanguage(lang.substring(0, 2)); }
  api.v1.user.appendMetadata('edulog_techid', eins('EdulogPersonTechID'));
  api.v1.user.appendMetadata('edulog_roles', werte('EdulogPersonRole'));
  api.v1.user.appendMetadata('edulog_orgs', werte('o'));
  api.v1.user.appendMetadata('edulog_canton', eins('EdulogPersonCanton'));
}
