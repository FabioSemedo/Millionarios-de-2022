;

select avg(len1), avg(len2)
from (select length(first_name) as len1, length(last_name) as len2 
    from test 
    order by length(first_name) desc
    limit (ROUND((select count(*)*0.05 from test)))) t
;

select avg(len1), avg(len2)
from (select length(first_name) as len1, length(last_name) as len2 from test) t
;


select max(t.ctr), max(t.ctz), max(t.city)
from (select length(country_of_residence) as ctr, length(citizenship) as ctz, length(city_of_residence) as city
from test) t
;

select country_of_residence
from (select DISTINCT country_of_residence from test)
where length(country_of_residence) >20
;

select city_of_residence
from (select DISTINCT city_of_residence from test)
where length(city_of_residence) >10
;
--4 names

select last_name
from (select distinct last_name from test)
where length(last_name) > 20
;
--10 names

select first_name
from (select distinct first_name from test)
where length(first_name) > 20
;
-- 2 names

SELECT max(length(industry)) as IND, max(length(first_name)) as fstName, max(length(last_name)) as LlastName, max(length(city_of_residence)) as city, max(length(country_of_residence)) as country, max(length(continent)) as continent
from test
order by industry desc
;
--26	26	27	24	24	13

select *
from (select distinct industry from test)
where length(industry) > 15
;