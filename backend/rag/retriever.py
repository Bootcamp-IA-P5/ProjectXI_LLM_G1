import chromadb
import logging
from typing import List

logger = logging.getLogger(__name__)

class Retriever:
    """ Buscar chunks similres en base de datos vectorial """
    
    def __init__(self, collection_name: str = "scientific_papers"):
        """
        collection_name: Nombre de la coleccion en Chroma
        (como una tabla en BBDD tradicional)
        """
        
        try:
            # Conecta a Chroma (crea DB local en .chroma/)
            self.client = chromadb.Client()
            self.collection_name = collection_name

            # La coleccion existe? si no, la crea
            self.collection = self.client.get_or_create_collection(
                name=collection_name,
                metadata={"hnsw:space": "cosine"} # Busqueda por similitud de coseno
            )

            logger.info(f"✅ Colección '{collection_name}' lista")
        except Exception as e:
            logger.error(f"❌ Error inicializando Chroma: {e}")
            raise
    
    def add_embeddings(self, chunks_with_embeddings: list):
        """
        Recibe chunks con embeddings y los guarda en Chroma
        
        Input: [
            {
                "arxiv_id": "2301.00001",
                "title": "Paper 1",
                "chunk": "Lorem ipsum...",
                "embedding": [0.23, -0.5, ...]
            },
            ...
        ]
        """
        
        try: 
            ids = []
            documents = []
            metadatas = []
            embeddings = []
            
            for chunk in chunks_with_embeddings:
                # Crear ID unico: "arxiv_id_chunk_id"
                chunk_id = f"{chunk['arxiv_id']}_chunk{chunk['chunk_id']}"
                
                ids.append(chunk_id)
                documents.append(chunk["chunk"]) # el texto
                embeddings.append(chunk["embedding"]) # El vector
                
                # Metadatos (informacion adicional para buscar despues)
                metadatas.append({
                    "title": chunk["title"],
                    "authors": ",".join(chunk["authors"]),
                    "year": str(chunk["year"]),
                    "arxiv_id": chunk["arxiv_id"]
                })
                
            # Guardar todo en Chroma
            self.collection.add(
                ids=ids,
                documents=documents,
                embeddings=embeddings,
                metadatas=metadatas
            )

            logger.info(f"✅ {len(ids)} chunks guardados en Chroma")

        except Exception as e:
            logger.error(f"❌ Error guardando embeddings: {e}")
            raise
    
    def search(self, query: str, query_embedding, top_k: int = 3) -> List[dict]:
        """
        Busca chunks similares a la query
        
        Input: 
            query: "cambio climático antropogénico"
            query_embedding: Vector numérico de la query
            top_k: Cuántos resultados devolver
        
        Output: [
            {
                "chunk": "El cambio climático es causado por...",
                "title": "Paper 1",
                "score": 0.95,  ← Similitud (0-1, más alto = más parecido)
                "authors": "Smith et al.",
                "year": 2023
            },
            ...
        ]
        """
        
        try:
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k
            )
            
            # Reformatear resultados
            retrieved_chunks = []
            
            for i in range(len(results["ids"][0])):
                retrieved_chunks.append({
                    "chunk": results["documents"][0][i],
                    "title": results["metadatas"][0][i]["title"],
                    "authors": results["metadatas"][0][i]["authors"],
                    "year": results["metadatas"][0][i]["year"],
                    "score": 1 - results["distances"][0][i]  # Convertir distancia a similitud
                })

            logger.info(f"✅ {len(retrieved_chunks)} chunks similares encontrados")
            return retrieved_chunks
        
        except Exception as e:
            logger.error(f"❌ Error buscando en Chroma: {e}")
            return []



