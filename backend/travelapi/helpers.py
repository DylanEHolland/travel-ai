import os
from openai import OpenAI
from openai.types.create_embedding_response import CreateEmbeddingResponse
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
# client.api_key = os.getenv("OPENAI_API_KEY")

def create_embeddings(content: str) -> str | None:
    try:
        client = OpenAI()

        response: CreateEmbeddingResponse = client.embeddings.create(
            input=content,
            model="text-embedding-3-small"
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"Error generating embedding: {e}")
        return None
    return "embeddings"
