from langchain.vectorstores import PGVector
from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.dialects.postgresql import ARRAY
from typing import Optional

class CustomPGVector(PGVector):
    def _get_embedding_collection_store(self, vector_dimension: Optional[int] = None):
        class CustomEmbeddingStore(self.Base):
            __tablename__ = "knowledge_base"
            # __table_args__ = {"schema": "your_schema_name"}
            
            id = Column(Integer, primary_key=True)
            content = Column(String)
            embedding = Column(ARRAY(Float))
            # Add any other columns that exist in your table

        return None, CustomEmbeddingStore