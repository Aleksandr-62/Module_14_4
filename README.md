_The BOT is written in aiogram 3.x version for Python 3.13_

БОТ написан на aiogram 3.x версии для Python 3.13


Цель: написать простейшие CRUD функции для взаимодействия с базой данных.

Задача "Продуктовая база":

Подготовка:

Для решения этой задачи вам понадобится код из предыдущей задачи. Дополните его, следуя пунктам задачи ниже.

Дополните ранее написанный код для Telegram-бота:

Создайте файл crud_functions.py и напишите там следующие функции:

initiate_db, которая создаёт таблицу Products, если она ещё не создана при помощи SQL запроса. Эта таблица
должна содержать следующие поля:

id - целое число, первичный ключ

title(название продукта) - текст (не пустой)

description(описание) - текст

price(цена) - целое число (не пустой)

get_all_products, которая возвращает все записи из таблицы Products, полученные при помощи SQL запроса.

Изменения в Telegram-бот:

В самом начале запускайте ранее написанную функцию get_all_products.

Измените функцию get_buying_list в модуле с Telegram-ботом, используя вместо обычной нумерации продуктов функцию get_all_products.
Полученные записи используйте в выводимой надписи: "Название: <title> | Описание: <description> | Цена: <price>"
Перед запуском бота пополните вашу таблицу Products 4 или более записями для последующего вывода в чате Telegram-бота.
