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

   # Показ ASCII-логотипа после появления названия
    show_logo()


def show_logo():
    """ASCII-логотип ITCinema"""
    logo = """
██╗████████╗ ██████╗██╗██╗   ██╗███████╗███╗   ███╗ █████╗ 
██║╚══██╔══╝██╔════╝██║███╗  ██║██╔════╝████╗ ████║██╔══██╗
██║   ██║   ██║     ██║██╔██╗██║█████╗  ██╔████╔██║███████║
██║   ██║   ██║     ██║██║  ███║██╔══╝  ██║╚██╔╝██║██╔══██║
██║   ██║   ╚██████╗██║██║   ██║███████╗██║ ╚═╝ ██║██║  ██║
╚═╝   ╚═╝    ╚═════╝╚═╝╚═╝   ╚═╝╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝
    """
    console.print(logo, style="bold cyan", justify="center")

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