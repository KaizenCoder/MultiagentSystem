#!/usr/bin/env python3
"""
🧪 Tests Unitaires et d'Intégration - TaskMaster NextGeneration
============================================================

Suite complète de tests pour valider toutes les fonctionnalités
du TaskMaster NextGen hybride.

Auteur: NextGeneration Team
Version: 1.0.0
Date: 2025-06-23
"""

import asyncio
import pytest
import json
import tempfile
from pathlib import Path
from datetime import datetime, timedelta
from unittest.mock import Mock, patch, AsyncMock
import sys
import os

# Ajout du chemin pour les imports
sys.path.append(str(Path(__file__).parent.parent))

from agents.taskmaster_nextgen import (
    TaskMasterNextGen, NLPProcessor, ComplexityAnalyzer, 
    DependencyResolver, ValidationEngine, TaskRepository,
    ExportManager, TaskDefinition, TaskType, TaskPriority,
    ValidationStatus, ComplexityLevel, SubTask, EvidenceEntry,
    RealityCheck, TaskMetrics
)

# ==========================================
# 1. TESTS NLP PROCESSOR
# ==========================================

class TestNLPProcessor:
    """Tests pour le processeur NLP"""
    
    def setup_method(self):
        """Setup avant chaque test"""
        self.nlp_processor = NLPProcessor()
    
    def test_initialize_nlp_without_spacy(self):
        """Test initialisation sans spaCy installé"""
        with patch('spacy.load', side_effect=OSError("Model not found")):
            processor = NLPProcessor()
            assert processor.nlp is None
    
    def test_parse_simple_request(self):
        """Test parsing d'une requête simple"""
        request = "Faire un audit de sécurité"
        task_def = self.nlp_processor.parse_request(request)
        
        assert isinstance(task_def, TaskDefinition)
        assert task_def.task_type == TaskType.AUDIT
        assert "audit" in task_def.title.lower()
        assert task_def.description == request
        assert "security_analysis" in task_def.required_capabilities
    
    def test_parse_complex_request(self):
        """Test parsing d'une requête complexe"""
        request = "Optimiser urgent les performances de la base de données PostgreSQL avec analyse ML"
        task_def = self.nlp_processor.parse_request(request)
        
        assert task_def.task_type == TaskType.OPTIMIZATION
        assert task_def.priority == TaskPriority.CRITICAL  # "urgent"
        assert "database_management" in task_def.required_capabilities
        assert "machine_learning" in task_def.required_capabilities
    
    def test_classify_task_types(self):
        """Test classification des différents types de tâches"""
        test_cases = [
            ("Créer la documentation", TaskType.DOCUMENTATION),
            ("Tester l'API", TaskType.TESTING),
            ("Refactoriser le code", TaskType.REFACTORING),
            ("Surveiller les performances", TaskType.MONITORING),
            ("Déployer l'application", TaskType.DEPLOYMENT),
            ("Parser le document", TaskType.PARSING),
            ("Planifier le projet", TaskType.PLANNING)
        ]
        
        for request, expected_type in test_cases:
            task_def = self.nlp_processor.parse_request(request)
            assert task_def.task_type == expected_type, f"Failed for: {request}"
    
    def test_detect_priority_levels(self):
        """Test détection des niveaux de priorité"""
        test_cases = [
            ("Tâche critique urgente", TaskPriority.CRITICAL),
            ("Important audit de sécurité", TaskPriority.HIGH),
            ("Faire plus tard si possible", TaskPriority.LOW),
            ("Tâche normale", TaskPriority.MEDIUM)
        ]
        
        for request, expected_priority in test_cases:
            task_def = self.nlp_processor.parse_request(request)
            assert task_def.priority == expected_priority, f"Failed for: {request}"
    
    @pytest.mark.skipif(not hasattr(NLPProcessor(), 'nlp') or NLPProcessor().nlp is None, 
                       reason="spaCy not available")
    def test_extract_entities_with_spacy(self):
        """Test extraction d'entités avec spaCy (si disponible)"""
        request = "Analyser les données de Paris pour Microsoft"
        task_def = self.nlp_processor.parse_request(request)
        
        # Vérification que les entités sont extraites
        entities = task_def.metadata.get("entities", {})
        assert isinstance(entities, dict)


# ==========================================
# 2. TESTS COMPLEXITY ANALYZER
# ==========================================

class TestComplexityAnalyzer:
    """Tests pour l'analyseur de complexité"""
    
    def setup_method(self):
        """Setup avant chaque test"""
        self.analyzer = ComplexityAnalyzer()
    
    def test_simple_task_complexity(self):
        """Test complexité d'une tâche simple"""
        task = TaskDefinition(
            id="test1",
            title="Test simple",
            description="Tâche de test simple",
            task_type=TaskType.DOCUMENTATION,
            priority=TaskPriority.LOW,
            required_capabilities=["writing"]
        )
        
        analysis = self.analyzer.analyze_task_complexity(task)
        
        assert analysis["complexity_level"] == ComplexityLevel.SIMPLE
        assert analysis["complexity_score"] < 15
        assert analysis["estimated_duration_minutes"] < 20
        assert "justification" in analysis
    
    def test_complex_task_complexity(self):
        """Test complexité d'une tâche complexe"""
        task = TaskDefinition(
            id="test2",
            title="Refactoring complexe",
            description="Refactoring complet avec ML",
            task_type=TaskType.REFACTORING,  # Type complexe
            priority=TaskPriority.CRITICAL,
            required_capabilities=["refactoring", "ml", "database", "security", "testing"],
            constraints={"deadline": "1 week", "quality": "high"},
            expected_outputs=["code", "tests", "documentation", "benchmarks"]
        )
        
        analysis = self.analyzer.analyze_task_complexity(task)
        
        assert analysis["complexity_level"] in [ComplexityLevel.COMPLEX, ComplexityLevel.VERY_COMPLEX]
        assert analysis["complexity_score"] > 35
        assert analysis["estimated_duration_minutes"] > 30
    
    def test_complexity_factors(self):
        """Test des facteurs de complexité individuels"""
        base_task = TaskDefinition(
            id="test3",
            title="Test factors",
            description="Test",
            task_type=TaskType.ANALYSIS,
            priority=TaskPriority.MEDIUM,
            required_capabilities=["analysis"]
        )
        
        analysis = self.analyzer.analyze_task_complexity(base_task)
        base_score = analysis["complexity_score"]
        
        # Ajouter plus de capacités augmente la complexité
        complex_task = TaskDefinition(
            id="test4",
            title="Test factors complex",
            description="Test",
            task_type=TaskType.ANALYSIS,
            priority=TaskPriority.MEDIUM,
            required_capabilities=["analysis", "db", "ml", "security"]
        )
        
        complex_analysis = self.analyzer.analyze_task_complexity(complex_task)
        assert complex_analysis["complexity_score"] > base_score
    
    def test_task_type_complexity_mapping(self):
        """Test du mapping complexité par type de tâche"""
        # REFACTORING doit être plus complexe que DOCUMENTATION
        refactoring_task = TaskDefinition(
            id="test5", title="Refactor", description="Test",
            task_type=TaskType.REFACTORING, priority=TaskPriority.MEDIUM,
            required_capabilities=["refactoring"]
        )
        
        doc_task = TaskDefinition(
            id="test6", title="Document", description="Test",
            task_type=TaskType.DOCUMENTATION, priority=TaskPriority.MEDIUM,
            required_capabilities=["writing"]
        )
        
        refactor_analysis = self.analyzer.analyze_task_complexity(refactoring_task)
        doc_analysis = self.analyzer.analyze_task_complexity(doc_task)
        
        assert refactor_analysis["complexity_score"] > doc_analysis["complexity_score"]


# ==========================================
# 3. TESTS DEPENDENCY RESOLVER
# ==========================================

class TestDependencyResolver:
    """Tests pour le résolveur de dépendances"""
    
    def setup_method(self):
        """Setup avant chaque test"""
        self.resolver = DependencyResolver()
    
    def test_analyze_audit_dependencies(self):
        """Test analyse des dépendances pour un audit"""
        task = TaskDefinition(
            id="audit_test",
            title="Security Audit",
            description="Audit de sécurité",
            task_type=TaskType.AUDIT,
            priority=TaskPriority.HIGH,
            required_capabilities=["security_analysis"]
        )
        
        dependencies = self.resolver.analyze_dependencies(task)
        
        assert len(dependencies) > 0
        assert any("scan" in dep.get("task", "") for dep in dependencies)
        assert any("analyze" in dep.get("task", "") for dep in dependencies)
        assert any("report" in dep.get("task", "") for dep in dependencies)
    
    def test_analyze_optimization_dependencies(self):
        """Test analyse des dépendances pour optimisation"""
        task = TaskDefinition(
            id="optim_test",
            title="Performance Optimization",
            description="Optimisation des performances",
            task_type=TaskType.OPTIMIZATION,
            priority=TaskPriority.HIGH,
            required_capabilities=["performance_tuning"]
        )
        
        dependencies = self.resolver.analyze_dependencies(task)
        
        # Vérifier la séquence logique
        task_names = [dep["task"] for dep in dependencies]
        assert "baseline_measurement" in task_names
        assert "profile_performance" in task_names
        assert "optimize_code" in task_names
        assert "validate_improvements" in task_names
    
    def test_create_execution_plan(self):
        """Test création du plan d'exécution"""
        dependencies = [
            {"task": "prepare", "parallel": True},
            {"task": "analyze", "parallel": False},
            {"task": "optimize", "parallel": False},
            {"task": "test", "parallel": True}
        ]
        
        execution_plan = self.resolver.create_execution_plan(dependencies)
        
        assert len(execution_plan) == len(dependencies)
        for i, step in enumerate(execution_plan):
            assert "order" in step
            assert step["order"] == i
    
    def test_unknown_task_type_dependencies(self):
        """Test gestion des types de tâches inconnus"""
        task = TaskDefinition(
            id="unknown_test",
            title="Unknown Task",
            description="Tâche de type inconnu",
            task_type=TaskType.ANALYSIS,  # Type non défini dans les templates
            priority=TaskPriority.MEDIUM,
            required_capabilities=["unknown"]
        )
        
        dependencies = self.resolver.analyze_dependencies(task)
        
        # Doit retourner un template générique
        assert len(dependencies) >= 3  # prepare, execute, validate minimum
        task_names = [dep["task"] for dep in dependencies]
        assert "prepare" in task_names
        assert "execute" in task_names
        assert "validate" in task_names


# ==========================================
# 4. TESTS VALIDATION ENGINE
# ==========================================

class TestValidationEngine:
    """Tests pour le moteur de validation anti-hallucination"""
    
    def setup_method(self):
        """Setup avant chaque test"""
        self.engine = ValidationEngine()
    
    @pytest.mark.asyncio
    async def test_validate_good_output(self):
        """Test validation d'une sortie correcte"""
        agent_id = "test_agent"
        output = {
            "status": "success",
            "findings": ["Issue 1", "Issue 2"],
            "recommendations": ["Fix 1", "Fix 2"],
            "timestamp": datetime.now().isoformat()
        }
        expected = {"findings": [], "recommendations": []}
        context = {"task_type": TaskType.AUDIT}
        
        result = await self.engine.validate_agent_output(agent_id, output, expected, context)
        
        assert result["validated"] == True
        assert result["confidence_score"] >= 0.8
        assert len(result["checks"]) >= 4
    
    @pytest.mark.asyncio
    async def test_validate_bad_output(self):
        """Test validation d'une sortie problématique"""
        agent_id = "test_agent"
        output = {
            "duration": -100,  # Valeur aberrante
            "percentage": 150,  # Pourcentage > 100
            "result": ""  # Champ critique vide
        }
        expected = {"duration": 60, "percentage": 80, "result": "some result"}
        context = {"task_type": TaskType.TESTING}
        
        result = await self.engine.validate_agent_output(agent_id, output, expected, context)
        
        assert result["validated"] == False
        assert result["confidence_score"] < 0.8
        
        # Vérifier que les outliers sont détectés
        outlier_check = next((check for check in result["checks"] 
                            if check.check_type == "outlier_detection"), None)
        assert outlier_check is not None
        assert not outlier_check.passed
    
    @pytest.mark.asyncio
    async def test_structural_consistency_check(self):
        """Test vérification de cohérence structurelle"""
        good_output = {"key1": "value1", "key2": "value2"}
        expected = {"key1": "expected1", "key2": "expected2"}
        
        check = self.engine._check_structural_consistency(good_output, expected)
        
        assert check.passed == True
        assert check.confidence > 0.8
        
        # Test avec structure incorrecte
        bad_output = {"wrong_key": "value"}
        check_bad = self.engine._check_structural_consistency(bad_output, expected)
        
        assert check_bad.passed == False
        assert check_bad.confidence < 0.8
    
    @pytest.mark.asyncio
    async def test_semantic_consistency_check(self):
        """Test vérification de cohérence sémantique"""
        # Test pour un audit
        audit_output = {"findings": ["security issue"], "recommendations": ["fix this"]}
        audit_context = {"task_type": TaskType.AUDIT}
        
        check = self.engine._check_semantic_consistency(audit_output, audit_context)
        assert check.passed == True
        
        # Test pour un audit sans findings
        bad_audit_output = {"other_data": "value"}
        check_bad = self.engine._check_semantic_consistency(bad_audit_output, audit_context)
        assert check_bad.confidence < 1.0
    
    def test_outlier_detection(self):
        """Test détection des valeurs aberrantes"""
        outlier_output = {
            "duration": -50,  # Négatif pour durée
            "percentage": 150,  # > 100 pour pourcentage
            "description": "",  # Vide pour champ critique
            "very_long_text": "x" * 15000  # Texte anormalement long
        }
        
        check = self.engine._check_for_outliers(outlier_output)
        
        assert not check.passed
        assert len(check.details["outliers"]) >= 3
        assert check.confidence < 0.4
    
    def test_temporal_consistency_check(self):
        """Test vérification de cohérence temporelle"""
        good_temporal_output = {
            "timestamp": datetime.now().isoformat(),
            "duration": 3600,  # 1 heure
            "date_created": "2025-06-23T10:00:00"
        }
        
        check = self.engine._check_temporal_consistency(good_temporal_output)
        assert check.passed == True
        
        # Test avec données temporelles incorrectes
        bad_temporal_output = {
            "timestamp": "2030-01-01T00:00:00Z",  # Future lointain
            "duration": -100,  # Durée négative
            "invalid_date": "not-a-date"
        }
        
        check_bad = self.engine._check_temporal_consistency(bad_temporal_output)
        assert not check_bad.passed
        assert len(check_bad.details["temporal_issues"]) > 0


# ==========================================
# 5. TESTS TASK REPOSITORY
# ==========================================

class TestTaskRepository:
    """Tests pour le repository de tâches"""
    
    def setup_method(self):
        """Setup avant chaque test"""
        # Utiliser un fichier temporaire pour les tests
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        self.temp_path = Path(self.temp_file.name)
        self.temp_file.close()
        
        self.repo = TaskRepository(self.temp_path)
    
    def teardown_method(self):
        """Cleanup après chaque test"""
        if self.temp_path.exists():
            self.temp_path.unlink()
    
    def test_create_and_get_task(self):
        """Test création et récupération de tâche"""
        task = TaskDefinition(
            id="test_task_001",
            title="Test Task",
            description="Test description",
            task_type=TaskType.TESTING,
            priority=TaskPriority.MEDIUM,
            required_capabilities=["testing"]
        )
        
        # Création
        task_id = self.repo.create_task(task)
        assert task_id == "test_task_001"
        
        # Récupération
        retrieved_task = self.repo.get_task(task_id)
        assert retrieved_task is not None
        assert retrieved_task.title == "Test Task"
        assert retrieved_task.task_type == TaskType.TESTING
    
    def test_update_task(self):
        """Test mise à jour de tâche"""
        task = TaskDefinition(
            id="update_test",
            title="Original Title",
            description="Original description",
            task_type=TaskType.TESTING,
            priority=TaskPriority.LOW,
            required_capabilities=["testing"]
        )
        
        task_id = self.repo.create_task(task)
        
        # Mise à jour
        updates = {
            "title": "Updated Title",
            "priority": TaskPriority.HIGH,
            "complexity_score": 75.5
        }
        success = self.repo.update_task(task_id, updates)
        assert success == True
        
        # Vérification
        updated_task = self.repo.get_task(task_id)
        assert updated_task.title == "Updated Title"
        assert updated_task.priority == TaskPriority.HIGH
        assert updated_task.complexity_score == 75.5
    
    def test_delete_task(self):
        """Test suppression de tâche"""
        task = TaskDefinition(
            id="delete_test",
            title="To Delete",
            description="Will be deleted",
            task_type=TaskType.TESTING,
            priority=TaskPriority.MEDIUM,
            required_capabilities=["testing"]
        )
        
        task_id = self.repo.create_task(task)
        assert self.repo.get_task(task_id) is not None
        
        # Suppression
        success = self.repo.delete_task(task_id)
        assert success == True
        
        # Vérification
        assert self.repo.get_task(task_id) is None
    
    def test_list_tasks_with_filters(self):
        """Test listing de tâches avec filtres"""
        # Créer plusieurs tâches
        tasks = [
            TaskDefinition(
                id=f"filter_test_{i}",
                title=f"Task {i}",
                description=f"Description {i}",
                task_type=TaskType.TESTING if i % 2 == 0 else TaskType.AUDIT,
                priority=TaskPriority.HIGH if i < 2 else TaskPriority.LOW,
                required_capabilities=["testing"]
            )
            for i in range(4)
        ]
        
        for task in tasks:
            self.repo.create_task(task)
        
        # Test sans filtre
        all_tasks = self.repo.list_tasks()
        assert len(all_tasks) == 4
        
        # Test avec filtre sur le type
        testing_tasks = self.repo.list_tasks({"task_type": TaskType.TESTING})
        assert len(testing_tasks) == 2
        
        # Test avec filtre sur la priorité
        high_priority_tasks = self.repo.list_tasks({"priority": TaskPriority.HIGH})
        assert len(high_priority_tasks) == 2
    
    def test_subtasks_management(self):
        """Test gestion des sous-tâches"""
        # Créer une tâche parent
        parent_task = TaskDefinition(
            id="parent_test",
            title="Parent Task",
            description="Parent description",
            task_type=TaskType.ANALYSIS,
            priority=TaskPriority.MEDIUM,
            required_capabilities=["analysis"]
        )
        
        parent_id = self.repo.create_task(parent_task)
        
        # Ajouter des sous-tâches
        subtasks = [
            SubTask(
                id=f"sub_{i}",
                parent_id=parent_id,
                title=f"Subtask {i}",
                status=ValidationStatus.PENDING
            )
            for i in range(3)
        ]
        
        for subtask in subtasks:
            success = self.repo.add_subtask(parent_id, subtask)
            assert success == True
        
        # Récupérer les sous-tâches
        retrieved_subtasks = self.repo.get_subtasks(parent_id)
        assert len(retrieved_subtasks) == 3
        assert all(st.parent_id == parent_id for st in retrieved_subtasks)
    
    def test_persistence(self):
        """Test persistance des données"""
        # Créer une tâche
        task = TaskDefinition(
            id="persistence_test",
            title="Persistent Task",
            description="Will persist",
            task_type=TaskType.DOCUMENTATION,
            priority=TaskPriority.MEDIUM,
            required_capabilities=["writing"]
        )
        
        self.repo.create_task(task)
        
        # Créer un nouveau repository avec le même fichier
        new_repo = TaskRepository(self.temp_path)
        
        # Vérifier que la tâche existe
        retrieved_task = new_repo.get_task("persistence_test")
        assert retrieved_task is not None
        assert retrieved_task.title == "Persistent Task"


# ==========================================
# 6. TESTS EXPORT MANAGER
# ==========================================

class TestExportManager:
    """Tests pour le gestionnaire d'export"""
    
    def setup_method(self):
        """Setup avant chaque test"""
        self.export_manager = ExportManager()
        self.sample_tasks = [
            TaskDefinition(
                id="export_test_1",
                title="Export Test Task 1",
                description="First test task for export",
                task_type=TaskType.TESTING,
                priority=TaskPriority.HIGH,
                required_capabilities=["testing", "analysis"],
                complexity_score=45.5,
                estimated_duration=120
            ),
            TaskDefinition(
                id="export_test_2",
                title="Export Test Task 2",
                description="Second test task for export",
                task_type=TaskType.DOCUMENTATION,
                priority=TaskPriority.MEDIUM,
                required_capabilities=["writing"],
                complexity_score=25.0,
                estimated_duration=60
            )
        ]
    
    def test_export_json(self):
        """Test export au format JSON"""
        result = self.export_manager.export_tasks(self.sample_tasks, "json")
        
        assert isinstance(result, str)
        
        # Parser le JSON pour vérifier la structure
        data = json.loads(result)
        assert "export_timestamp" in data
        assert "tasks_count" in data
        assert data["tasks_count"] == 2
        assert "tasks" in data
        assert len(data["tasks"]) == 2
        
        # Vérifier le contenu
        first_task = data["tasks"][0]
        assert first_task["title"] == "Export Test Task 1"
        assert first_task["task_type"] == "testing"
    
    def test_export_markdown(self):
        """Test export au format Markdown"""
        result = self.export_manager.export_tasks(self.sample_tasks, "markdown")
        
        assert isinstance(result, str)
        assert "# 📋 Export des Tâches TaskMaster" in result
        assert "Export Test Task 1" in result
        assert "Export Test Task 2" in result
        assert "**Type :** Testing" in result
        assert "**Priorité :** HIGH" in result
    
    def test_export_csv(self):
        """Test export au format CSV"""
        result = self.export_manager.export_tasks(self.sample_tasks, "csv")
        
        assert isinstance(result, str)
        lines = result.strip().split('\n')
        
        # Vérifier l'en-tête
        header = lines[0]
        assert "ID" in header
        assert "Titre" in header
        assert "Type" in header
        
        # Vérifier les données
        assert len(lines) == 3  # Header + 2 tâches
        assert "export_test_1" in lines[1]
        assert "Export Test Task 1" in lines[1]
    
    def test_export_html(self):
        """Test export au format HTML"""
        result = self.export_manager.export_tasks(self.sample_tasks, "html")
        
        assert isinstance(result, str)
        assert "<!DOCTYPE html>" in result
        assert "TaskMaster - Export des Tâches" in result
        assert "Export Test Task 1" in result
        assert "priority-high" in result  # Classe CSS pour priorité haute
        assert "capability" in result  # Classe CSS pour capacités
    
    def test_export_to_file(self):
        """Test export vers fichier"""
        with tempfile.NamedTemporaryFile(delete=False, suffix='.json') as temp_file:
            temp_path = Path(temp_file.name)
        
        try:
            result = self.export_manager.export_tasks(self.sample_tasks, "json", temp_path)
            
            assert result == temp_path
            assert temp_path.exists()
            
            # Vérifier le contenu du fichier
            with open(temp_path, 'r', encoding='utf-8') as f:
                content = f.read()
                data = json.loads(content)
                assert data["tasks_count"] == 2
        
        finally:
            if temp_path.exists():
                temp_path.unlink()
    
    def test_unsupported_format(self):
        """Test gestion des formats non supportés"""
        with pytest.raises(ValueError, match="Format non supporté"):
            self.export_manager.export_tasks(self.sample_tasks, "unsupported_format")


# ==========================================
# 7. TESTS D'INTÉGRATION TASKMASTER NEXTGEN
# ==========================================

class TestTaskMasterNextGenIntegration:
    """Tests d'intégration pour TaskMaster NextGen"""
    
    def setup_method(self):
        """Setup avant chaque test"""
        # Utiliser un répertoire temporaire pour les tests
        self.temp_dir = Path(tempfile.mkdtemp())
        
        # Mock de l'environnement pour utiliser le répertoire temporaire
        with patch.dict(os.environ, {"TASKMASTER_WORK_DIR": str(self.temp_dir)}):
            self.taskmaster = TaskMasterNextGen("test_taskmaster")
    
    def teardown_method(self):
        """Cleanup après chaque test"""
        import shutil
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
    
    @pytest.mark.asyncio
    async def test_startup_and_agent_discovery(self):
        """Test démarrage et découverte d'agents"""
        # Mock de la découverte d'agents
        mock_agents = {
            "test_agent_1": {
                "class": Mock,
                "capabilities": ["testing", "analysis"],
                "module_path": Path("test_agent_1.py"),
                "pattern_factory_compatible": True,
                "validation_ready": True
            }
        }
        
        with patch.object(self.taskmaster, '_discover_agents') as mock_discover:
            mock_discover.return_value = None
            self.taskmaster.agents = mock_agents
            
            result = await self.taskmaster.startup()
            
            assert result["status"] == "ready"
            assert result["agents_count"] == 1
            assert result["components"]["validation_ready"] == True
    
    @pytest.mark.asyncio
    async def test_create_task_full_pipeline(self):
        """Test pipeline complet de création de tâche"""
        request = "Faire un audit de sécurité urgent du module d'authentification"
        
        result = await self.taskmaster.create_task_from_natural_language(request)
        
        assert result["status"] == "success"
        assert "task_id" in result
        
        # Vérifier la tâche créée
        task_def = result["task_definition"]
        assert task_def["task_type"] == "audit"
        assert task_def["priority"] == "CRITICAL"  # "urgent" détecté
        assert len(task_def["required_capabilities"]) > 0
        
        # Vérifier l'analyse de complexité
        complexity = result["complexity_analysis"]
        assert "complexity_score" in complexity
        assert "estimated_duration_minutes" in complexity
        
        # Vérifier les sous-tâches
        subtasks = result["subtasks"]
        assert len(subtasks) > 0
        assert all("parent_id" in st for st in subtasks)
    
    @pytest.mark.asyncio
    async def test_execute_task_with_validation(self):
        """Test exécution de tâche avec validation"""
        # D'abord créer une tâche
        request = "Tester l'API REST"
        create_result = await self.taskmaster.create_task_from_natural_language(request)
        task_id = create_result["task_id"]
        
        # Mock d'un agent pour l'exécution
        mock_agent_class = Mock()
        mock_agent_instance = Mock()
        mock_agent_instance.run.return_value = {
            "status": "success",
            "tests_passed": 15,
            "tests_failed": 2,
            "coverage": 85.5
        }
        mock_agent_class.return_value = mock_agent_instance
        
        # Mock des agents disponibles
        self.taskmaster.agents = {
            "test_agent": {
                "class": mock_agent_class,
                "capabilities": ["testing", "api_testing"],
                "module_path": Path("test_agent.py"),
                "pattern_factory_compatible": True,
                "validation_ready": True
            }
        }
        
        # Exécution
        result = await self.taskmaster.execute_task(task_id, agent_validation=True)
        
        assert result["status"] == "success"
        assert result["agent_used"] == "test_agent"
        assert "execution_time" in result
        
        # Vérifier la validation
        agent_result = result["result"]
        assert "validation" in agent_result
        assert "confidence_score" in agent_result["validation"]
    
    def test_get_task_status(self):
        """Test récupération du statut de tâche"""
        # Créer une tâche directement dans le repository
        task = TaskDefinition(
            id="status_test",
            title="Status Test Task",
            description="Test task for status",
            task_type=TaskType.TESTING,
            priority=TaskPriority.MEDIUM,
            required_capabilities=["testing"]
        )
        
        self.taskmaster.task_repository.create_task(task)
        
        # Récupérer le statut
        status = self.taskmaster.get_task_status("status_test")
        
        assert status["task"]["id"] == "status_test"
        assert status["task"]["title"] == "Status Test Task"
        assert status["status"] == "stored"
        assert "subtasks" in status
    
    def test_list_and_filter_tasks(self):
        """Test listing et filtrage des tâches"""
        # Créer plusieurs tâches
        tasks = [
            TaskDefinition(
                id=f"list_test_{i}",
                title=f"List Test Task {i}",
                description=f"Test task {i}",
                task_type=TaskType.TESTING if i % 2 == 0 else TaskType.AUDIT,
                priority=TaskPriority.HIGH if i < 2 else TaskPriority.LOW,
                required_capabilities=["testing"]
            )
            for i in range(4)
        ]
        
        for task in tasks:
            self.taskmaster.task_repository.create_task(task)
        
        # Test listing complet
        result = self.taskmaster.list_tasks()
        assert result["tasks_count"] == 4
        
        # Test avec filtres
        filtered_result = self.taskmaster.list_tasks({"task_type": TaskType.TESTING})
        assert filtered_result["tasks_count"] == 2
    
    def test_export_functionality(self):
        """Test fonctionnalité d'export"""
        # Créer quelques tâches
        for i in range(3):
            task = TaskDefinition(
                id=f"export_integration_{i}",
                title=f"Export Integration Task {i}",
                description=f"Task for export testing {i}",
                task_type=TaskType.DOCUMENTATION,
                priority=TaskPriority.MEDIUM,
                required_capabilities=["writing"]
            )
            self.taskmaster.task_repository.create_task(task)
        
        # Test export JSON
        result = self.taskmaster.export_tasks("json")
        assert result["status"] == "success"
        assert result["tasks_exported"] == 3
        assert result["format"] == "json"
        
        # Test export vers fichier
        result_file = self.taskmaster.export_tasks("markdown", 
                                                  output_path=str(self.temp_dir / "test_export.md"))
        assert result_file["status"] == "success"
        assert Path(result_file["output_path"]).exists()
    
    def test_dashboard_data(self):
        """Test données du dashboard"""
        # Créer des tâches variées
        task_configs = [
            (TaskType.TESTING, TaskPriority.HIGH, 45.0),
            (TaskType.AUDIT, TaskPriority.CRITICAL, 85.0),
            (TaskType.DOCUMENTATION, TaskPriority.LOW, 15.0),
            (TaskType.OPTIMIZATION, TaskPriority.MEDIUM, 65.0)
        ]
        
        for i, (task_type, priority, complexity) in enumerate(task_configs):
            task = TaskDefinition(
                id=f"dashboard_test_{i}",
                title=f"Dashboard Task {i}",
                description=f"Task {i} for dashboard",
                task_type=task_type,
                priority=priority,
                required_capabilities=["testing"],
                complexity_score=complexity
            )
            self.taskmaster.task_repository.create_task(task)
        
        # Récupérer les données du dashboard
        dashboard = self.taskmaster.get_dashboard_data()
        
        assert dashboard["summary"]["total_tasks"] == 4
        assert len(dashboard["distributions"]["task_types"]) > 0
        assert len(dashboard["distributions"]["priorities"]) > 0
        assert len(dashboard["distributions"]["complexity_levels"]) > 0
        assert dashboard["system_status"]["storage_healthy"] == True


# ==========================================
# 8. TESTS DE PERFORMANCE
# ==========================================

class TestTaskMasterPerformance:
    """Tests de performance pour TaskMaster NextGen"""
    
    def setup_method(self):
        """Setup avant chaque test"""
        self.temp_dir = Path(tempfile.mkdtemp())
        with patch.dict(os.environ, {"TASKMASTER_WORK_DIR": str(self.temp_dir)}):
            self.taskmaster = TaskMasterNextGen("perf_test_taskmaster")
    
    def teardown_method(self):
        """Cleanup après chaque test"""
        import shutil
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
    
    @pytest.mark.asyncio
    async def test_bulk_task_creation_performance(self):
        """Test performance de création en masse de tâches"""
        import time
        
        start_time = time.time()
        
        # Créer 100 tâches
        tasks_created = []
        for i in range(100):
            request = f"Tâche de test numéro {i} pour validation des performances"
            result = await self.taskmaster.create_task_from_natural_language(request)
            if result["status"] == "success":
                tasks_created.append(result["task_id"])
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # Vérifications de performance
        assert len(tasks_created) == 100
        assert total_time < 30.0  # Moins de 30 secondes pour 100 tâches
        
        avg_time_per_task = total_time / 100
        assert avg_time_per_task < 0.3  # Moins de 300ms par tâche
        
        print(f"Performance: {total_time:.2f}s total, {avg_time_per_task*1000:.1f}ms/tâche")
    
    def test_repository_performance_large_dataset(self):
        """Test performance du repository avec beaucoup de données"""
        import time
        
        # Créer 1000 tâches
        start_time = time.time()
        
        for i in range(1000):
            task = TaskDefinition(
                id=f"perf_test_{i:04d}",
                title=f"Performance Test Task {i}",
                description=f"Task number {i} for performance testing",
                task_type=TaskType.TESTING,
                priority=TaskPriority.MEDIUM,
                required_capabilities=["testing"]
            )
            self.taskmaster.task_repository.create_task(task)
        
        creation_time = time.time() - start_time
        
        # Test de récupération
        start_time = time.time()
        all_tasks = self.taskmaster.task_repository.list_tasks()
        retrieval_time = time.time() - start_time
        
        # Test de recherche avec filtre
        start_time = time.time()
        filtered_tasks = self.taskmaster.task_repository.list_tasks({"task_type": TaskType.TESTING})
        filter_time = time.time() - start_time
        
        # Vérifications
        assert len(all_tasks) == 1000
        assert len(filtered_tasks) == 1000
        assert creation_time < 10.0  # Moins de 10 secondes pour créer 1000 tâches
        assert retrieval_time < 1.0   # Moins de 1 seconde pour récupérer 1000 tâches
        assert filter_time < 2.0      # Moins de 2 secondes pour filtrer 1000 tâches
        
        print(f"Repository performance: création={creation_time:.2f}s, "
              f"récupération={retrieval_time:.2f}s, filtre={filter_time:.2f}s")


# ==========================================
# 9. CONFIGURATION PYTEST
# ==========================================

def pytest_configure(config):
    """Configuration des marqueurs pytest"""
    config.addinivalue_line(
        "markers", "integration: marque les tests d'intégration"
    )
    config.addinivalue_line(
        "markers", "performance: marque les tests de performance"
    )


# ==========================================
# 10. FIXTURES COMMUNES
# ==========================================

@pytest.fixture
def sample_task_definition():
    """Fixture pour une définition de tâche de test"""
    return TaskDefinition(
        id="fixture_test_task",
        title="Fixture Test Task",
        description="Task created by pytest fixture",
        task_type=TaskType.TESTING,
        priority=TaskPriority.MEDIUM,
        required_capabilities=["testing", "validation"],
        constraints={"deadline": "1 week"},
        expected_outputs=["test_report", "coverage_report"],
        success_criteria=["all_tests_pass", "coverage_80_percent"]
    )

@pytest.fixture
def mock_agent_class():
    """Fixture pour une classe d'agent mockée"""
    class MockAgent:
        CAPABILITIES = ["testing", "analysis", "validation"]
        
        def __init__(self):
            self.name = "MockAgent"
        
        def run(self, task_prompt):
            return {
                "status": "success",
                "message": f"Mock execution of: {task_prompt[:50]}...",
                "timestamp": datetime.now().isoformat()
            }
        
        def shutdown(self):
            pass
    
    return MockAgent


# ==========================================
# 11. MAIN POUR EXÉCUTION DIRECTE
# ==========================================

if __name__ == "__main__":
    print("🧪 Tests TaskMaster NextGeneration")
    print("=" * 50)
    print("Exécution des tests avec pytest...")
    print()
    
    # Exécution avec pytest
    import subprocess
    result = subprocess.run([
        "python", "-m", "pytest", __file__, 
        "-v", "--tb=short", "--color=yes"
    ])
    
    if result.returncode == 0:
        print("\n✅ Tous les tests sont passés!")
    else:
        print("\n❌ Certains tests ont échoué.")
    
    exit(result.returncode)