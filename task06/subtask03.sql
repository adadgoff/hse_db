-- * Student( MatrNr, Name, Semester )
-- * Check( MatrNr, LectNr, ProfNr, Note )
-- * Lecture( LectNr, Title, Credit, ProfNr )
-- * Professor( ProfNr, Name, Room )

-- 1. Запрос возвращает имена и номера зачетных книжек (MatrNr) тех студентов,
-- которые никогда не получали оценку выше 4.0 по любой лекции.
SELECT s.Name, s.MatrNr FROM Student s
WHERE NOT EXISTS (
SELECT * FROM Check c WHERE c.MatrNr = s.MatrNr AND c.Note >= 4.0 ) ;

-- 2. Запрос показывает список всех профессоров и сумму кредитов всех лекций, которые он ведёт.
-- Для тех, кто не ведёт ни одной лекции, указано 0 кредитов.
( SELECT p.ProfNr, p.Name, sum(lec.Credit)
FROM Professor p, Lecture lec
WHERE p.ProfNr = lec.ProfNr
GROUP BY p.ProfNr, p.Name)
UNION
( SELECT p.ProfNr, p.Name, 0
FROM Professor p
WHERE NOT EXISTS (
SELECT * FROM Lecture lec WHERE lec.ProfNr = p.ProfNr ));

-- 3. Запрос выбирает имена студентов и их лучшие (максимальные) оценки, которые равны или выше 4.0.
-- То есть для каждого студента будет отображено его имя и максимальная оценка среди всех экзаменов,
-- которые он сдал (с оценкой не ниже 4.0).
SELECT s.Name, p.Note
FROM Student s, Lecture lec, Check c
WHERE s.MatrNr = c.MatrNr AND lec.LectNr = c.LectNr AND c.Note >= 4
AND c.Note >= ALL (
SELECT c1.Note FROM Check c1 WHERE c1.MatrNr = c.MatrNr )
