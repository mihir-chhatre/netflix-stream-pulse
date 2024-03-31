CREATE TABLE viewsByDeviceGenreAggregation (
    device_type VARCHAR(255),
    genre VARCHAR(255),
    view_count INT,
    window_end_utctime TIMESTAMP,
    PRIMARY KEY (device_type, genre, window_end_utctime)
);


CREATE TABLE viewsByGenderAgeGroupAggregation (
    gender VARCHAR(255),
    age_group VARCHAR(255),
    view_count INTEGER,
    window_end_utctime TIMESTAMP,
    PRIMARY KEY (gender, age_group, window_end_utctime)
);


CREATE TABLE viewsByLocationMRAggregation (
    country VARCHAR(255),
    maturity_rating VARCHAR(255),
    view_count INTEGER,
    window_end_utctime TIMESTAMP,
    PRIMARY KEY (country, maturity_rating, window_end_utctime)
);
