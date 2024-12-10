WITH tmp as (
SELECT s1.sourceID as ID, s1.source AS sourceT, count(s2.sourceID) as num
FROM SourcesOfWealth s1 
    JOIN
    SourcesOfWealth s2
WHERE s2.source LIKE ("%"||s1.source||"%") AND (s2.source NOT LIKE s1.source)
GROUP BY s1.sourceID
HAVING count(s2.source) > 1
ORDER BY s1.sourceID
)

Select ID, sourceT, count(*) as Found, GROUP_CONCAT(source,", ") as 'Similar Sources'
FROM SourcesOfWealth JOIN tmp
WHERE 
(
source like ("%"||sourceT||"%") AND (sourceT not like "Art")
) OR
(
source like ("% "||sourceT||"%") AND (sourceT like "Art")
) OR
(
source like ("%"||sourceT||" %") AND (sourceT like "Art")
)OR
(
source like sourceT AND (sourceT like "Art")
)
GROUP BY ID
ORDER BY sourceT
;