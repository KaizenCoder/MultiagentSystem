import ast
import re
from typing import List, Dict, Any, Optional
from agent_factory_implementation.core.agent_factory_architecture import Agent, Task, Result

class AgentMAINTENANCE11CodeEnhancer(Agent):
    """
    Agent chargé d'améliorer activement le code Python :
    - Refactoring automatique des patterns inefficaces
    - Modernisation du code (f-strings, walrus operator, etc.)
    - Simplification des structures complexes
    - Optimisation des algorithmes basiques
    - Application automatique des meilleures pratiques
    - Transformation des anti-patterns en code propre
    
    Contrairement au peer reviewer qui DÉTECTE, cet agent TRANSFORME.
    """
    
    def __init__(self, agent_id="agent_MAINTENANCE_11_code_enhancer", version="1.0", description="Améliore activement le code Python.", status="enabled"):
        super().__init__(agent_id, version, description, "code_enhancer", status)
        
        # Transformations disponibles
        self.transformations = {
            'string_formatting': True,      # % et .format() → f-strings
            'list_comprehensions': True,    # Boucles → comprehensions
            'generator_expressions': True,  # Listes → générateurs quand approprié
            'builtin_functions': True,      # Optimisations avec builtins
            'context_managers': True,       # with statements
            'pathlib_modernization': True,  # os.path → pathlib
            'type_hints': True,            # Ajout de type hints basiques
            'walrus_operator': False,      # := (Python 3.8+) - optionnel
            'match_statements': False      # match/case (Python 3.10+) - optionnel
        }

    async def startup(self):
        await super().startup()
        self.log("Code Enhancer prêt. Chargement des transformations...")

    async def execute_task(self, task: Task) -> Result:
        if task.type != "enhance_code":
            return Result(success=False, error="Type de tâche non supporté.")

        code = task.params.get("code")
        file_path = task.params.get("file_path", "unknown_file")
        enhancement_level = task.params.get("enhancement_level", "moderate")  # conservative/moderate/aggressive
        
        if not code:
            return Result(success=False, error="Code non fourni.")

        self.log(f"⚡ Amélioration du code pour : {file_path} (niveau: {enhancement_level})")

        try:
            # Analyse préliminaire
            original_metrics = self._analyze_code_metrics(code)
            
            # Application des améliorations par étapes
            enhanced_code = code
            transformations_applied = []
            
            # 1. Modernisation des strings (toujours sûr)
            if self.transformations['string_formatting']:
                enhanced_code, string_transforms = self._modernize_string_formatting(enhanced_code)
                transformations_applied.extend(string_transforms)
            
            # 2. Amélioration des opérations booléennes (sûr)
            enhanced_code, bool_transforms = self._modernize_boolean_operations(enhanced_code)
            transformations_applied.extend(bool_transforms)
            
            # 3. Amélioration de la gestion d'erreurs
            enhanced_code, error_transforms = self._enhance_error_handling(enhanced_code)
            transformations_applied.extend(error_transforms)
            
            # 4. Optimisation des structures de données
            if self.transformations['builtin_functions']:
                enhanced_code, data_transforms = self._optimize_data_structures(enhanced_code)
                transformations_applied.extend(data_transforms)
            
            # 5. Refactoring des boucles en comprehensions
            if self.transformations['list_comprehensions']:
                enhanced_code, comp_transforms = self._convert_to_comprehensions(enhanced_code)
                transformations_applied.extend(comp_transforms)
            
            # 6. Optimisations avancées de boucles
            enhanced_code, loop_transforms = self._optimize_loops_advanced(enhanced_code)
            transformations_applied.extend(loop_transforms)
            
            # 7. Optimisation avec builtins
            if self.transformations['builtin_functions']:
                enhanced_code, builtin_transforms = self._optimize_with_builtins(enhanced_code)
                transformations_applied.extend(builtin_transforms)
            
            # 8. Modernisation pathlib
            if self.transformations['pathlib_modernization']:
                enhanced_code, pathlib_transforms = self._modernize_pathlib(enhanced_code)
                transformations_applied.extend(pathlib_transforms)
            
            # 9. Amélioration des context managers
            if self.transformations['context_managers']:
                enhanced_code, context_transforms = self._improve_context_managers(enhanced_code)
                transformations_applied.extend(context_transforms)
            
            # 10. Amélioration des définitions de fonctions
            enhanced_code, func_transforms = self._enhance_function_definitions(enhanced_code)
            transformations_applied.extend(func_transforms)
            
            # 11. Type hints (si niveau >= moderate)
            if enhancement_level in ['moderate', 'aggressive']:
                if self.transformations['type_hints']:
                    enhanced_code, type_transforms = self._add_basic_type_hints(enhanced_code)
                    transformations_applied.extend(type_transforms)
                
                # Type hints avancés pour niveau aggressive
                if enhancement_level == 'aggressive':
                    enhanced_code, advanced_type_transforms = self._add_advanced_type_hints(enhanced_code)
                    transformations_applied.extend(advanced_type_transforms)
            
            # 12. Fonctionnalités Python modernes (si niveau aggressive)
            if enhancement_level == 'aggressive':
                enhanced_code, modern_transforms = self._apply_modern_python_features(enhanced_code)
                transformations_applied.extend(modern_transforms)
            
            # Analyse post-amélioration
            enhanced_metrics = self._analyze_code_metrics(enhanced_code)
            improvement_score = self._calculate_improvement_score(original_metrics, enhanced_metrics)
            
            # Classification des transformations par impact
            categorized_transforms = self._categorize_transformations(transformations_applied)
            
            # Génération de statistiques détaillées
            enhancement_stats = self._generate_enhancement_statistics(
                original_metrics, enhanced_metrics, transformations_applied
            )
            
            # Rapport d'amélioration complet
            enhancement_report = {
                "file_path": file_path,
                "enhancement_level": enhancement_level,
                "original_metrics": original_metrics,
                "enhanced_metrics": enhanced_metrics,
                "improvement_score": improvement_score,
                "transformations_applied": transformations_applied,
                "categorized_transformations": categorized_transforms,
                "enhancement_statistics": enhancement_stats,
                "total_transformations": len(transformations_applied),
                "code_quality_improvement": enhanced_metrics["quality_score"] - original_metrics["quality_score"],
                "performance_improvements": [t for t in transformations_applied if 'performance' in t.get('type', '')],
                "readability_improvements": [t for t in transformations_applied if 'readability' in t.get('description', '').lower()],
                "modernization_count": len([t for t in transformations_applied if 'modern' in t.get('type', '')]),
                "safety_improvements": len([t for t in transformations_applied if t.get('type') in ['error_handling', 'assertion_improvement']])
            }

            self.log(f"⚡ Amélioration terminée pour {file_path} - {len(transformations_applied)} transformations")
            self.log(f"   📊 Score: {original_metrics['quality_score']:.1f} → {enhanced_metrics['quality_score']:.1f} (+{improvement_score:.1f})")
            self.log(f"   🚀 Modernisation: {enhancement_stats['modernization_percentage']:.1f}%")
            
            return Result(success=True, data={
                "enhanced_code": enhanced_code,
                "enhancement_report": enhancement_report,
                "significant_improvement": improvement_score > 15,
                "modernization_level": enhancement_stats['modernization_percentage']
            }) type_transforms = self._add_basic_type_hints(enhanced_code)
                transformations_applied.extend(type_transforms)
            
            # 7. Fonctionnalités modernes (si niveau aggressive)
            if enhancement_level == 'aggressive':
                if self.transformations['walrus_operator']:
                    enhanced_code, walrus_transforms = self._apply_walrus_operator(enhanced_code)
                    transformations_applied.extend(walrus_transforms)
            
            # Analyse post-amélioration
            enhanced_metrics = self._analyze_code_metrics(enhanced_code)
            improvement_score = self._calculate_improvement_score(original_metrics, enhanced_metrics)
            
            # Rapport d'amélioration
            enhancement_report = {
                "file_path": file_path,
                "enhancement_level": enhancement_level,
                "original_metrics": original_metrics,
                "enhanced_metrics": enhanced_metrics,
                "improvement_score": improvement_score,
                "transformations_applied": transformations_applied,
                "total_transformations": len(transformations_applied),
                "code_quality_improvement": enhanced_metrics["quality_score"] - original_metrics["quality_score"]
            }

            self.log(f"⚡ Amélioration terminée pour {file_path} - {len(transformations_applied)} transformations, score: +{improvement_score:.1f}")
            
            return Result(success=True, data={
                "enhanced_code": enhanced_code,
                "enhancement_report": enhancement_report,
                "significant_improvement": improvement_score > 15
            })

        except Exception as e:
            self.log(f"Erreur lors de l'amélioration du code de {file_path}: {e}", level="error")
            return Result(success=False, error=str(e))

    def _analyze_code_metrics(self, code: str) -> Dict[str, Any]:
        """Analyse les métriques du code pour mesurer l'amélioration."""
        metrics = {
            "lines_of_code": len([line for line in code.splitlines() if line.strip()]),
            "complexity_score": 0,
            "readability_score": 0,
            "modern_features_count": 0,
            "quality_score": 0
        }
        
        try:
            tree = ast.parse(code)
            
            # Comptage des fonctionnalités modernes
            modern_features = 0
            for node in ast.walk(tree):
                if isinstance(node, ast.JoinedStr):  # f-strings
                    modern_features += 1
                elif isinstance(node, ast.ListComp):  # list comprehensions
                    modern_features += 1
                elif isinstance(node, ast.With):  # context managers
                    modern_features += 1
            
            metrics["modern_features_count"] = modern_features
            
            # Score de complexité (inverse de la complexité cyclomatique)
            complexity = self._calculate_complexity(tree)
            metrics["complexity_score"] = max(0, 100 - complexity * 2)
            
            # Score de lisibilité basé sur la longueur des noms et structures
            readability = self._calculate_readability(tree, code)
            metrics["readability_score"] = readability
            
            # Score qualité global
            metrics["quality_score"] = (
                metrics["complexity_score"] * 0.3 +
                metrics["readability_score"] * 0.4 +
                min(metrics["modern_features_count"] * 5, 30) * 0.3
            )
            
        except SyntaxError:
            # Code invalide
            metrics["quality_score"] = 0
        
        return metrics

    def _modernize_string_formatting(self, code: str) -> tuple[str, List[Dict]]:
        """Convertit les anciens formats de string en f-strings."""
        transformations = []
        lines = code.splitlines()
        modified_lines = []
        
        for i, line in enumerate(lines):
            original_line = line
            
            # Pattern 1: "string %s" % variable → f"string {variable}"
            percent_pattern = re.compile(r'"([^"]*?)%s([^"]*?)"\s*%\s*(\w+)')
            matches = percent_pattern.findall(line)
            for match in matches:
                old_format = f'"{match[0]}%s{match[1]}" % {match[2]}'
                new_format = f'f"{match[0]}{{{match[2]}}}{match[1]}"'
                line = line.replace(old_format, new_format)
                transformations.append({
                    'type': 'string_formatting',
                    'line': i + 1,
                    'description': 'Conversion % formatting vers f-string',
                    'before': old_format,
                    'after': new_format
                })
            
            # Pattern 2: "string {}".format(variable) → f"string {variable}"
            format_pattern = re.compile(r'"([^"]*?){}([^"]*?)"\.format\((\w+)\)')
            matches = format_pattern.findall(line)
            for match in matches:
                old_format = f'"{match[0]}{{}}{match[1]}".format({match[2]})'
                new_format = f'f"{match[0]}{{{match[2]}}}{match[1]}"'
                line = line.replace(old_format, new_format)
                transformations.append({
                    'type': 'string_formatting',
                    'line': i + 1,
                    'description': 'Conversion .format() vers f-string',
                    'before': old_format,
                    'after': new_format
                })
            
            modified_lines.append(line)
        
        return '\n'.join(modified_lines), transformations

    def _convert_to_comprehensions(self, code: str) -> tuple[str, List[Dict]]:
        """Convertit les boucles simples en list comprehensions."""
        transformations = []
        
        try:
            tree = ast.parse(code)
            transformer = LoopToComprehensionTransformer()
            new_tree = transformer.visit(tree)
            ast.fix_missing_locations(new_tree)
            
            # Utiliser ast.unparse si disponible (Python 3.9+)
            try:
                enhanced_code = ast.unparse(new_tree)
                transformations.extend(transformer.transformations)
            except AttributeError:
                # Fallback pour Python < 3.9
                enhanced_code = code
        
        except SyntaxError:
            enhanced_code = code
        
        return enhanced_code, transformations

    def _optimize_with_builtins(self, code: str) -> tuple[str, List[Dict]]:
        """Optimise avec les fonctions built-in."""
        transformations = []
        lines = code.splitlines()
        modified_lines = []
        
        for i, line in enumerate(lines):
            original_line = line
            
            # range(len(iterable)) → enumerate(iterable)
            if 'range(len(' in line and 'for ' in line:
                # Pattern simplifié - une vraie implémentation serait plus sophistiquée
                range_len_pattern = re.compile(r'for\s+(\w+)\s+in\s+range\(len\((\w+)\)\):')
                match = range_len_pattern.search(line)
                if match:
                    var_name = match.group(1)
                    iterable = match.group(2)
                    new_line = line.replace(
                        f'for {var_name} in range(len({iterable})):',
                        f'for {var_name}, item in enumerate({iterable}):'
                    )
                    line = new_line
                    transformations.append({
                        'type': 'builtin_optimization',
                        'line': i + 1,
                        'description': 'Remplacement range(len()) par enumerate()',
                        'before': f'for {var_name} in range(len({iterable})):',
                        'after': f'for {var_name}, item in enumerate({iterable}):'
                    })
            
            # Optimisation des any/all
            if 'for ' in line and ('return True' in code or 'return False' in code):
                # Cette optimisation nécessiterait une analyse plus poussée du contexte
                pass
            
            modified_lines.append(line)
        
        return '\n'.join(modified_lines), transformations

    def _modernize_pathlib(self, code: str) -> tuple[str, List[Dict]]:
        """Modernise l'usage des chemins avec pathlib."""
        transformations = []
        lines = code.splitlines()
        modified_lines = []
        
        has_os_path = 'os.path' in code
        pathlib_imported = 'from pathlib import' in code or 'import pathlib' in code
        
        for i, line in enumerate(lines):
            original_line = line
            
            # os.path.join() → Path() / operator
            if 'os.path.join(' in line and not pathlib_imported:
                # Ajouter l'import pathlib en haut du fichier si pas déjà présent
                if i == 0 and not pathlib_imported:
                    modified_lines.insert(0, "from pathlib import Path")
                    pathlib_imported = True
                
                join_pattern = re.compile(r'os\.path\.join\(([^)]+)\)')
                match = join_pattern.search(line)
                if match:
                    args = match.group(1)
                    # Simplification - une vraie implémentation parserait correctement les arguments
                    new_line = line.replace(match.group(0), f'Path({args.split(",")[0].strip()}) / {" / ".join(arg.strip() for arg in args.split(",")[1:])}')
                    line = new_line
                    transformations.append({
                        'type': 'pathlib_modernization',
                        'line': i + 1,
                        'description': 'Conversion os.path.join vers pathlib',
                        'before': match.group(0),
                        'after': f'Path(...) / ...'
                    })
            
            modified_lines.append(line)
        
        return '\n'.join(modified_lines), transformations

    def _improve_context_managers(self, code: str) -> tuple[str, List[Dict]]:
        """Améliore l'usage des context managers."""
        transformations = []
        lines = code.splitlines()
        
        # Détection des open() sans with
        for i, line in enumerate(lines):
            if re.search(r'(\w+)\s*=\s*open\s*\(', line) and 'with ' not in line:
                transformations.append({
                    'type': 'context_manager',
                    'line': i + 1,
                    'description': 'Suggérer l\'usage de "with open()" au lieu d\'open() direct',
                    'suggestion': 'Utiliser "with open(...) as f:" pour une gestion automatique des ressources'
                })
        
        return code, transformations

    def _add_basic_type_hints(self, code: str) -> tuple[str, List[Dict]]:
        """Ajoute des type hints basiques."""
        transformations = []
        
        try:
            tree = ast.parse(code)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    # Vérifier si la fonction a déjà des annotations
                    has_annotations = (
                        any(arg.annotation for arg in node.args.args) or
                        node.returns is not None
                    )
                    
                    if not has_annotations:
                        transformations.append({
                            'type': 'type_hints',
                            'line': getattr(node, 'lineno', 0),
                            'description': f'Suggérer des type hints pour la fonction "{node.name}"',
                            'suggestion': 'Ajouter des annotations de type pour améliorer la lisibilité'
                        })
        
        except SyntaxError:
            pass
        
        return code, transformations

    def _apply_walrus_operator(self, code: str) -> tuple[str, List[Dict]]:
        """Applique l'opérateur walrus (:=) quand approprié."""
        transformations = []
        
        # Pattern: if len(something) > 0: → if (n := len(something)) > 0:
        # Cette transformation est complexe et nécessite une analyse AST approfondie
        # Pour l'instant, on suggère seulement
        
        lines = code.splitlines()
        for i, line in enumerate(lines):
            if re.search(r'if\s+len\s*\([^)]+\)\s*[><=!]', line):
                transformations.append({
                    'type': 'walrus_operator',
                    'line': i + 1,
                    'description': 'Opportunité d\'utiliser l\'opérateur walrus (:=)',
                    'suggestion': 'Considérer l\'usage de := pour éviter la double évaluation'
                })
        
        return code, transformations

    def _calculate_complexity(self, tree: ast.AST) -> int:
        """Calcule la complexité cyclomatique basique."""
        complexity = 0
        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
                complexity += 1
        return complexity

    def _calculate_readability(self, tree: ast.AST, code: str) -> int:
        """Calcule un score de lisibilité basique."""
        score = 100
        
        # Pénalités pour la lisibilité
        lines = code.splitlines()
        long_lines = sum(1 for line in lines if len(line) > 100)
        score -= long_lines * 2
        
        # Bonus pour les bonnes pratiques
        if 'def ' in code:
            score += 5
        if 'class ' in code:
            score += 5
        if '"""' in code or "'''" in code:  # docstrings
            score += 10
        
        return max(0, min(100, score))

    def _calculate_improvement_score(self, original: Dict, enhanced: Dict) -> float:
        """Calcule le score d'amélioration."""
        return enhanced["quality_score"] - original["quality_score"]


    def _enhance_error_handling(self, code: str) -> tuple[str, List[Dict]]:
        """Améliore la gestion d'erreurs."""
        transformations = []
        lines = code.splitlines()
        modified_lines = []
        
        for i, line in enumerate(lines):
            original_line = line
            
            # Détection de try/except trop génériques
            if 'except:' in line or 'except Exception:' in line:
                transformations.append({
                    'type': 'error_handling',
                    'line': i + 1,
                    'description': 'Exception trop générique détectée',
                    'suggestion': 'Spécifier le type d\'exception (ValueError, TypeError, etc.)',
                    'before': line.strip(),
                    'after': 'except SpecificException as e:'
                })
            
            # Amélioration des assertions
            if line.strip().startswith('assert ') and ',' not in line:
                enhanced_line = line.replace('assert ', 'assert ', 1)
                if enhanced_line == line:  # Pas de message d'erreur
                    assertion_content = line.split('assert ')[1].strip()
                    new_line = line.replace(
                        f'assert {assertion_content}',
                        f'assert {assertion_content}, "Assertion failed: {assertion_content}"'
                    )
                    line = new_line
                    transformations.append({
                        'type': 'assertion_improvement',
                        'line': i + 1,
                        'description': 'Ajout de message d\'erreur à l\'assertion',
                        'before': original_line.strip(),
                        'after': new_line.strip()
                    })
            
            modified_lines.append(line)
        
        return '\n'.join(modified_lines), transformations

    def _optimize_data_structures(self, code: str) -> tuple[str, List[Dict]]:
        """Optimise l'usage des structures de données."""
        transformations = []
        lines = code.splitlines()
        modified_lines = []
        
        for i, line in enumerate(lines):
            original_line = line
            
            # Liste → set pour membership testing
            if ' in [' in line and not any(op in line for op in ['append', 'insert', 'remove']):
                # Pattern: if item in [val1, val2, val3]
                in_list_pattern = re.compile(r'(\w+)\s+in\s+\[([^\]]+)\]')
                match = in_list_pattern.search(line)
                if match and ',' in match.group(2):  # Plus d'un élément
                    var_name = match.group(1)
                    list_content = match.group(2)
                    new_line = line.replace(
                        f'{var_name} in [{list_content}]',
                        f'{var_name} in {{{list_content}}}'
                    )
                    line = new_line
                    transformations.append({
                        'type': 'data_structure_optimization',
                        'line': i + 1,
                        'description': 'Conversion liste → set pour test d\'appartenance',
                        'before': f'{var_name} in [{list_content}]',
                        'after': f'{var_name} in {{{list_content}}}',
                        'performance_gain': 'O(n) → O(1) pour membership testing'
                    })
            
            # Détection des dictionnaires avec get() répétitifs
            if '.get(' in line and 'defaultdict' not in code:
                get_count = code.count('.get(')
                if get_count > 3:
                    transformations.append({
                        'type': 'data_structure_optimization',
                        'line': i + 1,
                        'description': f'Multiples .get() détectés ({get_count})',
                        'suggestion': 'Considérer collections.defaultdict pour de meilleures performances',
                        'example': 'from collections import defaultdict; d = defaultdict(list)'
                    })
            
            modified_lines.append(line)
        
        return '\n'.join(modified_lines), transformations

    def _modernize_boolean_operations(self, code: str) -> tuple[str, List[Dict]]:
        """Modernise les opérations booléennes."""
        transformations = []
        lines = code.splitlines()
        modified_lines = []
        
        for i, line in enumerate(lines):
            original_line = line
            
            # if len(sequence) > 0: → if sequence:
            len_check_pattern = re.compile(r'if\s+len\s*\(([^)]+)\)\s*[>!=]+\s*0\s*:')
            match = len_check_pattern.search(line)
            if match:
                sequence = match.group(1)
                new_line = line.replace(match.group(0), f'if {sequence}:')
                line = new_line
                transformations.append({
                    'type': 'boolean_modernization',
                    'line': i + 1,
                    'description': 'Simplification test de longueur',
                    'before': match.group(0).rstrip(':') + ':',
                    'after': f'if {sequence}:',
                    'reason': 'Plus pythonique et plus lisible'
                })
            
            # if variable == True: → if variable:
            explicit_bool_pattern = re.compile(r'if\s+(\w+)\s*==\s*True\s*:')
            match = explicit_bool_pattern.search(line)
            if match:
                var_name = match.group(1)
                new_line = line.replace(match.group(0), f'if {var_name}:')
                line = new_line
                transformations.append({
                    'type': 'boolean_modernization',
                    'line': i + 1,
                    'description': 'Simplification comparaison booléenne',
                    'before': f'if {var_name} == True:',
                    'after': f'if {var_name}:',
                    'reason': 'Comparaison explicite avec True/False non recommandée'
                })
            
            # if variable == False: → if not variable:
            false_pattern = re.compile(r'if\s+(\w+)\s*==\s*False\s*:')
            match = false_pattern.search(line)
            if match:
                var_name = match.group(1)
                new_line = line.replace(match.group(0), f'if not {var_name}:')
                line = new_line
                transformations.append({
                    'type': 'boolean_modernization',
                    'line': i + 1,
                    'description': 'Simplification comparaison booléenne négative',
                    'before': f'if {var_name} == False:',
                    'after': f'if not {var_name}:',
                    'reason': 'Plus idiomatique en Python'
                })
            
            modified_lines.append(line)
        
        return '\n'.join(modified_lines), transformations

    def _optimize_loops_advanced(self, code: str) -> tuple[str, List[Dict]]:
        """Optimisations avancées de boucles."""
        transformations = []
        
        try:
            tree = ast.parse(code)
            transformer = AdvancedLoopOptimizer()
            new_tree = transformer.visit(tree)
            ast.fix_missing_locations(new_tree)
            
            try:
                enhanced_code = ast.unparse(new_tree)
                transformations.extend(transformer.transformations)
            except AttributeError:
                enhanced_code = code
                transformations.extend(transformer.transformations)
        
        except SyntaxError:
            enhanced_code = code
        
        return enhanced_code, transformations

    def _add_advanced_type_hints(self, code: str) -> tuple[str, List[Dict]]:
        """Ajoute des type hints avancés basés sur l'analyse du code."""
        transformations = []
        
        try:
            tree = ast.parse(code)
            type_analyzer = TypeHintAnalyzer()
            type_suggestions = type_analyzer.analyze(tree)
            
            for suggestion in type_suggestions:
                transformations.append({
                    'type': 'advanced_type_hints',
                    'line': suggestion['line'],
                    'description': f'Type hint suggéré pour {suggestion["element"]}',
                    'suggestion': suggestion['hint'],
                    'confidence': suggestion['confidence'],
                    'reasoning': suggestion['reasoning']
                })
        
        except SyntaxError:
            pass
        
        return code, transformations

    def _apply_modern_python_features(self, code: str) -> tuple[str, List[Dict]]:
        """Applique les fonctionnalités Python modernes."""
        transformations = []
        lines = code.splitlines()
        modified_lines = []
        
        for i, line in enumerate(lines):
            original_line = line
            
            # Pattern pour walrus operator: if (n := len(items)) > 5:
            if_len_pattern = re.compile(r'if\s+len\s*\(([^)]+)\)\s*([><=!]+)\s*(\d+)\s*:')
            match = if_len_pattern.search(line)
            if match:
                iterable = match.group(1)
                operator = match.group(2)
                value = match.group(3)
                new_line = line.replace(
                    match.group(0),
                    f'if (n := len({iterable})) {operator} {value}:'
                )
                line = new_line
                transformations.append({
                    'type': 'walrus_operator',
                    'line': i + 1,
                    'description': 'Application opérateur walrus (:=)',
                    'before': match.group(0),
                    'after': f'if (n := len({iterable})) {operator} {value}:',
                    'benefit': 'Évite la double évaluation de len()',
                    'python_version': '3.8+'
                })
            
            # Pattern pour match/case (très basique)
            if 'if ' in line and ' == ' in line and 'elif' in code[code.find(line):code.find(line) + 200]:
                # Suggérer match/case pour les chaînes de if/elif avec égalité
                transformations.append({
                    'type': 'match_statement',
                    'line': i + 1,
                    'description': 'Chaîne if/elif convertible en match/case',
                    'suggestion': 'Considérer match/case pour une meilleure lisibilité',
                    'python_version': '3.10+',
                    'example': 'match variable:\n    case "value1":\n        ...\n    case "value2":\n        ...'
                })
            
            modified_lines.append(line)
        
        return '\n'.join(modified_lines), transformations

    def _enhance_function_definitions(self, code: str) -> tuple[str, List[Dict]]:
        """Améliore les définitions de fonctions."""
        transformations = []
        
        try:
            tree = ast.parse(code)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    # Vérifier les arguments par défaut mutables
                    for default in node.args.defaults:
                        if isinstance(default, (ast.List, ast.Dict, ast.Set)):
                            transformations.append({
                                'type': 'mutable_default_argument',
                                'line': getattr(node, 'lineno', 0),
                                'description': f'Argument par défaut mutable dans "{node.name}"',
                                'issue': 'Les arguments par défaut mutables sont partagés entre les appels',
                                'solution': 'Utiliser None et créer l\'objet dans la fonction',
                                'example': 'def func(arg=None):\n    if arg is None:\n        arg = []'
                            })
                    
                    # Fonction trop longue
                    if len(node.body) > 20:
                        transformations.append({
                            'type': 'function_length',
                            'line': getattr(node, 'lineno', 0),
                            'description': f'Fonction "{node.name}" très longue ({len(node.body)} statements)',
                            'suggestion': 'Considérer la division en fonctions plus petites',
                            'maintainability': 'Les fonctions courtes sont plus faciles à tester et maintenir'
                        })
                    
                    # Trop de paramètres
                    total_args = len(node.args.args) + len(node.args.posonlyargs) + len(node.args.kwonlyargs)
                    if total_args > 5:
                        transformations.append({
                            'type': 'too_many_parameters',
                            'line': getattr(node, 'lineno', 0),
                            'description': f'Fonction "{node.name}" a beaucoup de paramètres ({total_args})',
                            'suggestion': 'Considérer l\'utilisation d\'une classe ou de **kwargs',
                            'refactoring': 'Grouper les paramètres liés en structures de données'
                        })
        
        except SyntaxError:
            pass
        
        return code, transformations


class AdvancedLoopOptimizer(ast.NodeTransformer):
    """Optimiseur avancé de boucles."""
    
    def __init__(self):
        self.transformations = []
    
    def visit_For(self, node):
        """Visite les boucles for pour optimisations avancées."""
        
        # Pattern 1: Boucle d'accumulation simple
        if (len(node.body) == 1 and
            isinstance(node.body[0], ast.Expr) and
            isinstance(node.body[0].value, ast.Call) and
            isinstance(node.body[0].value.func, ast.Attribute) and
            node.body[0].value.func.attr == 'append'):
            
            self.transformations.append({
                'type': 'list_comprehension_opportunity',
                'line': getattr(node, 'lineno', 0),
                'description': 'Boucle simple convertible en list comprehension',
                'performance_benefit': 'Plus rapide et plus lisible',
                'example': '[expression for item in iterable]'
            })
        
        # Pattern 2: Boucle avec condition (filtre)
        elif (len(node.body) == 1 and
              isinstance(node.body[0], ast.If) and
              len(node.body[0].body) == 1 and
              isinstance(node.body[0].body[0], ast.Expr)):
            
            self.transformations.append({
                'type': 'filtered_comprehension_opportunity',
                'line': getattr(node, 'lineno', 0),
                'description': 'Boucle avec condition convertible en comprehension filtrée',
                'example': '[expression for item in iterable if condition]'
            })
        
        # Pattern 3: Recherche booléenne
        elif self._is_boolean_search_loop(node):
            self.transformations.append({
                'type': 'any_all_optimization',
                'line': getattr(node, 'lineno', 0),
                'description': 'Boucle de recherche booléenne optimisable avec any()/all()',
                'performance_benefit': 'Court-circuit automatique, plus lisible',
                'example': 'any(condition(item) for item in iterable)'
            })
        
        return self.generic_visit(node)
    
    def _is_boolean_search_loop(self, node):
        """Détecte si une boucle fait une recherche booléenne."""
        for stmt in node.body:
            if isinstance(stmt, ast.If):
                for if_stmt in stmt.body:
                    if isinstance(if_stmt, ast.Return):
                        if (isinstance(if_stmt.value, ast.Constant) and
                            if_stmt.value.value in [True, False]):
                            return True
        return False


class TypeHintAnalyzer:
    """Analyseur pour suggérer des type hints basés sur l'usage."""
    
    def analyze(self, tree: ast.AST) -> List[Dict]:
        """Analyse le code pour suggérer des type hints."""
        suggestions = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Analyser les paramètres
                for arg in node.args.args:
                    if not arg.annotation:
                        hint_suggestion = self._infer_parameter_type(node, arg.arg)
                        if hint_suggestion:
                            suggestions.append({
                                'element': f'parameter {arg.arg} in {node.name}',
                                'line': getattr(node, 'lineno', 0),
                                'hint': hint_suggestion['type'],
                                'confidence': hint_suggestion['confidence'],
                                'reasoning': hint_suggestion['reasoning']
                            })
                
                # Analyser le retour
                if not node.returns:
                    return_hint = self._infer_return_type(node)
                    if return_hint:
                        suggestions.append({
                            'element': f'return type of {node.name}',
                            'line': getattr(node, 'lineno', 0),
                            'hint': return_hint['type'],
                            'confidence': return_hint['confidence'],
                            'reasoning': return_hint['reasoning']
                        })
        
        return suggestions
    
    def _infer_parameter_type(self, func_node: ast.FunctionDef, param_name: str) -> Optional[Dict]:
        """Infère le type d'un paramètre basé sur son usage."""
        usages = []
        
        for node in ast.walk(func_node):
            if isinstance(node, ast.Name) and node.id == param_name:
                parent = getattr(node, 'parent', None)
                if isinstance(parent, ast.Call) and parent.func == node:
                    usages.append('callable')
                elif isinstance(parent, ast.Subscript) and parent.value == node:
                    usages.append('subscriptable')
                elif isinstance(parent, ast.Attribute) and parent.value == node:
                    if parent.attr in ['append', 'extend', 'insert']:
                        usages.append('list')
                    elif parent.attr in ['add', 'remove', 'discard']:
                        usages.append('set')
                    elif parent.attr in ['keys', 'values', 'items', 'get']:
                        usages.append('dict')
                    elif parent.attr in ['split', 'strip', 'replace', 'lower', 'upper']:
                        usages.append('str')
        
        if usages:
            most_common = max(set(usages), key=usages.count)
            type_mapping = {
                'list': 'List[Any]',
                'dict': 'Dict[Any, Any]',
                'set': 'Set[Any]',
                'str': 'str',
                'callable': 'Callable[..., Any]',
                'subscriptable': 'Union[List, Dict, str]'
            }
            
            if most_common in type_mapping:
                return {
                    'type': type_mapping[most_common],
                    'confidence': 0.7 if usages.count(most_common) > 1 else 0.5,
                    'reasoning': f'Inferred from usage pattern: {most_common}'
                }
        
        return None
    
    def _infer_return_type(self, func_node: ast.FunctionDef) -> Optional[Dict]:
        """Infère le type de retour d'une fonction."""
        returns = []
        
        for node in ast.walk(func_node):
            if isinstance(node, ast.Return) and node.value:
                if isinstance(node.value, ast.Constant):
                    if isinstance(node.value.value, bool):
                        returns.append('bool')
                    elif isinstance(node.value.value, int):
                        returns.append('int')
                    elif isinstance(node.value.value, str):
                        returns.append('str')
                    elif node.value.value is None:
                        returns.append('None')
                elif isinstance(node.value, ast.List):
                    returns.append('List')
                elif isinstance(node.value, ast.Dict):
                    returns.append('Dict')
                elif isinstance(node.value, ast.Set):
                    returns.append('Set')
        
        if returns:
            unique_returns = list(set(returns))
            if len(unique_returns) == 1:
                return_type = unique_returns[0]
                if return_type == 'List':
                    return_type = 'List[Any]'
                elif return_type == 'Dict':
                    return_type = 'Dict[Any, Any]'
                elif return_type == 'Set':
                    return_type = 'Set[Any]'
                
                return {
                    'type': return_type,
                    'confidence': 0.8,
                    'reasoning': f'Inferred from return statements'
                }
            elif len(unique_returns) > 1:
                if 'None' in unique_returns:
                    other_types = [t for t in unique_returns if t != 'None']
                    if len(other_types) == 1:
                        return {
                            'type': f'Optional[{other_types[0]}]',
                            'confidence': 0.7,
                            'reasoning': 'Function returns value or None'
                        }
                
                return {
                    'type': f'Union[{", ".join(unique_returns)}]',
                    'confidence': 0.6,
                    'reasoning': 'Multiple return types detected'
                }
        
        return None