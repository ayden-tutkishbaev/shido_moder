import sqlite3


def insert_id(chat_id):
    database = sqlite3.connect("moder_bot.db")
    cursor = database.cursor()
    cursor.execute("""
    INSERT OR IGNORE INTO languages(chat_id)
    VALUES (?)
    """, (chat_id,))
    database.commit()
    database.close()


def insert_language(language, chat_id):
    database = sqlite3.connect("moder_bot.db")
    cursor = database.cursor()
    cursor.execute("""
    UPDATE languages
    SET language = ?
    WHERE chat_id = ?
    """, (language, chat_id))
    database.commit()
    database.close()


def identify_language(chat_id):
    database = sqlite3.connect("moder_bot.db")
    cursor = database.cursor()
    cursor.execute("""
    SELECT language FROM languages
    WHERE chat_id = ?
    """, (chat_id,))
    language = cursor.fetchone()[0]
    database.close()

    return language


def get_all_chats():
    database = sqlite3.connect("moder_bot.db")
    cursor = database.cursor()
    cursor.execute("""
    SELECT chat_id FROM languages
    """)
    users = cursor.fetchall()
    database.close()
    users = [user[0] for user in users]
    return users


def insert_eng_story(title, text):
    database = sqlite3.connect("moder_bot.db")
    cursor = database.cursor()
    cursor.execute("""
    INSERT INTO stories_eng(title, text)
    VALUES (?, ?)
    """, (title, text))
    database.commit()
    database.close()


def insert_rus_story(title, text):
    database = sqlite3.connect("moder_bot.db")
    cursor = database.cursor()
    cursor.execute("""
    INSERT INTO stories_rus(title, text)
    VALUES (?, ?)
    """, (title, text))
    database.commit()
    database.close()


def get_eng_story(random_id):
    database = sqlite3.connect("moder_bot.db")
    cursor = database.cursor()
    cursor.execute("""
    SELECT title, text FROM stories_eng
    WHERE story_id = ?
    """, (random_id,))
    story = cursor.fetchone()
    return story


def get_eng_story_del(title):
    database = sqlite3.connect("moder_bot.db")
    cursor = database.cursor()
    cursor.execute("""
    SELECT title, text FROM stories_eng
    WHERE title = ?
    """, (title,))
    story = cursor.fetchone()
    return story


def get_rus_story_del(title):
    database = sqlite3.connect("moder_bot.db")
    cursor = database.cursor()
    cursor.execute("""
    SELECT title, text FROM stories_rus
    WHERE title = ?
    """, (title,))
    story = cursor.fetchone()
    return story


def get_all_eng_stories_ids():
    database = sqlite3.connect("moder_bot.db")
    cursor = database.cursor()
    cursor.execute("""
    SELECT story_id FROM stories_eng""")
    story_ids = [story_id[0] for story_id in cursor.fetchall()]
    return story_ids


def get_all_rus_stories_ids():
    database = sqlite3.connect("moder_bot.db")
    cursor = database.cursor()
    cursor.execute("""
    SELECT story_id FROM stories_rus""")
    story_ids = [story_id[0] for story_id in cursor.fetchall()]
    return story_ids


def get_rus_story(random_id):
    database = sqlite3.connect("moder_bot.db")
    cursor = database.cursor()
    cursor.execute("""
    SELECT title, text FROM stories_rus
    WHERE story_id = ?
    """, (random_id,))
    story = cursor.fetchone()
    return story


def get_all_rus_stories_titles():
    database = sqlite3.connect("moder_bot.db")
    cursor = database.cursor()
    cursor.execute("""
    SELECT title FROM stories_rus""")
    story_titles = [story_title[0] for story_title in cursor.fetchall()]
    return story_titles


def get_all_eng_stories_titles():
    database = sqlite3.connect("moder_bot.db")
    cursor = database.cursor()
    cursor.execute("""
    SELECT title FROM stories_eng""")
    story_titles = [story_title[0] for story_title in cursor.fetchall()]
    return story_titles


def delete_eng_story(title):
    database = sqlite3.connect("moder_bot.db")
    cursor = database.cursor()
    cursor.execute("""
    DELETE FROM stories_eng WHERE title = ?
    """, (title,))
    database.commit()
    database.close()


def delete_rus_story(title):
    database = sqlite3.connect("moder_bot.db")
    cursor = database.cursor()
    cursor.execute("""
    DELETE FROM stories_rus WHERE title = ?
    """, (title,))
    database.commit()
    database.close()