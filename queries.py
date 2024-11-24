"""
counts how many billionaires moved out from their home country and where did they go

SELECT 
    cn.name AS Origin_Country,
    rc.name AS Destination_Country,
    COUNT(b.billionaireID) AS Total_Billionaires
FROM 
    Billionaires b
JOIN 
    CountriesNames cn ON b.citizenshipID = cn.countryNameID
JOIN 
    Cities c ON b.cityID = c.cityID
JOIN 
    ResidenceCountries rc ON c.countryID = rc.residenceCountryID
WHERE 
    b.citizenshipID != rc.countryNameID
GROUP BY 
    cn.name, rc.name
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
    YEAR(CURDATE()) - YEAR(b.date_of_birth) AS Age
FROM 
    Billionaires b
JOIN 
    Industries i ON b.industryID = i.industryID
JOIN 
    SourcesOfWealth s ON b.sourceID = s.sourceID
WHERE 
    (YEAR(CURDATE()) - YEAR(b.date_of_birth)) < 40
GROUP BY 
    i.name, b.billionaireID
HAVING 
    COUNT(b.billionaireID) <= 5
ORDER BY 
    Age ASC, i.name;


--------------------------------------------------------------------

this ones a bit funny, i thought that we could check how many billionaires have the same name and the avg location those ppl live in

SELECT 
    COUNT(b.billionaireID) AS Total_Billionaires_With_Same_Name,
    AVG(rc.lat) AS Avg_Latitude,
    AVG(rc.long) AS Avg_Longitude
FROM 
    Billionaires b
JOIN 
    CountriesNames cn ON b.citizenshipID = cn.countryNameID
JOIN 
    ResidenceCountries rc ON cn.countryNameID = rc.countryNameID
WHERE 
    b.first_name = 'João';


"""