#!/usr/bin/env python3
"""
OPTIMISATION CACHE ADAPTATEUR V4
===============================

Stratégie de cache intelligente avec :
- Prédiction des patterns fréquents
- Préchargement adaptatif
- Gestion LRU (Least Recently Used) avancée
"""

import time
import json
import hashlib
from typing import Dict, Any, Optional, List, Tuple
from collections import OrderedDict
import logging

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)

class CacheEntry:
    """Entrée de cache avec métadonnées"""
    
    def __init__(self, key: str, value: Any, pattern: str = ""):
        self.key = key
        self.value = value
        self.pattern = pattern
        self.access_count = 0
        self.last_access = time.time()
        self.creation_time = time.time()
    
    def access(self):
        """Enregistre un accès à cette entrée"""
        self.access_count += 1
        self.last_access = time.time()
    
    def get_score(self) -> float:
        """Calcule un score pour cette entrée basé sur fréquence et récence"""
        age = time.time() - self.creation_time
        recency = time.time() - self.last_access
        frequency = self.access_count / max(1, age)
        return frequency * (1 / (1 + recency))

class AdaptiveCacheOptimizer:
    """Cache intelligent avec optimisation adaptative"""
    
    def __init__(self, max_size: int = 1000):
        self.max_size = max_size
        self.cache = OrderedDict()  # LRU cache
        self.pattern_stats = {}  # Statistiques des patterns
        self.preload_patterns: List[str] = []
        
    def _generate_key(self, data: Any) -> str:
        """Génère une clé de cache unique"""
        if isinstance(data, str):
            return hashlib.sha256(data.encode()).hexdigest()
        return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()
    
    def _extract_pattern(self, code: str) -> str:
        """Extrait le pattern d'indentation du code"""
        try:
            lines = code.split('\n')
            indents = []
            for line in lines:
                if line.strip():
                    indent = len(line) - len(line.lstrip())
                    indents.append(str(indent))
            return ','.join(indents)
        except:
            return ""
    
    def _update_pattern_stats(self, pattern: str):
        """Met à jour les statistiques de patterns"""
        self.pattern_stats[pattern] = self.pattern_stats.get(pattern, 0) + 1
        
        # Mise à jour des patterns à précharger
        sorted_patterns = sorted(
            self.pattern_stats.items(),
            key=lambda x: x[1],
            reverse=True
        )
        self.preload_patterns = [p[0] for p in sorted_patterns[:5]]
    
    def _cleanup_cache(self):
        """Nettoie le cache en utilisant une stratégie intelligente"""
        if len(self.cache) <= self.max_size:
            return
            
        # Trie les entrées par score
        entries = list(self.cache.values())
        entries.sort(key=lambda e: e.get_score())
        
        # Garde les entrées avec les meilleurs scores
        to_keep = entries[len(entries) - self.max_size:]
        
        # Reconstruit le cache
        self.cache.clear()
        for entry in to_keep:
            self.cache[entry.key] = entry
    
    def get(self, key: str) -> Optional[Any]:
        """Récupère une valeur du cache"""
        if key in self.cache:
            entry = self.cache[key]
            entry.access_count += 1
            entry.last_access = time.time()
            # Déplacer l'entrée à la fin (LRU)
            self.cache.move_to_end(key)
            return entry.value
        return None
    
    def put(self, key: str, value: Any) -> None:
        """Ajoute une valeur dans le cache"""
        # Extraire le pattern d'indentation
        pattern = self._extract_pattern(key)
        
        # Créer l'entrée
        entry = CacheEntry(key, value, pattern)
        
        # Mettre à jour les statistiques du pattern
        if pattern in self.pattern_stats:
            self.pattern_stats[pattern] += 1
        else:
            self.pattern_stats[pattern] = 1
            
        # Ajouter au cache
        self.cache[key] = entry
        self.cache.move_to_end(key)
        
        # Nettoyer le cache si nécessaire
        if len(self.cache) > self.max_size:
            # Supprimer les entrées les moins utilisées
            while len(self.cache) > self.max_size:
                oldest_key, oldest_entry = next(iter(self.cache.items()))
                del self.cache[oldest_key]
                
    def preload(self, generator_func) -> int:
        """Précharge le cache avec des données générées"""
        count = 0
        for pattern in self.preload_patterns:
            try:
                data = generator_func(pattern)
                if data:
                    self.put(data, generator_func(data))
                    count += 1
            except Exception as e:
                logger.error(f"Erreur lors du préchargement pour pattern {pattern}: {e}")
        return count
    
    def get_stats(self) -> Dict[str, Any]:
        """Retourne les statistiques du cache"""
        total_entries = len(self.cache)
        total_accesses = sum(e.access_count for e in self.cache.values())
        
        pattern_distribution = {}
        for entry in self.cache.values():
            pattern_distribution[entry.pattern] = pattern_distribution.get(entry.pattern, 0) + 1
        
        return {
            "total_entries": total_entries,
            "total_accesses": total_accesses,
            "pattern_stats": self.pattern_stats,
            "pattern_distribution": pattern_distribution,
            "preload_patterns": self.preload_patterns
        }

# Exemple d'utilisation
if __name__ == "__main__":
    # Configuration du cache
    cache = AdaptiveCacheOptimizer(max_size=100)
    
    # Exemple de données
    test_data = [
        "def test():\n    print('test')\n    return True",
        "def test():\n  if True:\n    print('test')\n  return True",
        "class Test:\n    def __init__(self):\n        pass"
    ]
    
    # Test du cache
    for data in test_data:
        result = cache.get(data)
        if result is None:
            # Simulation de traitement
            time.sleep(0.1)
            result = f"processed_{data}"
            cache.put(data, result)
    
    # Affichage des stats
    stats = cache.get_stats()
    logger.info("\nStatistiques du cache :")
    logger.info(f"Entrées totales : {stats['total_entries']}")
    logger.info(f"Accès totaux : {stats['total_accesses']}")
    logger.info(f"Patterns les plus fréquents : {stats['preload_patterns']}") 