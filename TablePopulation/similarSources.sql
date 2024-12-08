-- SQLite
SELECT s1.*, s2.sourceID, s2.source
FROM SourcesOfWealth s1 
    JOIN
    SourcesOfWealth s2
WHERE s2.source LIKE ("%"||s1.source||"%")
GROUP BY s1.sourceID, s2.sourceID
;

SELECT s1.sourceID, count(s2.sourceID)
FROM SourcesOfWealth s1 
    JOIN
    SourcesOfWealth s2
WHERE s2.source LIKE ("%"||s1.source||"%")
GROUP BY s1.sourceID, s2.sourceID
HAVING count(s2.sourceID) > 2;