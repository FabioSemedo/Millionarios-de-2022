-- SQLite
WITH t1 as 
(
    SELECT SUM("AVG Gdp per Person") as num
    FROM 
    (
        SELECT AVG(Gdp_per_person) as "AVG Gdp per Person"
        FROM 
        (
            SELECT cn.name, cn.continent, ec.gdp/ec.country_pop as Gdp_per_person,  ec.gdp, ec.country_pop, ec.tax_rev, ec.tax_rate
            FROM 
                EconomicDetails ec INNER JOIN Countries cn
                ON ec.countryid = cn.countryid
            GROUP BY ec.countryid
        ) tmp
        GROUP BY continent
    )
)

SELECT continent, ROUND(AVG(Gdp_per_person),2) as "AVG Gdp per Person", ROUND(AVG(Gdp_per_person)/t1.num*100,2) as "%", AVG(tax_rate)
FROM t1,
(
    SELECT cn.name, cn.continent, ec.gdp/ec.country_pop as Gdp_per_person,  ec.gdp, ec.country_pop, ec.tax_rev, ec.tax_rate
    FROM 
        EconomicDetails ec INNER JOIN Countries cn
        ON ec.countryid = cn.countryid
    GROUP BY ec.countryid
) tmp
GROUP BY continent
ORDER BY "AVG Gdp per Person" DESC
;