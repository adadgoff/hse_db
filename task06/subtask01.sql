-- * Показать все названия книг вместе с именами издателей.
SELECT Book.Title, Publisher.PubName
FROM Book
         JOIN Publisher ON Book.PubName = Publisher.PubName;

-- * В какой книге наибольшее количество страниц?
SELECT Title, PagesNum
FROM Book
ORDER BY PagesNum DESC
LIMIT 1;

-- * Какие авторы написали более 5 книг?
SELECT Author, COUNT(*) AS BookCount
FROM Book
GROUP BY Author
HAVING COUNT(*) > 5;

-- * В каких книгах более чем в два раза больше страниц, чем среднее количество страниц для всех книг?
WITH AvgPages AS (SELECT AVG(PagesNum) AS AvgPageCount
                  FROM Book)
SELECT Title, PagesNum
FROM Book,
     AvgPages
WHERE PagesNum > 2 * AvgPages.AvgPageCount;

-- * Какие категории содержат подкатегории?
SELECT DISTINCT ParentCat
FROM Category
WHERE ParentCat IS NOT NULL;

-- * У какого автора (предположим, что имена авторов уникальны) написано максимальное количество книг?
SELECT Author, COUNT(*) AS BookCount
FROM Book
GROUP BY Author
ORDER BY BookCount DESC
LIMIT 1;

-- * Какие читатели забронировали все книги (не копии), написанные "Марком Твеном"?
WITH TwainBooks AS (SELECT DISTINCT br.ReaderNr, br.ISBN
                    FROM Borrowing br
                             INNER JOIN Book b ON br.ISBN = b.ISBN
                    WHERE b.Author = 'Марк Твен')
SELECT ReaderNr
FROM TwainBooks
GROUP BY ReaderNr
HAVING COUNT(ISBN) = (SELECT COUNT(ISBN)
                      FROM Book
                      WHERE Author = 'Марк Твен');

-- * Какие книги имеют более одной копии?
SELECT Book.Title, COUNT(*) AS CopyCount
FROM Copy
         JOIN Book ON Copy.ISBN = Book.ISBN
GROUP BY Book.Title
HAVING COUNT(*) > 1;

-- * ТОП 10 самых старых книг
SELECT Title, PubYear
FROM Book
ORDER BY PubYear
LIMIT 10;

-- * Перечислите все категории в категории “Спорт” (с любым уровнем вложености).
WITH RECURSIVE Subcategories AS (SELECT CategoryName
                                 FROM Category
                                 WHERE CategoryName = 'Спорт'

                                 UNION ALL

                                 SELECT c.CategoryName
                                 FROM Category c
                                          JOIN Subcategories s ON c.ParentCat = s.CategoryName)
SELECT CategoryName
FROM Subcategories;
