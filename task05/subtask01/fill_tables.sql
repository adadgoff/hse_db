INSERT INTO Publisher (PubName, PubAddress)
VALUES ('АСТ', 'Москва, ул. Красная Пресня, 12'),
       ('Эксмо', 'Москва, ул. Новослободская, 20'),
       ('Питер', 'Санкт-Петербург, ул. Лермонтова, 10');

INSERT INTO Book (ISBN, Title, Author, PagesNum, PubYear, PubName)
VALUES ('9785170104851', 'Путеводитель по Горам России', 'Алексей Смирнов', 320, 2015, 'АСТ'),
       ('9785699699826', 'Путешествия по миру', 'Ольга Петрова', 250, 2018, 'Эксмо'),
       ('9785392095191', 'Горы Кавказа', 'Иван Иванов', 280, 2020, 'Питер'),
       ('9785170761627', 'Русские походы', 'Дмитрий Волков', 400, 2021, 'АСТ'),
       ('9785961441906', 'Экстремальные экспедиции', 'Иван Иванов', 300, 2019, 'Питер');

INSERT INTO Category (CategoryName, ParentCat)
VALUES ('Горы', NULL),
       ('Путешествия', NULL),
       ('Походы', 'Путешествия');

INSERT INTO BookCat (ISBN, CategoryName)
VALUES ('9785170104851', 'Горы'),
       ('9785699699826', 'Путешествия'),
       ('9785392095191', 'Горы'),
       ('9785392095191', 'Путешествия'),
       ('9785170761627', 'Походы'),
       ('9785961441906', 'Горы');

INSERT INTO Copy (ISBN, CopyNumber, ShelfPosition)
VALUES ('9785170104851', 1, 'A-12'),
       ('9785699699826', 1, 'B-22'),
       ('9785392095191', 1, 'C-18'),
       ('9785170761627', 1, 'A-32'),
       ('9785961441906', 1, 'B-12');

INSERT INTO Reader (LastName, FirstName, Address, BirthDate)
VALUES ('Иванов', 'Иван', 'Москва, ул. Ленина, 15', '1985-06-15'),
       ('Петров', 'Александр', 'Москва, ул. Садовая, 9', '1990-03-22'),
       ('Смирнова', 'Мария', 'Москва, ул. Тверская, 4', '1995-11-30'),
       ('Волкова', 'Ольга', 'Москва, ул. Арбат, 22', '1987-08-14'),
       ('Кузнецов', 'Сергей', 'Санкт-Петербург, ул. Невский, 34', '1983-04-18'),
       ('Сидорова', 'Екатерина', 'Новосибирск, ул. Ленина, 12', '1992-07-22'),
       ('Николаев', 'Андрей', 'Екатеринбург, ул. Свердлова, 7', '1978-10-05'),
       ('Михайлова', 'Анна', 'Краснодар, ул. Победы, 15', '1989-01-25'),
       ('Федоров', 'Игорь', 'Казань, ул. Баумана, 4', '1995-09-10');


INSERT INTO Borrowing (ReaderNr, ISBN, CopyNumber, ReturnDate)
VALUES (1, '9785170104851', 1, '2023-01-15'),
       (1, '9785392095191', 1, '2023-03-10'),
       (2, '9785170761627', 1, '2023-02-05'),
       (3, '9785961441906', 1, '2023-03-12'),
       (4, '9785699699826', 1, NULL);
