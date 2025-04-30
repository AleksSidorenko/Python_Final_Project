# "app.py"

# Импортируем модуль с навигацией по меню
import menu

# Импортируем функцию показа приветственного логотипа
from logo import welcome_sequence


def main():
    """
    Запуск главного меню приложения.
    Вызов функции из модуля menu, отвечающей за основную логику навигации.
    """
    menu.navigate_menu()


# Точка входа в программу
if __name__ == "__main__":
    welcome_sequence()  # Показ приветственного логотипа при запуске
    main()              # Запуск главного меню




# import menu
# from logo import welcome_sequence
#
#
# def main():
#     """Запуск главного меню"""
#     menu.navigate_menu()
#
# if __name__ == "__main__":
#     welcome_sequence()  # Показ логотипа при запуске
#     main()