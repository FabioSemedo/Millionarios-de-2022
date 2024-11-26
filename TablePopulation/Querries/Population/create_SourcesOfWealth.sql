INSERT INTO SourcesOfWealth(source)
SELECT DISTINCT a.source
FROM Activities a
ORDER BY a.source;
-------------------------------------------------
Create TABLE SourcesOfWealth(
    sourceID INTEGER NOT NULL PRIMARY KEY,
    source TEXT NOT NULL UNIQUE
);
--Import atomised_source_v2.csv into new table Acivites 