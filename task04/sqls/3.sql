CREATE TABLE Station (
    stat_nr SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL UNIQUE
);

CREATE TABLE Room (
    room_nr SERIAL PRIMARY KEY,
    station_id INTEGER NOT NULL,
    beds INTEGER NOT NULL,
    FOREIGN KEY (station_id) REFERENCES Station(stat_nr)
);

CREATE TABLE StationPersonell (
    pers_nr SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    station_id INTEGER NOT NULL,
    FOREIGN KEY (station_id) REFERENCES Station(stat_nr)
);

CREATE TABLE Doctor (
    id INTEGER PRIMARY KEY,
    area VARCHAR NOT NULL,
    rank VARCHAR NOT NULL,
    FOREIGN KEY (id) REFERENCES StationPersonell(pers_nr)
);

CREATE TABLE Caregiver (
    id INTEGER PRIMARY KEY,
    qualification VARCHAR NOT NULL,
    FOREIGN KEY (id) REFERENCES StationPersonell(pers_nr)
);

CREATE TABLE Patient (
    patient_nr SERIAL PRIMARY KEY,
    treated_by_id INTEGER NOT NULL,
    room_id INTEGER NOT NULL,
    name VARCHAR NOT NULL,
    disease VARCHAR NOT NULL,
    admission_from TIMESTAMP NOT NULL,
    admission_to TIMESTAMP,
    FOREIGN KEY (treated_by_id) REFERENCES Doctor(id),
    FOREIGN KEY (room_id) REFERENCES Room(room_nr)
);