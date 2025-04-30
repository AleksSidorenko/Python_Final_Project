# "logo.py"

# Импорт стандартной библиотеки для работы со временем
import time

# Импорт rich-модуля для красивого вывода в консоли
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.align import Align

# Создаём объект консоли для форматированного вывода
console = Console()


def loading_screen():
    """
    Показывает анимированную загрузку с индикатором-спиннером.
    Используется при старте приложения.
    """
    with Progress(
        SpinnerColumn(),  # Символ вращения (индикатор активности)
        TextColumn("[progress.description]{task.description}"),  # Текстовое описание процесса
        transient=True,  # Автоматически скрыть индикатор после завершения
    ) as progress:
        progress.add_task("[cyan]Запуск ITCinema...", total=None)
        time.sleep(1)  # Задержка для эффекта загрузки


def reveal_title():
    """
    Постепенно "печатает" название ITCinema по одной букве.
    Создаёт анимацию появления текста по центру экрана.
    """
    title = "ITCinema"
    revealed = ""
    for letter in title:
        revealed += letter
        console.clear()  # Очистка экрана на каждой итерации
        console.print(f"[bold magenta]{revealed}[/bold magenta]", justify="center")
        time.sleep(0.1)  # Пауза между появлением букв


def goodbye_sequence():
    """
    Печатает финальное прощание при выходе из программы.
    Сообщения отображаются по центру с небольшой задержкой.
    """
    farewell_lines = [
        "[bold yellow]👋 Спасибо, что использовали ITCinema CLI![/bold yellow]",
        "[bold green]🎬 До новых встреч на наших киносеансах![/bold green]",
        "[italic white]Заглядывайте снова...[/italic white]"
    ]
    for line in farewell_lines:
        console.print(Align.center(line))  # Центрируем каждую строку
        time.sleep(0.2)  # Пауза между строками


def welcome_sequence():
    """
    Основная анимация при запуске приложения:
    сначала загрузка, затем анимация названия.
    """
    loading_screen()
    reveal_title()


# # "logo.py"
#
# import time
# from rich.console import Console
# from rich.progress import Progress, SpinnerColumn, TextColumn
# from rich.align import Align
#
# console = Console()
#
# def loading_screen():
#     """Эффект загрузки"""
#     with Progress(
#         SpinnerColumn(),
#         TextColumn("[progress.description]{task.description}"),
#         transient=True,
#     ) as progress:
#         progress.add_task("[cyan]Запуск ITCinema...", total=None)
#         time.sleep(1)
#
# def reveal_title():
#     """Постепенное появление названия ITCinema"""
#     title = "ITCinema"
#     revealed = ""
#     for letter in title:
#         revealed += letter
#         console.clear()
#         console.print(f"[bold magenta]{revealed}[/bold magenta]", justify="center")
#         time.sleep(0.1)
#
# def goodbye_sequence():
#     """Показ прощания без логотипа"""
#     farewell_lines = [
#         "[bold yellow]👋 Спасибо, что использовали ITCinema CLI![/bold yellow]",
#         "[bold green]🎬 До новых встреч на наших киносеансах![/bold green]",
#         "[italic white]Заглядывайте снова...[/italic white]"
#     ]
#     for line in farewell_lines:
#         console.print(Align.center(line))
#         time.sleep(0.2)
#
#
# def welcome_sequence():
#     loading_screen()
#     reveal_title()
