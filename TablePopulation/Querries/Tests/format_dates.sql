-- SQLite
--Rollback;
BEGIN TRANSACTION;

with tmp as (
select birth_date as date, 
    Case
        --Birth month, day, and year must be declared as ints
        when birth_month< 10 AND birth_day< 10 THEN birth_year || "-0" || birth_month || "-0" || birth_day
        when birth_month< 10 THEN birth_year || "-0" || birth_month || "-" || birth_day
        when birth_day< 10  THEN birth_year || "-" || birth_month || "-0" || birth_day
        ELSE birth_year || "-" || birth_month || "-" || birth_day
    END as format
    FROM test2
)
update Test2
set birth_date = format
FROM tmp
WHERE test2.birth_date = tmp.date
RETURNING *;

commit;