--part a
CREATE DATABASE advanced_lab;

CREATE TABLE employees(
    emp_id SERIAL PRIMARY KEY ,
    first_name VARCHAR(50) NOT NULL ,
    last_name VARCHAR(50) NOT NULL ,
    department VARCHAR(50) NOT NULL ,
    salary INT,
    hire_date DATE,
    status VARCHAR(50) default 'Active'
);

CREATE TABLE departments(
    dept_id SERIAL PRIMARY KEY ,
    dept_name VARCHAR(50) NOT NULL ,
    budget INT,
    manager_id INT
);

CREATE TABLE projects(
    project_id SERIAL PRIMARY KEY ,
    project_name VARCHAR(50) NOT NULL ,
    dept_id INT ,
    start_date DATE,
    end_date DATE,
    budget INT
);

--for tasks
INSERT INTO departments (dept_name, budget, manager_id)
VALUES
    ('Development', 130000, 1),
    ('PeopleOps', 65000, 2),
    ('Marketing', 95000, 3),
    ('Accounting', 155000, 4);

INSERT INTO employees (first_name, last_name, department, salary, hire_date, status)
VALUES
-- старый сотрудник с высокой зарплатой
('Serik', 'Tulegenov', 'Development', 92000, '2014-06-12', 'Active'),

-- средняя зарплата
('Kamila', 'Nurpeisova', 'PeopleOps', 68000, '2021-08-03', 'Active'),

-- низкая зарплата
('Rustam', 'Bekbolatov', 'Marketing', 36000, '2022-10-19', 'Active'),

-- для задачи 12 (Marketing + Promoted)
('Aigerim', 'Sadvakassova', 'Marketing', 42000, '2023-03-11', 'Active'),

-- уволенный сотрудник
('Dias', 'Mukhanov', 'PeopleOps', 51000, '2019-11-01', 'Terminated'),

-- сотрудник с NULL salary и NULL department
('Test', 'Nullovich', NULL, NULL, NULL, 'Active');

INSERT INTO projects (project_name, dept_id, start_date, end_date, budget)
VALUES
    ('Legacy System', 1, '2018-02-01', '2019-12-31', 60000),  -- удалится
    ('Future Platform', 2, '2023-06-01', '2024-04-01', 85000); -- останется

--part b
INSERT INTO employees (first_name,last_name,department)
VALUES ('Baurzhan','Yernazarov','Development');

INSERT INTO employees(first_name, last_name,department,salary,status)
VALUES ('Adilbek','Karim','Development',DEFAULT,DEFAULT);

INSERT INTO departments(dept_name, budget, manager_id)
VALUES
('Development',130000,1),
('PeopleOps',65000,2),
('Marketing',95000,3);

INSERT INTO employees (first_name, last_name, hire_date, salary, department)
VALUES ('Saniya', 'Abzalova', CURRENT_DATE, 52000 * 1.1, 'PeopleOps');

CREATE TEMP TABLE temp_employees AS
SELECT * FROM employees WHERE department = 'Development';

--part c
UPDATE employees
SET salary = salary * 1.1
WHERE salary IS NOT NULL;

UPDATE employees
SET status = 'Senior'
WHERE salary > 60000
    and hire_date < '2020-01-01';

UPDATE employees
SET department = CASE
    WHEN salary > 80000 then 'Management'
    WHEN salary BETWEEN 50000 and 80000 THEN 'Senior'
    ELSE 'Junior'
END
WHERE salary IS NOT NULL;

UPDATE employees
SET department = DEFAULT
WHERE status = 'Inactive';

UPDATE departments d
SET budget = (
    SELECT AVG(salary) * 1.2
    FROM employees e
    WHERE e.department = d.dept_name
)
WHERE EXISTS (
    SELECT 1 FROM employees e WHERE e.department = d.dept_name AND e.salary IS NOT NULL
);

UPDATE employees
SET salary = salary * 1.15,
    status = 'Promoted'
WHERE department = 'Marketing'
  AND salary IS NOT NULL;

--part d
DELETE FROM employees
WHERE status = 'Terminated';

DELETE FROM employees
WHERE salary < 40000
  AND hire_date > '2023-01-01'
  AND department IS NULL;

DELETE FROM departments d
WHERE d.dept_name NOT IN (
    SELECT DISTINCT department
    FROM employees
    WHERE department IS NOT NULL
);

DELETE FROM projects
WHERE end_date < '2023-01-01'
RETURNING *;

--part e
INSERT INTO employees (first_name, last_name, salary, department)
VALUES ('Test', 'Nullovich', NULL, NULL);

UPDATE employees
SET department = 'Unassigned'
WHERE department IS NULL;

DELETE FROM employees
WHERE salary IS NULL OR department IS NULL;

--task f
INSERT INTO employees (first_name, last_name, department, salary, hire_date)
VALUES ('Maksat', 'Zhanybekov', 'Accounting', 57000, CURRENT_DATE)
RETURNING emp_id, first_name || ' ' || last_name AS full_name;

UPDATE employees
SET salary = salary + 5000
WHERE department = 'Development'
RETURNING emp_id, salary - 5000 AS old_salary, salary AS new_salary;

DELETE FROM employees
WHERE hire_date < '2020-01-01'
RETURNING *;

--task g
INSERT INTO employees(first_name, last_name, department, salary, hire_date)
SELECT 'Unique','Person','Development',62000,current_date
WHERE NOT EXISTS(
    SELECT 1 FROM employees WHERE first_name='Unique' AND last_name = 'Person'
);

UPDATE employees e
SET salary = salary * CASE
                          WHEN (
                                   SELECT MAX(d.budget)
                                   FROM departments d
                                   WHERE d.dept_name = e.department
                               ) > 100000 THEN 1.1
                          ELSE 1.05
    END
WHERE salary IS NOT NULL;

INSERT INTO employees (first_name, last_name, department, salary, hire_date)
VALUES
    ('Bulk', 'One', 'Development', 52000, CURRENT_DATE),
    ('Bulk', 'Two', 'Marketing', 56000, CURRENT_DATE),
    ('Bulk', 'Three', 'PeopleOps', 61000, CURRENT_DATE),
    ('Bulk', 'Four', 'Accounting', 47000, CURRENT_DATE),
    ('Bulk', 'Five', 'Development', 73000, CURRENT_DATE);

UPDATE employees
SET salary = salary * 1.1
WHERE first_name LIKE 'Bulk%';

CREATE TABLE IF NOT EXISTS employee_archive AS
SELECT * FROM employees WHERE 1=0;

INSERT INTO employee_archive
SELECT * FROM employees WHERE status = 'Inactive';

DELETE FROM employees WHERE status = 'Inactive';

UPDATE projects
SET end_date = end_date + INTERVAL '30 days'
WHERE budget > 50000
  AND dept_id IN (
    SELECT d.dept_id
    FROM departments d
    WHERE (SELECT COUNT(*) FROM employees e WHERE e.department = d.dept_name) > 3
);
