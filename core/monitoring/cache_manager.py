#!/usr/bin/env python3
"""
Cache Manager Intelligent pour LibCST
===================================

Gestionnaire de cache intelligent utilisant Redis pour optimiser
les opérations de parsing et transformation LibCST.

Author: Équipe de Maintenance NextGeneration
Version: 1.0.0
"""

import redis
import hashlib
import json
import logging
from typing import Optional, Dict, Any
import asyncio
from functools import lru_cache

class IntelligentCacheManager:
    """
    Gestionnaire de cache intelligent pour LibCST avec Redis.
    Utilise un système de cache à deux niveaux (mémoire + Redis).
    """
    
    def __init__(self, redis_host: str = "localhost", redis_port: int = 6379,
                 redis_db: int = 0, ttl: int = 3600):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.redis_client = redis.Redis(
            host=redis_host,
            port=redis_port,
            db=redis_db,
            decode_responses=True
        )
        self.ttl = ttl
        self.logger.info("🔄 Cache Manager initialisé avec Redis")

    @lru_cache(maxsize=1000)
    def _compute_hash(self, content: str) -> str:
        """Calcule un hash unique pour le contenu."""
        return hashlib.sha256(content.encode()).hexdigest()

    async def get_cached_ast(self, code: str) -> Optional[Dict[str, Any]]:
        """Récupère l'AST mis en cache pour le code donné."""
        try:
            code_hash = self._compute_hash(code)
            cached = self.redis_client.get(f"ast:{code_hash}")
            if cached:
                self.logger.debug("⚡ AST récupéré du cache")
                return json.loads(cached)
        except Exception as e:
            self.logger.warning(f"⚠️ Erreur lors de la récupération du cache: {e}")
        return None

    async def cache_ast(self, code: str, ast_data: Dict[str, Any]) -> None:
        """Met en cache l'AST pour le code donné."""
        try:
            code_hash = self._compute_hash(code)
            self.redis_client.setex(
                f"ast:{code_hash}",
                self.ttl,
                json.dumps(ast_data)
            )
            self.logger.debug("💾 AST mis en cache")
        except Exception as e:
            self.logger.warning(f"⚠️ Erreur lors de la mise en cache: {e}")

    async def get_cached_transformation(self, code: str, 
                                      transformation_id: str) -> Optional[Dict[str, Any]]:
        """Récupère une transformation mise en cache."""
        try:
            code_hash = self._compute_hash(code)
            cached = self.redis_client.get(f"transform:{code_hash}:{transformation_id}")
            if cached:
                self.logger.debug(f"⚡ Transformation {transformation_id} récupérée du cache")
                return json.loads(cached)
        except Exception as e:
            self.logger.warning(f"⚠️ Erreur lors de la récupération de la transformation: {e}")
        return None

    async def cache_transformation(self, code: str, transformation_id: str,
                                 result: Dict[str, Any]) -> None:
        """Met en cache le résultat d'une transformation."""
        try:
            code_hash = self._compute_hash(code)
            self.redis_client.setex(
                f"transform:{code_hash}:{transformation_id}",
                self.ttl,
                json.dumps(result)
            )
            self.logger.debug(f"💾 Transformation {transformation_id} mise en cache")
        except Exception as e:
            self.logger.warning(f"⚠️ Erreur lors de la mise en cache de la transformation: {e}")

    async def invalidate_cache(self, code: str) -> None:
        """Invalide le cache pour le code donné."""
        try:
            code_hash = self._compute_hash(code)
            keys = self.redis_client.keys(f"*:{code_hash}*")
            if keys:
                self.redis_client.delete(*keys)
                self.logger.info(f"🗑️ Cache invalidé pour {len(keys)} entrées")
        except Exception as e:
            self.logger.warning(f"⚠️ Erreur lors de l'invalidation du cache: {e}")

    def get_cache_stats(self) -> Dict[str, int]:
        """Retourne des statistiques sur l'utilisation du cache."""
        try:
            total_keys = len(self.redis_client.keys("*"))
            ast_keys = len(self.redis_client.keys("ast:*"))
            transform_keys = len(self.redis_client.keys("transform:*"))
            return {
                "total_entries": total_keys,
                "ast_entries": ast_keys,
                "transform_entries": transform_keys
            }
        except Exception as e:
            self.logger.error(f"❌ Erreur lors de la récupération des stats: {e}")
            return {"error": str(e)} 