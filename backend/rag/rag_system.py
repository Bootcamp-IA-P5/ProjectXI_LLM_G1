# Orquestador RAG (Ahora actualizado con GRAPH RAG)

from typing import List, Dict
import logging
from rag.arxiv_loader import ArxivLoader
from rag.text_splitter import TextSplitter
from rag.embeddings_manager import EmbeddingsManager
from rag.retriever import Retriever
from rag.entity_extractor import EntityExtractor
from rag.graph_store import GraphStore
from rag.graph_query import GraphQueryEngine

logger = logging.getLogger(__name__)

class RAGSystem:
    """Orquestador: conecta Loader → Splitter → Embeddings → Retriever
    
    Update: Sistema RAG completo: Vector RAG + Graph RAG
    """

    def __init__(self):
        """Inicializa sistema RAG con ambas técnicas y todos los componentes"""
        self.arxiv_loader = ArxivLoader(max_papers=5)
        self.text_splitter = TextSplitter(chunk_size=500, chunk_overlap=50)
        self.embeddings_manager = EmbeddingsManager()
        self.retriever = Retriever()
        
        # Componentes Graph RAG
        self.entity_extractor = EntityExtractor()
        self.graph_store = GraphStore()
        self.graph_query_engine = GraphQueryEngine(self.graph_store)
        
        logger.info("✅ RAG System inicializado (Vector + Graph)")
        
    def process_query(self, query: str, use_graph_rag: bool = True) -> str:
        """
        Flujo completo:
        1. Buscar papers en ArXiv
        2. Dividir en chunks
        3. Crear embeddings
        4. Guardar en Chroma
        5. Buscar chunks similares
        6. Devolver contexto científico
        
        Update: Procesar query con ambas técnicas RAG:
        Query > Vector RAG + Graph RAG (combinado) > Respuesta
        
        Output: Contexto científico inyectable en LLM
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
            vector_context = ""
            if similar_chunks:
                vector_context = self._format_context(similar_chunks)
                logger.info(f"✅ Vector RAG: {len(similar_chunks)} chunks similares")
            else:
                logger.warning(f"⚠️ No chunks similares encontrados")
                
            # ============================================
            # PARTE 2: GRAPH RAG (NUEVO) ✅
            # ============================================
            
            if not use_graph_rag:
                return vector_context # Devolver solo Vector RAG  
            
            try:
                # Paso 7: Aprender del conjunto de papers (construir grafo)
                # Evitar reprocesar los mismos papers en cada consulta
                if not hasattr(self, "_processed_paper_ids"):
                    self._processed_paper_ids = set()
                
                new_papers = []
                new_paper_ids = set()
                for paper in papers:
                    paper_id = None
                    # Intentar obtener un identificador estable del paper
                    if isinstance(paper, dict):
                        paper_id = paper.get("id")
                    else:
                        paper_id = getattr(paper, "id", None)
                    
                    # Si no hay ID, lo tratamos como nuevo para no cambiar el comportamiento
                    if paper_id is None or paper_id not in self._processed_paper_ids:
                        new_papers.append(paper)
                        if paper_id is not None:
                            new_paper_ids.add(paper_id)
                
                if new_papers:
                    self.learn_from_papers(new_papers)
                    self._processed_paper_ids.update(new_paper_ids)
                else:
                    logger.info("ℹ️ Graph RAG: no hay nuevos papers para aprender; se reutiliza el grafo existente")
                
                # Paso 8: Consulta enriquecida al grafo
                graph_results = self.graph_query_engine.enriched_query(query)
                graph_context = graph_results.get("combined_context", "")
                logger.info(f"✅ Graph RAG: {len(graph_results.get('extracted_entities', []))} entidades extraídas")

            except Exception as e:
                logger.warning(f"⚠️ Graph RAG falló, usando solo Vector RAG: {e}")
                graph_context = ""
                
            # ============================================
            # PARTE 3: Combinar ambos contextos
            # ============================================
            
            combined_context = self._combine_contexts(vector_context, graph_context, query)
            logger.info("✅ RAG System procesó query (Vector + Graph)")
            return combined_context
        
        except Exception as e:
            logger.error(f"❌ Error en RAG: {e}")
            return ""
    
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
        

    # ============================================================
    # NUEVOS MÉTODOS
    # ============================================================

    def learn_from_papers(self, papers: List[Dict]):
        """ 
        Construir grafo de conceptos a partir de papers
        
        Para cada paper:
        1. Extraer entidades (conceptos clave)
        2. Extraer relaciones entre entidades
        3. Agregar al grafo
        4. Guardar grafo
        """
        
        if not papers: 
            logger.warning("⚠️ Lista de papers vacía")
            return
        
        for idx, paper in enumerate(papers, 1):
            try:
                # Combinar título + abstract + contenido
                text = f"{paper.get('title', '')} {paper.get('abstract', '')} {paper.get('content', '')}"
                
                logger.info(f"📚 Procesando paper {idx}/{len(papers)}: {paper.get('title', 'Unknown')[:50]}...")

                # Extraer entidades y relaciones
                graph_data = self.entity_extractor.extract_graph_data(text)
                
                if graph_data["entities"]:
                    # Agregar al grafo
                    self.graph_store.add_graph_data(
                        entities=graph_data["entities"],
                        relationships=graph_data["relationships"]
                    )

                    logger.info(f"✅ {len(graph_data['entities'])} entidades extraídas de paper {idx}")
            
            except Exception as e:
                logger.error(f"❌ Error procesando paper {idx}: {e}")
                continue
        
        # Guardar grafo después de procesar todos los papers
        self.graph_store.save_graph()
        stats = self.graph_store.get_stats()
        logger.info(f"✅ Grafo guardado. Stats: {stats}")

    def _combine_contexts(self, vector_context: str, graph_context: str, query: str) -> str:
        """
        Combinar contextos de Vector RAG + Graph RAG
        Orden: Graph RAG (relaciones) -> Vector RAG (fuentes)
        """
        
        combined = "CONTEXTO CIENTÍFICO COMPLETO (Vector + Graph RAG):\n"
        combined += "=" * 70 + "\n"
        combined += f"QUERY: {query}\n"
        combined += "=" * 70 + "\n\n"
        
        # Parte 1: Relaciones conceptuales (Graph RAG)
        if graph_context:
            combined += "PARTE 1: RELACIONES CONCEPTUALES (GRAPH RAG)\n"
            combined += "-" * 70 + "\n"
            combined += graph_context + "\n\n"
        
        # Parte 2: Fuentes científicas (Vector RAG)
        if vector_context:
            combined += "PARTE 2: FUENTES CIENTÍFICAS (VECTOR RAG)\n"
            combined += "-" * 70 + "\n"
            combined += vector_context + "\n"
        
        return combined