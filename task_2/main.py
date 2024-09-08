from bson.objectid import ObjectId

from pymongo import MongoClient, errors

# Підключення до локальної бази даних MongoDB
try:
    client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=5000)
    db = client.cats_db
    client.server_info()  # Перевірка підключення до сервера
except errors.ServerSelectionTimeoutError as err:
    print(f"Не вдалося підключитися до MongoDB: {err}")
    exit(1)


def handle_mongo_error(prefix):
    """
    Декоратор для обробки помилок MongoDB.

    :param prefix: Префікс для повідомлення про помилку
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except errors.PyMongoError as err:
                print(f"{prefix}: {err}")

        return wrapper

    return decorator


@handle_mongo_error("Помилка при створенні кота")
def create_cat(name, age, features):
    """
    Створює нового кота в колекції.

    :param name: Ім'я кота
    :param age: Вік кота
    :param features: Список характеристик кота
    """
    cat = {"name": name, "age": age, "features": features}
    result = db.cats.insert_one(cat)
    print(f"Додано кота з id: {result.inserted_id}")


@handle_mongo_error("Помилка при читанні котів")
def read_all_cats():
    """
    Виводить усі записи з колекції. Якщо колекція порожня, виводить відповідне повідомлення.
    """
    count = db.cats.count_documents({})
    if count == 0:
        print("Котів не знайдено")
        return

    cats = db.cats.find()
    print(f"Знайдено {count} котів:")
    for cat in cats:
        print(cat)


@handle_mongo_error("Помилка при пошуку кота за ім'ям")
def read_cat_by_name(name):
    """
    Шукає кота за ім'ям та виводить його інформацію. Якщо кота не знайдено, виводить відповідне повідомлення.

    :param name: Ім'я кота
    """
    cat = db.cats.find_one({"name": name})
    if cat:
        print(cat)
    else:
        print(f'Кота з ім\'ям "{name}" не знайдено')


@handle_mongo_error("Помилка при оновленні віку кота")
def update_cat_age(name, new_age):
    """
    Оновлює вік кота за його ім'ям.

    :param name: Ім'я кота
    :param new_age: Новий вік кота
    """
    result = db.cats.update_one({"name": name}, {"$set": {"age": new_age}})
    if result.matched_count:
        print(f'Оновлено вік кота з ім\'ям "{name}" до {new_age}')
    else:
        print(f'Кота з ім\'ям "{name}" не знайдено')


@handle_mongo_error("Помилка при додаванні нової характеристики")
def add_feature_to_cat(name, new_feature):
    """
    Додає нову характеристику до списку характеристик кота за його ім'ям.

    :param name: Ім'я кота
    :param new_feature: Нова характеристика
    """
    result = db.cats.update_one({"name": name}, {"$push": {"features": new_feature}})
    if result.matched_count:
        print(f'Додано характеристику "{new_feature}" для кота з ім\'ям "{name}"')
    else:
        print(f'Кота з ім\'ям "{name}" не знайдено')


@handle_mongo_error("Помилка при видаленні кота")
def delete_cat_by_name(name):
    """
    Видаляє кота за його ім'ям з колекції.

    :param name: Ім'я кота
    """
    result = db.cats.delete_one({"name": name})
    if result.deleted_count:
        print(f'Видалено кота з ім\'ям "{name}"')
    else:
        print(f'Кота з ім\'ям "{name}" не знайдено')


@handle_mongo_error("Помилка при видаленні всіх котів")
def delete_all_cats():
    """
    Видаляє всі записи з колекції котів.
    """
    result = db.cats.delete_many({})
    print(f"Видалено {result.deleted_count} котів")


def main():
    """
    Основна функція для демонстрації роботи CRUD операцій.
    """
    # Створення нового кота
    create_cat("barsik", 3, ["ходить в капці", "дає себе гладити", "рудий"])
    create_cat("murzik", 2, ["любить спати", "грає з м'ячем", "сірий"])
    create_cat("pushok", 1, ["грає зі шнурком", "прямовухий", "чорний"])
    create_cat("murka", 4, ["любить молоко", "грає з кулькою", "білий"])
    create_cat("bayun", 5, ["любить рибу", "грає з мишкою", "сірий"])

    # Читання всіх котів
    print("\nУсі коти в колекції db.cats:")
    read_all_cats()

    # Читання одного кота за ім'ям
    print("\nПошук кота за ім'ям:")
    read_cat_by_name("barsik")

    # Оновлення віку кота
    print("\nОновлення віку barsik:")
    update_cat_age("barsik", 4)
    read_cat_by_name("barsik")

    # Додавання нової характеристики
    print("\nДодавання нової характеристики для barsik:")
    add_feature_to_cat("barsik", "любит гратися")
    read_cat_by_name("barsik")

    # Видалення кота за ім'ям
    print("\nВидалення barsik:")
    delete_cat_by_name("barsik")
    read_all_cats()

    # Видалення всіх котів
    print("\nВидалення всіх котів:")
    delete_all_cats()
    read_all_cats()


if __name__ == "__main__":
    main()
