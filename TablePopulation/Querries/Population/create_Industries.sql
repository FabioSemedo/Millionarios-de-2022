DROP TABLE Industries;

CREATE TABLE Industries(
    industryID INTEGER PRIMARY KEY NOT NULL,
    name TEXT NOT NULL UNIQUE
)
;

INSERT INTO Industries(name)
SELECT DISTINCT industry
FROM test
ORDER BY industry
RETURNING *;
-------------------------------------------------

--CHECK industry ~~~~~ atomic, character encoding
SELECT distinct industry
from test
WHERE industry glob "*[^-A-Za-z0-9 ]*" OR industry in ("Food")
order by industry;