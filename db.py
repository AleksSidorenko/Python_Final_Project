import mysql.connector
from mysql.connector import Error
from config import db_config, log_db_config
from rich.console import Console

console = Console()

def connect_db(config):
    """Устанавливает соединение с базой данных по переданной конфигурации"""
    connection = mysql.connector.connect(**config)
    return connection


def get_movies_by_keyword(keyword):
    """Ищет фильмы, где ключевое слово встречается в названии или описании"""
    connection = connect_db(db_config)
    cursor = connection.cursor(dictionary=True)

    query = f"SELECT * FROM film WHERE title REGEXP '\\b{keyword}\\b' OR description REGEXP '\\b{keyword}\\b'"
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results


def search_movies_by_genre(genre_name):
    """Находит фильмы по жанру"""
    connection = connect_db(db_config)
    cursor = connection.cursor(dictionary=True)

    query = """
    SELECT f.*
    FROM film f
    JOIN film_category fc ON f.film_id = fc.film_id
    JOIN category c ON fc.category_id = c.category_id
    WHERE c.name = %s
    """
    cursor.execute(query, (genre_name,))
    results = cursor.fetchall()

    cursor.close()
    connection.close()
    return results


def save_search_query(query, query_type=None):
    """Сохраняет или обновляет статистику поискового запроса"""
    try:
        if not query:
            print("Ошибка: Пустой запрос.")
            return

        connection = mysql.connector.connect(**log_db_config)
        cursor = connection.cursor()

        if query_type == 'genre':
            # Обработка жанровых запросов
            cursor.execute("SELECT id FROM query_log WHERE query_type = %s", (query,))
            result = cursor.fetchone()
            if result:
                cursor.execute("UPDATE query_log SET amount_genre = amount_genre + 1 WHERE id = %s", (result[0],))
            else:
                cursor.execute("INSERT INTO query_log (query_type, amount_genre) VALUES (%s, 1)", (query,))
        elif query_type == 'keyword':
            # Обработка запросов по ключевому слову
            cursor.execute("SELECT id FROM query_log WHERE query_text = %s", (query,))
            result = cursor.fetchone()
            if result:
                cursor.execute("UPDATE query_log SET amount = amount + 1 WHERE id = %s", (result[0],))
            else:
                cursor.execute("INSERT INTO query_log (query_text, amount) VALUES (%s, 1)", (query,))

        connection.commit()

    except Error as e:
        print(f"Ошибка при сохранении запроса: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def get_top_queries(by_type=True):
    """Возвращает топ-5 самых популярных жанров или ключевых слов"""
    try:
        connection = mysql.connector.connect(**log_db_config)
        cursor = connection.cursor(dictionary=True)

        if by_type:
            # По жанрам
            cursor.execute("""
                SELECT query_type, amount_genre 
                FROM query_log 
                WHERE query_type IS NOT NULL AND query_type != '' 
                ORDER BY amount_genre DESC 
                LIMIT 5
            """)
        else:
            # По ключевым словам
            cursor.execute("""
                SELECT query_text, amount 
                FROM query_log 
                WHERE query_text IS NOT NULL AND query_text != '' 
                ORDER BY amount DESC 
                LIMIT 5
            """)

        results = cursor.fetchall()
        return results

    except Error as e:
        print(f"Ошибка при получении популярных запросов: {e}")
        return []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def get_popular_queries():
    """Получает все популярные запросы по ключевым словам"""
    connection = connect_db(log_db_config)
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT query_text, COUNT(*) as count 
        FROM query_log 
        WHERE query_text IS NOT NULL AND query_text != '' 
        GROUP BY query_text 
        ORDER BY count DESC
    """
    cursor.execute(query)
    results = cursor.fetchall()

    cursor.close()
    connection.close()
    return results


def fetch_movies_by_keyword(keyword):
    """Находит фильмы по ключевому слову с отображением 2 актёров"""
    conn = connect_db(db_config)
    cursor = conn.cursor(dictionary=True)
    keyword = f"\\b{keyword}\\b"

    query = """
        SELECT 
            f.film_id,
            f.title,
            f.description,
            f.release_year,
            f.length,
            f.rating,
            (
                SELECT GROUP_CONCAT(CONCAT(first_name, ' ', last_name) SEPARATOR ', ')
                FROM (
                    SELECT a.first_name, a.last_name
                    FROM film_actor fa
                    JOIN actor a ON fa.actor_id = a.actor_id
                    WHERE fa.film_id = f.film_id
                    ORDER BY fa.actor_id
                    LIMIT 2
                ) AS limited_actors
            ) AS actors
        FROM film f
        WHERE f.title REGEXP %s OR f.description REGEXP %s
        LIMIT 10;
    """
    cursor.execute(query, (keyword, keyword))
    results = cursor.fetchall()

    cursor.close()
    conn.close()
    return results


def fetch_movies_by_genre_and_year(genre, year):
    """Получает фильмы по заданному жанру и году выпуска, включая до 2 актёров"""
    conn = connect_db(db_config)
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT
        f.film_id,
        f.title,
        f.description,
        f.release_year,
        f.length,
        f.rating,
        GROUP_CONCAT(CONCAT(sub.first_name, ' ', sub.last_name) SEPARATOR ', ') AS actors
    FROM film f
    JOIN film_category fc ON f.film_id = fc.film_id
    JOIN category c ON fc.category_id = c.category_id
    JOIN (
        SELECT
            fa.film_id,
            a.first_name,
            a.last_name,
            ROW_NUMBER() OVER (PARTITION BY fa.film_id ORDER BY a.actor_id) AS row_num
        FROM film_actor fa
        JOIN actor a ON fa.actor_id = a.actor_id
    ) sub ON f.film_id = sub.film_id AND sub.row_num <= 2
    WHERE c.name = %s AND f.release_year = %s
    GROUP BY f.film_id
    LIMIT 20;
    """
    cursor.execute(query, (genre, year))
    results = cursor.fetchall()

    cursor.close()
    conn.close()
    return results


def fetch_all_keyword():
    """Возвращает все ключевые слова из логов"""
    conn = connect_db(log_db_config)
    cursor = conn.cursor()

    query = "SELECT query_text FROM query_log ORDER BY query_text"
    cursor.execute(query)
    genres = [row[0] for row in cursor.fetchall()]

    cursor.close()
    conn.close()
    return genres


def fetch_all_genres():
    """Получает список всех жанров из основной базы"""
    try:
        conn = connect_db(db_config)
        with conn.cursor() as cursor:
            cursor.execute("SELECT name FROM category ORDER BY name")
            genres = [row[0] for row in cursor.fetchall()]
        return genres
    finally:
        conn.close()


def execute_query(query, params=None, fetch_one=False):
    """Выполняет универсальный SQL-запрос"""
    conn = None
    cursor = None
    try:
        conn = connect_db(db_config)
        cursor = conn.cursor(dictionary=True)

        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)

        result = cursor.fetchone() if fetch_one else cursor.fetchall()
        return result

    except mysql.connector.Error as err:
        console.print(f"[red]Ошибка при выполнении запроса: {err}[/red]")
        return []

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def get_year_range_from_db():
    """Получает минимальный и максимальный год выпуска фильмов"""
    query = "SELECT MIN(release_year) AS min_year, MAX(release_year) AS max_year FROM film"
    result = execute_query(query, fetch_one=True)
    return result["min_year"], result["max_year"]


def fetch_movies_by_genre_and_year_range(genre, start_year, end_year):
    """Получает фильмы по жанру и диапазону годов"""
    query = """
        SELECT 
        f.title, 
        f.description, 
        f.release_year, 
        f.length, 
        f.rating,
        GROUP_CONCAT(CONCAT(sub.first_name, ' ', sub.last_name) SEPARATOR ', ') AS actors
    FROM film f
    JOIN film_category fc ON f.film_id = fc.film_id
    JOIN category c ON fc.category_id = c.category_id
    JOIN (
        SELECT 
            fa.film_id, 
            a.first_name, 
            a.last_name,
            ROW_NUMBER() OVER (PARTITION BY fa.film_id ORDER BY a.actor_id) AS row_num
        FROM film_actor fa
        JOIN actor a ON fa.actor_id = a.actor_id
    ) sub ON f.film_id = sub.film_id AND sub.row_num <= 2
    WHERE c.name = %s AND f.release_year BETWEEN %s AND %s
    GROUP BY f.film_id;
    """
    return execute_query(query, (genre, start_year, end_year))