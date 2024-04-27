# define configuration parameters for the project
DATABASE_NAME = '/Users/nallaperumal/workspace/bhagavatham/src/data/poem.db'
FAISS_DB = '/Users/nallaperumal/workspace/bhagavatham/src/data/faiss_db'
SENTENCE_TRANSFORMER_MODEL = 'sentence-transformers/distiluse-base-multilingual-cased-v2'
CONTEXT_INDEX_NAME = 'context_faiss_index'
MEANING_INDEX_NAME = 'meaning_faiss_index'
MODEL_KWARGS = {'device':'cpu'}
ENCODE_KWARGS = {'normalize_embeddings': False} 
AUDIO_ROOT = 'https://bhagavatamanimutyalu.org/a_animutyalu_Telugu/'
ANN_INDEX_SERVER = 'http://localhost:8081/'
QA_MODEL='distilbert-base-uncased-distilled-squad'