<?php
// Edulog-Ersatz für den PoC (#36): Testkonten im Format des Edulog-Leitfadens für Identitätsanbieter 1.2.1.
// Nur erfundene Daten. Passwort aller Konten: edulog-test
$std = ['preferredLanguage' => ['de-CH'], 'EdulogPersonCanton' => ['ZH']];
$config = [
    'admin' => ['core:AdminPassword'],
    'example-userpass' => [
        'exampleauth:UserPass',
        // Lehrperson mit zwei Rollen (je Wert ein AttributeValue) und zwei Institutionen
        'lehrperson:edulog-test' => array_merge($std, [
            'EdulogPersonTechID' => ['5ca28bef-e599-497f-9ae8-83ae4aef7001'], 'uid' => ['l.lehrer@musterhausen.example'],
            'givenName' => ['Lara'], 'sn' => ['Lehrer'], 'mail' => ['l.lehrer@musterhausen.example'],
            'EdulogPersonRole' => ['teacher', 'technician'], 'o' => ['Sekundarschule Musterhausen', 'SMH'],
            'EdulogPersonLevel' => ['secondary1'], 'EdulogPersonCycle' => ['3'],
        ]),
        // Schulleitung wie aus Entra ID: Mehrfachwerte mit ## in einem Wert
        'schulleitung:edulog-test' => array_merge($std, [
            'EdulogPersonTechID' => ['5ca28bef-e599-497f-9ae8-83ae4aef7002'], 'uid' => ['s.leiter@beispielthal.example'],
            'givenName' => ['Sandro'], 'sn' => ['Leiter'], 'mail' => ['s.leiter@beispielthal.example'],
            'EdulogPersonRole' => ['teacher##principal'], 'o' => ['Schulgemeinde Beispielthal'],
            'EdulogPersonLevel' => ['primary##secondary1'], 'EdulogPersonCycle' => ['2##3'], 'preferredLanguage' => ['fr-CH'],
        ]),
        // Schülerin: kein Zugang (pupil)
        'schuelerin:edulog-test' => array_merge($std, [
            'EdulogPersonTechID' => ['5ca28bef-e599-497f-9ae8-83ae4aef7003'], 'uid' => ['s.schuelerin@musterhausen.example'],
            'givenName' => ['Sina'], 'sn' => ['Schülerin'], 'mail' => ['s.schuelerin@musterhausen.example'],
            'EdulogPersonRole' => ['pupil'], 'o' => ['Sekundarschule Musterhausen'],
        ]),
        // Rolle leer = unbekannt: kein Zugang
        'unbekannt:edulog-test' => array_merge($std, [
            'EdulogPersonTechID' => ['5ca28bef-e599-497f-9ae8-83ae4aef7004'], 'uid' => ['u.unbekannt@musterhausen.example'],
            'givenName' => ['Uli'], 'sn' => ['Unbekannt'], 'mail' => ['u.unbekannt@musterhausen.example'],
            'EdulogPersonRole' => [''], 'o' => [''],
        ]),
        // Verwaltung (neu, erst mit Login V2 angemeldet)
        'verwaltung:edulog-test' => array_merge($std, [
            'EdulogPersonTechID' => ['5ca28bef-e599-497f-9ae8-83ae4aef7005'], 'uid' => ['v.verwaltung@musterhausen.example'],
            'givenName' => ['Vera'], 'sn' => ['Verwaltung'], 'mail' => ['v.verwaltung@musterhausen.example'],
            'EdulogPersonRole' => ['administration'], 'o' => ['SMH'], 'preferredLanguage' => ['it-CH'],
        ]),
    ],
];
