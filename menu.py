# menu.py

# Импорт необходимых библиотек для форматированного вывода, работы со временем и консоли
from rich.console import Console
from rich.panel import Panel
from datetime import datetime
import time
from logic import display_top_queries_and_select, display_top_genre_queries_and_select
from logic import search_by_keyword, search_by_genre_and_year
from logo import welcome_sequence, goodbye_sequence
from rich.align import Align
import shutil
from rich import box
from rich.console import Group

# Инициализация объекта консоли для вывода форматированного текста
console = Console()

def centered_input(prompt_text: str) -> str:
    """
    Запрашивает ввод от пользователя, выравнивая подсказку по центру терминала.
    """
    terminal_width = shutil.get_terminal_size().columns  # Получаем ширину терминала
    prompt = f"{prompt_text}:"
    padding = (terminal_width - len(prompt)) // 2  # Вычисляем отступы
    full_prompt = " " * padding + prompt
    return input(full_prompt)  # Возвращаем отформатированный ввод


def display_colored_menu():
    """
    Отображает главное меню с текущей датой, "погодой", местоположением и базой данных.
    Меню форматировано с использованием rich.
    """
    console.clear()  # Очищаем консоль

    # Получаем текущие дату и время
    now = datetime.now().strftime("%A, %d %B %Y г., %H:%M")
    location = "Вся галактика"
    weather = "Соответствует Вашему настроению"
    db = "[bold yellow]sakila[/bold yellow]"  # Название БД

    # Составляем информационную панель (верхняя часть интерфейса)
    info_text = "\n".join([
        f"[bold green]📅 Дата и время:[/] {now}",
        f"[bold magenta]📍 Местоположение:[/] {location}",
        f"[bold blue]🌤️ Погода:[/] {weather}",
        f"[bold yellow]🗄️ База данных:[/] {db}"
    ])

    info_panel = Panel(
        info_text,
        title="[bold cyan]🎬 ITCinema — Кино начинается здесь![/bold cyan]",
        border_style="bright_blue",
        box=box.HORIZONTALS,
        padding=(0, 0),
        expand=False,
    )

    # Список опций главного меню
    options = [
        "🔍 Поиск фильмов по ключевому слову",
        "🎭 Поиск фильмов по жанру и году выпуска",
        "📈 Просмотр популярных запросов",
        "❌ Выход из приложения"
    ]
    # Форматирование меню
    menu_text = "\n".join([f"{idx + 1}. {option}" for idx, option in enumerate(options)])

    menu_panel = Panel(
        menu_text,
        title="📜 Главное меню",
        border_style="bright_blue",
        box=box.DOUBLE,
        padding=(0, 1),
        width=49,
        expand=True
    )

    # Группируем панели и выравниваем по центру
    full_screen_content = Group(
        Align.center(info_panel),
        Align.center(menu_panel)
    )
    console.print(full_screen_content)


def navigate_menu():
    """
    Обработка взаимодействия пользователя с меню.
    Реагирует на выбор пользователя и вызывает соответствующие функции.
    """
    while True:
        display_colored_menu()  # Показываем меню
        choice = centered_input("Введите номер опции (1–4)").strip()
        console.clear()

        if choice == "1":
            # Поиск по ключевому слову
            search_by_keyword()
        elif choice == "2":
            # Поиск по жанру и году
            search_by_genre_and_year()
        elif choice == "3":
            # Просмотр популярных запросов
            display_top_genre_queries_and_select()
            display_top_queries_and_select()
            console.print("\n[bold green]⏎ Нажмите Enter для возврата в меню[/bold green]")
            input()
        elif choice == "4":
            # Выход из приложения
            console.clear()
            console.print(Align.center("[bold red]Выход из приложения...[/bold red]"))
            time.sleep(0.3)
            goodbye_sequence()  # Анимация прощания
            break
        else:
            # Обработка некорректного ввода
            console.print("[bold red]Некорректный ввод. Попробуйте снова.[/bold red]")
            time.sleep(1.5)
            input("Нажмите Enter для возврата в меню...")


# # menu.py
#
# from rich.console import Console
# from rich.panel import Panel
# from datetime import datetime
# import time
# from logic import display_top_queries_and_select, display_top_genre_queries_and_select
# from logic import search_by_keyword, search_by_genre_and_year
# from logo import welcome_sequence, goodbye_sequence
# from rich.align import Align
# import shutil
# from rich import box
# from rich.console import Group
#
# console = Console()
#
# def centered_input(prompt_text: str) -> str:
#     terminal_width = shutil.get_terminal_size().columns
#     prompt = f"{prompt_text}:"
#     padding = (terminal_width - len(prompt)) // 2
#     full_prompt = " " * padding + prompt
#     return input(full_prompt)
#
#
# def display_colored_menu():
#     console.clear()
#
#     now = datetime.now().strftime("%A, %d %B %Y г., %H:%M")
#     location = "Вся галактика"
#     weather = "Соответствует Вашему настроению"
#     db = "[bold yellow]sakila[/bold yellow]"
#
#     # Ровные строки (без выравнивания пробелами)
#     info_text = "\n".join([
#         f"[bold green]📅 Дата и время:[/] {now}",
#         f"[bold magenta]📍 Местоположение:[/] {location}",
#         f"[bold blue]🌤️ Погода:[/] {weather}",
#         f"[bold yellow]🗄️ База данных:[/] {db}"
#     ])
#
#     info_panel = Panel(
#         info_text,
#         title="[bold cyan]🎬 ITCinema — Кино начинается здесь![/bold cyan]",
#         border_style="bright_blue",
#         box=box.HORIZONTALS,
#         padding=(0, 0),
#         expand=False,
#     )
#
#     options = [
#         "🔍 Поиск фильмов по ключевому слову",
#         "🎭 Поиск фильмов по жанру и году выпуска",
#         "📈 Просмотр популярных запросов",
#         "❌ Выход из приложения"
#     ]
#     menu_text = "\n".join([f"{idx + 1}. {option}" for idx, option in enumerate(options)])
#
#     menu_panel = Panel(
#         menu_text,
#         title="📜 Главное меню",
#         border_style="bright_blue",
#         box=box.DOUBLE,
#         padding=(0, 1),
#         width=49,
#         expand=True
#     )
#  # Группируем панели и выравниваем всё по центру
#     full_screen_content = Group(
#         Align.center(info_panel),
#         Align.center(menu_panel)
#     )
#     console.print(full_screen_content)
#
#
# def navigate_menu():
#     while True:
#         display_colored_menu()
#         choice = centered_input("Введите номер опции (1–4)").strip()
#         console.clear()
#         if choice == "1":
#             search_by_keyword()
#         elif choice == "2":
#             search_by_genre_and_year()
#         elif choice == "3":
#             display_top_genre_queries_and_select()
#             display_top_queries_and_select()
#             console.print("\n[bold green]⏎ Нажмите Enter для возврата в меню[/bold green]")
#             input()
#
#         elif choice == "4":
#             console.clear()
#             console.print(Align.center("[bold red]Выход из приложения...[/bold red]"))
#             time.sleep(0.3)
#             goodbye_sequence()
#             break
#         else:
#             console.print("[bold red]Некорректный ввод. Попробуйте снова.[/bold red]")
#             time.sleep(1.5)
#             input("Нажмите Enter для возврата в меню...")