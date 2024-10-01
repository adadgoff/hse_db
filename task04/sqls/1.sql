CREATE TABLE Publisher (
    id SERIAL PRIMARY KEY,
    publisher_name VARCHAR NOT NULL,
    address VARCHAR NOT NULL
);

CREATE TABLE Category (
    id SERIAL PRIMARY KEY,
    category_name VARCHAR NOT NULL,
    parent_category_id INTEGER,
    FOREIGN KEY (parent_category_id) REFERENCES Category(id)
);

CREATE TABLE Book (
    id SERIAL PRIMARY KEY,
    ISBN VARCHAR NOT NULL,
    title VARCHAR NOT NULL,
    author VARCHAR NOT NULL,
    publication_year INTEGER NOT NULL,
    pages_count INTEGER NOT NULL,
    publisher_id INTEGER NOT NULL,
    category_id INTEGER,
    FOREIGN KEY (publisher_id) REFERENCES Publisher(id),
    FOREIGN KEY (category_id) REFERENCES Category(id)
);

CREATE TABLE Reader (
    id SERIAL PRIMARY KEY,
    last_name VARCHAR NOT NULL,
    first_name VARCHAR NOT NULL,
    address VARCHAR NOT NULL,
    birth_date DATE NOT NULL
);

CREATE TABLE Copy (
    id SERIAL PRIMARY KEY,
    shelf_location VARCHAR NOT NULL,
    return_date DATE,
    book_id INTEGER NOT NULL,
    reader_id INTEGER,
    FOREIGN KEY (book_id) REFERENCES Book(id),
    FOREIGN KEY (reader_id) REFERENCES Reader(id)
);