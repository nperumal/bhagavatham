from config import *
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from processor.annindex import FaissIndex
from processor.databasesetup import DatabaseManager
from transformers import AutoTokenizer, pipeline

class BhagavathamSearchService:
    def __init__(self, model, index_name):
        self.model = model
        self.index_name = index_name
        self.index = FaissIndex(FAISS_DB, self.index_name, HuggingFaceEmbeddings(model_name=self.model, model_kwargs=MODEL_KWARGS, encode_kwargs=ENCODE_KWARGS))
        # self.reader_model = QA_MODEL
        # self.reader_tokenizer = AutoTokenizer.from_pretrained(QA_MODEL)
    
    def get_poems(self):
        dm = DatabaseManager(DATABASE_NAME)
        contents = dm.get_poems()
        return contents

    def get_poem(self, poem_id, translation_id):
        dm = DatabaseManager(DATABASE_NAME)
        contents = dm.select_poems(poem_id, translation_id)
        return contents
    
    def search(self, search_query):
        meaning_results_with_scores = self.index.similarity_search_with_score(search_query, k=3) 

        doc, score = meaning_results_with_scores[0]
        poem_id = doc.metadata['poem_id']
        translation_id = doc.metadata['translation_id']
        similar_text = self.get_poem(poem_id, translation_id)
        #for similar_text in similar_texts:
        (poem, poemtitle, context, meaning, poemtitle_translation, context_translation, meaning_translation, audio_path) = similar_text[0]
        answer = self.reader(search_query, context_translation + meaning_translation)
        return [(*similar_text[0], answer)]
    
    def reader(self, search_query, similarity_text):
        qa_pipeline = pipeline("question-answering", model=QA_MODEL)
        answer = qa_pipeline({"question": search_query, "context": similarity_text})["answer"]
        return answer

    
    def MultiContentSearch(self, search_query):
        """Search for similar content in multiple columns the database using the provided query"""
        #TODO: Implement this method
        #         # Create an instance of the HuggingFaceEmbeddings class with specific parameters
        # embeddings = HuggingFaceEmbeddings(model_name=SENTENCE_TRANSFORMER_MODEL, model_kwargs={'device':'cpu'}, encode_kwargs={'normalize_embeddings': False})
        # # Query context faiss index
        # #context_faiss_index = FaissIndex(FAISS_DB, CONTEXT_INDEX_NAME, embeddings)
        # meaning_faiss_index = FaissIndex(FAISS_DB, MEANING_INDEX_NAME, embeddings)


        # # context_results_with_scores = context_faiss_index.similarity_search_with_score(search_query, k=3) 
        # # #doc, score = results_with_scores[0]
        # # print(context_results_with_scores)
        # # print(f"Metadata: {doc.metadata['poem_id']}, {doc.metadata['translation_id']}, Score: {score}")

        # meaning_results_with_scores = meaning_faiss_index.similarity_search_with_score(search_query, k=3) 
        # # restricted_result = [(doc, score) for doc, score in meaning_results_with_scores if score < 1]

        # doc, score = meaning_results_with_scores[0]
        # poem_id = doc.metadata['poem_id']
        # translation_id = doc.metadata['translation_id']
        
        # return self.get_poem(poem_id, translation_id)
        pass