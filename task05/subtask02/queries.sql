-- а) Найдите все прямые рейсы из Москвы в Тверь.
SELECT *
FROM Connection
WHERE FromStation = 'Москва'
  AND ToStation = 'Тверь';


-- б) Найдите все многосегментные маршруты, имеющие точно однодневный трансфер из Москвы в Санкт-Петербург
-- (первое отправление и прибытие в конечную точку должны быть в одну и ту же дату).
-- Вы можете применить функцию DAY () к атрибутам Departure и Arrival, чтобы определить дату.
SELECT c1.*, c2.*
FROM Connection c1
         JOIN Connection c2 ON c1.ToStation = c2.FromStation
WHERE c1.FromStation = 'Москва'
  AND c2.ToStation = 'Санкт-Петербург'
  AND c1.Departure::date = c2.Arrival::date;
