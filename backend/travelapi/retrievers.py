from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from sqlalchemy import text
from langchain.vectorstores.base import VectorStoreRetriever

class SQLVectorRetriever(BaseRetriever):
    def __init__(self, connection, embeddings, table_name="knowledge_base", top_k=5):
        self.connection = connection
        self.embeddings = embeddings
        self.table_name = table_name
        self.top_k = top_k

    def get_relevant_documents(self, query):
        # Generate query embedding
        query_embedding = self.embeddings.embed_query(query)
        
        # SQL for similarity search
        sql = text(f"""
            SELECT text, 1 - (vector <=> CAST(:query_embedding AS vector)) AS similarity
            FROM {self.table_name}
            ORDER BY vector <=> CAST(:query_embedding AS vector)
            LIMIT :top_k;
        """)
        print("query:", query)
        # print("query_embedding:", query_embedding)
        # Execute query
        results = self.connection.execute(sql, {"query_embedding": query_embedding, "top_k": self.top_k}).fetchall()
        # # Convert results to Documents
        return [
            Document(page_content=row[0], metadata={"similarity": row[1]})
            for row in results
        ]
