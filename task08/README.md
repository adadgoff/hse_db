# Task08

> Автор: Дадыков Артемий, БПИ225.
> Используемый диалект: Oracle PL/SQL

# Решение заданий

## Задание 1: Создание хранимой процедуры для добавления новой работы

**Создание процедуры:**

```sql
CREATE OR REPLACE PROCEDURE NEW_JOB(
    p_job_id VARCHAR,
    p_job_title VARCHAR,
    p_min_salary INTEGER
) AS
BEGIN
INSERT INTO jobs (job_id, job_title, min_salary, max_salary)
VALUES (p_job_id, p_job_title, p_min_salary, p_min_salary * 2);
END;
/
```

**Вызов процедуры:**

```sql
EXEC NEW_JOB('SY_ANAL', 'System Analyst', 6000);
```

## Задание 2: Создание процедуры для добавления записи в JOB_HISTORY

**Создание процедуры:**

```sql
CREATE OR REPLACE PROCEDURE ADD_JOB_HIST(
    p_employee_id INTEGER,
    p_new_job_id VARCHAR
) AS v_hire_date DATE;
v_min_salary INTEGER;
BEGIN
    -- Получение даты найма и минимальной зарплаты новой должности
SELECT hire_date
INTO v_hire_date
FROM employees
WHERE employee_id = p_employee_id;
SELECT min_salary
INTO v_min_salary
FROM jobs
WHERE job_id = p_new_job_id;

-- Добавление записи в JOB_HISTORY
INSERT INTO job_history (employee_id, start_date, end_date, job_id, department_id)
VALUES (p_employee_id, v_hire_date, CURRENT_DATE, p_new_job_id, NULL);

-- Обновление записи в EMPLOYEES
UPDATE employees
SET hire_date = CURRENT_DATE,
    job_id    = p_new_job_id,
    salary    = v_min_salary + 500
WHERE employee_id = p_employee_id;

EXCEPTION
    WHEN NO_DATA_FOUND THEN
        DBMS_OUTPUT.PUT_LINE('Ошибка: сотрудник или работа не найдены.');
END;
/
```

**Вызов процедуры:**

1. Отключить триггеры:

```sql
ALTER TABLE employees
    DISABLE ALL TRIGGERS;
ALTER TABLE jobs
    DISABLE ALL TRIGGERS;
ALTER TABLE job_history
    DISABLE ALL TRIGGERS;
```

2. Выполнение процедуры:

```sql
EXEC ADD_JOB_HIST(106, 'SY_ANAL');
```

3. Проверка изменений:

```sql
SELECT *
FROM job_history
WHERE employee_id = 106;
SELECT *
FROM employees
WHERE employee_id = 106;
COMMIT;
```

4. Включить триггеры:

```sql
ALTER TABLE employees
    ENABLE ALL TRIGGERS;
ALTER TABLE jobs
    ENABLE ALL TRIGGERS;
ALTER TABLE job_history
    ENABLE ALL TRIGGERS;
```

## Задание 3: Обновление зарплат для должности

**Создание процедуры:**

```sql
CREATE OR REPLACE PROCEDURE UPD_JOBSAL(
    p_job_id VARCHAR,
    p_new_min_salary INTEGER,
    p_new_max_salary INTEGER
) AS
BEGIN
-- Проверка, что максимальная зарплата >= минимальной
IF p_new_max_salary < p_new_min_salary THEN
        RAISE_APPLICATION_ERROR(-20001, 'Максимальная зарплата должна быть больше или равна минимальной.');
END IF;

-- Обновление зарплат
UPDATE jobs
SET min_salary = p_new_min_salary,
    max_salary = p_new_max_salary
WHERE job_id = p_job_id;

EXCEPTION
    WHEN OTHERS THEN
        IF SQLCODE = -54 THEN
            DBMS_OUTPUT.PUT_LINE('Запись заблокирована.');
ELSE
            RAISE;
END IF;
END;
/
```

**Выполнение шагов:**

1. Отключить триггеры:

```sql
ALTER TABLE employees
    DISABLE ALL TRIGGERS;
ALTER TABLE jobs
    DISABLE ALL TRIGGERS;
```

2. Выполнение процедуры с ошибкой:

```sql
EXEC UPD_JOBSAL('SY_ANAL', 7000, 140);
```

Ошибка: максимальная зарплата меньше минимальной.

3. Исправленный вызов:

```sql
EXEC UPD_JOBSAL('SY_ANAL', 7000, 14000);
```

4. Проверка изменений:

```sql
SELECT *
FROM jobs
WHERE job_id = 'SY_ANAL';
COMMIT;
```

5. Включить триггеры:

```sql
ALTER TABLE employees
    ENABLE ALL TRIGGERS;
ALTER TABLE jobs
    ENABLE ALL TRIGGERS;
```

## Задание 4: Функция для подсчета лет работы сотрудника

**Создание функции:**

```sql
CREATE OR REPLACE FUNCTION GET_YEARS_SERVICE(
    p_employee_id INTEGER
)
RETURN INTEGER AS
    v_hire_date DATE;
v_years INTEGER;
BEGIN
SELECT hire_date
INTO v_hire_date
FROM employees
WHERE employee_id = p_employee_id;
v_years := TRUNC(MONTHS_BETWEEN(SYSDATE, v_hire_date) / 12);
RETURN v_years;

EXCEPTION
    WHEN NO_DATA_FOUND THEN
        RAISE_APPLICATION_ERROR(-20002, 'Сотрудник не найден.');
END;
/
```

**Вызов функции:**

```sql
BEGIN
DBMS_OUTPUT.PUT_LINE('Years of service: ' || GET_YEARS_SERVICE(999));
EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE(SQLERRM);
END;

DBMS_OUTPUT.PUT_LINE('Years of service for 106: ' || GET_YEARS_SERVICE(106));
```

## Задание 5: Функция для подсчета уникальных должностей сотрудника

**Создание функции:**

```sql
CREATE OR REPLACE FUNCTION GET_JOB_COUNT(
    p_employee_id INTEGER
)
RETURN INTEGER AS
    v_job_count INTEGER;
BEGIN
SELECT COUNT(DISTINCT job_id)
INTO v_job_count
FROM (SELECT job_id
      FROM job_history
      WHERE employee_id = p_employee_id
      UNION
      SELECT job_id
      FROM employees
      WHERE employee_id = p_employee_id);
RETURN v_job_count;

EXCEPTION
    WHEN NO_DATA_FOUND THEN
        RAISE_APPLICATION_ERROR(-20003, 'Сотрудник не найден.');
END;
/
```

**Вызов функции:**

```sql
BEGIN
DBMS_OUTPUT.PUT_LINE('Job count for 176: ' || GET_JOB_COUNT(176));
END;
```

## Задание 6: Триггер проверки диапазона зарплат

**Создание триггера:**

```sql
CREATE OR REPLACE TRIGGER CHECK_SAL_RANGE
    BEFORE UPDATE OF min_salary, max_salary
    ON jobs
    FOR EACH ROW
DECLARE
    v_count INTEGER;
BEGIN
SELECT COUNT(*)
INTO v_count
FROM employees
WHERE job_id = :OLD.job_id
  AND (salary < :NEW.min_salary OR salary > :NEW.max_salary);

IF v_count > 0 THEN
        RAISE_APPLICATION_ERROR(-20004, 'Изменение диапазона зарплат влияет на сотрудников.');
END IF;
END;
/
```

**Тест триггера:**

1. Проверка текущего диапазона зарплат и сотрудников:

```sql
SELECT min_salary, max_salary
FROM jobs
WHERE job_id = 'SY_ANAL';
SELECT employee_id, last_name, salary
FROM employees
WHERE job_id = 'SY_ANAL';
```

2. Изменение диапазона:

```sql
UPDATE jobs
SET min_salary = 5000,
    max_salary = 7000
WHERE job_id = 'SY_ANAL';
Триггер остановит изменение, если диапазон затрагивает существующих сотрудников.
```

3. Повторное изменение:

```sql
UPDATE jobs
SET min_salary = 7000,
    max_salary = 18000
WHERE job_id = 'SY_ANAL';
```