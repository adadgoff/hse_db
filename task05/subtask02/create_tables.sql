DROP TABLE IF EXISTS
    City,
    Station,
    Train,
    Connection;

CREATE TABLE City
(
    Name   TEXT,
    Region TEXT,
    PRIMARY KEY (Name, Region)
);

CREATE TABLE Station
(
    Name        TEXT PRIMARY KEY,
    TracksCount INT NOT NULL,
    CityName    TEXT,
    Region      TEXT,
    FOREIGN KEY (CityName, Region) REFERENCES City (Name, Region)
);

CREATE TABLE Train
(
    TrainNr          INT PRIMARY KEY,
    Length           INT NOT NULL,
    StartStationName TEXT,
    EndStationName   TEXT,
    FOREIGN KEY (StartStationName) REFERENCES Station (Name),
    FOREIGN KEY (EndStationName) REFERENCES Station (Name)
);

CREATE TABLE Connection
(
    FromStation TEXT,
    ToStation   TEXT,
    TrainNr     INT,
    Departure   TIMESTAMP NOT NULL,
    Arrival     TIMESTAMP NOT NULL,
    FOREIGN KEY (FromStation) REFERENCES Station (Name),
    FOREIGN KEY (ToStation) REFERENCES Station (Name),
    FOREIGN KEY (TrainNr) REFERENCES Train (TrainNr)
);
