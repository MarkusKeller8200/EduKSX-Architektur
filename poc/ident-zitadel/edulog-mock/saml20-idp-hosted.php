<?php
// Edulog-Ersatz: NameID persistent = EdulogPersonTechID, Attributprofil «basic», Signatur SHA-256 (Edulog-Anforderungen 1.2)
$metadata['__DYNAMIC:1__'] = [
    'host' => '__DEFAULT__',
    'privatekey' => 'server.pem',
    'certificate' => 'server.crt',
    'auth' => 'example-userpass',
    'signature.algorithm' => 'http://www.w3.org/2001/04/xmldsig-more#rsa-sha256',
    'saml20.sign.response' => true,
    'saml20.sign.assertion' => true,
    'NameIDFormat' => 'urn:oasis:names:tc:SAML:2.0:nameid-format:persistent',
    'simplesaml.nameidattribute' => 'EdulogPersonTechID',
    'attributes.NameFormat' => 'urn:oasis:names:tc:SAML:2.0:attrname-format:basic',
];
