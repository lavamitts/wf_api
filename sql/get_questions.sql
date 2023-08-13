SELECT
    document_code,
    measure_type_id,
    question,
    hint,
    implies_wf_category,
    positive
FROM
    windsor_framework.wf_document_codes_to_measure_types wdctmt
WHERE
    measure_type_id || '_' || document_code IN %s
