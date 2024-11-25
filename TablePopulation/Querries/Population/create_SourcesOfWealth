Alter Table Sources
RENAME TO SourcesOfWealth;

INSERT INTO Sources(name)
    SELECT Distinct source 
    FROM Activities 
    ORDER BY source
RETURNING *;


-- Fixed entry {128,Casinos/hotels} -> {128,Casinos},{128,Hotels}
INSERT INTO Activities
VALUES 
    (128,"Casinos"),
    (128,"Hotels")
RETURNING*;

DELETE FROM Activities
WHERE source LIKE "Casinos/hotels"
RETURNING*;