BEGIN TRANSACTION;

create table tmp (
    cityID PRIMARY KEY,
    name,
    countryID
    );
    
INSERT INTO tmp(cityID, name, countryID)
SELECT DISTINCT c.cityID, c.name, cnt.countryID
FROM Cities c INNER JOIN test t INNER JOIN COUNTRYNAMES cnt
    ON c.name = UPPER(t.city_of_residence) AND t.country_of_residence = cnt.name
ORDER BY cityID  
;


;
    
--COMMIT;

-- check Cities tbl has all cities
select distinct city_of_residence from test WHERE UPPER(city_of_residence) NOT IN (SELECT name FROM CITIES ) ORDER BY city_of_residence;

-- check city:country uniqueness
Select  city_of_residence, country_of_residence
FROM (SELECT city_of_residence, country_of_residence FROM test GROUP BY city_of_residence)
GROUP BY city_of_residence
HAVING COUNT(country_of_residence) > 1
;

--check city cells
SELECT city_of_residence, first_name, last_name
FROM test
WHERE city_of_residence GLOB "*[^A-Za-z ]*"
;