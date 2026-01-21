# Como funciona un grafo
"""
import networkx as nx

# Crear grafo
G = nx.DiGraph() # Directed Graph (aristas con direccion)

# Agregar nodos
G.add_node("Machine Learning")
G.add_node("Neural Networks")

# Agregar aristas (relaciones)
G.add_edge("Machine Learning", "Neural Networks", relation= "usa")

# Buscar vecinos
vecinos = list(G.neighbors("Machine Learning"))
# OUTPUT: ["Neural Networks"]
"""

import networkx as nx
import logging
from typing import List, Dict, Tuple
import json
from pathlib import Path
import os

GRAPH_FILE_DEFAULT = Path(
    os.getenv(
        "KNOWLEDGE_GRAPH_PATH",
        str(Path(__file__).resolve().parent / "data" / "knowledge_graph.json"),
    )
)

logger = logging.getLogger(__name__)

class GraphStore:
    """ Almacena y gestiona grafo de conceptos científicos"""
    
    def __init__(self, graph_file: str = str(GRAPH_FILE_DEFAULT)):
        """ 
        Inicializar almacen de grafo
        """
        
        self.graph_file = str(graph_file)
        self.graph = nx.DiGraph()   # Directed Graph, las relaciones tienen direccion
        self.load_graph()           # Cargar grafo anterior si existe
        
        logger.info("✅ GraphStore inicializado")

    def add_entity(self, entity: str, metadata: Dict = None):
        """
        Agregar nodo (entidad/concepto) al grafo
        
        Args:
            entity: Nombre del concepto (ej: "Machine Learning")
            metadata: Información adicional (ej: {"tipo": "tecnica", "año": 2012})
            
        """
        
        if entity not in self.graph:
            self.graph.add_node(entity, metadata=metadata or {})
            logger.info(f"✅ Nodo agregado: {entity}")
        else:
            # Si ya existe, actualizar metadata
            if metadata:
                self.graph.nodes[entity].setdefault('metadata', {}).update(metadata)
                
    def add_relationship(self, source: str, relation: str, target: str):
        """
        Agregar relación (arista) entre dos nodos
        
        Args:  
            source: Concepto origen
            relation: Tipo de relación
            target: Concepto destino
        
        Output: Crea arista dirigida
            Machine Learning --[usa]--> Neural Networks
        """
        
        # Asegurar que ambos nodos existen
        self.add_entity(source)
        self.add_entity(target)
        
        # Agregar arista con relacion
        self.graph.add_edge(source, target, relation=relation)
        logger.info(f"✅ Relación: {source} --[{relation}]--> {target}")

    def add_graph_data(self, entities: List[str], relationships: List[Tuple[str, str, str]]):
        """
        Agregar multiples entradas y relaciones
        
        Input:
            entities: ...
            relationships: [
                ("Machine Learning", "usa", "Neural Networks"),
                ("Neural Networks", "requiere", "Data")
            ]
        """
        
        # Agregar todos los nodos
        for entity in entities:
            self.add_entity(entity)
            
        # Agregar todas las relaciones
        for source, relation, target in relationships:
            # Verificar que ambas entidades existen en la lista original
            if source in entities and target in entities:
                self.add_relationship(source, relation, target)
            else:
                logger.warning(f"⚠️ Relación ignorada: {source} → {target} (entidad no en lista)")
                
    def get_neighbors(self, entity: str, depth: int = 1) -> Dict[str, List]:
        """
        Obtener vecinos de un concepto (con profundidad)
        
        depth=1: Solo vecinos directos
        depth=2: Vecino de vecinos
        
        Input: entity="Machine Learning", depth=1
        Output: {
            "outgoing": [
                {"target": "Neural Networks", "relation": "usa", "depth": 1},
                {"target": "Data", "relation": "procesa", "depth": 1}
            ],
            "incoming": [
                {"source": "AI", "relation": "es_tipo_de", "depth": 1}
            ]
        }
        """
                
        if entity not in self.graph:
            logger.warning(f"⚠️ Entidad no encontrada: {entity}")
            return {"outgoing": [], "incoming": []}
        
        neighbors_info = {
            "outgoing": [], # Relaciones que salen de entity
            "incoming": [], # Relaciones que llegan a entity
        }
        
        visited_outgoing = set()
        visited_incoming = set()
        
        # Vecinos SALIENTES (entity -> X) con profundidad
        self._collect_outgoing_neighbors(entity, depth, 1, visited_outgoing, neighbors_info["outgoing"])
        
        # Vecinos ENTRANTES (X -> entity) con profundidad
        self._collect_incoming_neighbors(entity, depth, 1, visited_incoming, neighbors_info["incoming"])
            
        logger.info(f"✅ {len(neighbors_info['outgoing'])} relaciones salientes, {len(neighbors_info['incoming'])} entrantes (profundidad={depth})")
        return neighbors_info
    
    def _collect_outgoing_neighbors(self, entity: str, max_depth: int, current_depth: int, visited: set, results: List[Dict]):
        """Helper para recolectar vecinos salientes recursivamente"""
        if current_depth > max_depth:
            return
        
        for neighbor in self.graph.successors(entity):
            if neighbor not in visited:
                visited.add(neighbor)
                relation = self.graph[entity][neighbor]['relation']
                results.append({
                    "target": neighbor,
                    "relation": relation,
                    "depth": current_depth
                })
                
                # Recursión para siguiente nivel
                if current_depth < max_depth:
                    self._collect_outgoing_neighbors(neighbor, max_depth, current_depth + 1, visited, results)
    
    def _collect_incoming_neighbors(self, entity: str, max_depth: int, current_depth: int, visited: set, results: List[Dict]):
        """Helper para recolectar vecinos entrantes recursivamente"""
        if current_depth > max_depth:
            return
        
        for neighbor in self.graph.predecessors(entity):
            if neighbor not in visited:
                visited.add(neighbor)
                relation = self.graph[neighbor][entity]['relation']
                results.append({
                    "source": neighbor,
                    "relation": relation,
                    "depth": current_depth
                })
                
                # Recursión para siguiente nivel
                if current_depth < max_depth:
                    self._collect_incoming_neighbors(neighbor, max_depth, current_depth + 1, visited, results)
    
    def get_path(self, source: str, target: str) -> List[str]:
        """
        Obtener camino mas corto entre dos conceptos
        
        Input: source="Machine Learning", target="Data"
        Output: ["Machine Learning", "Neural Networks", "Data"]
        
        Esto muestra cómo están conectados los conceptos
        """
        
        try:
            path = nx.shortest_path(self.graph, source, target)
            logger.info(f"✅ Camino encontrado: {' → '.join(path)}")
            return path
        except nx.NetworkXNoPath:
            logger.warning(f"⚠️ No hay camino entre {source} y {target}")
            return []
        except Exception as e:
            logger.error(f"❌ Error buscando camino: {e}")
            return []
        
    def search_by_keyword(self, keyword: str) -> List[str]:
        """ 
        Buscar nodos que contengan una palabra clave
        
        Input: keyword="Learning"
        Output: ["Machine Learning", "Deep Learning", "Transfer Learning"]
        """
        
        keyword_lower = keyword.lower()
        matching_nodes = [
            node for node in self.graph.nodes()
            if keyword_lower in node.lower()
        ]
        
        logger.info(f"✅ {len(matching_nodes)} nodos contienen '{keyword}'")
        return matching_nodes
    
    def get_context(self, entity: str, depth: int = 2) -> Dict:
        """
        Obtener contexto completo de una entidad (vecinos + metadata)
        
        Output: {
            "entity": "Machine Learning",
            "metadata": {...},
            "neighbors": {...},
            "related_concepts": ["Neural Networks", "Deep Learning", ...]
        }
        
        Esto es lo que inyectaremos en el LLM como contexto
        """
        
        if entity not in self.graph:
            return {"error": f"Entidad '{entity}' no encontrada"}
        
        neighbors = self.get_neighbors(entity, depth)
        
        # Recopilar todos los conceptos relacionados
        related_concepts = set()
        for neighbor in neighbors["outgoing"]:
            related_concepts.add(neighbor["target"])
        for neighbor in neighbors["incoming"]:
            related_concepts.add(neighbor["source"])
            
        return {
            "entity": entity,
            "metadata": self.graph.nodes[entity].get('metadata', {}),
            "neighbors": neighbors,
            "related_concepts": list(related_concepts)
        }
        
    def save_graph(self):
        """ Guardar grafo a archivo JSON (persistencia)"""
        
        try: 
            # Preparar datos para JSON (los grafos no se serializan directamente)
            nodes_data = [
                {
                    "id": node,
                    "metadata": self.graph.nodes[node].get('metadata', {})
                }
                for node in self.graph.nodes()
            ]
            
            edges_data = [
                {
                    "source": source,
                    "target": target,
                    "relation": self.graph[source][target]["relation"]
                }
                for source, target in self.graph.edges()
            ]
            
            graph_data = {
                "nodes": nodes_data,
                "edges": edges_data
            }
            
            # Crear directorio si no existe
            Path(self.graph_file).parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.graph_file, 'w', encoding='utf-8') as f:
                json.dump(graph_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"✅ Grafo guardado en {self.graph_file}")

        except Exception as e:
            logger.error(f"❌ Error guardando grafo: {e}")

    def load_graph(self):
        """ Cargar grafo de archivo JSON"""
        
        try:
            if not Path(self.graph_file).exists():
                logger.info(f"ℹ️ Archivo {self.graph_file} no existe (grafo vacío)")
                return
            
            with open(self.graph_file, 'r', encoding='utf-8') as f:
                graph_data = json.load(f)
            
            # Reconstruir grafo
            for node in graph_data.get("nodes", []):
                self.add_entity(node["id"], node.get("metadata", {}))
            
            for edge in graph_data.get("edges", []):
                self.add_relationship(edge["source"], edge["relation"], edge["target"])
            
            logger.info(f"✅ Grafo cargado desde {self.graph_file}")
            
        except Exception as e:
            logger.error(f"❌ Error cargando grafo: {e}")

    def get_stats(self) -> Dict:
        """ Obtener estadísticas del grafo"""
        
        return {
            "total_nodes": self.graph.number_of_nodes(),
            "total_edges": self.graph.number_of_edges(),
            "density": nx.density(self.graph),              # Que tan conectado está (0-1)
            "avg_degree": sum(dict(self.graph.degree()).values()) / max(1, self.graph.number_of_nodes())    
        }