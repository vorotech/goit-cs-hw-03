-- Отримуємо всі завдання для конкретного користувача
-- Вказуємо user_id користувача для фільтрації завдань
SELECT
    tasks.id,
    tasks.title,
    tasks.description,
    status.name AS status
FROM
    tasks
JOIN
    status ON tasks.status_id = status.id
WHERE
    tasks.user_id = 3;


-- Вибираємо всі завдання з конкретним статусом 'new'
SELECT
    tasks.id,
    tasks.title,
    tasks.description,
    status.name AS status
FROM
    tasks
JOIN
    status ON tasks.status_id = status.id
WHERE
    tasks.status_id = (SELECT id FROM status WHERE name = 'new');


-- Оновлюємо статус конкретного завдання (task_id = 9) на 'in progress'
UPDATE
    tasks
SET
    status_id = (SELECT id FROM status WHERE name = 'in progress')
WHERE
    id = 9;

-- Вибираємо всіх користувачів, які не мають жодного завдання
SELECT
    id,
    fullname,
    email
FROM
    users
WHERE
    id NOT IN (SELECT user_id FROM tasks);

-- Додаємо нове завдання для конкретного користувача
-- Приклад: завдання для користувача з id = 13
INSERT INTO tasks (title, description, status_id, user_id)
VALUES ('New Task Title', 'This is the description of the new task',
        (SELECT id FROM status WHERE name = 'new'), 13);

-- Вибираємо всі завдання, які ще не завершено (статус не 'completed')
SELECT
    tasks.id,
    tasks.title,
    tasks.description,
    status.name AS status
FROM
    tasks
JOIN
    status ON tasks.status_id = status.id
WHERE
    status.name != 'completed';

-- Видаляємо конкретне завдання за його id
-- Приклад: видаляємо завдання з id = 10
DELETE FROM tasks
WHERE id = 10;

-- Знаходимо користувачів за електронною поштою з умовою LIKE
-- Приклад: шукаємо користувачів, чия електронна пошта містить 'example.com'
SELECT
    id,
    fullname,
    email
FROM
    users
WHERE
    email LIKE '%example.com%';


-- Оновлюємо ім'я користувача
-- Приклад: змінюємо ім'я користувача з id = 5 на 'John Doe'
UPDATE
    users
SET
    fullname = 'John Doe'
WHERE
    id = 5;

-- Отримуємо кількість завдань для кожного статусу
SELECT
    status.name AS status,
    COUNT(tasks.id) AS task_count
FROM
    tasks
JOIN
    status ON tasks.status_id = status.id
GROUP BY
    status.name;

-- Вибираємо завдання, призначені користувачам, чия електронна пошта містить домен '@example.com'
SELECT
    tasks.id,
    tasks.title,
    tasks.description,
    users.fullname,
    users.email,
    status.name AS status
FROM
    tasks
JOIN
    users ON tasks.user_id = users.id
JOIN
    status ON tasks.status_id = status.id
WHERE
    users.email LIKE '%@example.com';

-- Вибираємо завдання, у яких відсутній опис
SELECT
    id,
    title,
    user_id,
    status_id
FROM
    tasks
WHERE
    description IS NULL OR description = '';

-- Вибираємо користувачів та їхні завдання, які знаходяться у статусі 'in progress'
SELECT
    users.id AS user_id,
    users.fullname,
    tasks.id AS task_id,
    tasks.title,
    tasks.description,
    status.name AS status
FROM
    tasks
INNER JOIN
    users ON tasks.user_id = users.id
INNER JOIN
    status ON tasks.status_id = status.id
WHERE
    status.name = 'in progress';

-- Отримуємо користувачів та кількість їхніх завдань
SELECT
    users.id AS user_id,
    users.fullname,
    users.email,
    COUNT(tasks.id) AS task_count
FROM
    users
LEFT JOIN
    tasks ON users.id = tasks.user_id
GROUP BY
    users.id, users.fullname, users.email;
