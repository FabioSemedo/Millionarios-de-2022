CREATE TABLE CountryDetails (
    countryNameID  INTEGER NOT NULL
                           PRIMARY KEY,
    cpi            REAL    NOT NULL,
    cpi_change     REAL    NOT NULL,
    gdp            INTEGER NOT NULL,
    grs_trt_enroll REAL    NOT NULL,
    grs_prm_enroll REAL    NOT NULL,
    life_expect    INTEGER NOT NULL,
    tax_rev        REAL    NOT NULL,
    tax_rate       REAL    NOT NULL,
    population     INTEGER NOT NULL,
    latitude       REAL    NOT NULL,
    longitude      REAL    NOT NULL,
    continent      TEXT    NOT NULL
    CHECK (continent IN ("Europe", "North America", "South America", "Asia", "Oceania", "Africa") ) 
);
