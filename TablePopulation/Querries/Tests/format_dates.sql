--check dates
select birth_day, birth_month, birth_date
from test2
where (birth_day > 31) OR (birth_month > 12) 
    OR (birth_month < 1) OR (birth_day < 1 )
    or ((birth_day >29) and (birth_month = 2))
    ;
--format date
update test2
set birth_date = birth_year || "-" || birth_month || "-" || birth_day
where true;