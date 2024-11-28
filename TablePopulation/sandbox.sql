select full_name
from test2
where   

SELECT distinct full_name, first_name, last_name
from test2
--where full_name glob "*,*";
--where full_name glob "*[^-&'0-9A-Za-z ]*(*)*";
limit 100;

-- SQLite
select * 
from (
    select country_of_residence from Test2
    UNION
    select full_name from Test2
    UNION
    select city_of_residence from Test2
    UNION
    select source from SourcesOfWealth
    )
where country_of_residence glob "*[^-&'0-9A-Za-z ]*"
;