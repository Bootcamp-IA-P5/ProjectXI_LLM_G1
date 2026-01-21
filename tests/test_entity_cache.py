"""Tests for EntityExtractionCache"""

import pytest
import sys
import os
import tempfile
import json
from pathlib import Path

# Add backend to path so we can import from backend modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from rag.entity_cache import EntityExtractionCache


class TestEntityExtractionCache:
    """Unit tests for EntityExtractionCache"""
    
    def test_cache_initialization(self):
        """Test that cache initializes correctly"""
        with tempfile.TemporaryDirectory() as tmpdir:
            cache_file = os.path.join(tmpdir, "test_cache.json")
            cache = EntityExtractionCache(cache_file=cache_file)
            
            assert cache is not None
            assert cache.cache_file == cache_file
            assert isinstance(cache.cache, dict)
    
    def test_cache_put_and_get(self):
        """Test storing and retrieving from cache"""
        with tempfile.TemporaryDirectory() as tmpdir:
            cache_file = os.path.join(tmpdir, "test_cache.json")
            cache = EntityExtractionCache(cache_file=cache_file)
            
            # Test data
            text = "Machine learning is a subset of AI"
            entities = ["Machine Learning", "AI"]
            relationships = [("Machine Learning", "is_subset_of", "AI")]
            
            # Store in cache
            cache.put(text, entities, relationships)
            
            # Retrieve from cache
            result = cache.get(text)
            
            assert result is not None
            assert result["entities"] == entities
            assert result["relationships"] == relationships
    
    def test_cache_miss(self):
        """Test that cache returns None for non-existent entries"""
        with tempfile.TemporaryDirectory() as tmpdir:
            cache_file = os.path.join(tmpdir, "test_cache.json")
            cache = EntityExtractionCache(cache_file=cache_file)
            
            result = cache.get("Non-existent text")
            assert result is None
    
    def test_cache_persistence(self):
        """Test that cache persists to disk and can be loaded"""
        with tempfile.TemporaryDirectory() as tmpdir:
            cache_file = os.path.join(tmpdir, "test_cache.json")
            
            # Create cache and add data
            cache1 = EntityExtractionCache(cache_file=cache_file)
            text = "Neural networks process data"
            entities = ["Neural Networks", "Data"]
            relationships = [("Neural Networks", "process", "Data")]
            cache1.put(text, entities, relationships)
            cache1.save_cache()
            
            # Create new cache instance and verify data is loaded
            cache2 = EntityExtractionCache(cache_file=cache_file)
            result = cache2.get(text)
            
            assert result is not None
            assert result["entities"] == entities
            assert result["relationships"] == relationships
    
    def test_cache_hash_consistency(self):
        """Test that same text produces same hash"""
        with tempfile.TemporaryDirectory() as tmpdir:
            cache_file = os.path.join(tmpdir, "test_cache.json")
            cache = EntityExtractionCache(cache_file=cache_file)
            
            text = "Consistent text for hashing"
            entities = ["Entity1"]
            relationships = []
            
            # Store twice with same text
            cache.put(text, entities, relationships)
            cache.put(text, entities, relationships)
            
            # Should only have one entry (same hash)
            assert len(cache.cache) == 1
    
    def test_cache_different_texts(self):
        """Test that different texts produce different cache entries"""
        with tempfile.TemporaryDirectory() as tmpdir:
            cache_file = os.path.join(tmpdir, "test_cache.json")
            cache = EntityExtractionCache(cache_file=cache_file)
            
            text1 = "First text"
            text2 = "Second text"
            
            cache.put(text1, ["Entity1"], [])
            cache.put(text2, ["Entity2"], [])
            
            # Should have two entries
            assert len(cache.cache) == 2
            
            result1 = cache.get(text1)
            result2 = cache.get(text2)
            
            assert result1["entities"] == ["Entity1"]
            assert result2["entities"] == ["Entity2"]
    
    def test_cache_clear(self):
        """Test clearing the cache"""
        with tempfile.TemporaryDirectory() as tmpdir:
            cache_file = os.path.join(tmpdir, "test_cache.json")
            cache = EntityExtractionCache(cache_file=cache_file)
            
            # Add some data
            cache.put("Text", ["Entity"], [])
            assert len(cache.cache) == 1
            
            # Clear cache
            cache.clear()
            assert len(cache.cache) == 0
    
    def test_cache_stats(self):
        """Test getting cache statistics"""
        with tempfile.TemporaryDirectory() as tmpdir:
            cache_file = os.path.join(tmpdir, "test_cache.json")
            cache = EntityExtractionCache(cache_file=cache_file)
            
            # Add some entries
            cache.put("Text1", ["E1"], [])
            cache.put("Text2", ["E2"], [])
            cache.put("Text3", ["E3"], [])
            
            stats = cache.get_stats()
            
            assert stats["total_entries"] == 3
            assert stats["cache_file"] == cache_file
