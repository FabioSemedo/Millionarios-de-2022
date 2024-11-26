PRAGMA foreign_keys = 0;

BEGIN TRANSACTION;

DROP TABLE States;

CREATE TABLE States (
    stateID INTEGER PRIMARY KEY
                    NOT NULL,
    state   TEXT    UNIQUE
                    NOT NULL,
    region  TEXT,
    CHECK (UPPER(region) IN ("SOUTH", "WEST", "MIDWEST", "NORTHEAST", "U.S. TERRITORIES") ) 
);

INSERT INTO States(state, region)
SELECT residence_state, residence_region
FROM   (
    SELECT residence_state, residence_region --, max(num)
    FROM (SELECT DISTINCT residence_state, residence_region, count(*) as num
        FROM test
        WHERE residence_state in (
            SELECT residence_state
            FROM test
            WHERE residence_state not like "%unknown%"
            )
            GROUP BY residence_state, residence_region
    )
    GROUP BY residence_state
    HAVING residence_state not like "No subdivisions info"
    )
;
Commit;

PRAGMA foreign_keys = 1;    
;
----------------------------------------
/*
with temp_state as (
    SELECT DISTINCT residence_state as state, residence_region as region from test
)
SELECT state, count(*)
FROM temp_state
group by state
having count(*) > 1
ORDER BY region
;
SELECT *
FROM test
WHERE residence_state like "%unknown%";
--"Illinois","Ohio","Florida","Texas","California"
with temp_state as (
SELECT DISTINCT residence_state, residence_region, count(*) as num
FROM test
WHERE residence_state in (
        "Illinois",
        "Ohio",
        "Florida",
        "Texas",
        "California")
GROUP BY residence_state, residence_region
ORDER BY residence_state
)
SELECT residence_state, residence_region , max(num)
FROM temp_state
GROUP BY residence_state;

/*
California	South	1
California	Unknown	1
California	West	176
Florida	         South	92
Florida	         Unknown	2
Illinois	         Midwest	22
Illinois	         Unknown	2
Ohio	         Midwest	6
Ohio	         Unknown	1
Texas	         South	69
Texas	         Unknown	1
*/

/*
California	West	176
Florida	          South	92
Illinois	          Midwest	22
Ohio	          Midwest	6
Texas	          South	69
*/
