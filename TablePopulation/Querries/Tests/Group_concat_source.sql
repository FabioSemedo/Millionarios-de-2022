select b.personId, b.first_name ||" "|| b.last_name,
     b.wealth_millions, Group_Concat(s.source, ', ') as source,
     c.name, c2.name
FROM Billionaires b 
    INNER JOIN Countries c ON b.citizenshipID = c.countryID
    INNER JOIN Cities    c1 ON c1.cityid = b.cityID
    INNER JOIN Countries c2 ON c2.countryID = c1.countryid 
    INNER JOIN Activities a ON a.personId = b.personId
    INNER JOIN SourcesOfWealth s ON s.sourceID = a.sourceID
GROUP BY b.personId    