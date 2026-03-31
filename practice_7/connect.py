import psycopg2
import config

def get_connection():
    try:
        conn = psycopg2.connect(
            host=config.host,
            database=config.database,
            user=config.user,
            password=config.password,
            port=config.port
        )
        return conn
    except Exception as error:
        print(f"Ошибка при подключении к базе: {error}")
        return None