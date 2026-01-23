CREATE SECRET (
    TYPE gcs,
    KEY_ID '{{ hmac_key }}',
    SECRET '{{ hmac_password }}'
);

SELECT *
FROM delta_scan('{{ path_gcs_deltalake }}')
