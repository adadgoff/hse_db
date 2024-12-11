## Задание 3

1. Создайте таблицу с большим количеством данных:
    ```sql
    CREATE TABLE test_cluster AS 
    SELECT 
        generate_series(1,1000000) as id,
        CASE WHEN random() < 0.5 THEN 'A' ELSE 'B' END as category,
        md5(random()::text) as data;
    ```

2. Создайте индекс:
    ```sql
    CREATE INDEX test_cluster_cat_idx ON test_cluster(category);
    ```

3. Измерьте производительность до кластеризации:
    ```sql
    EXPLAIN ANALYZE
    SELECT * FROM test_cluster WHERE category = 'A';
    ```

   *План выполнения:*
    ```
    Bitmap Heap Scan on test_cluster  (cost=59.17..7696.73 rows=5000 width=68) (actual time=21.692..65.618 rows=500755 loops=1)
      Recheck Cond: (category = 'A'::text)
      Heap Blocks: exact=8334
      ->  Bitmap Index Scan on test_cluster_cat_idx  (cost=0.00..57.92 rows=5000 width=0) (actual time=20.243..20.243 rows=500755 loops=1)
            Index Cond: (category = 'A'::text)
    Planning Time: 0.092 ms
    Execution Time: 76.794 ms
    ```

   *Объясните результат:*
   Запрос использует Bitmap Heap Scan, чтобы отобрать строки с категорией A, а большое количество разрозненных блоков
   данных увеличивает время выполнения.

4. Выполните кластеризацию:
    ```sql
    CLUSTER test_cluster USING test_cluster_cat_idx;
    ```

   *Результат:*
    ```
    workshop.public> CLUSTER test_cluster USING test_cluster_cat_idx
    [2024-12-12 00:41:16] completed in 1 s 90 ms
    ```

5. Измерьте производительность после кластеризации:
    ```sql
    EXPLAIN ANALYZE
    SELECT * FROM test_cluster WHERE category = 'A';
    ```

   *План выполнения:*
    ```
    Bitmap Heap Scan on test_cluster  (cost=5578.78..20168.19 rows=500433 width=39) (actual time=12.112..53.058 rows=500755 loops=1)
      Recheck Cond: (category = 'A'::text)
      Heap Blocks: exact=4173
      ->  Bitmap Index Scan on test_cluster_cat_idx  (cost=0.00..5453.67 rows=500433 width=0) (actual time=11.598..11.598 rows=500755 loops=1)
            Index Cond: (category = 'A'::text)
    Planning Time: 0.123 ms
    Execution Time: 63.571 ms
    ```

   *Объясните результат:*
   После кластеризации запрос также использует Bitmap Heap Scan, но меньшее количество разбросанных блоков (Heap Blocks)
   приводит к небольшому сокращению времени выполнения.

6. Сравните производительность до и после кластеризации:

   *Сравнение:*
   После кластеризации производительность улучшилась за счет упорядоченности данных, что уменьшило число обрабатываемых
   блоков и время выполнения запроса.