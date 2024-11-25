# Task09

> Автор: Дадыков Артемий, БПИ225.

## 1. Maths with String Manipulations

```sql
SELECT BIT_LENGTH(name) + CHARACTER_LENGTH(race) AS calculation
FROM demographics;
```

## 2. Bit Length

```sql
SELECT id,
       BIT_LENGTH(name) AS name,
       birthday,
       BIT_LENGTH(race) AS race
FROM demographics;
```

## 3. ASCII Converter

```sql
SELECT id,
       ASCII(SUBSTRING(name, 1, 1)) AS name,
       birthday,
       ASCII(SUBSTRING(race, 1, 1)) AS race
FROM demographics;
```

## 4. Concatenating Columns

```sql
SELECT CONCAT_WS(' ', prefix, first, last, suffix) AS title
FROM names;
```

## 5. Padding Encryption

```sql
SELECT LPAD(md5, LENGTH(sha256), '1')  AS md5,
       LPAD(sha1, LENGTH(sha256), '0') AS sha1,
       sha256
FROM encryption;
```

## 6. Right and Left

```sql
SELECT LEFT(project, commits)       AS project,
       RIGHT(address, contributors) AS address
FROM repositories;
```

## 7. Regex Replace

```sql
SELECT project,
       commits,
       contributors,
       REGEXP_REPLACE(address, '[0-9]', '!') AS address
FROM repositories;
```

## 8. Real Price

```sql
SELECT name,
       weight,
       price,
       ROUND((price / (weight / 1000)), 2) AS price_per_kg
FROM products
ORDER BY price_per_kg ASC,
         name ASC;
```