# Orquestador RAG

import logging
from rag.arxiv_loader import ArxivLoader
from rag.text_splitter import TextSplitter
from rag.embeddings_manager import EmbeddingsManager
from rag.retriever import Retriever

logger = logging.getLogger(__name__)

class RAGSystem:
    """Orquestador: conecta Loader → Splitter → Embeddings → Retriever"""

    def __init__(self):
        """Inicializa todos los componentes"""
        self.arxiv_loader = ArxivLoader(max_papers=5)
        self.text_splitter = TextSplitter(chunk_size=500, chunk_overlap=50)
        self.embeddings_manager = EmbeddingsManager()
        self.retriever = Retriever()
        
    def process_query(self, query: str) -> str:
        """
        Flujo completo:
        1. Buscar papers en ArXiv
        2. Dividir en chunks
        3. Crear embeddings
        4. Guardar en Chroma
        5. Buscar chunks similares
        6. Devolver contexto científico
        """
        
        try:
            logger.info(f"🔍 Iniciando RAG para query: {query}")
            
            # Paso 1: Descargar papers de ArXiv
            papers = self.arxiv_loader.search_and_download(query)
            if not papers:
                logger.warning(f"⚠️ Sin papers encontrados, fallback a sin RAG")
                return "" # Devuelve contexto vacio, se usará sin RAG
            
            # Paso 2: Dividir en chunks
            chunks = self.text_splitter.split_papers(papers)
            
            # Paso 3: Crear embeddings
            chunks_with_embeddings = self.embeddings_manager.embed_chunks(chunks)
            
            # Paso 4: Guardar en base de datos vectorial
            self.retriever.add_embeddings(chunks_with_embeddings)
            
            # Paso 5: Buscar chunks similares
            query_embedding = self.embeddings_manager.embed_text(query)
            similar_chunks = self.retriever.search(query, query_embedding, top_k=3)
            
            # Paso 6: Formatear contexto para el LLM
            if similar_chunks:
                context = self._format_context(similar_chunks)
                logger.info(f"✅ Contexto científico generado ({len(similar_chunks)} chunks)")
                return context
            else:
                logger.warning(f"⚠️ No chunks similares encontrados")
                return ""
            
        except Exception as e:
            logger.error(f"❌ Error en RAG: {e}")
            return "" # Fallback: sin RAG        
        
    def _format_context(self, chunks: list) -> str:
        """
        Formatea los chunks para que el LLM pueda usarlos
        
        Input: [
            {"chunk": "...", "title": "...", "year": 2023, "score": 0.95},
            {"chunk": "...", "title": "...", "year": 2022, "score": 0.88}
        ]
        
        Output: String formateado para inyectar en prompt
        """
        
        context = "CONTEXTO CIENTIFICO RELEVANTE:\n"
        context += "=" * 50 + "\n\n"

        for idx, chunk in enumerate(chunks, 1):
            context += f"[Fuente {idx}] {chunk['title']} ({chunk['year']})\n"
            context += f"Relevancia: {chunk['score']:.2%}\n"
            context += f"Autores: {chunk['authors']}\n"
            context += f"Contenido: {chunk['chunk'][:500]}...\n"  # Primeras 500 caracteres
            context += "-" * 50 + "\n\n"        
        
        return context
        
        
        
        