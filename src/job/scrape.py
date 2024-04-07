
import requests
from bs4 import BeautifulSoup
import re
from processor.databasesetup import DatabaseManager
from config import DATABASE_NAME, ROOT_URL

def number_and_title(title):
    print(title)
    result = re.search(r"(\d+[A-Z]?.?-\s?\d+[A-Z]?)\s+(.*)", title)
    return result.group(1), result.group(2)

def extract_data(page):
    """
    Extracts data from a specific page of the website and returns it as a list of tuples.

    Parameters:
    - page: The page number to extract data from.

    Returns:
    - data: A list of tuples containing the extracted data.
    """
    url = ROOT_URL.format(page)
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
        number, poemtitle = number_and_title(padyamhead)
        data.append((page, number, poemtitle, padyam, context, meaning, antidote, audio_src))
    return data


def main():
    dbname = DATABASE_NAME
    data = []
    for page in range(1, 13):
        print(f"Extracting data from page {page}")
        data.extend(extract_data(page))
    databaseManager = DatabaseManager(DATABASE_NAME)
    databaseManager.insert_poem(dbname, data)

if __name__ == '__main__':
    main()