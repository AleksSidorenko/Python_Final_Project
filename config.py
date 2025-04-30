# config.py

import os


# Конфигурация подключения к базам данных

# Основная база данных (sakila), содержащая информацию о фильмах,
# актёрах, жанрах и другой справочной информации.
db_config = {
    'host': os.environ.get("host_read"),         # Адрес сервера базы данных
    'user': os.environ.get("user_read"),         # Имя пользователя для подключения
    'password': os.environ.get("password_read"), # Пароль пользователя
    'database': 'sakila'                         # Название базы данных
}

# Отдельная база данных для хранения логов пользовательской активности,
# такой как популярные запросы, действия и история поиска.
log_db_config = {
    'host': os.environ.get("host_write"),         # Адрес сервера базы данных для логов
    'user': os.environ.get("user_write"),         # Имя пользователя
    'password': os.environ.get("password_write"), # Пароль пользователя
    'database': 'group_111124_fp_AlexSidorenko'   # Название базы данных для логов
}

