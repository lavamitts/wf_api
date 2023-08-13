SELECT
    m.measure_sid,
    mc.measure_condition_sid,
    mc.condition_code,
    mc.certificate_type_code,
    mc.certificate_code,
    mc.condition_duty_amount,
    mc.condition_monetary_unit_code,
    mc.condition_measurement_unit_code,
    mc.condition_measurement_unit_qualifier_code,
    c.code,
    c.description
FROM
    utils.materialized_measures_real_end_dates m,
    measure_types mt,
    measure_conditions mc
    LEFT OUTER JOIN utils.materialized_certificates c ON (c.certificate_type_code = mc.certificate_type_code
        AND c.certificate_code = mc.certificate_code)
WHERE
    m.measure_type_id = mt.measure_type_id
    AND m.measure_sid = mc.measure_sid
    AND mt.measure_type_series_id IN ('A', 'B')
    AND m.goods_nomenclature_sid IN %s
    AND m.measure_type_id <= '999'
    AND mt.trade_movement_code != '1'
    AND m.validity_start_date::date <= CURRENT_DATE
    AND (m.validity_end_date IS NULL
        OR m.validity_end_date::date >= CURRENT_DATE)
ORDER BY
    mc.measure_sid,
    mc.component_sequence_number
