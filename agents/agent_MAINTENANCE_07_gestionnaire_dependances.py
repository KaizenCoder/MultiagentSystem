import ast
import sys
import subprocess
import importlib.util
from collections import defaultdict
from core.agent_factory_architecture import Agent, Task, Result
import logging

class AgentMAINTENANCE07GestionnaireDependances(Agent):
    """
    Agent chargé de gérer les dépendances Python :
    - Détecte les imports manquants ou inutilisés
    - Vérifie la disponibilité des modules
    - Suggère des alternatives pour les dépendances obsolètes
    - Organise et optimise les imports
    """
    
    def __init__(self, **kwargs):
        super().__init__(agent_type="dependency_manager", **kwargs)
        # ✅ MIGRATION SYSTÈME LOGGING UNIFIÉ
        try:
            from core.manager import LoggingManager
            logging_manager = LoggingManager()
            self.logger = logging_manager.get_logger(
                config_name="maintenance",
                custom_config={
                    "logger_name": f"nextgen.maintenance.gestionnaire_dependances.{self.id}",
                    "log_dir": "logs/maintenance/gestionnaire",
                    "metadata": {
                        "agent_type": "MAINTENANCE_07_gestionnaire_dependances",
                        "agent_role": "gestionnaire_dependances",
                        "system": "nextgeneration"
                    }
                }
            )
        except ImportError:
            # Fallback en cas d'indisponibilité du LoggingManager
            self.logger = logging.getLogger(self.__class__.__name__)
        
        self.stdlib_modules = {
            'ast', 'asyncio', 'os', 'sys', 'json', 'datetime', 'pathlib', 're', 
            'tempfile', 'subprocess', 'importlib', 'collections', 'logging',
            'typing', 'functools', 'itertools', 'math', 'random', 'time', 'uuid',
            'abc'
        }
        
        self.alternatives = {
            'astor': 'ast.unparse (Python 3.9+)',
            'imp': 'importlib',
            'optparse': 'argparse',
            'urllib2': 'urllib.request',
            'ConfigParser': 'configparser'
        }

    async def startup(self):
        await super().startup()
        self.logger.info("Gestionnaire de dépendances prêt.")

    async def execute_task(self, task: Task) -> Result:
        if task.type != "manage_dependencies":
            return Result(success=False, error="Type de tâche non supporté.")

        code = task.params.get("code_content")
        file_path = task.params.get("file_path", "unknown_file")
        if not code:
            return Result(success=False, error="Code non fourni dans les paramètres de la tâche.")

        self.logger.info(f"Analyse des dépendances pour : {file_path}")

        try:
            tree = ast.parse(code)
            analysis = self._analyze_dependencies(tree)
            
            optimized_code, applied = self._optimize_imports(code, analysis)
            analysis["optimization_applied"] = applied
            
            report = {
                "file_path": file_path,
                "imports_found": analysis["imports"],
                "missing_modules": analysis["missing"],
                "unused_imports": analysis["unused"],
                "obsolete_modules": analysis["obsolete"],
                "suggestions": analysis["suggestions"],
                "optimization_applied": analysis["optimization_applied"]
            }

            self.logger.info(f"Analyse des dépendances terminée pour {file_path}")
            
            return Result(success=True, data={
                "adapted_content": optimized_code,
                "description": f"Analyse des dépendances effectuée. Optimisations d'imports appliquées: {applied}.",
                "dependency_report": report
            })

        except SyntaxError as e:
            self.logger.error(f"Erreur de syntaxe lors de l'analyse de {file_path}: {e}")
            return Result(success=False, error=f"SyntaxError: {e}")
        except Exception as e:
            self.logger.error(f"Erreur inattendue lors de l'analyse de {file_path}: {e}")
            return Result(success=False, error=str(e))

    def _analyze_dependencies(self, tree: ast.AST) -> dict:
        analysis = {
            "imports": [], "missing": [], "unused": [],
            "obsolete": [], "suggestions": [],
        }
        
        imports_info = self._extract_imports(tree)
        analysis["imports"] = imports_info
        used_names = self._extract_used_names(tree)
        
        for imp in imports_info:
            if not imp.get('module'): continue
            module_name = imp["module"].split('.')[0]
            if not self._is_module_available(module_name):
                analysis["missing"].append(module_name)
                analysis["suggestions"].append(f"Module '{module_name}' non trouvé.")
            
            if module_name in self.alternatives:
                analysis["obsolete"].append({"module": module_name, "alternative": self.alternatives[module_name]})
                analysis["suggestions"].append(f"Remplacer '{module_name}' par '{self.alternatives[module_name]}'.")
        
        all_imported_names = {item for imp in imports_info for item in self._get_names_from_import(imp)}
        truly_used_imports = all_imported_names.intersection(used_names)

        for imp in imports_info:
            imported_names_for_this_node = self._get_names_from_import(imp)
            if not any(name in truly_used_imports for name in imported_names_for_this_node):
                analysis["unused"].append(imp)
        return analysis

    def _get_names_from_import(self, imp_node: dict) -> set:
        names = set()
        if imp_node['type'] == 'import':
            names.add(imp_node['asname'] or imp_node['module'])
        elif imp_node['type'] == 'from_import':
            for name, asname in imp_node['items']:
                names.add(asname or name)
        return names

    def _extract_imports(self, tree: ast.AST) -> list:
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append({"type": "import", "module": alias.name, "asname": alias.asname, "line": node.lineno})
            elif isinstance(node, ast.ImportFrom) and node.module is not None:
                imports.append({"type": "from_import", "module": node.module, "items": [(alias.name, alias.asname) for alias in node.names], "level": node.level, "line": node.lineno})
        return imports

    def _extract_used_names(self, tree: ast.AST) -> set:
        used_names = set()
        class NameCollector(ast.NodeVisitor):
            def visit_Name(self, node):
                if isinstance(node.ctx, ast.Load):
                    used_names.add(node.id)
            def visit_Import(self, node): pass
            def visit_ImportFrom(self, node): pass
        NameCollector().visit(tree)
        return used_names

    def _is_module_available(self, module_name: str) -> bool:
        if not module_name: return False
        try:
            if module_name in self.stdlib_modules:
                return True
            spec = importlib.util.find_spec(module_name)
            return spec is not None
        except (ImportError, ValueError, ModuleNotFoundError):
            return False

    def _optimize_imports(self, code: str, analysis: dict) -> (str, bool):
        unused_import_lines = {imp['line'] for imp in analysis.get('unused', [])}
        if not unused_import_lines:
            return code, False

        used_import_nodes = [imp for imp in analysis.get('imports', []) if imp['line'] not in unused_import_lines]
        all_import_lines = {imp['line'] for imp in analysis.get('imports', [])}
        
        lines = code.split('\n')
        
        first_code_line_index = 0
        in_docstring = False
        for i, line in enumerate(lines):
            stripped = line.strip()
            if '"""' in stripped or "'''" in stripped:
                if stripped.count('"""') == 1 or stripped.count("'''") == 1:
                    in_docstring = not in_docstring
            if not stripped or stripped.startswith('#') or in_docstring or (i + 1) in all_import_lines:
                continue
            
            first_code_line_index = i
            break
        else: 
            first_code_line_index = len(lines)

        header_and_imports = lines[:first_code_line_index]
        body = lines[first_code_line_index:]

        header_without_imports = [line for i, line in enumerate(header_and_imports) if (i + 1) not in all_import_lines]
        body_without_imports = [line for i, line in enumerate(body, start=first_code_line_index) if (i + 1) not in all_import_lines]

        organized_imports_str = self._organize_imports_nodes(used_import_nodes)
        
        final_header = '\n'.join(header_without_imports)
        final_body = '\n'.join(body_without_imports)

        new_code = ""
        if final_header:
            new_code += final_header.strip() + "\n"
        if organized_imports_str:
            new_code += organized_imports_str + "\n\n"
        
        new_code += final_body.strip()
        
        return new_code.strip(), new_code.strip() != code.strip()

    def _organize_imports_nodes(self, imports: list) -> str:
        stdlib_imports, third_party_imports, local_imports = set(), set(), set()
        
        for imp in imports:
            line = self._reconstruct_import_line(imp)
            if not imp.get('module'): continue
            module_root = imp['module'].split('.')[0]
            if imp.get('level', 0) > 0 or "core" in imp['module'] or imp['module'].startswith('agents'):
                local_imports.add(line)
            elif module_root in self.stdlib_modules:
                stdlib_imports.add(line)
            else:
                third_party_imports.add(line)

        import_groups = []
        if stdlib_imports:
            import_groups.append('\n'.join(sorted(list(stdlib_imports))))
        if third_party_imports:
            import_groups.append('\n'.join(sorted(list(third_party_imports))))
        if local_imports:
            import_groups.append('\n'.join(sorted(list(local_imports))))
            
        return '\n\n'.join(filter(None, import_groups))

    def _reconstruct_import_line(self, imp_node: dict) -> str:
        if imp_node['type'] == 'import':
            if imp_node['asname']:
                return f"import {imp_node['module']} as {imp_node['asname']}"
            return f"import {imp_node['module']}"
        else:
            items_str = ', '.join([f"{name} as {asname}" if asname else name for name, asname in imp_node['items']])
            return f"from {'.' * imp_node['level']}{imp_node['module']} import {items_str}"

    # --- MÉTHODES ABSTRAITES MANQUANTES ---
    def get_capabilities(self) -> list[str]:
        """Retourne les capacités de l'agent."""
        return ["manage_dependencies"]

    async def health_check(self) -> dict[str, any]:
        """Effectue un contrôle de santé de l'agent."""
        return {"status": "healthy", "agent_id": self.agent_id}

    async def shutdown(self):
        """Arrête l'agent."""
        self.logger.info("Gestionnaire de dépendances éteint.")

def create_agent_MAINTENANCE_07_gestionnaire_dependances(**config) -> "AgentMAINTENANCE07GestionnaireDependances":
    return AgentMAINTENANCE07GestionnaireDependances(**config)
    # ✅ MÉTHODES STANDARDISÉES DE RAPPORT

    def _calculate_report_score(self, metrics: Dict[str, Any]) -> int:
        """Calcule le score global du rapport basé sur les métriques."""
        score = 0
        issues_critiques = []
        
        # Logique de scoring spécifique à l'agent
        # À adapter selon le type d'agent
        
        return score
    
    def _assess_conformity(self, score: int) -> str:
        """Évalue la conformité basée sur le score."""
        if score >= 90:
            return "✅ CONFORME - OPTIMAL"
        elif score >= 70:
            return "✅ CONFORME - ACCEPTABLE"
        else:
            return "❌ NON CONFORME - CRITIQUE"
    
    def _get_quality_level(self, score: int) -> str:
        """Détermine le niveau de qualité."""
        if score >= 90:
            return "OPTIMAL"
        elif score >= 70:
            return "ACCEPTABLE"
        else:
            return "CRITIQUE"
    
    def _generate_recommendations(self, metrics: Dict[str, Any], issues: List[str]) -> List[str]:
        """Génère les recommandations basées sur l'analyse."""
        recommendations = []
        
        # Logique de génération de recommandations
        # À adapter selon le type d'agent
        
        return recommendations
    
    def _generate_standard_report(self, context: Dict, metrics: Dict, timestamp) -> Dict[str, Any]:
        """Génère un rapport selon le format standard de l'agent 06."""
        
        score = self._calculate_report_score(metrics)
        conformity = self._assess_conformity(score)
        quality_level = self._get_quality_level(score)
        
        agent_filename = Path(__file__).name
        
        # Issues critiques (à personnaliser selon l'agent)
        issues_critiques = []
        
        return {
            'agent_id': getattr(self, 'agent_id', 'unknown'),
            'agent_file_name': agent_filename,
            'type_rapport': 'standard',  # À personnaliser
            'timestamp': timestamp.isoformat(),
            'specialisation': 'Agent Spécialisé',  # À personnaliser
            'score_global': score,
            'niveau_qualite': quality_level,
            'conformite': conformity,
            'signature_cryptographique': 'N/A (Fonctionnalité non implémentée pour cet agent)',
            'issues_critiques_identifies': len(issues_critiques),
            'architecture': {
                'description': "Description de l'architecture de l'agent",
                'statut_operationnel': f"Système {getattr(self, 'agent_id', 'unknown')} opérationnel.",
                'confirmation_specialisation': f"{getattr(self, 'agent_id', 'unknown')} confirmé comme spécialiste.",
                'objectifs_principaux': [
                    "Objectif principal 1",
                    "Objectif principal 2",
                    "Objectif principal 3"
                ],
                'technologies_cles': ["Technologie 1", "Technologie 2"]
            },
            'recommandations': self._generate_recommendations(metrics, issues_critiques),
            'issues_critiques_details': issues_critiques if issues_critiques else [
                "Aucun issue critique majeur détecté. Le système fonctionne dans les paramètres attendus."
            ],
            'details_techniques': {
                'strategie': "Stratégie technique de l'agent",
                'composants_actifs': [],
                'metriques_collectees': metrics
            },
            'metriques_detaillees': {
                'score_global': {'actuel': score, 'cible': 100},
                'conformite_pourcentage': {'actuel': score, 'cible': 100, 'unite': '%'}
            },
            'impact_business': {
                'criticite': 'MOYENNE' if score >= 70 else 'HAUTE',
                'domaines_impactes': [],
                'actions_requises': []
            }
        }


    def _generate_markdown_report(self, rapport_json: Dict, context: Dict, timestamp) -> str:
        """Génère un rapport Markdown selon le format standard."""
        
        agent_name = rapport_json.get('agent_id', 'Agent Inconnu')
        type_rapport = rapport_json.get('type_rapport', 'standard')
        score = rapport_json.get('score_global', 0)
        quality = rapport_json.get('niveau_qualite', 'UNKNOWN')
        conformity = rapport_json.get('conformite', 'NON ÉVALUÉ')
        
        markdown_content = f"""# 📊 RAPPORT STRATÉGIQUE : {agent_name.upper()}

## 🎯 RÉSUMÉ EXÉCUTIF

**Agent :** {agent_name}  
**Type de Rapport :** {type_rapport}  
**Date de Génération :** {timestamp.strftime('%Y-%m-%d %H:%M:%S')}  
**Score Global :** {score}/100  
**Niveau de Qualité :** {quality}  
**Conformité :** {conformity}  

## 📈 ANALYSE GLOBALE

### Score de Performance
- **Score Actuel :** {score}/100
- **Objectif :** 100/100
- **Statut :** {'🟢 ACCEPTABLE' if score >= 70 else '🔴 CRITIQUE'}

### Architecture
{rapport_json.get('architecture', {}).get('description', 'Description non disponible')}

**Objectifs Principaux :**
"""
        
        # Ajouter les objectifs
        for obj in rapport_json.get('architecture', {}).get('objectifs_principaux', []):
            markdown_content += f"- {obj}\n"
        
        markdown_content += f"""
**Technologies Clés :**
"""
        
        # Ajouter les technologies
        for tech in rapport_json.get('architecture', {}).get('technologies_cles', []):
            markdown_content += f"- {tech}\n"
        
        markdown_content += f"""

## 🔍 RECOMMANDATIONS

"""
        
        # Ajouter les recommandations
        for reco in rapport_json.get('recommandations', []):
            markdown_content += f"- {reco}\n"
        
        markdown_content += f"""

## ⚠️ ISSUES CRITIQUES

"""
        
        # Ajouter les issues critiques
        for issue in rapport_json.get('issues_critiques_details', []):
            markdown_content += f"- {issue}\n"
        
        markdown_content += f"""

## 📊 MÉTRIQUES DÉTAILLÉES

### Performance Globale
- **Score Global :** {rapport_json.get('metriques_detaillees', {}).get('score_global', {}).get('actuel', 0)}/{rapport_json.get('metriques_detaillees', {}).get('score_global', {}).get('cible', 100)}
- **Conformité :** {rapport_json.get('metriques_detaillees', {}).get('conformite_pourcentage', {}).get('actuel', 0)}%

## 🎯 IMPACT BUSINESS

**Criticité :** {rapport_json.get('impact_business', {}).get('criticite', 'NON ÉVALUÉ')}

### Domaines Impactés
"""
        
        # Ajouter les domaines impactés
        for domaine in rapport_json.get('impact_business', {}).get('domaines_impactes', []):
            markdown_content += f"- {domaine}\n"
        
        markdown_content += f"""

### Actions Requises
"""
        
        # Ajouter les actions requises
        for action in rapport_json.get('impact_business', {}).get('actions_requises', []):
            markdown_content += f"- {action}\n"
        
        markdown_content += f"""

---
*Rapport généré automatiquement par {agent_name} - NextGeneration System*  
*Timestamp: {timestamp.isoformat()}*
"""
        
        return markdown_content

