SELECT
    m.measure_sid,
    m.measure_type_id,
    m.geographical_area_id,
    mt.description AS measure_type_description,
    m.validity_start_date,
    m.validity_end_date,
    m.measure_generating_regulation_id,
    m.goods_nomenclature_item_id,
    m.goods_nomenclature_sid,
    r.impacts_windsor_framework,
    r.theme_id,
    r.information_text
FROM
    utils.measure_types mt,
    utils.materialized_measures_real_end_dates m
    LEFT OUTER JOIN windsor_framework.wf_regulations r ON m.measure_generating_regulation_id = r.regulation_id
    LEFT OUTER JOIN windsor_framework.wf_themes t ON t.theme_id = r.theme_id
WHERE
    m.measure_type_id = mt.measure_type_id
    AND mt.measure_type_series_id IN ('A', 'B')
    AND m.goods_nomenclature_sid IN %s
    AND m.measure_type_id <= '999'
    AND mt.trade_movement_code != '1'
    AND m.validity_start_date::date <= CURRENT_DATE
    AND (m.validity_end_date IS NULL
        OR m.validity_end_date::date >= CURRENT_DATE)
ORDER BY
    m.measure_type_id,
    m.geographical_area_id
