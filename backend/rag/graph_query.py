import logging
from typing import List, Dict
from rag.graph_store import GraphStore
from rag.entity_extractor import EntityExtractor

logger = logging.getLogger(__name__)

class GraphQueryEngine:
    """ Motor de busqueda en grafos de conceptos"""
    
    def __init__(self, graph_store: GraphStore):
        """
        Inicializar motor de busqueda
        """
        
        self.graph_store = graph_store
        logger.info("✅ GraphQueryEngine inicializado")

    def query_by_entity(self, entity: str) -> Dict:
        """ Buscar contexto alrededor de una entidad
        
        Input: entity="Machine Learning"
        Output: {
            "entity": "Machine Learning",
            "context": "Concepto que usa Neural Networks, requiere Data...",
            "neighbors": {...},
            "related_concepts": [...]
        }
        Esto es lo que inyectaremos en el LLM
        """
        
        context_data = self.graph_store.get_context(entity)
        
        if "error" in context_data:
            logger.warning(f"⚠️ {context_data['error']}")
            return context_data
        
        # Formatear contexto para el LLM
        formatted_context = self._format_context(context_data)
        
        return {
            "entity": entity,
            "context": formatted_context,
            "neighbors": context_data["neighbors"],
            "related_concepts": context_data["related_concepts"]
        }
    
    def query_by_relationship(self, source: str, target: str) -> Dict:
        """ 
        Buscar camino entre dos conceptos y devolver contexto
        
        Output: {
            "path": ["ML", "Neural Networks", "Data Analysis", "Climate Models", "Climate Change"],
            "context": "Machine Learning utiliza Neural Networks para procesar datos...",
            "edges": [lista de relaciones en el camino]
        }
        """
        
        path = self.graph_store.get_path(source, target)
        
        if not path:
            logger.warning(f"⚠️ No hay conexión entre {source} y {target}")
            return {
                "path": [],
                "context": f"No se encontró conexion directa entre '{source}' y '{target}'",
                "edges": []
            }
            
        # Obtener todas las relaciones en el camino
        edges_in_path = []
        for i in range(len(path) - 1):
            source_node = path[i]
            target_node = path[i+1]
            
            # buscar la arista entre estos nodos
            if self.graph_store.graph.has_edge(source_node, target_node):
                relation = self.graph_store.graph[source_node][target_node]['relation']
                edges_in_path.append({
                    "from": source_node,
                    "relation": relation,
                    "to": target_node
                })
                
        # Formatear contexto
        formatted_context = self._format_path_context(path, edges_in_path)
        
        return {
            "path": path,
            "context": formatted_context,
            "edges": edges_in_path
        }
        
    def query_by_keyword(self, keyword: str) -> Dict:
        """ 
        Buscar conceptos que contengan una palabra clave
        
        Input: keyword="Learning"
        Output: {
            "keyword": "Learning",
            "matched_concepts": ["Machine Learning", "Deep Learning", "Transfer Learning"],
            "contexts": [contexto de cada concepto]
        }
        """
        
        matched_concepts = self.graph_store.search_by_keyword(keyword)
        
        if not matched_concepts:
            logger.warning(f"⚠️ No se encontraron conceptos con '{keyword}'")
            return {
                "keyword": keyword,
                "matched_concepts": [],
                "contexts": []
            }
            
        # Obtener contexto para cada concepto encontrado
        contexts = []
        for concept in matched_concepts:
            context_data = self.graph_store.get_context(concept)
            if "error" not in context_data:
                contexts.append(self._format_context(context_data))
            
        return {
            "keyword": keyword,
            "matched_concepts": matched_concepts,
            "contexts": contexts
        }
    
    def enriched_query(self, query_text: str) -> Dict:
        """
        Query enriquecida: extrae entidades y busca su contexto en el grafo
        
        Input: query_text="¿Qué relación hay entre Machine Learning y Climate Change?"
        Output: {
            "query": "¿Qué relación...",
            "extracted_entities": ["Machine Learning", "Climate Change"],
            "entity_contexts": {...},
            "relationship_context": {...},
            "combined_context": "Texo formateado para LLM con toda la información"
        }
        """
        
        from rag.entity_extractor import EntityExtractor
        
        # Paso 1: Extraer entidades de la query
        extractor = EntityExtractor()
        extracted_entities = extractor.extract_entities(query_text, max_entities=5)
        
        if not extracted_entities:
            logger.warning(f"⚠️ No se extrajeron entidades de la query")
            return {"error": "No se pudieron extraer entidades de la pregunta"}

        # Paso 2: Buscar contexto para cada entidad
        entity_contexts = {}
        for entity in extracted_entities:
            # buscar si existe en el grafo
            if entity in self.graph_store.graph:
                entity_contexts[entity] = self.query_by_entity(entity)
            else:
                # Si no existe, buscar conceptos similares
                similar = self.graph_store.search_by_keyword(entity)
                if similar:
                    entity_contexts[entity] = {
                        "original": entity,
                        "similar_found": similar,
                        "context": self.query_by_entity(similar[0])
                    }    
                    
        # Paso 3: Si hay 2+ entidades, buscar relacion entre ellas
        relationship_context = {}
        if len(extracted_entities) >= 2:
            for i in range(len(extracted_entities) -1):
                source = extracted_entities[i]
                target = extracted_entities[i+1]
                relationship_context[f"{source}_to_{target}"] = self.query_by_relationship(source, target)
        
        # Paso 4: Combinar todo en contexto para el LLM
        combined_context = self._format_enriched_context(
            extracted_entities, 
            entity_contexts,
            relationship_context
        )
        
        return {
            "query": query_text,
            "extracted_entities": extracted_entities,
            "entity_contexts": entity_contexts,
            "relationship_context": relationship_context,
            "combined_context": combined_context
        }
    def _format_context(self, context_data: Dict) -> str:
        """ Formatear contexto de una entidad para el LLM"""
        
        entity = context_data["entity"]
        neighbors = context_data["neighbors"]
        
        formatted = f"CONCEPTO: {entity}\n"
        formatted += "=" * 50 + "\n\n"
        
        if neighbors["outgoing"]:
            formatted += "UTILIZA / CONECTA CON:\n"
            for rel in neighbors["outgoing"]:
                formatted += f"  • {rel['target']} (vía: {rel['relation']})\n"
            formatted += "\n"
        
        if neighbors["incoming"]:
            formatted += "ES UTILIZADO POR / CONECTADO DESDE:\n"
            for rel in neighbors["incoming"]:
                formatted += f"  • {rel['source']} (vía: {rel['relation']})\n"
            formatted += "\n"
        
        return formatted

    def _format_path_context(self, path: List[str], edges: List[Dict]) -> str:
        """Formatear contexto de un camino entre conceptos"""
        
        formatted = "CAMINO ENTRE CONCEPTOS:\n"
        formatted += "=" * 50 + "\n\n"
        
        for i, edge in enumerate(edges):
            formatted += f"{edge['from']} --[{edge['relation']}]--> {edge['to']}\n"
        
        formatted += f"\nSecuencia completa: {' → '.join(path)}\n"
        return formatted
    
    def _format_enriched_context(self, entities: List[str], 
                                 entity_contexts: Dict, 
                                 relationship_context: Dict) -> str:
        """Formatear contexto enriquecido para el LLM"""
        
        formatted = "CONTEXTO ENRIQUECIDO DEL GRAFO:\n"
        formatted += "=" * 70 + "\n\n"
        
        # Contextos de entidades
        for entity, ctx in entity_contexts.items():
            if "context" in ctx:
                formatted += ctx["context"] + "\n"
        
        # Contextos de relaciones
        if relationship_context:
            formatted += "\nRELACIONES ENTRE CONCEPTOS:\n"
            formatted += "-" * 70 + "\n"
            for relation_name, rel_ctx in relationship_context.items():
                if rel_ctx.get("context"):
                    formatted += rel_ctx["context"] + "\n"
        
        return formatted