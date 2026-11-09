
import csv
import xml.etree.ElementTree as ET
from datetime import datetime


# ==========================================
# ЧАСТЬ 1. РАБОТА С CSV - books.csv
# ==========================================

# Читаем CSV-файл
with open("books.csv", "r", encoding="cp1251", newline="") as file:
    reader = csv.DictReader(file, delimiter=";")
    books = list(reader)


print("=" * 50)
print("ЛАБОРАТОРНАЯ РАБОТА №2")
print("=" * 50)

print("\nКоличество записей:", len(books))


# ------------------------------------------
# ЗАДАНИЕ 1. Количество книг,
# название которых длиннее 30 символов
# ------------------------------------------

count = 0

for book in books:
    title = book["Название"]

    if len(title) > 30:
        count += 1

print("\n1. Книги с названием длиннее 30 символов:")
print("Количество:", count)


# ------------------------------------------
# ЗАДАНИЕ 2. Поиск книг по автору
# с ценой до 150 рублей
# ------------------------------------------

print("\n2. Поиск книг по автору")

author_name = input("Введите имя или фамилию автора: ")

found_books = []

for book in books:
    author = book["Автор"]
    price_text = book["Цена поступления"].strip()

    try:
        price = float(price_text.replace(",", "."))
    except ValueError:
        continue

    if author_name.lower() in author.lower() and price <= 150:
        found_books.append(book)

if found_books:
    for book in found_books:
        print(
            "Автор:", book["Автор"],
            "| Название:", book["Название"],
            "| Цена:", book["Цена поступления"]
        )
    print("Найдено книг:", len(found_books))
else:
    print("Книги не найдены")


# ------------------------------------------
# ЗАДАНИЕ 3. Создание 20 библиографических
# ссылок и сохранение в текстовый файл
# ------------------------------------------

references = []

for book in books:
    author = book["Автор"].strip()
    title = book["Название"].strip()
    date_text = book["Дата поступления"].strip()

    if not author or not title or not date_text:
        continue

    try:
        year = datetime.strptime(
            date_text, "%d.%m.%Y %H:%M"
        ).year
    except ValueError:
        try:
            year = datetime.strptime(
                date_text, "%d.%m.%Y"
            ).year
        except ValueError:
            continue

    reference = f"{author}. {title} - {year}"
    references.append(reference)

    if len(references) == 20:
        break


with open("bibliography.txt", "w", encoding="utf-8") as file:
    for number, reference in enumerate(references, start=1):
        file.write(f"{number}. {reference}\n")

print("\n3. Библиографические ссылки:")
for number, reference in enumerate(references, start=1):
    print(f"{number}. {reference}")

print("Ссылки сохранены в файле bibliography.txt")


# ------------------------------------------
# ЗАДАНИЕ 4. Поиск уникальных жанров
# ------------------------------------------


genres = set()

for book in books:
    genre_text = book["Жанр книги"].strip()

    if genre_text:
        parts = genre_text.split("#")

        for genre in parts:
            genre = genre.strip()

            if genre:
                genres.add(genre)

print("\n4. Уникальные жанры:")

for genre in sorted(genres):
    print(genre)

print("Количество уникальных жанров:", len(genres))



# ------------------------------------------
# ЗАДАНИЕ 5. ТОП-20 популярных книг
# по количеству выдач
# ------------------------------------------


# ЗАДАНИЕ 5. ТОП-20 популярных книг
# по общему количеству выдач

popular_books = {}

for book in books:
    try:
        loans = int(book["Кол-во выдач"].strip())
    except ValueError:
        continue

    title = book["Название"].strip()
    author = book["Автор"].strip()

    key = (title, author)

    if key in popular_books:
        popular_books[key] += loans
    else:
        popular_books[key] = loans


sorted_books = sorted(
    popular_books.items(),
    key=lambda item: item[1],
    reverse=True
)

print("\n5. ТОП-20 популярных книг:")

for number, (book_info, loans) in enumerate(sorted_books[:20], start=1):
    title, author = book_info

    print(
        f"{number}. {title} | "
        f"Автор: {author} | "
        f"Количество выдач: {loans}"
    )



# ==========================================
# ЧАСТЬ 2. РАБОТА С XML - currency.xml
# ==========================================

print("\n" + "=" * 50)
print("РАБОТА С XML")
print("=" * 50)


# Читаем XML-файл
tree = ET.parse("currency.xml")
root = tree.getroot()


# Создаём словарь: Название валюты - Значение
currency_dict = {}

for currency in root.findall("Valute"):
    name = currency.findtext("Name")
    value = currency.findtext("Value")

    if name and value:
        currency_dict[name] = float(value.replace(",", "."))


print("\n6. Словарь валют:")

for name, value in currency_dict.items():
    print(f"{name} - {value}")


print("\nКоличество валют:", len(currency_dict))

print("\nРабота программы завершена!")
