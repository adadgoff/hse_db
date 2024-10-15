-- * Добавьте запись о бронировании читателем ‘Василеем Петровым’ книги с ISBN 123456 и номером копии 4.
INSERT INTO Borrowing (ReaderNr, ISBN, CopyNumber, ReturnDate)
SELECT r.ID, '123456', 4, NULL
FROM Reader r
WHERE r.FirstName = 'Василий'
  AND r.LastName = 'Петров';

-- * Удалить все книги, год публикации которых превышает 2000 год.
DELETE
FROM Book
WHERE PubYear > 2000;

-- * Измените дату возврата для всех книг категории "Базы данных", начиная с 01.01.2016,
-- чтобы они были в заимствовании на 30 дней дольше (предположим, что в SQL можно добавлять числа к датам).
UPDATE Borrowing br
SET ReturnDate = ReturnDate + INTERVAL '30' DAY
WHERE br.ISBN IN (SELECT bc.ISBN
                  FROM BookCat bc
                           JOIN Category c ON bc.CategoryName = c.CategoryName
                  WHERE c.CategoryName = 'Базы данных')
  AND br.ReturnDate >= '2016-01-01';
