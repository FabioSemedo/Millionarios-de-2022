-- SQLite
SELECT *
FROM
(SELECT ct.name as city, GROUP_CONCAT(cn.name) as country
FROM 
    Cities ct INNER JOIN Countries cn
    ON ct.countryid = cn.countryid
GROUP BY UPPER(ct.name)
) t1
INNER JOIN
(SELECT city_of_residence , GROUP_CONCAT(country_of_residence) AS country_of_residence
FROM Test
GROUP BY UPPER(city_of_residence)
) t2
ON t1.city = t2.city_of_residence
WHERE t1.country NOT LIKE t2.country_of_residence
;

SELECT *
FROM Cities
WHERE name LIKE "%Peter%"
;

SELECT DISTINCT city_of_residence, country_of_residence
FROM Test
WHERE city_of_residence LIKE "%Peter%"
;

--tuples of the 6 cities from the except query
SELECT DISTINCT
    city_of_residence, country_of_residence
FROM Test
WHERE UPPER(city_of_residence) in
(
SELECT city FROM (
SELECT DISTINCT UPPER(city_of_residence) as city, country_of_residence
FROM Test
WHERE city_of_residence NOT LIKE '%unknown%'
GROUP BY city_of_residence, country_of_residence
EXCEPT
SELECT city_of_residence, country_of_residence
FROM 
    (
    SELECT DISTINCT ct.name as city_of_residence, cn.name as country_of_residence
    FROM    
        Cities ct INNER JOIN Countries cn ON ct.countryid = cn.countryid
    )
GROUP BY city_of_residence, country_of_residence)
)
ORDER BY city_of_residence
;

SELECT DISTINCT bl.personId, bl.first_name ||" "||bl.last_name as Name,ct.cityID, ct.name as City1, cn.countryid, cn.name as Country1, t.city_of_residence, t.country_of_residence
FROM Billionaires bl INNER JOIN Cities ct INNER JOIN Countries cn INNER JOIN Test t
    ON bl.cityid = ct.cityID AND ct.name = UPPER(t.city_of_residence) AND ct.countryid = cn.countryid AND t.wealth = bl.wealth_millions AND t.first_name = bl.first_name
WHERE cn.name NOT LIKE t.country_of_residence AND ct.name not like "unknown"
;

--tuples of the 6 cities from the except query
SELECT DISTINCT
    city_of_residence, country_of_residence
FROM Test
WHERE UPPER(city_of_residence) in
(
SELECT city FROM (
SELECT DISTINCT UPPER(city_of_residence) as city, country_of_residence
FROM Test
WHERE city_of_residence NOT LIKE '%unknown%'
GROUP BY city_of_residence, country_of_residence
EXCEPT
SELECT city_of_residence, country_of_residence
FROM 
    (
    SELECT DISTINCT ct.name as city_of_residence, cn.name as country_of_residence
    FROM
        Cities ct INNER JOIN Countries cn ON ct.countryid = cn.countryid
    )
GROUP BY city_of_residence, country_of_residence)
)
ORDER BY city_of_residence
;