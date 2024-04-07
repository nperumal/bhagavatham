import sqlite3
from sqlite3 import Error

class DatabaseManager:
    def __init__(self, db_file):
        self.db_file = db_file

    def create_connection(self):
        """Create a database connection to a SQLite database"""
        conn = None
        try:
            conn = sqlite3.connect(self.db_file)
        except Error as e:
            print(e)
        
        return conn

    def create_table(self, table_name, table_definition):
        """Create a table in the database"""
        # TODO: move create connection to create_table()
        conn = self.create_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} {table_definition}")
            conn.commit()
        except Error as e:
            print(e)
        finally:
            conn.close()

    def create_tables(self):
        """Create all tables in the database"""
        self.create_table('poem', '''
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
            chapter INTEGER NOT NULL,
            poemnumber INTEGER NOT NULL,
            poemtitle TEXT NOT NULL,
            poem TEXT NOT NULL,
            context TEXT NOT NULL,
            meaning TEXT NOT NULL,
            antidote TEXT NOT NULL,
            audiopath VARCHAR(128) NOT NULL)
        ''')

        self.create_table('translation', '''
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
            language TEXT NOT NULL,
            poem_id INTEGER NOT NULL,
            poem_translation TEXT NOT NULL,
            poemtitle_translation TEXT NOT NULL,
            context_translation TEXT NOT NULL,
            meaning_translation TEXT NOT NULL,
            antidote_translation TEXT NOT NULL,
            FOREIGN KEY (poem_id) REFERENCES poem(id))
        ''')

        self.create_table('vector', '''
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
            translation_id INTEGER NOT NULL,
            poem_id INTEGER NOT NULL,
            poem_vector BLOB NOT NULL,
            poemtitle_vector BLOB NOT NULL,
            context_vector BLOB NOT NULL,
            meaning_vector BLOB NOT NULL,
            antidote_vector BLOB NOT NULL,
            FOREIGN KEY (poem_id) REFERENCES poem(id))
        ''')

    def insert_poem(self, dbname, data):
        """
        Inserts the provided data into the poem table in the database.

        Parameters:
        - dbname: The name of the SQLite database file.
        - data: A list of tuples containing the data to be inserted.

        Returns:
        None
        """
        conn = self.create_connection()
        cursor = conn.cursor()
        cursor.executemany("INSERT INTO poem (chapter, poemnumber, poemtitle, poem, context, meaning, antidote, audiopath) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", data)
        conn.commit()
        conn.close()

    def insert_translation(self, dbname, data):
        """
        Inserts the provided data into the translation table in the database.

        Parameters:
        - dbname: The name of the SQLite database file.
        - data: A list of tuples containing the data to be inserted.

        Returns:
        None
        """
        conn = self.create_connection()
        cursor = conn.cursor()
        cursor.executemany("INSERT INTO translation (language, poem_id, poem_translation, poemtitle_translation, context_translation, meaning_translation, antidote_translation) VALUES (?, ?, ?, ?, ?, ?, ?)", data)
        conn.commit()
        conn.close()