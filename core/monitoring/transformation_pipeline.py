#!/usr/bin/env python3
"""
Pipeline de Transformation LibCST Optimisé
========================================

Pipeline optimisé pour les transformations LibCST avec :
- Cache intelligent AST
- Object pooling
- Métriques de performance
- Gestion des erreurs robuste

Author: Équipe de Maintenance NextGeneration
Version: 1.0.0
"""

import libcst as cst
from typing import List, Dict, Any, Type, Optional, Tuple
import logging
import time
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor
import asyncio
from functools import lru_cache
import weakref

from .cache_manager import IntelligentCacheManager

@dataclass
class TransformationMetrics:
    """Métriques de performance pour une transformation"""
    parsing_time: float = 0.0
    transformation_time: float = 0.0
    total_time: float = 0.0
    nodes_processed: int = 0
    cache_hits: int = 0
    cache_misses: int = 0
    memory_usage: float = 0.0

class TransformerPool:
    """Pool d'instances de transformateurs pour réutilisation"""
    
    def __init__(self, max_size: int = 50):
        self.pool: Dict[Type, List[cst.CSTTransformer]] = {}
        self.max_size = max_size
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def get_transformer(self, transformer_class: Type, **kwargs) -> cst.CSTTransformer:
        """Récupère une instance du transformateur depuis le pool"""
        if transformer_class not in self.pool:
            self.pool[transformer_class] = []
        
        if self.pool[transformer_class]:
            transformer = self.pool[transformer_class].pop()
            # Réinitialisation des attributs si nécessaire
            if hasattr(transformer, 'reset'):
                transformer.reset()
            return transformer
        
        return transformer_class(**kwargs)
    
    def return_transformer(self, transformer: cst.CSTTransformer):
        """Retourne un transformateur au pool"""
        transformer_class = type(transformer)
        if transformer_class not in self.pool:
            self.pool[transformer_class] = []
        
        if len(self.pool[transformer_class]) < self.max_size:
            self.pool[transformer_class].append(transformer)
            self.logger.debug(f"♻️ Transformateur {transformer_class.__name__} retourné au pool")

class OptimizedTransformationPipeline:
    """Pipeline de transformation LibCST optimisé"""
    
    def __init__(self, cache_manager: Optional[IntelligentCacheManager] = None):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.cache = cache_manager or IntelligentCacheManager()
        self.transformer_pool = TransformerPool()
        self.metrics: Dict[str, TransformationMetrics] = {}
        self._executor = ThreadPoolExecutor(max_workers=4)
    
    async def transform(self, code: str, transformers: List[Tuple[Type, Dict[str, Any]]],
                       transformation_id: str) -> Tuple[str, TransformationMetrics]:
        """
        Applique une série de transformations au code avec optimisations.
        
        Args:
            code: Code source à transformer
            transformers: Liste de tuples (transformer_class, kwargs)
            transformation_id: Identifiant unique pour le cache
            
        Returns:
            Tuple (code transformé, métriques)
        """
        start_time = time.time()
        metrics = TransformationMetrics()
        
        # Vérification du cache
        cached_result = await self.cache.get_cached_transformation(code, transformation_id)
        if cached_result:
            metrics.cache_hits += 1
            self.logger.debug(f"⚡ Transformation {transformation_id} récupérée du cache")
            return cached_result["transformed_code"], metrics
        
        metrics.cache_misses += 1
        
        try:
            # Parsing AST avec cache
            parse_start = time.time()
            tree = await self._parse_with_cache(code)
            metrics.parsing_time = time.time() - parse_start
            
            # Application des transformations
            transform_start = time.time()
            for transformer_class, kwargs in transformers:
                # Récupération du transformateur depuis le pool
                transformer = self.transformer_pool.get_transformer(transformer_class, **kwargs)
                
                try:
                    # Transformation
                    tree = tree.visit(transformer)
                    
                    # Métriques
                    if hasattr(transformer, 'nodes_processed'):
                        metrics.nodes_processed += transformer.nodes_processed
                    
                finally:
                    # Retour du transformateur au pool
                    self.transformer_pool.return_transformer(transformer)
            
            metrics.transformation_time = time.time() - transform_start
            
            # Génération du code transformé
            transformed_code = tree.code
            
            # Mise en cache du résultat
            await self.cache.cache_transformation(code, transformation_id, {
                "transformed_code": transformed_code,
                "metrics": metrics.__dict__
            })
            
            metrics.total_time = time.time() - start_time
            self.metrics[transformation_id] = metrics
            
            return transformed_code, metrics
            
        except Exception as e:
            self.logger.error(f"❌ Erreur de transformation: {e}")
            raise
    
    @lru_cache(maxsize=100)
    async def _parse_with_cache(self, code: str) -> cst.Module:
        """Parse le code avec cache intelligent"""
        cached_ast = await self.cache.get_cached_ast(code)
        if cached_ast:
            return cst.Module([])  # TODO: Implémenter la désérialisation AST
        
        tree = cst.parse_module(code)
        await self.cache.cache_ast(code, {})  # TODO: Implémenter la sérialisation AST
        return tree
    
    def get_metrics(self, transformation_id: str) -> Optional[TransformationMetrics]:
        """Récupère les métriques d'une transformation"""
        return self.metrics.get(transformation_id)
    
    def get_all_metrics(self) -> Dict[str, TransformationMetrics]:
        """Récupère toutes les métriques"""
        return self.metrics.copy()
    
    async def clear_metrics(self):
        """Nettoie les métriques"""
        self.metrics.clear()
        
    async def shutdown(self):
        """Arrête proprement le pipeline"""
        self._executor.shutdown(wait=True)
        await self.cache.invalidate_cache("")  # Invalide tout le cache 