SELECT
    geographical_area_sid,
    geographical_area_id,
    description,
    geographical_code
FROM
    utils.geographical_areas
WHERE
    geographical_area_id IN %s
