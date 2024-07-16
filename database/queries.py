import sqlite3


def insert_data_to_creation(telegram_id, full_name):
    database = sqlite3.connect("moder_bot.db")
    cursor = database.cursor()
    cursor.execute("""
    INSERT INTO users(telegram_id, full_name)
    VALUES (?, ?) ON CONFLICT DO NOTHING
    """, (telegram_id, full_name))
    database.commit()
    database.close()