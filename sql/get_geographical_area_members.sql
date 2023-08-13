SELECT
    parent_id,
    parent_description,
    child_id,
    child_description
FROM
    utils.geographical_area_memberships gam
WHERE
    parent_id IN %s
