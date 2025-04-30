# config.py

# Конфигурация подключения к базам данных

# Основная база данных (sakila), содержащая информацию о фильмах,
# актёрах, жанрах и другой справочной информации.
db_config = {
    'host': 'ich-db.edu.itcareerhub.de',         # Адрес сервера базы данных
    'user': 'ich1',                              # Имя пользователя для подключения
    'password': 'password',                      # Пароль пользователя
    'database': 'sakila'                         # Название базы данных
}

# Отдельная база данных для хранения логов пользовательской активности,
# такой как популярные запросы, действия и история поиска.
log_db_config = {
    'host': 'ich-edit.edu.itcareerhub.de',       # Адрес сервера базы данных для логов
    'user': 'ich1',                              # Имя пользователя
    'password': 'ich1_password_ilovedbs',        # Пароль пользователя
    'database': 'group_111124_fp_AlexSidorenko'  # Название базы данных для логов
}


# # "config.py"
#
# # Конфигурация подключения к базам данных
#
# # Основная база данных (sakila)
# db_config = {
#     'host': 'ich-db.edu.itcareerhub.de',
#     'user': 'ich1',
#     'password': 'password',
#     'database': 'sakila'
# }
#
# # База данных для логов (group_111124_fp_AlexSidorenko)
# log_db_config = {
#     'host': 'ich-edit.edu.itcareerhub.de',
#     'user': 'ich1',
#     'password': 'ich1_password_ilovedbs',
#     'database': 'group_111124_fp_AlexSidorenko'
# }
