## Задание 2

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

4. Создайте полнотекстовый индекс:
    ```sql
    CREATE INDEX t_books_fts_idx ON t_books 
    USING GIN (to_tsvector('english', title));
    ```

5. Найдите книги, содержащие слово 'expert':
    ```sql
    EXPLAIN ANALYZE
    SELECT * FROM t_books 
    WHERE to_tsvector('english', title) @@ to_tsquery('english', 'expert');
    ```

   *План выполнения:*
    ```
    Bitmap Heap Scan on t_books  (cost=21.03..1336.08 rows=750 width=33) (actual time=0.017..0.018 rows=1 loops=1)
      Recheck Cond: (to_tsvector('english'::regconfig, (title)::text) @@ '''expert'''::tsquery)"
      Heap Blocks: exact=1
      ->  Bitmap Index Scan on t_books_fts_idx  (cost=0.00..20.84 rows=750 width=0) (actual time=0.013..0.013 rows=1 loops=1)
            Index Cond: (to_tsvector('english'::regconfig, (title)::text) @@ '''expert'''::tsquery)"
    Planning Time: 0.442 ms
    Execution Time: 0.055 ms

    ```

   *Объясните результат:*
   Запрос использует Bitmap Heap Scan, чтобы эффективно найти строки, содержащие слово 'expert', используя
   полнотекстовый индекс. Битовая карта сначала отбирает потенциально подходящие страницы, а затем для каждой записи
   выполняется дополнительная проверка с помощью Recheck Cond.

6. Удалите индекс:
    ```sql
    DROP INDEX t_books_fts_idx;
    ```

7. Создайте таблицу lookup:
    ```sql
    CREATE TABLE t_lookup (
         item_key VARCHAR(10) NOT NULL,
         item_value VARCHAR(100)
    );
    ```

8. Добавьте первичный ключ:
    ```sql
    ALTER TABLE t_lookup 
    ADD CONSTRAINT t_lookup_pk PRIMARY KEY (item_key);
    ```

9. Заполните данными:
    ```sql
    INSERT INTO t_lookup 
    SELECT 
         LPAD(CAST(generate_series(1, 150000) AS TEXT), 10, '0'),
         'Value_' || generate_series(1, 150000);
    ```

10. Создайте кластеризованную таблицу:
     ```sql
     CREATE TABLE t_lookup_clustered (
          item_key VARCHAR(10) PRIMARY KEY,
          item_value VARCHAR(100)
     );
     ```

11. Заполните её теми же данными:
     ```sql
     INSERT INTO t_lookup_clustered 
     SELECT * FROM t_lookup;
     
     CLUSTER t_lookup_clustered USING t_lookup_clustered_pkey;
     ```

12. Обновите статистику:
     ```sql
     ANALYZE t_lookup;
     ANALYZE t_lookup_clustered;
     ```

13. Выполните поиск по ключу в обычной таблице:
     ```sql
     EXPLAIN ANALYZE
     SELECT * FROM t_lookup WHERE item_key = '0000000455';
     ```

    *План выполнения:*
    ```
    Index Scan using t_lookup_pk on t_lookup  (cost=0.42..8.44 rows=1 width=23) (actual time=0.010..0.011 rows=1 loops=1)
      Index Cond: ((item_key)::text = '0000000455'::text)
    Planning Time: 0.113 ms
    Execution Time: 0.020 ms
    ```

    *Объясните результат:*
    Запрос использует Index Scan, чтобы быстро найти строку с ключом '0000000455' благодаря индексу t_lookup_pk.

14. Выполните поиск по ключу в кластеризованной таблице:
     ```sql
     EXPLAIN ANALYZE
     SELECT * FROM t_lookup_clustered WHERE item_key = '0000000455';
     ```

    *План выполнения:*
    ```
    Index Scan using t_lookup_clustered_pkey on t_lookup_clustered  (cost=0.42..8.44 rows=1 width=23) (actual time=0.067..0.069 rows=1 loops=1)
      Index Cond: ((item_key)::text = '0000000455'::text)
    Planning Time: 0.169 ms
    Execution Time: 0.085 ms
    ```

    *Объясните результат:*
    Запрос использует Index Scan для поиска записи с ключом '0000000455', аналогично некластеризованной таблице. Порядок
    данных, установленный с помощью CLUSTER, не влияет на производительность, так как запрос обращается к индексу, а не
    к упорядоченности таблицы.

15. Создайте индекс по значению для обычной таблицы:
     ```sql
     CREATE INDEX t_lookup_value_idx ON t_lookup(item_value);
     ```

16. Создайте индекс по значению для кластеризованной таблицы:
     ```sql
     CREATE INDEX t_lookup_clustered_value_idx 
     ON t_lookup_clustered(item_value);
     ```

17. Выполните поиск по значению в обычной таблице:
     ```sql
     EXPLAIN ANALYZE
     SELECT * FROM t_lookup WHERE item_value = 'T_BOOKS';
     ```

    *План выполнения:*
    ```
    Index Scan using t_lookup_value_idx on t_lookup  (cost=0.42..8.44 rows=1 width=23) (actual time=0.032..0.033 rows=0 loops=1)
      Index Cond: ((item_value)::text = 'T_BOOKS'::text)
    Planning Time: 0.228 ms
    Execution Time: 0.049 ms
    ```

    *Объясните результат:*
    Запрос использует Index Scan по индексу t_lookup_value_idx, чтобы эффективно найти строки с указанным значением
    item_value. Поскольку значения равенства нет в таблице, результатом будет пустой набор строк, но индекс помогает
    избежать полного сканирования таблицы.

18. Выполните поиск по значению в кластеризованной таблице:
     ```sql
     EXPLAIN ANALYZE
     SELECT * FROM t_lookup_clustered WHERE item_value = 'T_BOOKS';
     ```

    *План выполнения:*
    ```
    Index Scan using t_lookup_clustered_value_idx on t_lookup_clustered  (cost=0.42..8.44 rows=1 width=23) (actual time=0.025..0.026 rows=0 loops=1)
      Index Cond: ((item_value)::text = 'T_BOOKS'::text)
    Planning Time: 0.194 ms
    Execution Time: 0.039 ms
    ```

    *Объясните результат:*
    Запрос также использует Index Scan по индексу t_lookup_clustered_value_idx для поиска строк с заданным значением
    item_value. Как и в случае с некластеризованной таблицей, результатом является пустой набор строк, но использование
    индекса минимизирует затраты на выполнение.

19. Сравните производительность поиска по значению в обычной и кластеризованной таблицах:

    *Сравнение:*
    И в обычной, и в кластеризованной таблицах поиск по значению с использованием индекса имеет схожую
    производительность. Кластеризация не влияет на скорость таких запросов.