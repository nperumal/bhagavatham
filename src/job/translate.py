import sqlite3
from processor.translator import Translator
from multiprocessing import Pool
import time

# Module to read poems from sqllite database called bhagavatam.db which is created by scrape.py and resided in ./data folder.
# Function to read poems from the database and return the poems in a list of dictionaries.
# Function to enumerate the poems and translate them to English using Translator class defined in ./processor/translator.py.
# Function to insert the translations back into the database.
def read_poems_from_database(database, start, end):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute(f"SELECT id, poemtitle, poem, context, meaning, antidote  FROM poem where id between {start} and {end}")
    poems = cursor.fetchall()
    # Convert each column of the poem and 'id' column into a tuple of id and list of other columns
    poem_touple = []
    for poem in poems:
        poem_id = poem[0]
        # remove leading and trailing whitespaces from each column and convert to list
        poem = list(map(lambda x: x.strip(), poem[1:]))
        poem_touple.append((poem_id, poem))

    conn.close()
    return poem_touple

# def multiprocessing_translate_poem(poem):
#     id, content = poem
#     translator = Translator()
#     print(content)
#     print(f"Translating poem {id}")
#     return (id, translator.translate_sentences("tel_Telu", "eng_Latn", content))

# def multiprocessing_translate_poems(poems):
#     with Pool() as pool:
#         start_time = time.time()
#         translated_poems = pool.map(multiprocessing_translate_poem, poems)
#         end_time = time.time()
#         print(f"Time taken to translate poems: {end_time - start_time} seconds")
#     return translated_poems

def translate_poems(poems):
    translator = Translator()
    translated_poems = []
    for poem in poems:
        id, content = poem
        print(f"Translating poem {id}")
        start_time = time.time()
        translated_poem = (id, translator.translate_sentences("tel_Telu", "eng_Latn", content))
        end_time = time.time()
        print(f"Time taken to translate {id} : {end_time - start_time} seconds")
        translated_poems.append(translated_poem)
    return translated_poems

def insert_translations_into_database(database, translated_poems):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    language = 'en'
    for poem in translated_poems:
        poem_id, contents = poem
        title = contents[0]
        poem = contents[1]
        context = contents[2]
        meaning = contents[3]
        antidote = contents[4]

        cursor.execute("INSERT INTO translation (language, poem_id, poemtitle_translation, poem_translation, context_translation, meaning_translation, antidote_translation) VALUES (?, ?, ?, ?, ?, ?, ?)", ( language, poem_id, title, poem, context, meaning, antidote))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    database = 'src/data/bhagavatam.db'
    batch_size = 10
    total_poems = 330
    for epoch in range(total_poems // batch_size):
        start = (epoch * batch_size) + 1
        end = (epoch * batch_size) + batch_size
        print(f"Epoch {epoch} started.")
        print(f"Processing row: {start} to row: {end}")
        poems = read_poems_from_database(database, start, end)
        translated_poems = translate_poems(poems)
        insert_translations_into_database(database, translated_poems)
        print(f"Epoch {epoch} completed.")
