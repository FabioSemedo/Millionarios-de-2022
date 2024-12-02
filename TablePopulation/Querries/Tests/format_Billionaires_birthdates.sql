BEGIN TRANSACTION;

update Billionaires
SET birth_date = t.format
FROM(
    SELECT Distinct birth_date,
           CASE/* Birth month, day, and year must be declared as ints */ 
           WHEN birth_month < 10 AND birth_day < 10 THEN birth_year || "-0" || birth_month || "-0" || birth_day 
           WHEN birth_month < 10 THEN birth_year || "-0" || birth_month || "-" || birth_day 
           WHEN birth_day < 10 THEN birth_year || "-" || birth_month || "-0" || birth_day 
           ELSE birth_year || "-" || birth_month || "-" || birth_day 
           END AS format
      FROM (select birth_date, 
          cast(birth_day as integer) as birth_day,
          cast(birth_month as integer) as birth_month,
          cast(birth_year as integer) as birth_year 
          from test)
          ) t
WHERE Billionaires.birth_date = t.birth_date          
;
Commit;
 