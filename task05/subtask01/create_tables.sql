DROP TABLE IF EXISTS
    Publisher,
    Book,
    BookCat,
    Category,
    Copy,
    Reader,
    Borrowing;

CREATE TABLE Publisher
(
    PubName    VARCHAR(100) PRIMARY KEY,
    PubAddress VARCHAR(255) NOT NULL
);

CREATE TABLE Book
(
    ISBN     CHAR(13) PRIMARY KEY,
    Title    VARCHAR(255) NOT NULL,
    Author   VARCHAR(100) NOT NULL,
    PagesNum INT          NOT NULL,
    PubYear  INT          NOT NULL,
    PubName  VARCHAR(100),
    FOREIGN KEY (PubName) REFERENCES Publisher (PubName) ON DELETE SET NULL
);

CREATE TABLE Category
(
    CategoryName VARCHAR(100) PRIMARY KEY,
    ParentCat    VARCHAR(100),
    FOREIGN KEY (ParentCat) REFERENCES Category (CategoryName) ON DELETE SET NULL
);

CREATE TABLE BookCat
(
    ISBN         CHAR(13),
    CategoryName VARCHAR(100),
    PRIMARY KEY (ISBN, CategoryName),
    FOREIGN KEY (ISBN) REFERENCES Book (ISBN) ON DELETE CASCADE,
    FOREIGN KEY (CategoryName) REFERENCES Category (CategoryName) ON DELETE CASCADE
);

CREATE TABLE Copy
(
    ISBN          CHAR(13),
    CopyNumber    INT,
    ShelfPosition VARCHAR(50),
    PRIMARY KEY (ISBN, CopyNumber),
    FOREIGN KEY (ISBN) REFERENCES Book (ISBN) ON DELETE CASCADE
);

CREATE TABLE Reader
(
    ID        SERIAL PRIMARY KEY,
    LastName  VARCHAR(100) NOT NULL,
    FirstName VARCHAR(100) NOT NULL,
    Address   VARCHAR(255) NOT NULL,
    BirthDate DATE         NOT NULL
);

CREATE TABLE Borrowing
(
    ReaderNr   INT,
    ISBN       CHAR(13),
    CopyNumber INT,
    ReturnDate DATE,
    PRIMARY KEY (ReaderNr, ISBN, CopyNumber),
    FOREIGN KEY (ReaderNr) REFERENCES Reader (ID) ON DELETE CASCADE,
    FOREIGN KEY (ISBN, CopyNumber) REFERENCES Copy (ISBN, CopyNumber) ON DELETE CASCADE
);
