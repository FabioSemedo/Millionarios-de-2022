INSERT INTO CountryNames(name)
SELECT *
  FROM (
           SELECT citizenship
             FROM test
           UNION
           SELECT country_of_residence
             FROM test
       )
;
-------------------------------------------------
CREATE TABLE CountryNames(
  countryNameID INTEGER NOT NULL PRIMARY KEY,
  name TEXT NOT NULL 
);