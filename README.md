# goit-cs-hw-03

## Передумова

Налаштуйте `.venv` та встановіть залежності

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Завдання 1

Створіть базу даних для системи управління завданнями, використовуючи PostgreSQL. База даних має містити таблиці для користувачів, статусів завдань і самих завдань. Виконайте необхідні запити в базі даних системи управління завданнями.

### Запуск PostgreSQL

```sh
cd task_1
docker compose up -d
```

## Завдання 2

Розробіть Python скрипт, який використовує бібліотеку PyMongo для реалізації основних CRUD (Create, Read, Update, Delete) операцій у MongoDB.


### Запуск MongoDB

```sh
cd task_2
docker compose up -d
