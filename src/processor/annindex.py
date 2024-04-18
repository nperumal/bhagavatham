
from langchain_community.vectorstores import FAISS

# Class to handle the faiss index using langchain faiss wrapper
class FaissIndex:
    def __init__(self, folder_path, index_name, embeddings):
        self.folder_path = folder_path
        self.index_name = index_name
        self.embeddings = embeddings
        self.faiss_index = None
        self.load_index()
    
    def create_index(self, docs):
        try:
            self.faiss_index = FAISS.from_document(docs, self.embeddings)
            self.faiss_index.save_local(
                folder_path=self.folder_path,
                index_name=self.index_name
            )
            print("Faiss index created ")
        except Exception as e:
            print("Fiass store failed \n", e)

    def load_index(self):
        try:
            self.faiss_index = FAISS.load_local(
                folder_path=self.folder_path,
                embeddings=self.embeddings,
                index_name=self.index_name,
                allow_dangerous_deserialization=True
            )
            print("Faiss index loaded ")
        except Exception as e:
            print("Fiass index loading failed \n", e)

    def search(self, query):
        searchDocs = self.faiss_index.similarity_search(query)
        return searchDocs
    
    def similarity_search_with_score(self, query, k=3):
        searchDocs = self.faiss_index.similarity_search_with_score(query, k=k)
        return searchDocs

