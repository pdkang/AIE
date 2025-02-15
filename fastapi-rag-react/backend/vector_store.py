from typing import List, Tuple
import numpy as np
from openai import AsyncOpenAI
import os

def cosine_similarity(a, b):
    """Calculate cosine similarity between two vectors."""
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

class VectorDatabase:
    def __init__(self):
        self.embeddings = []
        self.texts = []
        self.client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    async def abuild_from_list(self, texts):
        self.texts = texts
        self.embeddings = []  # Clear existing embeddings
        
        try:
            for text in texts:
                if not text.strip():  # Skip empty texts
                    continue
                    
                response = await self.client.embeddings.create(
                    model="text-embedding-ada-002",
                    input=text.replace("\n", " ")  # Replace newlines with spaces
                )
                if response and response.data and len(response.data) > 0:
                    self.embeddings.append(response.data[0].embedding)
                else:
                    print(f"Warning: No embedding generated for text: {text[:100]}...")
            
            return self
        except Exception as e:
            print(f"Error in abuild_from_list: {str(e)}")
            raise e

    async def search_by_text(self, query, k=4):
        if not query.strip():
            return []
            
        try:
            # Get query embedding
            response = await self.client.embeddings.create(
                model="text-embedding-ada-002",
                input=query.replace("\n", " ")  # Replace newlines with spaces
            )
            
            if not response or not response.data or len(response.data) == 0:
                print("Warning: No embedding generated for query")
                return []
                
            query_embedding = response.data[0].embedding
            
            # Calculate similarities
            similarities = []
            for idx, embedding in enumerate(self.embeddings):
                if embedding:  # Check if embedding exists
                    similarity = cosine_similarity(query_embedding, embedding)
                    similarities.append((self.texts[idx], similarity))
            
            # Sort by similarity
            similarities.sort(key=lambda x: x[1], reverse=True)
            
            # Return top k results
            return similarities[:k]
            
        except Exception as e:
            print(f"Error in search_by_text: {str(e)}")
            raise e 