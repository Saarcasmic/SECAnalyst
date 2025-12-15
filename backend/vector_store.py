import os
import time
from typing import List
from openai import OpenAI
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv

load_dotenv()

class VectorDB:
    def __init__(self, api_key: str):
        self.openai_client = OpenAI(api_key=api_key)
        self.pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        self.index_name = "sec-financial-index"
        
        # Ensure index exists
        self.get_or_create_index(self.index_name)
        self.index = self.pc.Index(self.index_name)

    def get_or_create_index(self, index_name: str):
        """
        Check if index exists, else create it.
        """
        existing_indexes = [i.name for i in self.pc.list_indexes()]
        
        if index_name not in existing_indexes:
            print(f"Creating index '{index_name}'...")
            self.pc.create_index(
                name=index_name,
                dimension=1536, # text-embedding-3-small
                metric="cosine",
                spec=ServerlessSpec(
                    cloud="aws",
                    region="us-east-1"
                )
            )
            # Wait for index to be ready
            while not self.pc.describe_index(index_name).status['ready']:
                time.sleep(1)
            print(f"Index '{index_name}' created successfully.")
        else:
            print(f"Index '{index_name}' already exists.")

    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings using OpenAI.
        """
        try:
            # OpenAI recommends replacing newlines with spaces for best results
            texts = [t.replace("\n", " ") for t in texts]
            
            response = self.openai_client.embeddings.create(
                input=texts,
                model="text-embedding-3-small"
            )
            return [data.embedding for data in response.data]
        except Exception as e:
            print(f"Error generating embeddings: {e}")
            raise

    def upsert_chunks(self, chunks: List[str], metadata_base: dict):
        """
        Generate embeddings for chunks and upsert to Pinecone.
        """
        print(f"Generating embeddings for {len(chunks)} chunks...")
        embeddings = self.generate_embeddings(chunks)
        
        vectors = []
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            # Create a unique ID for each chunk
            chunk_id = f"{metadata_base['company']}_{metadata_base['year']}_{i}"
            
            # Prepare metadata
            metadata = metadata_base.copy()
            metadata["text"] = chunk
            
            vectors.append({
                "id": chunk_id,
                "values": embedding,
                "metadata": metadata
            })
            
        print(f"Upserting {len(vectors)} vectors to Pinecone...")
        # Batch upsert (Pinecone recommends batches of 100-200 if vectors are large, 
        # but for small text chunks, larger batches might work. We'll stick to a safe 100.)
        batch_size = 100
        for i in range(0, len(vectors), batch_size):
            batch = vectors[i:i + batch_size]
            self.index.upsert(vectors=batch)
            
        print("Upsert complete.")

    def query_vectors(self, query_text: str, top_k: int = 3) -> List[str]:
        """
        Query the Pinecone index for similar text chunks.
        """
        # Generate embedding for the query
        query_embedding = self.generate_embeddings([query_text])[0]
        
        # Query Pinecone
        results = self.index.query(
            vector=query_embedding,
            top_k=top_k,
            include_metadata=True
        )
        
        matches = []
        for match in results['matches']:
            if match.get('metadata') and 'text' in match['metadata']:
                matches.append(match['metadata']['text'])
                
        return matches
