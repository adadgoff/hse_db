# Задание 1: BRIN индексы и bitmap-сканирование

1. Удалите старую базу данных, если есть:
   ```shell
   docker compose down
   ```

2. Поднимите базу данных из src/docker-compose.yml:
   ```shell
   docker compose down && docker compose up -d
   ```

3. Обновите статистику:
   ```sql
   ANALYZE t_books;
   ```

4. Создайте BRIN индекс по колонке category:
   ```sql
   CREATE INDEX t_books_brin_cat_idx ON t_books USING brin(category);
   ```

5. Найдите книги с NULL значением category:
   ```sql
   EXPLAIN ANALYZE
   SELECT * FROM t_books WHERE category IS NULL;
   ```

   *План выполнения:*
   ```
   Bitmap Heap Scan on t_books  (cost=12.00..16.01 rows=1 width=33) (actual time=0.012..0.013 rows=0 loops=1)
     Recheck Cond: (category IS NULL)
     ->  Bitmap Index Scan on t_books_brin_cat_idx  (cost=0.00..12.00 rows=1 width=0) (actual time=0.011..0.011 rows=0 loops=1)
           Index Cond: (category IS NULL)
   Planning Time: 0.215 ms
   Execution Time: 0.043 ms
   ```

   *Объясните результат:*
   BRIN индекс хранит информацию о наличии или отсутствии NULL значений на уровне страниц, что позволяет исключить из
   обработки страницы, не содержащие нужных данных. Планировщик запросов использовал эту возможность,
   применив Bitmap Index Scan совместно с BRIN индексом. Затем с помощью Bitmap Heap Scan
   были обработаны оставшиеся страницы, где для каждой записи дополнительно проверялось условие на NULL категорию.

6. Создайте BRIN индекс по автору:
   ```sql
   CREATE INDEX t_books_brin_author_idx ON t_books USING brin(author);
   ```

7. Выполните поиск по категории и автору:
   ```sql
   EXPLAIN ANALYZE
   SELECT * FROM t_books 
   WHERE category = 'INDEX' AND author = 'SYSTEM';
   ```

   *План выполнения:*
   ```
   Bitmap Heap Scan on t_books  (cost=12.17..2411.51 rows=1 width=33) (actual time=23.400..23.401 rows=0 loops=1)
     Recheck Cond: ((category)::text = 'INDEX'::text)
     Rows Removed by Index Recheck: 150000
     Filter: ((author)::text = 'SYSTEM'::text)
     Heap Blocks: lossy=1224
     ->  Bitmap Index Scan on t_books_brin_cat_idx  (cost=0.00..12.17 rows=78356 width=0) (actual time=0.114..0.114 rows=12240 loops=1)
           Index Cond: ((category)::text = 'INDEX'::text)
   Planning Time: 0.316 ms
   Execution Time: 23.434 ms
   ```

   *Объясните результат (обратите внимание на bitmap scan):*
   В данном случае BRIN индекс был использован для исключения страниц, которые точно не содержат записи с 'INDEX'
   категории. Категории содержат небольшое количество уникальных значений, что
   позволяет BRIN индексу эффективно отсекать значительное количество страниц.

8. Получите список уникальных категорий:
   ```sql
   EXPLAIN ANALYZE
   SELECT DISTINCT category 
   FROM t_books 
   ORDER BY category;
   ```

   *План выполнения:*
   ```
   Sort  (cost=3099.14..3099.15 rows=6 width=7) (actual time=32.518..32.519 rows=6 loops=1)
     Sort Key: category
     Sort Method: quicksort  Memory: 25kB
     ->  HashAggregate  (cost=3099.00..3099.06 rows=6 width=7) (actual time=32.509..32.511 rows=6 loops=1)
           Group Key: category
           Batches: 1  Memory Usage: 24kB
           ->  Seq Scan on t_books  (cost=0.00..2724.00 rows=150000 width=7) (actual time=0.007..8.255 rows=150000 loops=1)
   Planning Time: 0.096 ms
   Execution Time: 32.542 ms
   ```

   *Объясните результат:*
   В этом случае PostgreSQL не обладает сведениями о распределении значений в столбце category. Планировщик
   производит полный обход таблицы, выполняя группировку записей по столбцу category с применением метода
   HashAggregate, а затем сортирует полученные значения.

9. Подсчитайте книги, где автор начинается на 'S':
   ```sql
   EXPLAIN ANALYZE
   SELECT COUNT(*) 
   FROM t_books 
   WHERE author LIKE 'S%';
   ```

   *План выполнения:*
   ```
   Aggregate  (cost=3099.04..3099.05 rows=1 width=8) (actual time=15.882..15.883 rows=1 loops=1)
     ->  Seq Scan on t_books  (cost=0.00..3099.00 rows=15 width=0) (actual time=15.878..15.879 rows=0 loops=1)
           Filter: ((author)::text ~~ 'S%'::text)
           Rows Removed by Filter: 150000
   Planning Time: 0.085 ms
   Execution Time: 15.906 ms
   ```

   *Объясните результат:*
   BRIN индекс не поддерживает индексацию паттернов, поэтому планировщик выбирает
   последовательное сканирование с применением фильтра. После этого для подсчета
   подходящих записей используется метод агрегирования.

10. Создайте индекс для регистронезависимого поиска:
    ```sql
    CREATE INDEX t_books_lower_title_idx ON t_books(LOWER(title));
    ```

11. Подсчитайте книги, начинающиеся на 'O':
    ```sql
    EXPLAIN ANALYZE
    SELECT COUNT(*) 
    FROM t_books 
    WHERE LOWER(title) LIKE 'o%';
    ```

*План выполнения:*
```
Aggregate (cost=3475.88..3475.89 rows=1 width=8) (actual time=45.311..45.312 rows=1 loops=1)
  ->  Seq Scan on t_books  (cost=0.00..3474.00 rows=750 width=0) (actual time=45.305..45.307 rows=1 loops=1)
        Filter: (lower((title)::text) ~~ 'o%'::text)
        Rows Removed by Filter: 149999
Planning Time: 0.257 ms
Execution Time: 45.333 ms
```

*Объясните результат:*
Несмотря на создание индекса B-Tree для колонки, этот индекс не поддерживает поиск по шаблонам.

12. Удалите созданные индексы:
    ```sql
    DROP INDEX t_books_brin_cat_idx;
    DROP INDEX t_books_brin_author_idx;
    DROP INDEX t_books_lower_title_idx;
    ```

13. Создайте составной BRIN индекс:
    ```sql
    CREATE INDEX t_books_brin_cat_auth_idx ON t_books 
    USING brin(category, author);
    ```

14. Повторите запрос из шага 7:
    ```sql
    EXPLAIN ANALYZE
    SELECT * FROM t_books 
    WHERE category = 'INDEX' AND author = 'SYSTEM';
    ```

*План выполнения:*
```
Bitmap Heap Scan on t_books  (cost=12.17..2411.51 rows=1 width=33) (actual time=2.561..2.562 rows=0 loops=1)
  Recheck Cond: (((category)::text = 'INDEX'::text) AND ((author)::text = 'SYSTEM'::text))
  Rows Removed by Index Recheck: 8812
  Heap Blocks: lossy=72
  ->  Bitmap Index Scan on t_books_brin_cat_auth_idx  (cost=0.00..12.17 rows=78356 width=0) (actual time=0.039..0.039 rows=720 loops=1)
        Index Cond: (((category)::text = 'INDEX'::text) AND ((author)::text = 'SYSTEM'::text))
Planning Time: 0.255 ms
Execution Time: 2.597 ms
```   

*Объясните результат:*
Использование составного BRIN индекса помогло избежать фильтрации после проверки условия и сразу отсеять страницы, на
которых нет нужных значений в колонках category или author.