from config import SENTENCE_TRANSFORMER_MODEL, MEANING_INDEX_NAME, DATABASE_NAME
from service.bhagavathamsearch import BhagavathamSearchService

def query(search_query):
    service = BhagavathamSearchService(SENTENCE_TRANSFORMER_MODEL, MEANING_INDEX_NAME)
    return service.search(search_query)

if __name__ == "__main__":
    query('Shiva is the one who can not stand anyone')
