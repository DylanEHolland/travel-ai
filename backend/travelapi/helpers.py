import os
from typing import Optional
from langchain_core.documents.base import Document
from langchain_core.retrievers import BaseRetriever
from openai import OpenAI
from dotenv import load_dotenv
# from langchain.chat_models import ChatOpenAI
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
# from langchain.embeddings.openai import OpenAIEmbeddings
from langchain_community.embeddings import OpenAIEmbeddings
from sqlalchemy import text
from langchain.chains import RetrievalQA
from sqlalchemy.orm import Session
from langchain_community.utilities import OpenWeatherMapAPIWrapper
from langchain.tools import Tool
from langchain.agents import initialize_agent, AgentType

from .models import get_db

# from .retrievers import SQLVectorRetriever
from .models import KnowledgeBase, engine
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def embeddings_client():
    embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"), )
    print("\n\n\n\n\n")
    return embeddings

def save_to_knowledge_base(db: Session, destinationId: str, content: str):
    embeddings = create_embeddings(content)
    new_knowledgebase_item: KnowledgeBase = KnowledgeBase(text=content, destination_id=destinationId, vector=embeddings)
    db.add(new_knowledgebase_item)
    db.commit()
    db.refresh(new_knowledgebase_item) 

    return new_knowledgebase_item

def create_embeddings(content: str) -> list[float] | None:
    try:
        embeddings = embeddings_client()
        vector = embeddings.embed_query(content)
        return vector

        # text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
        # docs = text_splitter.split_text(content)
        # print(docs)
        # db = PGVector.from_texts(
        #     texts=docs,
        #     embedding=embeddings,
        #     collection_name="knowledge_base",
        #     connection=engine,
        # )

        # print(db.add_texts(docs))
    except Exception as e:
        print(f"Error generating embedding: {e}")
        return None

def naive_similarity_search(destinationId: str, query: str, top_k=3):
    embeddings = embeddings_client()
    query_emb = embeddings.embed_query(query)
    query_emb_str = "ARRAY[" + ",".join(str(x) for x in query_emb) + "]::vector"
    db = next(get_db())
    # query_emb_str = "{" + ",".join(map(str, query_emb)) + "}"
    print("query_emb_str:", len(query_emb))
    print("engine:", engine)
    with engine.connect() as conn:
        result = conn.execute(text(f"SELECT text, vector, vector_dims(vector) from knowledge_base where destination_id = {destinationId} ORDER BY vector <-> {query_emb_str} LIMIT 3"))
        # result = conn.execute(text(f"select current_database(), current_schema()"))
        docs = [Document(page_content=row[0]) for row in result.fetchall()]
        conn.close()
        print("got docs:", docs)
        return docs

class CustomRetriever(BaseRetriever):
    destinationId: Optional[str] = None
    def setDestinationId(self, destinationId: str):
        self.destinationId = destinationId

    def get_relevant_documents(self, query: str):
        return naive_similarity_search(self.destinationId, query)

    async def aget_relevant_documents(self, query: str):
        return self.get_relevant_documents(query)

#https://bugbytes.io/posts/retrieval-augmented-generation-with-langchain-and-pgvector/
def runAugmentedChat(message: str, destinationId: str) -> str | None:
    embeddings = embeddings_client()
    llm = ChatOpenAI(
        model="gpt-4",  # Choose the model (e.g., 'gpt-3.5-turbo' or 'gpt-4')
        temperature=0.7,
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )

    custom_retriever = CustomRetriever()
    custom_retriever.setDestinationId(destinationId)

    retriever_chain = RetrievalQA.from_chain_type(llm=llm, retriever=custom_retriever)

    
    weather = OpenWeatherMapAPIWrapper(openweathermap_api_key=os.getenv("OPENWEATHERMAP_API_KEY"))
    weather_tool = Tool(
        name="Weather",
        func=weather.run,
        description="Useful for getting weather information for a specific location."
    )

    retrieval_tool = Tool(
        name="Knowledge Base",
        func=retriever_chain.run,
        description="Useful for answering questions about topics, things to do or see, etc that the user has saved in the knowledge base related to their travel destination."
    )

    agent = initialize_agent([retrieval_tool, weather_tool], llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
    prompt = ChatPromptTemplate.from_template("Answer this question: {question}")
    input_data = {"question": message}  
    formatted_prompt = prompt.format(**input_data)
    response = agent.run(formatted_prompt)


    return {
        "response": response
    }

# if __name__ == "__main__":
#     db = next(get_db())
    # save_to_knowledge_base(db, "1", "Want to see the Eiffel Tower")
    # save_to_knowledge_base(db, "1", "The Louvre is a world-famous museum in Paris...")
    # save_to_knowledge_base(db, "1", "Jackie lives right outside of Paris")
    # runAugmentedChat("Where does jackie live?")
    # naive_similarity_search("museum")