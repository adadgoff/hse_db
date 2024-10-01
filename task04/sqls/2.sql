CREATE TABLE City (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL UNIQUE,
    region VARCHAR NOT NULL UNIQUE
);

CREATE TABLE Station (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL UNIQUE,
    tracks INTEGER,
    city_id INTEGER NOT NULL,
    FOREIGN KEY (city_id) REFERENCES City(id)
);

CREATE TABLE Train (
    train_nr SERIAL PRIMARY KEY,
    length INTEGER,
    start_station_id INTEGER NOT NULL,
    end_station_id INTEGER NOT NULL,
    FOREIGN KEY (start_station_id) REFERENCES Station(id),
    FOREIGN KEY (end_station_id) REFERENCES Station(id)
);

CREATE TABLE Connected (
    id SERIAL PRIMARY KEY,
    from_station_id INTEGER NOT NULL,
    to_station_id INTEGER NOT NULL,
    departure TIMESTAMP NOT NULL,
    arrival TIMESTAMP NOT NULL,
    FOREIGN KEY (from_station_id) REFERENCES Station(id),
    FOREIGN KEY (to_station_id) REFERENCES Station(id)
);

CREATE TABLE TrainConnected (
    id SERIAL PRIMARY KEY,
    connected_id INTEGER NOT NULL,
    train_id INTEGER NOT NULL,
    FOREIGN KEY (connected_id) REFERENCES Connected(id),
    FOREIGN KEY (train_id) REFERENCES Train(train_nr)
);
