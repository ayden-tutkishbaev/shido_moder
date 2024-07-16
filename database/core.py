import sqlite3


def create_users_table():
    database = sqlite3.connect("moder_bot.db")
    cursor = database.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id INTEGER UNIQUE,
        full_name TEXT
    )
    """)
    database.commit()
    database.close()
