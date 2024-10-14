-- а) Какие фамилии читателей в Москве?
SELECT LastName as "Московские читатели"
FROM Reader
WHERE LOWER(Address) LIKE '%москва%';

-- б) Какие книги (author, title) брал Иван Иванов?
SELECT Book.Author, Book.Title
FROM Borrowing
         JOIN Book ON Book.ISBN = Borrowing.ISBN
         JOIN Reader ON Reader.ID = Borrowing.ReaderNr
WHERE Reader.LastName = 'Иванов'
  AND Reader.FirstName = 'Иван';

-- в) Какие книги (ISBN) из категории "Горы" не относятся к категории "Путешествия"?
-- Подкатегории не обязательно принимать во внимание!
SELECT bc1.ISBN
FROM BookCat bc1
         LEFT JOIN BookCat bc2 ON bc1.ISBN = bc2.ISBN AND bc2.CategoryName = 'Путешествия'
WHERE bc1.CategoryName = 'Горы'
  AND bc2.ISBN IS NULL;

-- г) Какие читатели (LastName, FirstName) вернули копию книги?
SELECT r.LastName, r.FirstName
FROM Borrowing br
         JOIN Reader r ON br.ReaderNr = r.ID
WHERE br.ReturnDate IS NOT NULL;

-- д) Какие читатели (LastName, FirstName) брали хотя бы одну книгу (не копию),
-- которую брал также Иван Иванов (не включайте Ивана Иванова в результат)?
SELECT DISTINCT r.LastName, r.FirstName
FROM Borrowing br1
         JOIN Borrowing br2 ON br1.ISBN = br2.ISBN AND br1.ReaderNr != br2.ReaderNr
         JOIN Reader r ON br2.ReaderNr = r.ID
         JOIN Reader r_ivan ON br1.ReaderNr = r_ivan.ID
WHERE r_ivan.LastName = 'Иванов'
  AND r_ivan.FirstName = 'Иван'
  AND r.LastName != 'Иванов'
  AND r.FirstName != 'Иван';
