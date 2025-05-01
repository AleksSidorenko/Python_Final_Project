# Импорт стандартных библиотек Python
import os
import sys
import re
import time
from time import sleep
import random

# Импорт библиотек для красивого вывода и взаимодействия с пользователем
from rich.table import Table
from rich.console import Console
from rich import box
import questionary
import emoji

# Импорт собственных функций из модуля db.py (работа с базой данных)
from db import (
    get_movies_by_keyword, get_top_queries, save_search_query,
    fetch_movies_by_keyword, get_popular_queries, search_movies_by_genre,
    fetch_all_keyword, fetch_movies_by_genre_and_year, fetch_all_genres,
    get_year_range_from_db, fetch_movies_by_genre_and_year_range
)

# Создание объекта консоли для форматированного вывода
console = Console()

# Сопоставление жанров с эмодзи для красивого вывода
GENRE_EMOJIS = {
    "Action": "💥", "Animation": "🎨", "Comedy": "😂", "Drama": "🎭",
    "Horror": "👻", "Music": "🎵", "Sci-Fi": "🚀", "Fantasy": "🧙",
    "Romance": "❤️", "Thriller": "🔪", "Adventure": "🗺️", "Crime": "🕵️",
    "Documentary": "📚", "Children": "👶", "Classics": "🎥", "Family": "👨‍👩‍👦‍👦",
    "Games": "🎮", "Travel": "✈️", "Sports": "⚽️", "Foreign": "🗯", "New": "📖️"
}

# Удаляет эмодзи из строки (используется для "очистки" жанров перед запросом)
def remove_emoji(text):
    return emoji.replace_emoji(text, replace='').strip()

# Простая "эмуляция" очистки экрана — печать множества пустых строк
def fake_clear():
    print("\n" * 100)

# Функция для отображения результатов фильмов в виде таблицы
def display_movie_results(results, start_index=0):
    if not results:
        console.print("[bold red]По вашему запросу ничего не найдено![/bold red]")
        return

    # Создаём таблицу для вывода
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("№", style="bold green", width=2, justify="center")
    table.add_column("Название", style="bold blue", width=15, justify="center")
    table.add_column("Описание", style="dim", overflow="fold", max_width=60, justify="center")
    table.add_column("Год", style="yellow", width=4)
    table.add_column("⏱", header_style="dim", width=3, justify="center")
    table.add_column("★", header_style="dim", width=5, justify="center")
    table.add_column("Актёры", style="dim", overflow="fold", max_width=50, justify="center")

    # Заполняем таблицу строками
    for idx, movie in enumerate(results):
        table.add_row(
            str(start_index + idx + 1),
            movie.get("title", "N/A"),
            movie.get("description", "N/A"),
            str(movie.get("release_year", "N/A")),
            str(movie.get("length", "N/A")) + " мин",
            str(movie.get("rating", "N/A")),
            movie.get("actors", "N/A")
        )
    console.print(table)

# Выводит сообщение об ошибке и ждёт, пока пользователь нажмёт Enter
def show_error_and_wait(message):
    console.print(f"[bold red]{message}[/bold red]")
    console.print("[bold green]⏎ Нажмите Enter для возврата к списку[/bold green]")
    input()

# Постраничный вывод фильмов
def paginate_results(results, keyword):
    page = 0
    page_size = 10  # Количество фильмов на странице
    selected_action = "Следующие 10 фильмов"

    while True:
        start = page * page_size
        end = start + page_size
        page_movies = results[start:end]

        if not page_movies:
            console.print("[bold red]Нет фильмов на этой странице.[/bold red]")
            page = max(0, page - 1)
            continue

        display_movie_results(page_movies, start_index=start)

        # Отображение текущего состояния страницы
        if end >= len(results):
            console.print("[bold yellow]Это последняя страница.[/bold yellow]")
        elif end <= 10:
            console.print("[bold yellow]Это первая страница.[/bold yellow]")

        console.print(f"[bold blue]🔎 Найдено {len(results)} фильмов: по запросу '{keyword}'[/bold blue]")

        # Предложение действий пользователю
        actions = ["Следующие 10 фильмов", "Предыдущие 10 фильмов", "Выбрать фильм по номеру", "Вернуться в главное меню"]
        selected_action = questionary.select(
            "Для выбора используйте клавиши со стрелками",
            choices=actions,
            default=selected_action,
            qmark=""
        ).ask()

        # Обработка выбора
        if selected_action == "Следующие 10 фильмов":
            if end < len(results):
                page += 1
        elif selected_action == "Предыдущие 10 фильмов":
            if page > 0:
                page -= 1
        elif selected_action == "Выбрать фильм по номеру":
            number_input = questionary.text("Введите номер фильма (по отображенному списку):", qmark="").ask()
            if number_input and number_input.isdigit():
                number = int(number_input)
                if start < number <= start + len(page_movies):
                    selected_movie = results[number - 1]
                    console.clear()
                    display_movie_details(selected_movie)
                    show_error_and_wait('')
                else:
                    show_error_and_wait("❗ Неверный номер фильма.")
            else:
                show_error_and_wait("❗ Введите корректный номер.")
        else:
            break  # Возврат в меню

# Поиск по ключевому слову
def search_by_keyword():
    while True:
        method = questionary.select(
            "Используйте клавиши со стрелками",
            choices=[
                "📈 Выбрать из списка популярных запросов",
                "⌨️ Ввести своё слово",
                "⬅️ Вернуться в главное меню"
            ],
            qmark=""
        ).ask()
        if not method or method == "⬅️ Вернуться в главное меню":
            fake_clear()
            return

        if method == "📈 Выбрать из списка популярных запросов":
            genres = fetch_all_keyword()
            keyword = questionary.select("Выберите слово из списка:", choices=genres, qmark="").ask()
        else:
            keyword = questionary.text("Введите ключевое слово:", qmark="").ask()

            if not keyword or not keyword.strip():
                console.print("[bold red]❗ Пустой запрос. Повторите попытку.[/bold red]")
                continue

            keyword = keyword.strip()

        save_search_query(keyword, query_type="keyword")
        results = fetch_movies_by_keyword(keyword)

        if not results:
            console.print(f"[bold red]❗ Фильмы по запросу '{keyword}' не найдены.[/bold red]")
            choice = questionary.select("Что дальше?", choices=["🔁 Попробовать снова", "⬅️ Вернуться в главное меню"], qmark="").ask()
            if choice == "🔁 Попробовать снова":
                continue
            else:
                fake_clear()
                return
        else:
            break

    paginate_results(results, keyword)

# Поиск фильмов по жанру и году
def search_by_genre_and_year():
    genres = fetch_all_genres()
    if not genres:
        console.print("[bold red]Нет доступных жанров.[/bold red]")
        return

    genre_choices = [f"{GENRE_EMOJIS.get(genre, '🎞️')} {genre}" for genre in sorted(genres)]
    selected = questionary.select("Выберите жанр из списка:", choices=genre_choices, qmark='').ask()
    selected = remove_emoji(selected)

    if not selected:
        console.print("[bold red]Выбор не сделан. Возврат в меню.[/bold red]")
        return

    selected_genre = selected.strip()

    save_search_query(selected_genre, query_type='genre')

    genre_results = search_movies_by_genre(selected_genre)

    if not genre_results:
        console.print(f"[bold red]Фильмы с жанром '{selected_genre}' не найдены.[/bold red]")
        return

    min_year, max_year = get_year_range_from_db()

    while True:
        year_input = questionary.text(f"Введите год или диапазон годов ({min_year}-{max_year}):", qmark='').ask()
        if not year_input:
            console.print("[bold red]Ввод пустой. Повторите попытку.[/bold red]")
            continue

        results = []
        keyword_label = ""
        year_input = year_input.strip()

        if re.fullmatch(r"\d{4}\s*-\s*\d{4}", year_input):
            try:
                start_year, end_year = map(int, year_input.split("-"))
                if start_year > end_year or start_year < min_year or end_year > max_year:
                    raise ValueError
                results = fetch_movies_by_genre_and_year_range(selected_genre, start_year, end_year)
                keyword_label = f"{selected_genre} ({start_year}-{end_year})"
            except ValueError:
                console.print("[bold red]Неверный диапазон: вне допустимого интервала.[/bold red]")
                continue

        elif re.fullmatch(r"\d{4}", year_input):
            year = int(year_input)
            if year < min_year or year > max_year:
                console.print(f"[bold red]Год должен быть в пределах от {min_year} до {max_year}.[/bold red]")
                continue

            results = fetch_movies_by_genre_and_year(selected_genre, year)
            keyword_label = f"{selected_genre} ({year})"
        else:
            console.print("[bold red]Ошибка формата. Введите 4 цифры или диапазон (например, 2005-2010).[/bold red]")
            continue

        if results:
            break
        else:
            console.print(f"[bold red]Фильмы с жанром '{selected_genre}' и заданным годом не найдены.[/bold red]")

    paginate_results(results, keyword_label)

# Вывод карточки фильма
def display_movie_details(movie):
    console.clear()
    console.print(f"[bold cyan]Карточка фильма: {movie['title']}[/bold cyan]")
    console.print(f"[bold yellow]Описание:[/bold yellow] {movie['description']}")
    console.print(f"[bold yellow]Год выпуска:[/bold yellow] {movie['release_year']}")
    console.print("[bold green]У вас очень хороший вкус, приятного просмотра![/bold green]")

# Показать топ-5 популярных поисковых запросов
def display_top_queries_and_select():
    top_queries = get_top_queries(by_type=False)
    if not top_queries:
        console.print("[bold red]Нет популярных слов для отображения![/bold red]")
        return
    console.print("\n[bold blue]Топ-5 популярных ключевых запросов:[/bold blue]")
    for idx, query in enumerate(top_queries, start=1):
        query_text = query.get('query_text', 'Неизвестный запрос')
        query_count = query.get('amount', 0)
        console.print(f"{idx}. {query_text} ({query_count} раз)")

# Показать топ-5 популярных жанров
def display_top_genre_queries_and_select():
    top_genres = get_top_queries(by_type=True)
    if not top_genres:
        console.print("[bold red]Нет популярных жанров для отображения![/bold red]")
        return
    console.print("\n[bold blue]Топ-5 популярных жанров:[/bold blue]")
    for idx, query in enumerate(top_genres, start=1):
        genre_name = query.get('query_type', 'Неизвестный жанр')
        genre_count = query.get('amount_genre', 0)
        console.print(f"{idx}. {genre_name} ({genre_count} раз)")
