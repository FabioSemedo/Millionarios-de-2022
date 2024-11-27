-- Check country -> countryInfo. numCountries = numSetsOfCountryDetails
SELECT count(a.num), count(b.num) 
  FROM (
           SELECT COUNT( * ) AS num
             FROM (
                      SELECT country_of_residence,
                             cpi_country,
                             cpi_change_country,
                             gdp_country,
                             g_primary_ed_enroll,
                             g_tertiary_ed_enroll,
                             life_expectancy,
                             tax_revenue,
                             tax_rate
                        FROM test
                       GROUP BY country_of_residence
                  )
       )
       a,
       (
           SELECT COUNT( * ) AS num
             FROM (
                      SELECT DISTINCT country_of_residence
                        FROM test
                  )
       )
       b;
