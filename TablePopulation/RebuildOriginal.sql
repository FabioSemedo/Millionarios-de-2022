SELECT
    Rank() OVER(ORDER BY bl.wealth_millions DESC) as Position,
    bl.wealth_millions,
    bl.industry,
    bl.first_name ||" "|| bl.last_name ||
        CASE
            WHEN ((bl.name_suffix = "")  AND (bl.conglomorate = 0))THEN ""
            WHEN ((NOT (bl.name_suffix = ""))  AND (bl.conglomorate = 0))THEN ", "||bl.name_suffix
            WHEN ((bl.name_suffix = "") AND (bl.conglomorate = 1))THEN "& family"
            ELSE ", "||bl.name_suffix ||" "||"& family"
        END  AS Full_name,
        FLOOR(CAST((JULIANDAY('2022-12-31') - JULIANDAY(bl.birth_date)) AS INTEGER) / 365.25) AS Age,
        cn.name as Country_of_residence,
        ct.name as City_of_residence,
        group_concat(sr.source, ", ") as Source,
        cz.name as Citizenship,
        bl.gender AS Gender,
        CAST(strftime('%d', bl.birth_date) AS INTEGER) ||"/"||
        CAST(strftime('%m', bl.birth_date) AS INTEGER) ||"/"||
        CAST(strftime('%Y',bl.birth_date) AS INTEGER) as Birth_date
        , bl.last_name
        , bl.first_name
        , CASE 
            WHEN (usct.cityID IS NULL) THEN "No subdivision info"
            ELSE usst.state
            END as Residence_state
        , CASE 
            WHEN (usct.cityID IS NULL) THEN "No subdivision info"
            ELSE usst.region
            END as Residence_region             
        , strftime('%Y', bl.birth_date) as Birth_Year
        , CAST (strftime('%m', bl.birth_date) AS INTEGER) AS Birth_Month
        , CAST (strftime('%d', bl.birth_date) AS INTEGER) AS Birth_Day
        , ec.cpi as Cpi_country
        , ec.cpi_change as Cpi_change_country
        , ec.gdp as Gdp_country
        , ec.grs_trt_enroll as G_tertiary_ed_enroll
        , ec.grs_prm_enroll as G_primary_ed_enroll
        , ec.life_expect as life_expectancy
        , ec.tax_rev as tax_revenue
        , ec.tax_rate as tax_rate
        , ec.population as country_pop
        , cn.latitude as country_lat
        , cn.longitude as country_long
        , cn.continent as continent
FROM
    Billionaires bl 
    INNER JOIN Activities ac ON bl.personId = ac.personId
    INNER JOIN SourcesOfWealth sr ON sr.sourceID = ac.sourceID
    INNER JOIN Cities ct ON ct.cityid = bl.cityID
    INNER JOIN Countries cn ON cn.countryid = ct.countryid
    INNER JOIN EconomicDetails ec ON ec.countryid = cn.countryid
    INNER JOIN Countries cz ON cz.countryid = bl.citizenshipID
    LEFT JOIN (USCities usct INNER JOIN USStates usst ON usct.stateID = usst.stateID)
    ON usct.cityID = ct.cityid
GROUP BY bl.personId
ORDER BY bl.wealth_millions DESC;