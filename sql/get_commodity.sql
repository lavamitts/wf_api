SELECT
    *
FROM
    windsor_framework.wf_hierarchy
WHERE
    productline_suffix = '80'
    AND goods_nomenclature_item_id = %s
