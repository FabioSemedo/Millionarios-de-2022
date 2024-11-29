create table tmpCities( cityid integer primary key, name, countryid);
    
insert into tmpCities (name, countryID)
select city, countryID
FROM (
    select distinct UPPER(city_of_residence) as city, country_of_residence from test2 group by UPPER(city_of_residence)
    )
    inner join countrynames on countrynames.name = country_of_residence
;

alter table tmpcities
rename to Cities;