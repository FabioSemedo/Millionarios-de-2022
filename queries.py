"""
counts how many billionaires moved out from their home country and where did they go

SELECT 
    c1.name AS Origin_Country,
    c2.name AS Destination_Country,
    COUNT(b.personId) AS Total_Billionaires
FROM 
    Billionaires b
JOIN 
    Countries c1 ON b.citizenshipID = c1.countryid
JOIN 
    Cities ci ON b.cityID = ci.cityid
JOIN 
    Countries c2 ON ci.countryid = c2.countryid
WHERE 
    b.citizenshipID != ci.countryid
GROUP BY 
    c1.name, c2.name
ORDER BY 
    Total_Billionaires DESC;

--------------------------------------------------------------------

checks billionaires younger than 40 in industries with equal or less than 5 billionaires. useful to check young ententrepreneurs on emerging fields

WITH IndustryCounts AS (
    SELECT 
        b.industry,
        COUNT(*) AS Total_Billionaires
    FROM 
        Billionaires b
    GROUP BY 
        b.industry
    HAVING 
        COUNT(*) <= 50 /* CHANGE MAX NUMBER OF BILLIONAIRES PER INDUSTRY */
)
SELECT 
    b.first_name AS First_name,
    b.last_name AS Last_name,
    b.industry AS Industry,
    b.wealth_millions AS Wealth_in_Millions,
    (CAST((JULIANDAY('now') - JULIANDAY(b.birth_date)) AS INTEGER) / 365) AS Age
FROM 
    Billionaires b
JOIN 
    IndustryCounts ic ON b.industry = ic.industry
WHERE 
    (CAST((JULIANDAY('now') - JULIANDAY(b.birth_date)) AS INTEGER) / 365) < 45 /* CHANGE AGE OF BILLIONAIRES */
ORDER BY 
    Age ASC, Wealth_in_Millions DESC;

--------------------------------------------------------------------

this ones a bit funny, i thought that we could check how many billionaires have the same name and the avg location those ppl live in

SELECT 
    COUNT(b.personId) AS Total_Billionaires_With_Same_Name,
    AVG(c.latitude) AS Avg_Latitude,
    AVG(c.longitude) AS Avg_Longitude
FROM 
    Billionaires b
JOIN 
    Cities ci ON b.cityID = ci.cityid
JOIN 
    Countries c ON ci.countryid = c.countryid
WHERE 
    b.first_name like '%John%';

--------------------------------------------------------------------
"""