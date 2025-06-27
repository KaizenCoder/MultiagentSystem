#!/usr/bin/env python3
"""
AGENT 3 - ADAPTATEUR DE CODE (LibCST)
🛠️ ADAPTATEUR DE CODE - Agent 03
=================================

# Fallback pour pyflakes
try:
    import pyflakes
except ImportError:
    class pyflakes:
        class api:
            @staticmethod
            def check(code, filename):
                return []


🎯 Mission : Corriger et adapter le code source sur la base d'un feedback.
⚡ Capacités : Manipulation de l'AST avec LibCST pour des refactorings sécurisés.
🏢 Équipe : NextGeneration Tools Migration

Author: Équipe de Maintenance NextGeneration
Version: 4.3.0 - Priorités Moyennes : Patterns d'Indentation Complexes + ChromaDB + PostgreSQL Analytics
"""
import sys
from pathlib import Path
import logging
import asyncio
import re
import ast
import inspect
import time
import hashlib
from datetime import datetime
from typing import List, Dict, Any, Tuple, Optional, Set
import textwrap
from dataclasses import dataclass, field
from enum import Enum

# --- Pyflakes Import ---
from pyflakes.api import check
from pyflakes.reporter import Reporter
import io

# --- Imports conditionnels pour les bases de données (v4.3.0 - Priorités Moyennes) ---
try:
    import chromadb
    from chromadb.config import Settings
    CHROMADB_AVAILABLE = True
except ImportError:
    CHROMADB_AVAILABLE = False
    chromadb = None

try:
    from sqlalchemy import create_engine, Column, Integer, String, Float, JSON, DateTime
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import sessionmaker
    SQLALCHEMY_AVAILABLE = True
    Base = declarative_base()
except ImportError:
    SQLALCHEMY_AVAILABLE = False
    Base = None

# --- Configuration Robuste du Chemin d'Importation ---
try:
    project_root = Path(__file__).resolve().parents[2]
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
except (IndexError, NameError):
    if '.' not in sys.path:
        sys.path.insert(0, '.')

from core.agent_factory_architecture import Agent, Task, Result
import libcst as cst

# --- Classes d'amélioration v4.2.0 (Priorités Hautes) ---

class ErrorType(Enum):
    """Types d'erreurs étendus pour classification avancée"""
    INDENTATION = "indentation"
    NAME = "name"
    IMPORT = "import"
    SYNTAX = "syntax"
    TYPE_ERROR = "type_error"
    ATTRIBUTE_ERROR = "attribute_error"
    VALUE_ERROR = "value_error"
    MODULE_NOT_FOUND = "module_not_found"
    GENERIC = "generic"

@dataclass
class ErrorClassification:
    """Classification d'erreur avec score de confiance"""
    error_type: ErrorType
    confidence_score: float  # 0.0 à 1.0
    error_message: str
    line_number: Optional[int] = None
    suggested_fixes: List[str] = None

@dataclass
class ImportDiscovery:
    """Résultat de découverte automatique d'imports"""
    module_name: str
    import_statement: str
    confidence: float
    source_files: List[str]  # Fichiers où cet import est utilisé
    usage_count: int

@dataclass
class ValidationResult:
    """Résultat de validation multi-niveaux"""
    syntax_valid: bool
    semantic_valid: bool
    compilation_successful: bool
    import_resolution: bool
    confidence_score: float
    issues: List[str]
    warnings: List[str]

# --- Nouvelles classes v4.3.0 (Priorités Moyennes) ---

@dataclass
class IndentationPattern:
    """Pattern d'indentation pour ChromaDB"""
    pattern_id: str
    code_before: str
    code_after: str
    success_rate: float
    pattern_type: str  # "expected_block", "unexpected_indent", "unindent_mismatch", etc.
    indentation_style: str  # "spaces", "tabs", "mixed"
    indentation_level: int
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

@dataclass
class CorrectionHistory:
    """Historique de correction pour ChromaDB"""
    correction_id: str
    original_code: str
    corrected_code: str
    error_type: str
    confidence_score: float
    validation_result: Dict[str, Any]
    patterns_used: List[str]
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

@dataclass
class AnalyticsMetrics:
    """Métriques d'analytique pour PostgreSQL"""
    metric_id: str
    error_type: str
    confidence_score: float
    success: bool
    processing_time: float
    pattern_type: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

# --- Classes de Reporter pour Pyflakes ---

class PyflakesErrorCollector(Reporter):
    def __init__(self):
        self.errors = []
        super().__init__(io.StringIO(), io.StringIO())

    def syntaxError(self, filename, msg, lineno, offset, text):
        self.errors.append({'type': 'SyntaxError', 'message': msg, 'lineno': lineno, 'offset': offset, 'text': text})

    def unexpectedError(self, filename, msg):
        self.errors.append({'type': 'UnexpectedError', 'message': msg})

    def flake(self, message):
        self.errors.append({'type': 'Flake', 'message': str(message)})

# --- Modèles de base de données PostgreSQL (v4.3.0) ---

if SQLALCHEMY_AVAILABLE and Base is not None:
    class CorrectionMetrics(Base):
        """Métriques de correction pour PostgreSQL"""
        __tablename__ = 'correction_metrics'
        
        id = Column(Integer, primary_key=True)
        error_type = Column(String)
        confidence_score = Column(Float)
        validation_result = Column(JSON)
        processing_time = Column(Float)
        success = Column(String)  # 'true'/'false' pour compatibilité
        created_at = Column(DateTime, default=datetime.now)
        
    class IndentationAnalytics(Base):
        """Analytics des patterns d'indentation"""
        __tablename__ = 'indentation_analytics'
        
        id = Column(Integer, primary_key=True)
        pattern_type = Column(String)
        success_count = Column(Integer, default=0)
        failure_count = Column(Integer, default=0)
        avg_confidence = Column(Float, default=0.0)
        pattern_metadata = Column(JSON)
        last_updated = Column(DateTime, default=datetime.now)
else:
    # Classes factices si SQLAlchemy n'est pas disponible
    class CorrectionMetrics:
        pass
    class IndentationAnalytics:
        pass


# --- Fonctions et Classes de Transformation CST ---

class CstPassInserter(cst.CSTTransformer):
    """
    Un CSTTransformer qui insère 'pass' dans les blocs de code vides.
    C'est une approche plus robuste que le traitement de texte.
    """
    def leave_IndentedBlock(self, original_node: cst.IndentedBlock, updated_node: cst.IndentedBlock) -> cst.IndentedBlock:
        if not updated_node.body:
            return updated_node.with_changes(body=[cst.SimpleStatementLine(body=[cst.Pass()])])
        return updated_node

    def leave_Try(self, original_node: cst.Try, updated_node: cst.Try) -> cst.Try:
        if not updated_node.body.body:
            new_body = updated_node.body.with_changes(body=[cst.SimpleStatementLine(body=[cst.Pass()])])
            updated_node = updated_node.with_changes(body=new_body)
        
        if not updated_node.handlers:
            new_handler = cst.ExceptHandler(
                body=cst.IndentedBlock(body=[cst.SimpleStatementLine(body=[cst.Pass()])]),
                type=cst.Name("Exception")
            )
            return updated_node.with_changes(handlers=[new_handler])
        return updated_node

class CstImportAdder(cst.CSTTransformer):
    """
    Un CSTTransformer qui ajoute des imports simples (`import module`)
    en évitant les doublons.
    """
    def __init__(self, modules_to_add: List[str]):
        self.modules_to_add = modules_to_add

    def leave_Module(self, original_node: cst.Module, updated_node: cst.Module) -> cst.Module:
        existing_imports = set()
        for stmt in updated_node.body:
            if isinstance(stmt, cst.SimpleStatementLine) and isinstance(stmt.body[0], cst.Import):
                for alias in stmt.body[0].names:
                    existing_imports.add(alias.name.value)
        
        new_imports = []
        for module in self.modules_to_add:
            if module not in existing_imports:
                new_imports.append(
                    cst.SimpleStatementLine(
                        body=[cst.Import(names=[cst.ImportAlias(name=cst.Name(module))])]
                    )
                )

        if not new_imports:
            return updated_node
            
        insert_idx = 0
        if len(updated_node.body) > 0:
            first_stmt = updated_node.body[0]
            if isinstance(first_stmt, cst.SimpleStatementLine) and \
               isinstance(first_stmt.body[0], cst.Expr) and \
               isinstance(first_stmt.body[0].value, cst.SimpleString):
                insert_idx = 1
                
        body_list = list(updated_node.body)
        body_list[insert_idx:insert_idx] = new_imports
        return updated_node.with_changes(body=tuple(body_list))

def _build_module_path(path: str) -> cst.BaseExpression:
    """
    Construit une arborescence CST pour un chemin de module avec des points (ex: 'a.b.c').
    Ceci est la CORRECTION CLÉ pour le bug de `libcst`.
    """
    parts = path.split('.')
    if not all(part.isidentifier() for part in parts):
        raise ValueError(f"Chemin de module invalide: {path}")

    node = cst.Name(value=parts[0])
    for part in parts[1:]:
        node = cst.Attribute(value=node, attr=cst.Name(value=part))
    return node

class CstComplexImportAdder(cst.CSTTransformer):
    """
    Un CSTTransformer qui ajoute des imports 'from ... import ...'
    en évitant les doublons et en gérant les chemins de modules complexes.
    """
    def __init__(self, from_module: str, names_to_import: List[str]):
        self.from_module = from_module
        self.names_to_import = names_to_import

    def leave_Module(self, original_node: cst.Module, updated_node: cst.Module) -> cst.Module:
        existing_imports = set()
        for stmt in updated_node.body:
            if isinstance(stmt, cst.SimpleStatementLine) and isinstance(stmt.body[0], cst.ImportFrom):
                module_node = stmt.body[0].module
                module_str = ""
                try:
                    module_str = updated_node.code_for_node(module_node)
                except Exception:
                    pass

                if module_str == self.from_module:
                    if isinstance(stmt.body[0].names, cst.ImportStar):
                        return updated_node
                    for alias in stmt.body[0].names:
                        existing_imports.add(alias.name.value)
        
        new_names_to_import = [name for name in self.names_to_import if name not in existing_imports]

        if not new_names_to_import:
            return updated_node

        # *** LA CORRECTION EST ICI ***
        # Utilisation de la fonction helper pour construire le chemin du module.
        new_import_statement = cst.SimpleStatementLine(
            body=[cst.ImportFrom(
                module=_build_module_path(self.from_module), # <-- C'ÉTAIT L'ERREUR
                names=[cst.ImportAlias(name=cst.Name(name)) for name in new_names_to_import]
            )]
        )

        insert_idx = 0
        if len(updated_node.body) > 0:
            first_stmt = updated_node.body[0]
            if isinstance(first_stmt, cst.SimpleStatementLine) and \
               isinstance(first_stmt.body[0], cst.Expr) and \
               isinstance(first_stmt.body[0].value, cst.SimpleString):
                insert_idx = 1
                
        body_list = list(updated_node.body)
        body_list.insert(insert_idx, new_import_statement)
        return updated_node.with_changes(body=tuple(body_list))

# --- Services d'intégration de base de données (v4.3.0 - Priorités Moyennes) ---

class ChromaDBIndentationStore:
    """Service de stockage des patterns d'indentation dans ChromaDB"""
    
    def __init__(self, collection_name: str = "indentation_patterns"):
        self.collection_name = collection_name
        self.client = None
        self.collection = None
        self.enabled = CHROMADB_AVAILABLE
        
        if self.enabled:
            try:
                self.client = chromadb.Client()
                self.collection = self.client.get_or_create_collection(
                    name=collection_name,
                    metadata={"hnsw:space": "cosine"}
                )
            except Exception as e:
                logging.warning(f"ChromaDB indisponible: {e}")
                self.enabled = False
    
    def _generate_embeddings(self, code: str) -> List[float]:
        """Génère des embeddings simples pour le code (version simplifiée)"""
        if not self.enabled:
            return []
        
        # Version simplifiée : hash du code pour les embeddings
        # En production, utiliser un modèle d'embedding approprié
        code_hash = hashlib.md5(code.encode()).hexdigest()
        # Convertir en vecteur numérique simple
        return [float(ord(c)) / 255.0 for c in code_hash[:384]]  # Vecteur de 384 dimensions
    
    def store_pattern(self, pattern: IndentationPattern) -> bool:
        """Stocke un pattern d'indentation réussi"""
        if not self.enabled:
            return False
            
        try:
            embeddings = self._generate_embeddings(pattern.code_before)
            self.collection.add(
                ids=[pattern.pattern_id],
                embeddings=[embeddings],
                metadatas=[{
                    "code_after": pattern.code_after,
                    "success_rate": pattern.success_rate,
                    "pattern_type": pattern.pattern_type,
                    "indentation_style": pattern.indentation_style,
                    "indentation_level": pattern.indentation_level,
                    "created_at": pattern.created_at,
                    **pattern.metadata
                }]
            )
            return True
        except Exception as e:
            logging.error(f"Erreur stockage pattern ChromaDB: {e}")
            return False
    
    def find_similar_patterns(self, code: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Trouve des patterns similaires pour suggestion"""
        if not self.enabled:
            return []
            
        try:
            embeddings = self._generate_embeddings(code)
            results = self.collection.query(
                query_embeddings=[embeddings],
                n_results=limit
            )
            
            patterns = []
            if results['metadatas']:
                for metadata in results['metadatas'][0]:
                    patterns.append(metadata)
            
            return patterns
        except Exception as e:
            logging.error(f"Erreur recherche patterns ChromaDB: {e}")
            return []

class ChromaDBCorrectionHistory:
    """Service d'historique des corrections dans ChromaDB"""
    
    def __init__(self, collection_name: str = "correction_history"):
        self.collection_name = collection_name
        self.client = None
        self.collection = None
        self.enabled = CHROMADB_AVAILABLE
        
        if self.enabled:
            try:
                self.client = chromadb.Client()
                self.collection = self.client.get_or_create_collection(
                    name=collection_name,
                    metadata={"hnsw:space": "cosine"}
                )
            except Exception as e:
                logging.warning(f"ChromaDB correction history indisponible: {e}")
                self.enabled = False
    
    def _generate_embeddings(self, code: str) -> List[float]:
        """Génère des embeddings pour le code original"""
        if not self.enabled:
            return []
        
        code_hash = hashlib.md5(code.encode()).hexdigest()
        return [float(ord(c)) / 255.0 for c in code_hash[:384]]
    
    def log_correction(self, history: CorrectionHistory) -> bool:
        """Enregistre une correction dans ChromaDB"""
        if not self.enabled:
            return False
            
        try:
            embeddings = self._generate_embeddings(history.original_code)
            
            self.collection.add(
                ids=[history.correction_id],
                embeddings=[embeddings],
                metadatas=[{
                    "corrected_code": history.corrected_code,
                    "error_type": history.error_type,
                    "confidence_score": history.confidence_score,
                    "validation_result": history.validation_result,
                    "patterns_used": str(history.patterns_used),  # Conversion en string
                    "timestamp": history.timestamp
                }]
            )
            return True
        except Exception as e:
            logging.error(f"Erreur log correction ChromaDB: {e}")
            return False

class PostgreSQLAnalyticsService:
    """Service d'analytics et métriques PostgreSQL"""
    
    def __init__(self, db_url: str = None):
        self.enabled = SQLALCHEMY_AVAILABLE
        self.engine = None
        self.Session = None
        
        if self.enabled and db_url:
            try:
                self.engine = create_engine(db_url, echo=False)
                Base.metadata.create_all(self.engine)
                self.Session = sessionmaker(bind=self.engine)
            except Exception as e:
                logging.warning(f"PostgreSQL indisponible: {e}")
                self.enabled = False
        else:
            self.enabled = False
    
    def log_correction_metrics(self, metrics: AnalyticsMetrics) -> bool:
        """Enregistre les métriques de correction"""
        if not self.enabled:
            return False
            
        session = self.Session()
        try:
            db_metrics = CorrectionMetrics(
                error_type=metrics.error_type,
                confidence_score=metrics.confidence_score,
                validation_result=metrics.metadata,
                processing_time=metrics.processing_time,
                success=str(metrics.success).lower(),
                created_at=datetime.fromisoformat(metrics.created_at)
            )
            session.add(db_metrics)
            session.commit()
            return True
        except Exception as e:
            logging.error(f"Erreur log métriques PostgreSQL: {e}")
            session.rollback()
            return False
        finally:
            session.close()
    
    def update_pattern_analytics(self, pattern_type: str, success: bool, confidence: float) -> bool:
        """Met à jour les analytics des patterns"""
        if not self.enabled:
            return False
            
        session = self.Session()
        try:
            analytics = session.query(IndentationAnalytics)\
                             .filter_by(pattern_type=pattern_type)\
                             .first()
            
            if not analytics:
                analytics = IndentationAnalytics(
                    pattern_type=pattern_type,
                    success_count=0,
                    failure_count=0,
                    avg_confidence=0.0,
                    pattern_metadata={},
                    last_updated=datetime.now()
                )
                session.add(analytics)
            
            if success:
                analytics.success_count += 1
            else:
                analytics.failure_count += 1
                
            total_count = analytics.success_count + analytics.failure_count
            analytics.avg_confidence = ((analytics.avg_confidence * (total_count - 1)) + confidence) / total_count
            analytics.last_updated = datetime.now()
            
            session.commit()
            return True
        except Exception as e:
            logging.error(f"Erreur update analytics PostgreSQL: {e}")
            session.rollback()
            return False
        finally:
            session.close()
    
    def get_pattern_stats(self, pattern_type: str = None) -> Dict[str, Any]:
        """Récupère les statistiques des patterns"""
        if not self.enabled:
            return {}
            
        session = self.Session()
        try:
            query = session.query(IndentationAnalytics)
            if pattern_type:
                query = query.filter_by(pattern_type=pattern_type)
            
            stats = {}
            for analytics in query.all():
                stats[analytics.pattern_type] = {
                    "success_count": analytics.success_count,
                    "failure_count": analytics.failure_count,
                    "avg_confidence": analytics.avg_confidence,
                    "success_rate": analytics.success_count / (analytics.success_count + analytics.failure_count) if (analytics.success_count + analytics.failure_count) > 0 else 0
                }
            
            return stats
        except Exception as e:
            logging.error(f"Erreur récupération stats PostgreSQL: {e}")
            return {}
        finally:
            session.close()

class AgentMAINTENANCE03AdaptateurCode(Agent):
    """
    🔧 Agent MAINTENANCE 03 - Adaptateur de Code NextGeneration
    
    Agent spécialisé dans l'adaptation et la réparation de code Python via LibCST,
    manipulation sécurisée de l'AST et stratégies de réparation multi-niveaux.
    
    Capacités principales :
    - Réparation d'erreurs d'indentation avec stratégies ciblées
    - Manipulation sécurisée AST via LibCST (blocs vides, imports)
    - Correction automatique NameError avec mapping intelligent
    - Insertion robuste 'pass' dans blocs vides (try/except, functions)
    - Gestion imports complexes avec évitement doublons
    - Classification erreurs pour stratégies adaptées
    
    Technologies avancées :
    - LibCST : Transformations AST préservant formatage
    - Pyflakes : Détection erreurs statiques
    - CSTTransformer : Classes personnalisées insertion/adaptation
    - Multi-level repair : Stratégies en cascade selon type erreur
    
    Workflow type :
    1. Classification erreur (indentation/import/name/generic)
    2. Application stratégie ciblée
    3. Transformation LibCST sécurisée
    4. Validation et traçabilité adaptations
    
    Conformité : Pattern Factory NextGeneration v3.1.0
    """
    def __init__(self, **kwargs):
        super().__init__(agent_type="adaptateur", **kwargs)
        # ✅ MIGRATION SYSTÈME LOGGING UNIFIÉ
        try:
            from core.manager import LoggingManager
            logging_manager = LoggingManager()
            self.logger = logging_manager.get_logger(
                config_name="maintenance",
                custom_config={
                    "logger_name": f"nextgen.maintenance.adaptateur_code.{self.id}",
                    "log_dir": "logs/maintenance/adaptateur",
                    "metadata": {
                        "agent_type": "MAINTENANCE_03_adaptateur_code",
                        "agent_role": "adaptateur_code",
                        "system": "nextgeneration"
                    }
                }
            )
        except ImportError:
            # Fallback en cas d'indisponibilité du LoggingManager
            self.logger = logging.getLogger(self.__class__.__name__)
        self.agent_id = self.id
        self.logger.info(f"Adaptateur de code CST ({self.agent_id}) initialisé.")
        
        self.COMPLEX_IMPORT_MAP = {
            "Path": ("pathlib", "Path"),
            "datetime": ("datetime", "datetime"),
            "Optional": ("typing", "Optional"),
            "List": ("typing", "List"),
            "Dict": ("typing", "Dict"),
            "Any": ("typing", "Any"),
            "Agent": ("core.agent_factory_architecture", "Agent"),
            "Task": ("core.agent_factory_architecture", "Task"),
            "Result": ("core.agent_factory_architecture", "Result"),
        }
        
        # Cache pour découverte automatique d'imports
        self._import_discovery_cache: Dict[str, ImportDiscovery] = {}
        self._project_imports_cache: Optional[Dict[str, Set[str]]] = None
        
        # Historique des corrections pour apprentissage
        self._correction_history: List[Dict[str, Any]] = []
        
        # Services d'intégration de base de données v4.3.0 (Priorités Moyennes)
        self.chroma_patterns = ChromaDBIndentationStore()
        self.chroma_history = ChromaDBCorrectionHistory()
        
        # PostgreSQL Analytics (optionnel, nécessite configuration)
        db_url = kwargs.get('postgres_db_url')
        self.pg_analytics = PostgreSQLAnalyticsService(db_url=db_url)
        
        # Configuration avancée pour patterns complexes
        self._pattern_confidence_threshold = kwargs.get('pattern_confidence_threshold', 0.8)
        self._enable_pattern_learning = kwargs.get('enable_pattern_learning', True)
        self._max_similar_patterns = kwargs.get('max_similar_patterns', 5)

    def get_capabilities(self) -> List[str]:
        """Retourne les capacités spécialisées de l'Adaptateur de Code v4.3.0."""
        return [
            "code_adaptation",
            "import_fixing",
            "indentation_error_fix",
            "libcst_ast_transformation",
            "pyflakes_static_analysis",
            "multi_level_repair_strategy",
            "complex_import_management",
            "empty_block_correction",
            "name_error_resolution",
            "formatting_preservation",
            # Nouvelles capacités v4.2.0 (Priorités Hautes)
            "extended_error_classification",
            "auto_import_discovery",
            "multi_level_validation",
            "confidence_scoring",
            "type_error_resolution",
            "attribute_error_fix",
            "value_error_correction",
            "module_resolution_advanced",
            # Nouvelles capacités v4.3.0 (Priorités Moyennes)
            "complex_indentation_patterns",
            "chromadb_pattern_storage",
            "pattern_similarity_search",
            "postgresql_analytics",
            "advanced_confidence_scoring",
            "pattern_learning_system",
            "correction_history_tracking",
            "adaptive_pattern_matching"
        ]
    
    def classify_error_extended(self, error: Exception, code_context: str = "") -> ErrorClassification:
        """
        Classification d'erreur étendue avec score de confiance v4.2.0
        
        Args:
            error: Exception capturée
            code_context: Contexte du code pour analyse
            
        Returns:
            ErrorClassification: Classification avec score de confiance
        """
        error_str = str(error).lower()
        error_type_str = type(error).__name__.lower()
        
        # Classification basée sur le type d'exception
        if isinstance(error, (IndentationError, TabError)):
            return ErrorClassification(
                error_type=ErrorType.INDENTATION,
                confidence_score=0.95,
                error_message=str(error),
                line_number=getattr(error, 'lineno', None),
                suggested_fixes=["Fix indentation", "Normalize tabs/spaces"]
            )
        
        elif isinstance(error, NameError):
            confidence = 0.9
            fixes = ["Add import statement", "Check variable definition"]
            
            # Analyse plus fine pour NameError
            if "is not defined" in error_str:
                # Extraction du nom de variable
                match = re.search(r"name '(\w+)' is not defined", str(error))
                if match:
                    undefined_name = match.group(1)
                    fixes.append(f"Import or define '{undefined_name}'")
                    
                    # Check si c'est un import potentiel
                    if undefined_name[0].isupper() or undefined_name in self.COMPLEX_IMPORT_MAP:
                        confidence = 0.95
                        fixes.insert(0, f"Add import for '{undefined_name}'")
            
            return ErrorClassification(
                error_type=ErrorType.NAME,
                confidence_score=confidence,
                error_message=str(error),
                suggested_fixes=fixes
            )
        
        elif isinstance(error, (ImportError, ModuleNotFoundError)):
            error_type = ErrorType.MODULE_NOT_FOUND if "No module named" in error_str else ErrorType.IMPORT
            return ErrorClassification(
                error_type=error_type,
                confidence_score=0.9,
                error_message=str(error),
                suggested_fixes=["Check module installation", "Verify import path", "Add to requirements"]
            )
        
        elif isinstance(error, TypeError):
            return ErrorClassification(
                error_type=ErrorType.TYPE_ERROR,
                confidence_score=0.85,
                error_message=str(error),
                suggested_fixes=["Check argument types", "Verify function signature", "Add type annotations"]
            )
        
        elif isinstance(error, AttributeError):
            confidence = 0.8
            fixes = ["Check object type", "Verify attribute exists"]
            
            # Analyse spécifique AttributeError
            if "has no attribute" in error_str:
                match = re.search(r"'(\w+)' object has no attribute '(\w+)'", str(error))
                if match:
                    obj_type, attr_name = match.groups()
                    fixes.append(f"Check if '{obj_type}' should have '{attr_name}' attribute")
                    confidence = 0.9
            
            return ErrorClassification(
                error_type=ErrorType.ATTRIBUTE_ERROR,
                confidence_score=confidence,
                error_message=str(error),
                suggested_fixes=fixes
            )
        
        elif isinstance(error, ValueError):
            return ErrorClassification(
                error_type=ErrorType.VALUE_ERROR,
                confidence_score=0.75,
                error_message=str(error),
                suggested_fixes=["Validate input values", "Check value ranges", "Handle edge cases"]
            )
        
        elif isinstance(error, SyntaxError):
            confidence = 0.9
            fixes = ["Fix syntax error", "Check parentheses/brackets"]
            
            # Analyse spécifique SyntaxError
            if hasattr(error, 'text') and error.text:
                if ":" in error.text and "expected" in error_str:
                    fixes.append("Add missing colon or fix statement structure")
                elif "(" in error.text and ")" not in error.text:
                    fixes.append("Check missing closing parenthesis")
                    confidence = 0.95
            
            return ErrorClassification(
                error_type=ErrorType.SYNTAX,
                confidence_score=confidence,
                error_message=str(error),
                line_number=getattr(error, 'lineno', None),
                suggested_fixes=fixes
            )
        
        # Classification générique
        return ErrorClassification(
            error_type=ErrorType.GENERIC,
            confidence_score=0.5,
            error_message=str(error),
            suggested_fixes=["Manual inspection required", "Check documentation"]
        )
    
    def discover_project_imports(self, project_root: Optional[Path] = None) -> Dict[str, ImportDiscovery]:
        """
        Auto-découverte des imports dans le projet v4.2.0
        
        Args:
            project_root: Racine du projet (auto-détection si None)
            
        Returns:
            Dict[str, ImportDiscovery]: Mapping nom -> découverte d'import
        """
        if project_root is None:
            project_root = Path(__file__).resolve().parents[2]  # Remonte vers le projet
        
        self.logger.info(f"Découverte automatique d'imports dans: {project_root}")
        
        import_usage = {}
        
        # Parcours récursif des fichiers Python
        for py_file in project_root.rglob("*.py"):
            if any(part.startswith('.') for part in py_file.parts):
                continue  # Skip hidden directories
            
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Parse AST pour extraire les imports
                try:
                    tree = ast.parse(content)
                    for node in ast.walk(tree):
                        if isinstance(node, ast.Import):
                            for alias in node.names:
                                module_name = alias.name
                                if module_name not in import_usage:
                                    import_usage[module_name] = {
                                        'files': set(),
                                        'statements': set(),
                                        'count': 0
                                    }
                                import_usage[module_name]['files'].add(str(py_file))
                                import_usage[module_name]['statements'].add(f"import {module_name}")
                                import_usage[module_name]['count'] += 1
                        
                        elif isinstance(node, ast.ImportFrom):
                            if node.module:
                                for alias in node.names:
                                    name = alias.name
                                    module = node.module
                                    
                                    if name not in import_usage:
                                        import_usage[name] = {
                                            'files': set(),
                                            'statements': set(),
                                            'count': 0
                                        }
                                    import_usage[name]['files'].add(str(py_file))
                                    import_usage[name]['statements'].add(f"from {module} import {name}")
                                    import_usage[name]['count'] += 1
                
                except SyntaxError:
                    continue  # Skip files with syntax errors
                    
            except Exception as e:
                self.logger.warning(f"Erreur lecture fichier {py_file}: {e}")
                continue
        
        # Conversion en ImportDiscovery avec scoring
        discoveries = {}
        total_files = len(list(project_root.rglob("*.py")))
        
        for name, usage in import_usage.items():
            if usage['count'] >= 2:  # Utilisé au moins 2 fois
                # Score basé sur fréquence d'usage et nombre de fichiers
                file_ratio = len(usage['files']) / max(total_files, 1)
                frequency_score = min(usage['count'] / 10, 1.0)
                confidence = (file_ratio + frequency_score) / 2
                
                # Sélection de la meilleure instruction d'import
                statements = list(usage['statements'])
                best_statement = min(statements, key=len)  # Plus court = plus simple
                
                discoveries[name] = ImportDiscovery(
                    module_name=name,
                    import_statement=best_statement,
                    confidence=confidence,
                    source_files=list(usage['files']),
                    usage_count=usage['count']
                )
        
        # Mise en cache
        self._import_discovery_cache.update(discoveries)
        self.logger.info(f"Découvert {len(discoveries)} imports dans le projet")
        
        return discoveries
    
    def validate_multi_level(self, code: str, file_path: Optional[Path] = None) -> ValidationResult:
        """
        Validation multi-niveaux v4.2.0
        
        Args:
            code: Code source à valider
            file_path: Chemin du fichier (optionnel)
            
        Returns:
            ValidationResult: Résultat de validation complète
        """
        issues = []
        warnings = []
        
        # Niveau 1: Validation syntaxique
        syntax_valid = True
        try:
            ast.parse(code)
        except SyntaxError as e:
            syntax_valid = False
            issues.append(f"Syntax error: {e}")
        
        # Niveau 2: Validation sémantique (AST)
        semantic_valid = True
        try:
            tree = ast.parse(code)
            # Vérifications sémantiques basiques
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    if not node.name.islower():
                        warnings.append(f"Function '{node.name}' should be lowercase (PEP 8)")
                elif isinstance(node, ast.ClassDef):
                    if not node.name[0].isupper():
                        warnings.append(f"Class '{node.name}' should start with uppercase")
        except:
            semantic_valid = False
            issues.append("Semantic validation failed")
        
        # Niveau 3: Test de compilation
        compilation_successful = True
        try:
            compile(code, file_path or '<string>', 'exec')
        except Exception as e:
            compilation_successful = False
            issues.append(f"Compilation failed: {e}")
        
        # Niveau 4: Résolution des imports
        import_resolution = True
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.ImportFrom) and node.module:
                    # Test basique de résolution d'import
                    try:
                        __import__(node.module)
                    except ImportError:
                        import_resolution = False
                        warnings.append(f"Cannot resolve import: {node.module}")
        except:
            import_resolution = False
        
        # Calcul du score de confiance global
        scores = [
            1.0 if syntax_valid else 0.0,
            1.0 if semantic_valid else 0.5,
            1.0 if compilation_successful else 0.0,
            1.0 if import_resolution else 0.7
        ]
        confidence_score = sum(scores) / len(scores)
        
        return ValidationResult(
            syntax_valid=syntax_valid,
            semantic_valid=semantic_valid,
            compilation_successful=compilation_successful,
            import_resolution=import_resolution,
            confidence_score=confidence_score,
            issues=issues,
            warnings=warnings
        )
        
    def _fix_indentation_errors(self, code: str, error: Exception) -> Tuple[str, List[str]]:
        """
        Moteur de correction d'indentation amélioré - Version complète robuste.
        
        Gère tous les types d'erreurs d'indentation avec stratégies adaptées :
        - "expected an indented block" : insertion intelligente de 'pass'
        - "unexpected indent" : normalisation contextuelle
        - "unindent does not match" : réparation globale cohérente
        - Détection automatique des niveaux d'indentation
        - Préservation du style d'indentation existant (espaces vs tabs)
        
        Args:
            code: Code source à corriger
            error: Exception d'indentation capturée
            
        Returns:
            Tuple[str, List[str]]: (code_corrigé, liste_des_adaptations)
        """
        notes = []
        if not isinstance(error, (SyntaxError, IndentationError)):
            return code, notes

        lines = code.splitlines()
        msg = error.msg.lower() if error.msg else ""
        lineno = error.lineno or 0
        
        # Détection automatique du style d'indentation (espaces vs tabs)
        indent_char = " "
        indent_size = 4
        for line in lines:
            if line.startswith((" ", "\t")):
                if line.startswith("\t"):
                    indent_char = "\t"
                    indent_size = 1
                else:
                    # Compte les espaces du premier niveau d'indentation trouvé
                    stripped = line.lstrip()
                    if stripped:
                        indent_size = len(line) - len(stripped)
                        break

        # Cas 1: "expected an indented block" -> insertion intelligente de 'pass'
        if "expected an indented block" in msg and 0 < lineno <= len(lines):
            target_indent = ""
            
            # Analyse intelligente du contexte pour déterminer l'indentation requise
            if lineno > 1:
                prev_line = lines[lineno - 2].rstrip()
                
                # Si la ligne précédente finit par ':', c'est un bloc de contrôle
                if prev_line.endswith(':'):
                    prev_indent = len(lines[lineno - 2]) - len(lines[lineno - 2].lstrip())
                    target_indent = indent_char * (prev_indent + indent_size)
                else:
                    # Cherche le niveau d'indentation approprié en remontant
                    for i in range(lineno - 2, -1, -1):
                        if lines[i].strip() and lines[i].endswith(':'):
                            base_indent = len(lines[i]) - len(lines[i].lstrip())
                            target_indent = indent_char * (base_indent + indent_size)
                            break
                    else:
                        # Fallback : indentation par défaut
                        target_indent = indent_char * indent_size
            else:
                target_indent = indent_char * indent_size
            
            lines.insert(lineno - 1, f"{target_indent}pass")
            notes.append(f"Auto-correction: Ajout de 'pass' avec indentation adaptée à la ligne {lineno} pour bloc attendu.")
        
        # Cas 2: "unexpected indent" -> correction contextuelle intelligente
        elif "unexpected indent" in msg and 0 < lineno <= len(lines):
            problematic_line = lines[lineno - 1]
            
            # Détermine le niveau d'indentation correct en analysant le contexte
            correct_indent_level = 0
            if lineno > 1:
                # Cherche le niveau d'indentation de référence
                for i in range(lineno - 2, -1, -1):
                    if lines[i].strip():  # Ligne non vide
                        reference_indent = len(lines[i]) - len(lines[i].lstrip())
                        
                        # Si c'est une ligne de définition (def, class, if, etc.), 
                        # le niveau courant devrait être au même niveau
                        if any(lines[i].strip().startswith(keyword) for keyword in ['def ', 'class ', 'if ', 'elif ', 'else:', 'for ', 'while ', 'try:', 'except', 'finally:', 'with ']):
                            correct_indent_level = reference_indent
                        else:
                            correct_indent_level = reference_indent
                        break
            
            # Applique la correction d'indentation
            corrected_line = (indent_char * correct_indent_level) + problematic_line.lstrip()
            lines[lineno - 1] = corrected_line
            notes.append(f"Auto-correction: Ajustement intelligent de l'indentation à la ligne {lineno} (niveau {correct_indent_level}).")
            
        # Cas 3: "unindent does not match" -> réparation intelligente ligne par ligne
        elif "unindent does not match" in msg:
            notes.append("Auto-correction: Réparation intelligente des niveaux d'indentation incohérents.")
            
            # Stratégie intelligente : reconstruction avec analyse contextuelle
            fixed_lines = []
            indent_stack = [0]  # Stack des niveaux d'indentation valides
            
            for i, line in enumerate(lines):
                stripped = line.strip()
                if not stripped:
                    fixed_lines.append("")
                    continue
                
                original_indent = len(line) - len(stripped)
                
                # Détermine le niveau d'indentation approprié selon le contexte
                if any(stripped.startswith(kw) for kw in ['def ', 'class ']):
                    # Définitions de classe/fonction : niveau de base
                    target_indent = 0
                    indent_stack = [0, indent_size]  # Reset stack pour nouvelle définition
                    
                elif any(stripped.startswith(kw) for kw in ['if ', 'for ', 'while ', 'try:', 'with ']):
                    # Structures de contrôle : niveau actuel
                    target_indent = indent_stack[-1]
                    if stripped.endswith(':'):
                        indent_stack.append(target_indent + indent_size)
                        
                elif any(stripped.startswith(kw) for kw in ['elif ', 'else:', 'except', 'finally:']):
                    # Clauses alternatives : même niveau que la structure parente
                    if len(indent_stack) >= 2:
                        target_indent = indent_stack[-2]
                        if stripped.endswith(':'):
                            indent_stack[-1] = target_indent + indent_size
                    else:
                        target_indent = 0
                        
                elif stripped in ['pass', 'break', 'continue'] or stripped.startswith(('return', 'raise', 'yield')):
                    # Instructions terminales : niveau courant
                    target_indent = indent_stack[-1] if len(indent_stack) > 1 else indent_size
                    
                else:
                    # Instructions normales : niveau courant
                    target_indent = indent_stack[-1] if len(indent_stack) > 1 else indent_size
                
                # Validation et ajustement du niveau calculé
                if target_indent < 0:
                    target_indent = 0
                    
                # Construction de la ligne corrigée
                corrected_line = (indent_char * target_indent) + stripped
                fixed_lines.append(corrected_line)
                
                # Gestion de la fermeture de blocs (détection heuristique)
                if not stripped.endswith(':') and target_indent > 0:
                    # Si on détecte une ligne qui devrait fermer un bloc
                    next_line_indent = 0
                    if i + 1 < len(lines) and lines[i + 1].strip():
                        next_line_indent = len(lines[i + 1]) - len(lines[i + 1].lstrip())
                        
                    # Si la ligne suivante a moins d'indentation, on ferme potentiellement des blocs
                    if next_line_indent < target_indent and len(indent_stack) > 1:
                        # Recherche du niveau d'indentation correspondant dans la stack
                        while len(indent_stack) > 1 and indent_stack[-1] > next_line_indent:
                            indent_stack.pop()
            
            return '\n'.join(fixed_lines), notes

        return "\n".join(lines), notes

    # --- Nouvelles méthodes v4.3.0 (Priorités Moyennes) ---
    
    def analyze_indentation_pattern(self, code: str, error_msg: str) -> Dict[str, Any]:
        """Analyse approfondie du pattern d'indentation pour stockage ChromaDB"""
        pattern_info = {
            "pattern_type": "generic",
            "indentation_style": "unknown",
            "indentation_level": 4,
            "complexity_score": 0.0,
            "nested_structures": [],
            "common_errors": []
        }
        
        lines = code.split('\n')
        
        # Détection du style d'indentation
        spaces_count = sum(1 for line in lines if line.startswith('    '))
        tabs_count = sum(1 for line in lines if line.startswith('\t'))
        
        if tabs_count > spaces_count:
            pattern_info["indentation_style"] = "tabs"
            pattern_info["indentation_level"] = 1
        elif spaces_count > 0:
            pattern_info["indentation_style"] = "spaces"
            # Calcul du niveau d'indentation moyen
            indented_lines = [line for line in lines if line.strip() and line.startswith(' ')]
            if indented_lines:
                avg_indent = sum(len(line) - len(line.lstrip()) for line in indented_lines) / len(indented_lines)
                pattern_info["indentation_level"] = int(avg_indent) if avg_indent > 0 else 4
        else:
            pattern_info["indentation_style"] = "mixed"
            
        # Classification du type d'erreur d'indentation
        if "expected an indented block" in error_msg:
            pattern_info["pattern_type"] = "expected_block"
        elif "unexpected indent" in error_msg:
            pattern_info["pattern_type"] = "unexpected_indent"
        elif "unindent does not match" in error_msg:
            pattern_info["pattern_type"] = "unindent_mismatch"
        elif "inconsistent use of tabs and spaces" in error_msg:
            pattern_info["pattern_type"] = "mixed_indentation"
            
        # Analyse de la complexité
        complexity_factors = 0
        nested_structures = []
        
        for line in lines:
            stripped = line.strip()
            if any(keyword in stripped for keyword in ['def ', 'class ', 'if ', 'for ', 'while ', 'try:', 'with ']):
                nested_structures.append(stripped.split()[0])
                complexity_factors += 1
                
        pattern_info["nested_structures"] = nested_structures
        pattern_info["complexity_score"] = min(complexity_factors / len(lines) if lines else 0, 1.0)
        
        return pattern_info
    
    def find_similar_indentation_patterns(self, code: str, error_msg: str) -> List[Dict[str, Any]]:
        """Recherche de patterns d'indentation similaires dans ChromaDB"""
        if not self.chroma_patterns.enabled:
            return []
            
        # Recherche des patterns similaires
        similar_patterns = self.chroma_patterns.find_similar_patterns(
            code, limit=self._max_similar_patterns
        )
        
        # Filtrage par type d'erreur si possible
        pattern_analysis = self.analyze_indentation_pattern(code, error_msg)
        relevant_patterns = []
        
        for pattern in similar_patterns:
            if pattern.get("pattern_type") == pattern_analysis["pattern_type"]:
                # Pattern très pertinent
                pattern["relevance_score"] = 1.0
                relevant_patterns.append(pattern)
            elif pattern.get("indentation_style") == pattern_analysis["indentation_style"]:
                # Pattern moyennement pertinent
                pattern["relevance_score"] = 0.7
                relevant_patterns.append(pattern)
            else:
                # Pattern peu pertinent mais potentiellement utile
                pattern["relevance_score"] = 0.3
                relevant_patterns.append(pattern)
        
        # Tri par pertinence et score de succès
        relevant_patterns.sort(
            key=lambda x: (x.get("relevance_score", 0) * x.get("success_rate", 0)), 
            reverse=True
        )
        
        return relevant_patterns[:self._max_similar_patterns]
    
    def apply_pattern_based_correction(self, code: str, similar_patterns: List[Dict[str, Any]]) -> Tuple[str, List[str]]:
        """Applique une correction basée sur les patterns similaires trouvés"""
        if not similar_patterns:
            return code, []
            
        adaptations = []
        best_pattern = similar_patterns[0]  # Pattern avec le meilleur score
        
        if best_pattern.get("relevance_score", 0) > 0.5:
            try:
                # Tentative d'application du pattern
                corrected_code = best_pattern.get("code_after", "")
                
                if corrected_code and len(corrected_code.strip()) > 0:
                    # Adaptation du pattern au code actuel
                    # Pour l'instant, adaptation simple - à améliorer avec ML
                    pattern_type = best_pattern.get("pattern_type", "generic")
                    indentation_style = best_pattern.get("indentation_style", "spaces")
                    indentation_level = best_pattern.get("indentation_level", 4)
                    
                    adaptations.append(f"Pattern appliqué: {pattern_type} (style: {indentation_style}, niveau: {indentation_level})")
                    adaptations.append(f"Basé sur pattern avec taux de succès: {best_pattern.get('success_rate', 0):.2f}")
                    
                    # Application des règles du pattern trouvé
                    lines = code.split('\n')
                    corrected_lines = []
                    
                    for line in lines:
                        if line.strip():
                            if indentation_style == "spaces":
                                # Normalisation vers espaces
                                stripped = line.lstrip()
                                if line != stripped:  # Ligne indentée
                                    indent_char = ' '
                                    target_indent = indentation_level
                                    corrected_line = (indent_char * target_indent) + stripped
                                    corrected_lines.append(corrected_line)
                                else:
                                    corrected_lines.append(line)
                            else:
                                corrected_lines.append(line)
                        else:
                            corrected_lines.append(line)
                    
                    return '\n'.join(corrected_lines), adaptations
                    
            except Exception as e:
                adaptations.append(f"Erreur application pattern: {e}")
        
        return code, adaptations
    
    def calculate_advanced_confidence_score(self, 
                                          original_code: str,
                                          corrected_code: str,
                                          validation_result: ValidationResult,
                                          patterns_used: List[Dict[str, Any]]) -> float:
        """Calcule un score de confiance avancé basé sur plusieurs facteurs"""
        base_confidence = validation_result.confidence_score
        
        # Facteur de patterns similaires
        pattern_factor = 0.0
        if patterns_used:
            avg_pattern_success = sum(p.get("success_rate", 0) for p in patterns_used) / len(patterns_used)
            avg_relevance = sum(p.get("relevance_score", 0) for p in patterns_used) / len(patterns_used)
            pattern_factor = (avg_pattern_success + avg_relevance) / 2
        
        # Facteur de complexité du code
        complexity_factor = 1.0
        lines = original_code.split('\n')
        if lines:
            complexity_score = sum(1 for line in lines if any(keyword in line for keyword in ['def ', 'class ', 'if ', 'for ', 'while ', 'try:'])) / len(lines)
            complexity_factor = max(0.5, 1.0 - complexity_score)  # Plus c'est complexe, moins on est confiant
        
        # Facteur de similarité entre original et corrigé
        similarity_factor = 1.0
        if original_code != corrected_code:
            # Mesure simple de similarité
            original_lines = set(original_code.split('\n'))
            corrected_lines = set(corrected_code.split('\n'))
            if original_lines:
                similarity_factor = len(original_lines.intersection(corrected_lines)) / len(original_lines)
        
        # Score final pondéré
        advanced_confidence = (
            base_confidence * 0.4 +
            pattern_factor * 0.3 +
            complexity_factor * 0.2 +
            similarity_factor * 0.1
        )
        
        return min(max(advanced_confidence, 0.0), 1.0)
    
    def get_pattern_statistics(self, pattern_type: str = None) -> Dict[str, Any]:
        """Récupère les statistiques des patterns depuis PostgreSQL"""
        if not self.pg_analytics.enabled:
            return {"error": "PostgreSQL analytics non disponible"}
        
        try:
            stats = self.pg_analytics.get_pattern_stats(pattern_type)
            
            # Enrichissement avec informations ChromaDB
            chroma_info = {
                "chromadb_enabled": self.chroma_patterns.enabled,
                "patterns_cache_size": len(self._correction_history)
            }
            
            return {
                "pattern_statistics": stats,
                "chromadb_info": chroma_info,
                "total_patterns": len(stats),
                "best_performing_pattern": max(stats.items(), key=lambda x: x[1]["success_rate"]) if stats else None
            }
        except Exception as e:
            self.logger.error(f"Erreur récupération statistiques: {e}")
            return {"error": str(e)}
    
    def analyze_learning_progress(self) -> Dict[str, Any]:
        """Analyse les progrès du système d'apprentissage"""
        progress = {
            "total_corrections": len(self._correction_history),
            "successful_corrections": sum(1 for entry in self._correction_history if entry["success"]),
            "pattern_learning_enabled": self._enable_pattern_learning,
            "confidence_threshold": self._pattern_confidence_threshold,
            "databases_status": {
                "chromadb": self.chroma_patterns.enabled,
                "postgresql": self.pg_analytics.enabled
            }
        }
        
        # Calcul du taux de succès
        if progress["total_corrections"] > 0:
            progress["success_rate"] = progress["successful_corrections"] / progress["total_corrections"]
        else:
            progress["success_rate"] = 0.0
        
        # Analyse par type d'erreur
        error_types_stats = {}
        for entry in self._correction_history:
            error_type = entry["error_type"]
            if error_type not in error_types_stats:
                error_types_stats[error_type] = {"count": 0, "successes": 0}
            
            error_types_stats[error_type]["count"] += 1
            if entry["success"]:
                error_types_stats[error_type]["successes"] += 1
        
        # Calcul des taux de succès par type
        for error_type, stats in error_types_stats.items():
            stats["success_rate"] = stats["successes"] / stats["count"] if stats["count"] > 0 else 0
        
        progress["error_types_analysis"] = error_types_stats
        
        return progress

    async def execute_task(self, task: Task) -> Result:
        """
        Exécute la tâche d'adaptation du code v4.3.0 avec classification étendue, validation multi-niveaux 
        et patterns d'indentation complexes via ChromaDB/PostgreSQL.
        """
        code = task.params.get("code")
        feedback = task.params.get("feedback")
        error_type = task.params.get("error_type", "generic")
        use_discovery = task.params.get("use_import_discovery", True)
        validate_result = task.params.get("validate_result", True)
        # Nouvelles options v4.3.0
        use_pattern_learning = task.params.get("use_pattern_learning", self._enable_pattern_learning)
        enable_analytics = task.params.get("enable_analytics", True)

        if not code:
            return Result(success=False, error="Le code source est manquant.")

        self.logger.info(f"Tâche d'adaptation v4.3.0 reçue. Type d'erreur: '{error_type}'.")

        # Variables d'état
        adaptations = []
        modified_code = code
        classification = None
        validation_pre = None
        validation_post = None
        
        # Nouvelles variables v4.3.0 (Priorités Moyennes)
        similar_patterns = []
        patterns_used = []
        start_time = time.time()
        pattern_analysis = None

        try:
            # Validation pré-correction (si demandée)
            if validate_result:
                validation_pre = self.validate_multi_level(code)
                self.logger.info(f"Validation pré-correction: {validation_pre.confidence_score:.2f}")

            # Classification étendue de l'erreur si une exception est fournie
            if isinstance(feedback, Exception):
                classification = self.classify_error_extended(feedback, code)
                self.logger.info(f"Classification: {classification.error_type.value} (confiance: {classification.confidence_score:.2f})")
                
                # Mise à jour du type d'erreur basé sur la classification
                if classification.confidence_score > 0.8:
                    error_type = classification.error_type.value
            
            # Recherche de patterns similaires v4.3.0 (pour erreurs d'indentation)
            if use_pattern_learning and error_type in ["indentation", "syntax"]:
                try:
                    pattern_analysis = self.analyze_indentation_pattern(code, str(feedback) if feedback else "")
                    similar_patterns = self.find_similar_indentation_patterns(code, str(feedback) if feedback else "")
                    
                    if similar_patterns:
                        self.logger.info(f"Trouvé {len(similar_patterns)} patterns similaires")
                        patterns_used = similar_patterns
                    else:
                        self.logger.info("Aucun pattern similaire trouvé")
                        
                except Exception as e:
                    self.logger.warning(f"Erreur recherche patterns: {e}")

            # Auto-découverte des imports si nécessaire
            if use_discovery and not self._import_discovery_cache:
                try:
                    discoveries = self.discover_project_imports()
                    self.logger.info(f"Cache d'imports mis à jour: {len(discoveries)} éléments")
                except Exception as e:
                    self.logger.warning(f"Échec auto-découverte imports: {e}")

            # Stratégies de réparation étendues v4.3.0
            if error_type == "indentation":
                self.logger.info("Stratégie indentation avancée v4.3.0 activée.")
                
                # Tentative d'application de patterns similaires d'abord
                if patterns_used:
                    pattern_corrected_code, pattern_adaptations = self.apply_pattern_based_correction(modified_code, patterns_used)
                    if pattern_corrected_code != modified_code:
                        modified_code = pattern_corrected_code
                        adaptations.extend(pattern_adaptations)
                        self.logger.info("Correction basée sur patterns appliquée")
                    else:
                        # Fallback vers méthode traditionnelle
                        modified_code, indent_adaptations = self._fix_indentation_errors(modified_code, feedback)
                        adaptations.extend(indent_adaptations)
                else:
                    # Méthode traditionnelle si pas de patterns
                    modified_code, indent_adaptations = self._fix_indentation_errors(modified_code, feedback)
                    adaptations.extend(indent_adaptations)
                
            elif error_type == "name":
                self.logger.info("Stratégie NameError avancée avec auto-découverte.")
                if "name" in str(feedback).lower() and "is not defined" in str(feedback).lower():
                    match = re.search(r"name '(\w+)' is not defined", str(feedback))
                    if match:
                        undefined_name = match.group(1)
                        
                        # 1. Recherche dans mapping statique
                        if undefined_name in self.COMPLEX_IMPORT_MAP:
                            module_path, import_name = self.COMPLEX_IMPORT_MAP[undefined_name]
                            success = self._apply_import_fix(modified_code, module_path, import_name)
                            if success:
                                modified_code = success
                                adaptations.append(f"Import statique ajouté: from {module_path} import {import_name}")
                        
                        # 2. Recherche dans cache d'auto-découverte
                        elif undefined_name in self._import_discovery_cache:
                            discovery = self._import_discovery_cache[undefined_name]
                            if discovery.confidence > 0.7:
                                # Parse et applique l'import découvert
                                success = self._apply_discovered_import(modified_code, discovery)
                                if success:
                                    modified_code = success
                                    adaptations.append(f"Import découvert ajouté: {discovery.import_statement} (confiance: {discovery.confidence:.2f})")
                                    
            elif error_type in ["type_error", "attribute_error", "value_error"]:
                self.logger.info(f"Stratégie {error_type} avancée activée.")
                
                if error_type == "type_error" and isinstance(feedback, TypeError):
                    # Analyse spécifique TypeError
                    fixes = self._analyze_type_error(str(feedback), code)
                    adaptations.extend(fixes)
                    
                elif error_type == "attribute_error" and isinstance(feedback, AttributeError):
                    # Analyse spécifique AttributeError
                    fixes = self._analyze_attribute_error(str(feedback), code)
                    adaptations.extend(fixes)
                    
            elif error_type == "module_not_found":
                self.logger.info("Stratégie module_not_found avancée activée.")
                if "No module named" in str(feedback):
                    module_name = self._extract_module_name(str(feedback))
                    if module_name:
                        adaptations.append(f"Module manquant détecté: {module_name}")
                        # Suggestions d'installation ou imports alternatifs
                        suggestions = self._suggest_module_alternatives(module_name)
                        adaptations.extend(suggestions)
                                
            elif error_type == "import":
                self.logger.info("Stratégie import avancée activée.")
                # Logique import étendue
                if "cannot import name" in str(feedback).lower():
                    import_suggestions = self._analyze_import_error(str(feedback), code)
                    adaptations.extend(import_suggestions)
                    
            elif error_type == "syntax":
                self.logger.info("Stratégie syntaxe avancée activée.")
                # Corrections syntaxiques spécialisées
                if isinstance(feedback, SyntaxError):
                    syntax_fixes = self._fix_syntax_error(feedback, code)
                    if syntax_fixes:
                        modified_code, syntax_adaptations = syntax_fixes
                        adaptations.extend(syntax_adaptations)

            # Correction des blocs vides (toujours appliquée)
            try:
                source_tree = cst.parse_module(modified_code)
                pass_inserter = CstPassInserter()
                modified_tree = source_tree.visit(pass_inserter)
                if not source_tree.deep_equals(modified_tree):
                    modified_code = modified_tree.code
                    adaptations.append("Correction LibCST: Ajout de 'pass' dans blocs vides.")
            except cst.ParserSyntaxError as e:
                self.logger.warning(f"Erreur parsing LibCST: {e}")

            # Validation post-correction (si demandée)
            if validate_result:
                validation_post = self.validate_multi_level(modified_code)
                self.logger.info(f"Validation post-correction: {validation_post.confidence_score:.2f}")
                
                # Amélioration détectée ?
                if validation_pre and validation_post.confidence_score > validation_pre.confidence_score:
                    improvement = validation_post.confidence_score - validation_pre.confidence_score
                    adaptations.append(f"Amélioration qualité: +{improvement:.2f} points")

            # Calcul du score de confiance avancé v4.3.0
            advanced_confidence = validation_post.confidence_score if validation_post else 0.0
            if patterns_used and validation_post:
                advanced_confidence = self.calculate_advanced_confidence_score(
                    code, modified_code, validation_post, patterns_used
                )
                self.logger.info(f"Score de confiance avancé: {advanced_confidence:.2f}")
            
            # Enregistrement dans ChromaDB v4.3.0 (si pattern d'indentation réussi)
            if (use_pattern_learning and error_type == "indentation" and 
                len(adaptations) > 0 and advanced_confidence > self._pattern_confidence_threshold):
                
                try:
                    if pattern_analysis:
                        pattern_id = f"pat_{int(time.time())}_{hash(code) % 10000}"
                        indentation_pattern = IndentationPattern(
                            pattern_id=pattern_id,
                            code_before=code,
                            code_after=modified_code,
                            success_rate=advanced_confidence,
                            pattern_type=pattern_analysis["pattern_type"],
                            indentation_style=pattern_analysis["indentation_style"],
                            indentation_level=pattern_analysis["indentation_level"],
                            metadata={
                                "error_msg": str(feedback) if feedback else "",
                                "adaptations": adaptations,
                                "complexity_score": pattern_analysis.get("complexity_score", 0.0)
                            }
                        )
                        
                        success = self.chroma_patterns.store_pattern(indentation_pattern)
                        if success:
                            adaptations.append(f"Pattern stocké dans ChromaDB: {pattern_id}")
                            self.logger.info(f"Pattern d'indentation stocké: {pattern_id}")

                except Exception as e:
                    self.logger.warning(f"Erreur stockage pattern ChromaDB: {e}")
            
            # Enregistrement de l'historique dans ChromaDB v4.3.0
            if use_pattern_learning:
                try:
                    correction_id = f"corr_{int(time.time())}_{hash(code) % 10000}"
                    correction_history = CorrectionHistory(
                        correction_id=correction_id,
                        original_code=code,
                        corrected_code=modified_code,
                        error_type=error_type,
                        confidence_score=advanced_confidence,
                        validation_result=validation_post.__dict__ if validation_post else {},
                        patterns_used=[p.get("pattern_type", "unknown") for p in patterns_used]
                    )
                    
                    success = self.chroma_history.log_correction(correction_history)
                    if success:
                        self.logger.info(f"Correction stockée dans historique: {correction_id}")
                        
                except Exception as e:
                    self.logger.warning(f"Erreur stockage historique ChromaDB: {e}")
            
            # Enregistrement des métriques PostgreSQL v4.3.0
            if enable_analytics:
                try:
                    processing_time = time.time() - start_time
                    metrics_id = f"metrics_{int(time.time())}_{hash(code) % 10000}"
                    
                    analytics_metrics = AnalyticsMetrics(
                        metric_id=metrics_id,
                        error_type=error_type,
                        confidence_score=advanced_confidence,
                        success=len(adaptations) > 0,
                        processing_time=processing_time,
                        pattern_type=pattern_analysis["pattern_type"] if pattern_analysis else None,
                        metadata={
                            "adaptations_count": len(adaptations),
                            "patterns_used_count": len(patterns_used),
                            "validation_improvement": (validation_post.confidence_score - validation_pre.confidence_score) if (validation_pre and validation_post) else None
                        }
                    )
                    
                    success = self.pg_analytics.log_correction_metrics(analytics_metrics)
                    if success:
                        self.logger.info(f"Métriques PostgreSQL enregistrées: {metrics_id}")
                    
                    # Mise à jour des analytics de patterns
                    if pattern_analysis:
                        pattern_success = len(adaptations) > 0 and advanced_confidence > 0.5
                        self.pg_analytics.update_pattern_analytics(
                            pattern_analysis["pattern_type"],
                            pattern_success,
                            advanced_confidence
                        )
                        
                except Exception as e:
                    self.logger.warning(f"Erreur enregistrement métriques PostgreSQL: {e}")

            # Enregistrement dans l'historique pour apprentissage (legacy)
            correction_entry = {
                "error_type": error_type,
                "success": len(adaptations) > 0,
                "adaptations": adaptations.copy(),
                "classification": classification.__dict__ if classification else None,
                "validation_improvement": (validation_post.confidence_score - validation_pre.confidence_score) if (validation_pre and validation_post) else None,
                "advanced_confidence": advanced_confidence,
                "patterns_used": len(patterns_used)
            }
            self._correction_history.append(correction_entry)

            # Résultat final v4.3.0
            result_data = {
                "adapted_code": modified_code,
                "adaptations": adaptations or ["Aucune adaptation nécessaire."],
                "error_classification": classification.__dict__ if classification else None,
                "validation_pre": validation_pre.__dict__ if validation_pre else None,
                "validation_post": validation_post.__dict__ if validation_post else None,
                "import_discoveries_used": len([a for a in adaptations if "découvert" in a]),
                # Nouvelles données v4.3.0 (Priorités Moyennes)
                "advanced_confidence_score": advanced_confidence,
                "patterns_found": len(similar_patterns),
                "patterns_used": len(patterns_used),
                "pattern_analysis": pattern_analysis,
                "processing_time": time.time() - start_time,
                "chromadb_enabled": self.chroma_patterns.enabled,
                "postgresql_enabled": self.pg_analytics.enabled,
                "pattern_learning_used": use_pattern_learning and len(patterns_used) > 0
            }

            return Result(success=True, data=result_data)

        except Exception as e:
            self.logger.error(f"Erreur inattendue durant l'adaptation v4.3.0: {e}", exc_info=True)
            return Result(success=False, error=str(e))
    
    def _apply_import_fix(self, code: str, module_path: str, import_name: str) -> Optional[str]:
        """Applique un fix d'import via LibCST"""
        try:
            source_tree = cst.parse_module(code)
            import_adder = CstComplexImportAdder(module_path, [import_name])
            modified_tree = source_tree.visit(import_adder)
            if not source_tree.deep_equals(modified_tree):
                return modified_tree.code
        except Exception as e:
            self.logger.warning(f"Échec application import {module_path}.{import_name}: {e}")
        return None
    
    def _apply_discovered_import(self, code: str, discovery: ImportDiscovery) -> Optional[str]:
        """Applique un import découvert automatiquement"""
        try:
            # Parse la déclaration d'import
            if discovery.import_statement.startswith("from "):
                # from module import name
                parts = discovery.import_statement.split()
                if len(parts) >= 4:
                    module = parts[1]
                    name = parts[3]
                    return self._apply_import_fix(code, module, name)
            elif discovery.import_statement.startswith("import "):
                # import module
                module = discovery.import_statement.split()[1]
                source_tree = cst.parse_module(code)
                import_adder = CstImportAdder([module])
                modified_tree = source_tree.visit(import_adder)
                if not source_tree.deep_equals(modified_tree):
                    return modified_tree.code
        except Exception as e:
            self.logger.warning(f"Échec application import découvert: {e}")
        return None
    
    def _analyze_type_error(self, error_msg: str, code: str) -> List[str]:
        """Analyse spécialisée des TypeError"""
        fixes = []
        if "takes" in error_msg and "positional argument" in error_msg:
            fixes.append("Analyse TypeError: Vérifier le nombre d'arguments de fonction")
        elif "unsupported operand type" in error_msg:
            fixes.append("Analyse TypeError: Vérifier les types des opérandes")
        elif "not callable" in error_msg:
            fixes.append("Analyse TypeError: Objet utilisé comme fonction")
        return fixes
    
    def _analyze_attribute_error(self, error_msg: str, code: str) -> List[str]:
        """Analyse spécialisée des AttributeError"""
        fixes = []
        match = re.search(r"'(\w+)' object has no attribute '(\w+)'", error_msg)
        if match:
            obj_type, attr_name = match.groups()
            fixes.append(f"Analyse AttributeError: '{obj_type}' n'a pas l'attribut '{attr_name}'")
            # Suggestions basées sur des patterns communs
            if attr_name in ["append", "extend"] and obj_type != "list":
                fixes.append("Suggestion: Vérifier que l'objet est bien une liste")
        return fixes
    
    def _extract_module_name(self, error_msg: str) -> Optional[str]:
        """Extrait le nom du module depuis l'erreur"""
        match = re.search(r"No module named '([^']+)'", error_msg)
        return match.group(1) if match else None
    
    def _suggest_module_alternatives(self, module_name: str) -> List[str]:
        """Suggère des alternatives pour un module manquant"""
        suggestions = []
        common_alternatives = {
            "cv2": "opencv-python",
            "PIL": "Pillow",
            "sklearn": "scikit-learn",
            "bs4": "beautifulsoup4"
        }
        
        if module_name in common_alternatives:
            suggestions.append(f"Suggestion: installer {common_alternatives[module_name]} (pip install {common_alternatives[module_name]})")
        else:
            suggestions.append(f"Suggestion: pip install {module_name}")
        
        return suggestions
    
    def _analyze_import_error(self, error_msg: str, code: str) -> List[str]:
        """Analyse les erreurs d'import pour suggestions"""
        fixes = []
        if "cannot import name" in error_msg:
            match = re.search(r"cannot import name '([^']+)' from '([^']+)'", error_msg)
            if match:
                name, module = match.groups()
                fixes.append(f"Import error: '{name}' non trouvé dans '{module}'")
                fixes.append(f"Suggestion: Vérifier que '{name}' existe dans '{module}'")
        return fixes
    
    def _fix_syntax_error(self, error: SyntaxError, code: str) -> Optional[Tuple[str, List[str]]]:
        """Corrections automatiques de SyntaxError simples"""
        if not hasattr(error, 'text') or not error.text:
            return None
            
        fixes = []
        lines = code.splitlines()
        lineno = error.lineno or 1
        
        if lineno <= len(lines):
            problematic_line = lines[lineno - 1]
            
            # Correction : deux points manquants
            if "invalid syntax" in str(error) and not problematic_line.rstrip().endswith(':'):
                if any(problematic_line.strip().startswith(kw) for kw in ['if ', 'def ', 'class ', 'for ', 'while ', 'try', 'except', 'elif ', 'else']):
                    lines[lineno - 1] = problematic_line.rstrip() + ':'
                    fixes.append(f"Ajout ':' manquant ligne {lineno}")
                    return '\n'.join(lines), fixes
        
        return None

    async def startup(self) -> None:
        self.logger.info(f"Agent Adaptateur CST démarré.")

    async def shutdown(self) -> None:
        self.logger.info(f"Agent Adaptateur CST arrêté.")

    async def health_check(self) -> Dict[str, Any]:
        return {"status": "healthy", "version": self.version}

def create_agent_MAINTENANCE_03_adaptateur_code(**config) -> "AgentMAINTENANCE03AdaptateurCode":
    """Factory function pour créer l'agent."""
    return AgentMAINTENANCE03AdaptateurCode(**config)