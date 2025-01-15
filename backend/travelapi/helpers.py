import os
from langchain_core.messages import HumanMessage
from openai import OpenAI
from openai.types.create_embedding_response import CreateEmbeddingResponse
from dotenv import load_dotenv
# from langchain.chat_models import ChatOpenAI
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_postgres import PGVector
# from langchain.embeddings.openai import OpenAIEmbeddings
from langchain_community.embeddings import OpenAIEmbeddings
from sqlalchemy import text
from langchain.chains import RetrievalQA
from sqlalchemy.orm import Session

from .models import get_db

# from .retrievers import SQLVectorRetriever
from .models import KnowledgeBase, engine
from langchain.text_splitter import RecursiveCharacterTextSplitter

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def embeddings_client():
    embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
    print("\n\n\n\n\n")
    return embeddings

def save_to_knowledge_base(db: Session, destinationId: str, content: str):
    embeddings = create_embeddings(content)
    new_knowledgebase_item: KnowledgeBase = KnowledgeBase(text=content, destination_id=destinationId, vector=embeddings)
    db.add(new_knowledgebase_item)
    db.commit()
    db.refresh(new_knowledgebase_item) 

    return new_knowledgebase_item

def create_embeddings(content: str) -> str | None:
    try:
        embeddings = embeddings_client()
        vector = embeddings.embed_query(content)
        print(len(vector))

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
        docs = text_splitter.split_text(content)
        print(docs)
        db = PGVector.from_texts(
            texts=docs,
            embedding=embeddings,
            collection_name="knowledge_base",
            connection=engine,
        )

        print(db.add_texts(docs))
    except Exception as e:
        print(f"Error generating embedding: {e}")
        return None
    return "embeddings"

def runAugmentedChat(message: str) -> str | None:
    embeddings = embeddings_client()
    vector_store = PGVector(
        embeddings=embeddings,
        collection_name="knowledge_base",
        connection=engine,
    )

    retriever = vector_store.as_retriever(k=3)
    
    llm = ChatOpenAI(
        model="gpt-4",  # Choose the model (e.g., 'gpt-3.5-turbo' or 'gpt-4')
        temperature=0.7,
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )

    chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
    response = chain.run(message)


    return {
        "response": response
    }

if __name__ == "__main__":
    db = next(get_db())
    # save_to_knowledge_base(db, "1", "Want to see the Eiffel Tower")
    runAugmentedChat("Whats a good place to visit?")