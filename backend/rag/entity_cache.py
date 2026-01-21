"""
Cache for entity extraction results to avoid redundant LLM calls.

This cache stores the results of entity extraction (entities and relationships)
keyed by paper content hash, allowing us to skip expensive LLM API calls for
papers we've already processed.
"""

import json
import hashlib
import logging
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import os

logger = logging.getLogger(__name__)

CACHE_FILE_DEFAULT = Path(
    os.getenv(
        "ENTITY_CACHE_PATH",
        str(Path(__file__).resolve().parent / "data" / "entity_cache.json"),
    )
)


class EntityExtractionCache:
    """Cache for storing entity extraction results to avoid redundant LLM calls"""

    def __init__(self, cache_file: str = str(CACHE_FILE_DEFAULT)):
        """Initialize cache"""
        self.cache_file = str(cache_file)
        self.cache: Dict[str, Dict] = {}
        self.load_cache()
        logger.info(f"✅ EntityExtractionCache inicializado con {len(self.cache)} entradas")

    def _compute_hash(self, text: str) -> str:
        """Compute SHA-256 hash of text for cache key"""
        return hashlib.sha256(text.encode('utf-8')).hexdigest()

    def get(self, text: str) -> Optional[Dict[str, any]]:
        """
        Get cached extraction results for text
        
        Args:
            text: Paper text to look up
            
        Returns:
            Dict with 'entities' and 'relationships' if cached, None otherwise
        """
        cache_key = self._compute_hash(text)
        cached_data = self.cache.get(cache_key)
        
        if cached_data:
            logger.info(f"✅ Cache hit para paper (hash: {cache_key[:8]}...)")
            return {
                "entities": cached_data["entities"],
                "relationships": [tuple(rel) for rel in cached_data["relationships"]]
            }
        
        return None

    def put(self, text: str, entities: List[str], relationships: List[Tuple[str, str, str]]):
        """
        Store extraction results in cache
        
        Args:
            text: Paper text (used as cache key)
            entities: List of extracted entities
            relationships: List of extracted relationships (as tuples)
        """
        cache_key = self._compute_hash(text)
        
        # Convert tuples to lists for JSON serialization
        self.cache[cache_key] = {
            "entities": entities,
            "relationships": [list(rel) for rel in relationships]
        }
        
        logger.info(f"✅ Guardado en cache: {len(entities)} entidades, {len(relationships)} relaciones (hash: {cache_key[:8]}...)")

    def save_cache(self):
        """Save cache to disk"""
        try:
            # Create directory if it doesn't exist
            Path(self.cache_file).parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.cache, f, indent=2, ensure_ascii=False)
            
            logger.info(f"✅ Cache guardado en {self.cache_file} ({len(self.cache)} entradas)")
        
        except Exception as e:
            logger.error(f"❌ Error guardando cache: {e}")

    def load_cache(self):
        """Load cache from disk"""
        try:
            if not Path(self.cache_file).exists():
                logger.info(f"ℹ️ Archivo de cache {self.cache_file} no existe (cache vacío)")
                return
            
            with open(self.cache_file, 'r', encoding='utf-8') as f:
                self.cache = json.load(f)
            
            logger.info(f"✅ Cache cargado desde {self.cache_file} ({len(self.cache)} entradas)")
        
        except Exception as e:
            logger.error(f"❌ Error cargando cache: {e}")
            self.cache = {}

    def clear(self):
        """Clear all cached entries"""
        self.cache = {}
        logger.info("✅ Cache limpiado")

    def get_stats(self) -> Dict:
        """Get cache statistics"""
        return {
            "total_entries": len(self.cache),
            "cache_file": self.cache_file
        }
