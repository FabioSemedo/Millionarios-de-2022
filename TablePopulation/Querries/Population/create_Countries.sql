CREATE TABLE tmpCountries(
    countryID INTEGER PRIMARY KEY,
    name, 
    population, 
    latitude,
    longitude
    );
    
insert into tmpCountries (name, population, latitude, longitude)
select c1.name, c2.population, c2.latitude, c2.longitude
from countrynames c1 inner join countrydetails c2 on c1.countryid = c2.countryid
;

alter table tmpcountries
rename to Countries;