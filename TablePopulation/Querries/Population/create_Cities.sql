BEGIN TRANSACTION;
DROP TABLE Cities;

CREATE TABLE Cities(
    cityID INTEGER NOT NULL PRIMARY KEY,
    name TEXT
);
INSERT INTO Cities(name)
SELECT DISTINCT UPPER(city_of_residence)
FROM test
ORDER BY city_of_residence;

COMMIT;

--find errors (if any) in the city column
/*
SELECT country_of_residence ,city_of_residence
FROM test
WHERE city_of_residence GLOB "*[^-.A-Za-z0-9' ]*";
*/
--Character encoding errors:----------------------------------------------------------------
/*
UPDATE test
    SET city_of_residence = "Sant'Elpidio a Mare"          
    WHERE city_of_residence = "Sant'' Elpidio A Mare"          
    RETURNING country_of_residence, city_of_residence;
UPDATE test
    SET city_of_residence = "A Coruna"          
    WHERE city_of_residence = "A CoruÃ±a"          
    RETURNING country_of_residence, city_of_residence;
UPDATE test
    SET city_of_residence = "Kussnacht"           
    WHERE city_of_residence = "KÃ¼snacht"           
    RETURNING country_of_residence, city_of_residence;
UPDATE test
    SET city_of_residence = "Goteborg"          
    WHERE city_of_residence = "GÃ¶teborg"          
    RETURNING country_of_residence, city_of_residence;
UPDATE test
    SET city_of_residence = "Grafelfing"         
    WHERE city_of_residence = "GrÃ¤felfing"         
    RETURNING country_of_residence, city_of_residence;
UPDATE test
    SET city_of_residence = "Rheda-Wiedenbruck"  
    WHERE city_of_residence = "Rheda-WiedenbrÃ¼ck"  
    RETURNING country_of_residence, city_of_residence;
UPDATE test
    SET city_of_residence = "Sao Paulo"          
    WHERE city_of_residence = "SÃ£o Paulo"          
    RETURNING country_of_residence, city_of_residence;
UPDATE test
    SET city_of_residence = "Felcsut" 
    WHERE city_of_residence = "FelcsÃºt" 
    RETURNING country_of_residence, city_of_residence;
*/

--Atomisation issues:----------------------------------------------------------------
/*
UPDATE test
SET city_of_residence = "Krotoszyn"
WHERE city_of_residence = "Krotoszyn,"
RETURNING *;
UPDATE test
SET city_of_residence = "St. Brelade"
WHERE city_of_residence = "St. Brelade, Jersey"
RETURNING *;
UPDATE test
SET city_of_residence = "Tawau"
WHERE city_of_residence = "Tawau, Sabah"
RETURNING *;
UPDATE test
SET city_of_residence = "London"
WHERE city_of_residence = "London, Suffolk"
RETURNING *;
UPDATE test
SET city_of_residence = "Tokyo"
WHERE city_of_residence = "Nakano, Tokyo"
RETURNING *;
*/