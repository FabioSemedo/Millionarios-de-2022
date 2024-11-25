;

SELECT avg(len1),
       avg(len2) 
  FROM (
           SELECT length(first_name) AS len1,
                  length(last_name) AS len2
             FROM test
            ORDER BY length(first_name) DESC
            LIMIT (ROUND( (
                              SELECT count( * ) * 0.05
                                FROM test
                          )
                  ) ) 
       )
       t;

SELECT avg(len1),
       avg(len2) 
  FROM (
           SELECT length(first_name) AS len1,
                  length(last_name) AS len2
             FROM test
       )
       t;

SELECT max(t.ctr),
       max(t.ctz),
       max(t.city) 
  FROM (
           SELECT length(country_of_residence) AS ctr,
                  length(citizenship) AS ctz,
                  length(city_of_residence) AS city
             FROM test
       )
       t;

SELECT country_of_residence
  FROM (
           SELECT DISTINCT country_of_residence
             FROM test
       )
 WHERE length(country_of_residence) > 20;

SELECT city_of_residence
  FROM (
           SELECT DISTINCT city_of_residence
             FROM test
       )
 WHERE length(city_of_residence) > 10;-- 4 names

SELECT last_name
  FROM (
           SELECT DISTINCT last_name
             FROM test
       )
 WHERE length(last_name) > 20;-- 10 names

SELECT first_name
  FROM (
           SELECT DISTINCT first_name
             FROM test
       )
 WHERE length(first_name) > 20;-- 2 names

SELECT max(length(industry) ) AS IND,
       max(length(first_name) ) AS fstName,
       max(length(last_name) ) AS LlastName,
       max(length(city_of_residence) ) AS city,
       max(length(country_of_residence) ) AS country,
       max(length(continent) ) AS continent
  FROM test
 ORDER BY industry DESC;-- 26	26	27	24	24	13

SELECT *
  FROM (
           SELECT DISTINCT industry
             FROM test
       )
 WHERE length(industry) > 15;
