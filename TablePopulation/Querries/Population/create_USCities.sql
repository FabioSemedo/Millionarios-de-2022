
PRAGMA foreign_keys = 0;

BEGIN TRANSACTION;

DROP TABLE USCities;

CREATE TABLE USCities (
    cityID  INTEGER NOT NULL,
    stateID INTEGER NOT NULL,
    PRIMARY KEY (
        cityID,
        stateID
    )
);

INSERT INTO USCities(cityID, stateID)
    SELECT DISTINCT cityID, 
        --city_of_residence, residence_state, 
                   stateID
    FROM Cities c inner join test t on c.name = UPPER(t.city_of_residence)
        inner join States s on residence_state = s.state
;

Commit;

PRAGMA foreign_keys = 1;    
;

/*
--checking for errors
SELECT city_of_residence, residence_state
FROM test
WHERE city_of_residence GLOB "*[^A-Za-z ]*" AND residence_state not like "no subdivisions info"
;