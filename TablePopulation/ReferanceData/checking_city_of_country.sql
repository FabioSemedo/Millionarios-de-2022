SELECT distinct city_of_residence, country_of_residence, name, country
FROM 
    (Select distinct city_of_residence, country_of_residence FROM test2) t 
    Join 
    (Select name, GROUP_CoNCAT(country, ', ') as country
    from RefCities r
    group by name) r 
    on t.city_of_residence = r.name
WHERE  r.country not like ("%"|| t.country_of_residence  ||"%") OR name is null
