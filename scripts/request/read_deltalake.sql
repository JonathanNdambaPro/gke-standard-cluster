CREATE SECRET (
    TYPE gcs,
    KEY_ID 'AKIAIOSFODNN7EXAMPLE',
    SECRET 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY'
);

SELECT *
FROM delta_scan('{{ path_gcs_deltalake }}')