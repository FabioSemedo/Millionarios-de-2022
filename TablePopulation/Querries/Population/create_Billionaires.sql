PRAGMA foreign_keys = 0;

BEGIN TRANSACTION;

ALTER TABLE Billionaires
RENAME TO temp_Bills;

CREATE TABLE Billionaires
(
    personId          INTEGER     PRIMARY KEY,
    last_name         TEXT,
    first_name        TEXT,
    wealth_millions   INTEGER,
    conglomorate      INTEGER,
    industryID        INTEGER,
    birth_date        TEXT,
    gender            TEXT        CHECK (gender IN ("F", "M", "O") ),
    cityID            INTEGER,
    citizenshipID     INTEGER
                                  
);

INSERT INTO Billionaires (personId,first_name,last_name,
                            wealth_millions, conglomorate,
                            industryID,
                            gender, birth_date,
                            cityID, 
                            citizenshipID) 
SELECT  b.personId, b.first_name, b.last_name,
        t.wealth, (t.full_name LIKE "%& family"),
        i.industryID,
        t.gender, t.birth_date,
        c.cityID,
        CountryNames.countryID
FROM    temp_Bills b INNER JOIN test t on b.full_name = t.full_name AND b.wealth_millions = t.wealth
        INNER JOIN Industries i on t.industry = i.name
        INNER JOIN Cities c ON UPPER(t.city_of_residence) = c.name 
        INNER JOIN CountryNames ON t.citizenship = CountryNames.name
;

drop table temp_Bills;

COMMIT;

Pragma foreign_keys = 1;