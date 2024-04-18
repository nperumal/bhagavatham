
import requests
from bs4 import BeautifulSoup
import sqlite3
from sqlite3 import Error
from processor.databasesetup import DatabaseSetup

def create_connection(db_file):
    """Create a database connection to a SQLite database"""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn

def create_table(dbname):
    """Create a table in the database to store the scraped data"""
    conn = create_connection(dbname)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS poem
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 chapter INTEGER NOT NULL,
                 poemtitle TEXT NOT NULL,
                 poem TEXT NOT NULL,
                 context TEXT NOT NULL,
                 meaning TEXT NOT NULL,
                 antidote TEXT NOT NULL,
                 audiopath VARCHAR(128) NOT NULL)''')
    # create table called translation which is child table of poem table for storing translations of the poem, poemtitle, context, meaning, antidote in different languages
    cursor.execute('''CREATE TABLE IF NOT EXISTS translation
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    language TEXT NOT NULL,
                    poem_id INTEGER NOT NULL,
                    poem_translation TEXT NOT NULL,
                    poemtitle_translation TEXT NOT NULL,
                    context_translation TEXT NOT NULL,
                    meaning_translation TEXT NOT NULL,
                    antidote_translation TEXT NOT NULL,
                    FOREIGN KEY (poem_id) REFERENCES poem(id))''')
    # create table called vector which is child table of translation table for storing the vectors of the poem, poemtitle, context, meaning, antidote
    cursor.execute('''CREATE TABLE IF NOT EXISTS vector
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    translation_id INTEGER NOT NULL,
                    poem_id INTEGER NOT NULL,
                    poem_vector BLOB NOT NULL,
                    poemtitle_vector BLOB NOT NULL,
                    context_vector BLOB NOT NULL,
                    meaning_vector BLOB NOT NULL,
                    antidote_vector BLOB NOT NULL,
                    FOREIGN KEY (poem_id) REFERENCES poem(id))''')
    
    
    conn.commit()
    conn.close()

def insert_data(dbname, data):
    """
    Inserts the provided data into the poem table in the database.

    Parameters:
    - dbname: The name of the SQLite database file.
    - data: A list of tuples containing the data to be inserted.

    Returns:
    None
    """
    conn = create_connection(dbname)
    cursor = conn.cursor()
    cursor.executemany("INSERT INTO poem (chapter, poemtitle, poem, context, meaning, antidote, audiopath) VALUES (?, ?, ?, ?, ?, ?, ?)", data)
    conn.commit()
    conn.close()

def extract_data(page):
    """
    Extracts data from a specific page of the website and returns it as a list of tuples.

    Parameters:
    - page: The page number to extract data from.

    Returns:
    - data: A list of tuples containing the extracted data.
    """
    url = f"https://bhagavatamanimutyalu.org/a_animutyalu_Telugu/iBam{page}.html"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    divs = soup.find_all("div", attrs={"class": "card mb-3"})
    data=[]
    for div in divs:
        padyamhead = div.find("div", attrs={"class": "padyamhead"})
        if padyamhead is None:
            continue
        padyamhead = padyamhead.text
        padyam = div.find_all("div", attrs={"class": "padyam"})[0].text
        context = div.find_all("div", attrs={"class": "Context"})[0].text if div.find_all("div", attrs={"class": "Context"}) else ""
        m_and_a = div.find_all("div", attrs={"class": "pardham_content"})
        if m_and_a == []:
            meaning = div.find("div", attrs={"class": "tatparyam"}).text
            antidote = div.find("div", attrs={"class": "pratipadardham"}).text
        else:
            meaning = m_and_a[0].text
            antidote = m_and_a[1].text
        
        audio_src = div.find("source").get("src")
        data.append((page, padyamhead, padyam, context, meaning, antidote, audio_src))
    return data


def main():
    dbname = 'src/data/bhagavatam.db'
    create_table(dbname)
    data = []
    for page in range(1, 13):
        print(f"Extracting data from page {page}")
        data.extend(extract_data(page))
    insert_data(dbname, data)

if __name__ == '__main__':
    dbm = DatabaseSetup()
    data = []
    for page in range(1, 13):
        print(f"Extracting data from page {page}")
        data.extend(extract_data(page))
    insert_data(dbname, data)