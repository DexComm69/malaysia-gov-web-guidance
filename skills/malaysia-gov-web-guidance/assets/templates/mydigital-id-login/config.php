<?php
/**
 * MyDigital ID login settings. The values come from MyDigital ID Sdn. Bhd. when the agency is onboarded:
 * never invent them. Keep the client secret out of the repository (environment variable or a file outside
 * the web root).
 */
declare(strict_types=1);

return [
    // e.g. https://<MYDID_HOST>/realms/<REALM>  (TODO: from MyDigital ID)
    'issuer'        => getenv('MYID_ISSUER') ?: 'TODO-issuer',
    'client_id'     => getenv('MYID_CLIENT_ID') ?: 'TODO-client-id',
    'client_secret' => getenv('MYID_CLIENT_SECRET') ?: '',        // confidential (server-side) client
    'redirect_uri'  => getenv('MYID_REDIRECT_URI') ?: 'https://TODO.gov.my/myid/callback.php',   // registered with MyDigital ID, HTTPS
    'after_logout'  => getenv('MYID_AFTER_LOGOUT') ?: 'https://TODO.gov.my/',

    // Claim names for the person's name and IC number. The guide calls them "Nama" and "Nric":
    // confirm the exact names with MyDigital ID (TODO) and adjust.
    'claim_name'    => getenv('MYID_CLAIM_NAME') ?: 'nama',
    'claim_nric'    => getenv('MYID_CLAIM_NRIC') ?: 'nric',

    // Store a keyed hash of the IC number instead of the number itself, if the agency's data owner agrees
    // (decide with them: see guide mydigital-id). Keep this secret outside the database.
    'nric_pepper'   => getenv('MYID_NRIC_PEPPER') ?: '',

    // Only for the automated tests against a local mock provider. Never in production.
    'allow_http_for_local_testing' => getenv('MYID_ALLOW_HTTP_FOR_TESTS') === '1',
];
