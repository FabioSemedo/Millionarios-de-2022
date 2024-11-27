-------------------------------------------------
CREATE TABLE CountryNames(
  countryNameID INTEGER NOT NULL PRIMARY KEY,
  name TEXT NOT NULL 
);

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

--find errors (if any) in the Countries.name column
SELECT name
FROM Countries
WHERE name GLOB "*[^.A-Za-z' ]*"
;