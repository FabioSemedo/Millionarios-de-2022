BEGIN TRANSACTION;

INSERT INTO CountryDetails (countryNameID, continent, latitude, longitude, population,
                            cpi, cpi_change, gdp, grs_trt_enroll,grs_prm_enroll,
                            life_expect, tax_rev, tax_rate)
SELECT DISTINCT c.countryID, t.continent,
        t.country_lat, t.country_long, t.country_pop, 
        t.cpi_country, t.cpi_change_country,
        t.gdp_country, t.g_tertiary_ed_enroll, g_primary_ed_enroll,
        t.life_expectancy, t.tax_revenue, t.tax_rate
FROM CountryNames c INNER JOIN test t ON c.name = t.country_of_residence
RETURNING *
;

COMMIT;

--Check all countries only have one set of details associated to them
SELECT country_of_residence, count(*)
FROM (
SELECT country_of_residence, continent,
        country_lat, country_long, country_pop, 
        cpi_country, cpi_change_country,
        gdp_country, g_tertiary_ed_enroll, g_primary_ed_enroll,
        life_expectancy, tax_revenue, tax_rate
FROM test
GROUP BY country_of_residence)
GROUP BY Country_of_residence
HAVING COUNT(*) > 1
;

WITH tmpTbl AS (
SELECT DISTINCT country_of_residence
FROM test
WHERE cpi_country like "No CPI info")

SELECT country_of_residence, cpi_country, cpi_change_country
FROM test
WHERE country_of_residence in (SELECT * from tmpTbl);