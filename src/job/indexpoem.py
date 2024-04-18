from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
from processor.annindex import FaissIndex
from config import FAISS_DB, SENTENCE_TRANSFORMER_MODEL, DATABASE_NAME
import sqlite3

# Create a function to read translations from the database and prepare them as a list of Document objects
def read_translations_from_database(database, start, end):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute(f"SELECT id, poem_id, poem_translation, poemtitle_translation, context_translation, meaning_translation, antidote_translation FROM translation where id between {start} and {end}")
    translations = cursor.fetchall()
    # Convert each column of the translation and 'id' column into a tuple of id and list of other columns
    context = []
    meaning = []
    for translation in translations:
        context.append(Document(page_content=translation[4], metadata=dict(translation_id=translation[0], poem_id=translation[1])))
        meaning.append(Document(page_content=translation[5], metadata=dict(translation_id=translation[0], poem_id=translation[1])))
    
    conn.close()
    return context, meaning

def main():
    # Create an instance of the HuggingFaceEmbeddings class with specific parameters
    folder_path = FAISS_DB
    contex_index_name = "context_faiss_index"
    meaning_index_name = "meaning_faiss_index"
    embeddings = HuggingFaceEmbeddings(model_name=SENTENCE_TRANSFORMER_MODEL, model_kwargs={'device':'cpu'}, encode_kwargs={'normalize_embeddings': False})
    context, meaning = read_translations_from_database(DATABASE_NAME, 1, 10)

    print("Context: ", context)
    print("Meaning: ", meaning)

    # Create fiass index for context and create the index
    context_faiss_index = FaissIndex(folder_path, contex_index_name, embeddings)
    print("creating context index...")
    context_faiss_index.create_index(context)

    # Create fiass index for meaning and create the index
    meaning_faiss_index = FaissIndex(folder_path, meaning_index_name, embeddings)
    print("creating meaning index...")
    meaning_faiss_index.create_index(meaning)

if __name__ == "__main__":
    main()






