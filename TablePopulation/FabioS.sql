SELECT t1.continent, ROUND(t1.RelativeGdp,2) AS Relative_Gdp, ROUND(t1.RelativeGdp/(SUM(t2.RelativeGdp))*100, 2) as "%"
FROM 
(    SELECT continent, AVG(AdjGdp) as RelativeGdp
    FROM
    (SELECT cn.name, cn.continent, e1.gdp/e1.population AS AdjGdp, e1.*
    FROM EconomicDetails e1 INNER JOIN Countries cn on e1.countryid = cn.countryid
    )
    GROUP BY continent
    ORDER BY AVG(AdjGdp) Desc
) t1, 
(    SELECT continent, AVG(AdjGdp) as RelativeGdp
    FROM
    (SELECT cn.name, cn.continent, e1.gdp/e1.population AS AdjGdp, e1.*
    FROM EconomicDetails e1 INNER JOIN Countries cn on e1.countryid = cn.countryid
    )
    GROUP BY continent
    ORDER BY AVG(AdjGdp) Desc
) t2
GROUP BY t1.continent
ORDER BY "%" DESC