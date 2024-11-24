"""
counts how many billionaires moved out from their home country and where did they go

SELECT 
    cn.name AS Origin_Country,
    rcn.name AS Destination_Country,
    COUNT(b.billionaireID) AS Total_Billionaires
FROM 
    Billionaires b
JOIN 
    CountriesNames cn ON b.citizenshipID = cn.countryNameID
JOIN 
    Cities c ON b.cityID = c.cityID
JOIN 
    ResidenceCountries rc ON c.countryID = rc.countryNameID
JOIN 
    CountriesNames rcn ON rc.countryNameID = rcn.countryNameID
WHERE 
    b.citizenshipID != rc.countryNameID
GROUP BY 
    cn.name, rcn.name
ORDER BY 
    Total_Billionaires DESC;

--------------------------------------------------------------------

checks billionaires younger than 40 in industries with equal or less than 5 billionaires. useful to check young ententrepreneurs on emerging fields

SELECT 
    b.first_name,
    b.last_name,
    i.name AS Industry_Name,
    s.name AS Source_of_Wealth,
    b.wealth_millions AS Wealth_Millions,
    (CAST((JULIANDAY('now') - JULIANDAY(b.date_of_birth)) AS INTEGER) / 365) AS Age
FROM 
    Billionaires b
JOIN 
    Industries i ON b.industryID = i.industryID
JOIN 
    SourcesOfWealth s ON b.sourceID = s.sourceID
WHERE 
    (CAST((JULIANDAY('now') - JULIANDAY(b.date_of_birth)) AS INTEGER) / 365) < 40
GROUP BY 
    i.name
HAVING 
    COUNT(b.billionaireID) <= 5
ORDER BY 
    Age ASC, i.name;

--------------------------------------------------------------------

this ones a bit funny, i thought that we could check how many billionaires have the same name and the avg location those ppl live in

SELECT 
    COUNT(b.billionaireID) AS Total_Billionaires_With_Same_Name,
    AVG(rc.latitude) AS Avg_Latitude,
    AVG(rc.longitude) AS Avg_Longitude
FROM 
    Billionaires b
JOIN 
    CountriesNames cn ON b.citizenshipID = cn.countryNameID
JOIN 
    ResidenceCountries rc ON cn.countryNameID = rc.countryNameID
WHERE 
    b.first_name = 'João';

--------------------------------------------------------------------
"""