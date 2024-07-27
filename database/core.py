import sqlite3


def create_languages_table():
    database = sqlite3.connect("moder_bot.db")
    cursor = database.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS languages(
        language_id INTEGER PRIMARY KEY AUTOINCREMENT,
        chat_id INTEGER UNIQUE,
        language TEXT DEFAULT ""
    )
    """)
    database.commit()
    database.close()


def eng_stories_table():
    sqlite3.connect("moder_bot.db").cursor().execute("""
    CREATE TABLE IF NOT EXISTS stories_eng(
        story_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        text TEXT
    )
    """)


def rus_stories_table():
    sqlite3.connect("moder_bot.db").cursor().execute("""
    CREATE TABLE IF NOT EXISTS stories_rus(
        story_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        text TEXT
    )
    """)


def chat_permissions():
    sqlite3.connect("moder_bot.db").cursor().execute("""
    CREATE TABLE IF NOT EXISTS permissions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chat_id INTEGER UNIQUE,
        is_swear_words BOOLEAN DEFAULT FALSE,
        is_links BOOLEAN DEFAULT TRUE
    )
    """)