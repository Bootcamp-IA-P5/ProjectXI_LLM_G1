from sentence_transformers import SentenceTransformer
import logging

logger = logging.getLogger(__name__)

class EmbeddingsManager:
    """ Convertir textos a vectores numericos """

    def __init__(self, model_name: str = "all-MiniLm-L6-v2"):
        """
        model_name: Nombre del modelo preentrenado
        "all-MiniLm-L6-v2" es pequeño, rapido y gratis

        ¿Qué hace __init__?
        descarga el modelo de HF la primera vez, luego se cachea
        """

        try:
            self.model = SentenceTransformer(model_name)
            logger.info(f"✅ Embeddings model cargado: {model_name}")
        except Exception as e:
            logger.error(f"❌ Error cargando embeddings model: {e}")
            raise
    
    def embed_text(self, text: str):
        """
        Input: "La IA es..."
        Output: [0.23, -0.5, 0.8, ..., 0.12]  ← Vector de 384 números
        ¿Por qué 384 números? El modelo "all-MiniLM" tiene dimensión 384.
        """
        try:
            embedding = self.model.encode(text)
            return embedding
        except Exception as e:
            logger.error(f"❌ Error embeding texto: {e}")
            return None

    def embed_chunks(self, chunks_data: list) -> list:
        """ 
        Recibe lista de chunks y crea embeddings para cad auno
        
        Input: [
            {"title": "Paper 1", "chunk": "Lorem ipsum...", ...},
            {"title": "Paper 1", "chunk": "Dolor sit...", ...}
        ]
        
        Output: [
            {"title": "Paper 1", "chunk": "Lorem ipsum...", "embedding": [0.23, -0.5, ...], ...},
            {"title": "Paper 1", "chunk": "Dolor sit...", "embedding": [0.12, 0.4, ...], ...}
        ]
        """
        embedded_chunks = []

        for idx, chunk_data in enumerate(chunks_data):
            
            embedding = self.embed_text(chunk_data["chunk"])

            if embedding is not None:
                chunk_data["embedding"] = embedding
                embedded_chunks.append(chunk_data)

                if (idx + 1) % 5 == 0: # Cada 5 chunks, log
                    logger.info(f"✅ {idx + 1} chunks embebidos")

        logger.info(f"✅ Total: {len(embedded_chunks)} chunks embebidos")
        return embedded_chunks