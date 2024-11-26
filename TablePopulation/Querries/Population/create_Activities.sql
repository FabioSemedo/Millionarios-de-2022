--delete Activities.source column

PRAGMA foreign_keys = 0;

CREATE TABLE sqlitestudio_temp_table AS SELECT *
                                          FROM Activities;

DROP TABLE Activities;

CREATE TABLE Activities (
    personId,
    source,
    sourceID INTEGER REFERENCES SourcesOfWealth (sourceID),
    PRIMARY KEY (personID, sourceID)
);

INSERT INTO Activities (
                           personId,
                           source,
                           sourceID
                       )
                       SELECT q.personId,
                              q.source,
                              s.sourceID
                         FROM sqlitestudio_temp_table q INNER JOIN SourcesOfWealth s ON q.source = s.source;

DROP TABLE sqlitestudio_temp_table;

PRAGMA foreign_keys = 1;

--Create and populate SourcesOFWealth tbl *see create_SourcesOfWealth.sql
--Import atomised_source_v2.csv into new table Acivites 