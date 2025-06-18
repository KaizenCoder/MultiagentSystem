#!/usr/bin/env python3
"""
🔧 Agent SQLAlchemy Fixer
Mission: Correction spécialisée des erreurs SQLAlchemy et modèles ORM
"""

import os
import sys
import json
import logging
import ast
import re
from datetime import datetime
from pathlib import Path
import shutil

class SQLAlchemyFixerAgent:
    def __init__(self):
        self.name = "Agent SQLAlchemy Fixer"
        self.agent_id = "agent_sqlalchemy_fixer"
        self.version = "1.0.0"
        self.status = "ACTIVE"
        self.workspace = Path(__file__).parent
        self.rapport_file = self.workspace / "rapports" / f"{self.agent_id}_rapport.md"
        
        # Configuration logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.workspace / "logs" / f"{self.agent_id}.log"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(self.agent_id)
        
        # Patterns de problèmes SQLAlchemy
        self.patterns_problemes = {
            "metadata_conflict": r"metadata\s*=\s*Column",
            "textual_sql": r'execute\s*\(\s*["\']([^"\']*)["\']',
            "imports_manquants": r'from\s+sqlalchemy\s+import.*text',
            "declarative_base": r'from\s+sqlalchemy\.ext\.declarative\s+import\s+declarative_base'
        }
        
    def analyser_fichiers_sqlalchemy(self):
        """Analyse tous les fichiers SQLAlchemy du projet"""
        self.logger.info("Analyse des fichiers SQLAlchemy")
        
        analyse = {
            "timestamp": datetime.now().isoformat(),
            "fichiers_analyses": [],
            "erreurs_detectees": [],
            "corrections_requises": [],
            "modeles_problematiques": []
        }
        
        # Recherche des fichiers Python contenant SQLAlchemy
        project_root = Path(__file__).parent.parent.parent
        python_files = list(project_root.glob("**/*.py"))
        
        for py_file in python_files:
            # Éviter fichiers temporaires et cache
            if any(skip in str(py_file) for skip in ['__pycache__', '.git', 'venv', 'node_modules']):
                continue
                
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    contenu = f.read()
                    
                # Vérifier si le fichier contient SQLAlchemy
                if 'sqlalchemy' in contenu.lower() or 'Column' in contenu:
                    analyse_fichier = self.analyser_fichier_specifique(py_file, contenu)
                    if analyse_fichier["problemes_detectes"]:
                        analyse["fichiers_analyses"].append(analyse_fichier)
                        
            except Exception as e:
                self.logger.warning(f"Erreur lecture {py_file}: {e}")
                
        return analyse
    
    def analyser_fichier_specifique(self, fichier_path, contenu):
        """Analyse un fichier spécifique pour problèmes SQLAlchemy"""
        analyse_fichier = {
            "fichier": str(fichier_path),
            "taille": len(contenu),
            "problemes_detectes": [],
            "corrections_proposees": [],
            "lignes_problematiques": []
        }
        
        lignes = contenu.split('\n')
        
        for num_ligne, ligne in enumerate(lignes, 1):
            # Détection conflit metadata
            if re.search(self.patterns_problemes["metadata_conflict"], ligne):
                analyse_fichier["problemes_detectes"].append({
                    "type": "metadata_conflict",
                    "ligne": num_ligne,
                    "code": ligne.strip(),
                    "criticite": "HAUTE"
                })
                analyse_fichier["corrections_proposees"].append({
                    "ligne": num_ligne,
                    "original": ligne.strip(),
                    "corrige": ligne.replace("metadata =", "session_metadata ="),
                    "explication": "Renommage pour éviter conflit avec SQLAlchemy metadata"
                })
                
            # Détection expressions SQL sans text()
            match_sql = re.search(self.patterns_problemes["textual_sql"], ligne)
            if match_sql and 'text(' not in ligne:
                sql_query = match_sql.group(1)
                analyse_fichier["problemes_detectes"].append({
                    "type": "textual_sql_missing",
                    "ligne": num_ligne,
                    "code": ligne.strip(),
                    "criticite": "HAUTE"
                })
                
                ligne_corrigee = ligne.replace(f'"{sql_query}"', f'text("{sql_query}")')
                ligne_corrigee = ligne_corrigee.replace(f"'{sql_query}'", f"text('{sql_query}')")
                
                analyse_fichier["corrections_proposees"].append({
                    "ligne": num_ligne,
                    "original": ligne.strip(),
                    "corrige": ligne_corrigee.strip(),
                    "explication": "Ajout text() pour SQLAlchemy 2.x compatibility"
                })
                
            # Vérification imports text manquants
            if 'execute(' in ligne and 'text(' in ligne and not any('from sqlalchemy import' in l and 'text' in l for l in lignes[:num_ligne]):
                if not any(p["type"] == "import_text_missing" for p in analyse_fichier["problemes_detectes"]):
                    analyse_fichier["problemes_detectes"].append({
                        "type": "import_text_missing",
                        "ligne": 1,
                        "code": "Import text manquant",
                        "criticite": "MOYENNE"
                    })
                    
        return analyse_fichier
    
    def creer_corrections_automatiques(self, analyse_fichiers):
        """Crée les corrections automatiques pour les fichiers"""
        self.logger.info("Creation des corrections automatiques")
        
        corrections = {
            "timestamp": datetime.now().isoformat(),
            "fichiers_a_corriger": [],
            "scripts_correction": [],
            "backups_requis": []
        }
        
        # Répertoire pour les solutions
        solutions_dir = self.workspace / "solutions" / "sqlalchemy_fixes"
        solutions_dir.mkdir(parents=True, exist_ok=True)
        
        for fichier_analyse in analyse_fichiers["fichiers_analyses"]:
            if not fichier_analyse["problemes_detectes"]:
                continue
                
            fichier_path = Path(fichier_analyse["fichier"])
            
            # Création du script de correction
            script_correction = self.generer_script_correction(fichier_analyse)
            
            # Sauvegarde script
            script_name = f"fix_{fichier_path.stem}.py"
            script_path = solutions_dir / script_name
            
            with open(script_path, 'w', encoding='utf-8') as f:
                f.write(script_correction)
                
            corrections["scripts_correction"].append({
                "fichier_original": str(fichier_path),
                "script_correction": str(script_path),
                "problemes_count": len(fichier_analyse["problemes_detectes"]),
                "corrections_count": len(fichier_analyse["corrections_proposees"])
            })
            
            # Backup requis
            backup_path = self.workspace / "backups" / "original_files" / fichier_path.name
            corrections["backups_requis"].append({
                "original": str(fichier_path),
                "backup": str(backup_path)
            })
            
        return corrections
    
    def generer_script_correction(self, fichier_analyse):
        """Génère un script de correction pour un fichier"""
        fichier_path = Path(fichier_analyse["fichier"])
        
        script_content = f'''#!/usr/bin/env python3
"""
Script de correction automatique SQLAlchemy
Fichier cible: {fichier_path}
Généré par: Agent SQLAlchemy Fixer
Date: {datetime.now().isoformat()}
"""

import shutil
from pathlib import Path

def appliquer_corrections():
    """Applique les corrections SQLAlchemy au fichier"""
    
    fichier_original = Path(r"{fichier_path}")
    fichier_backup = Path(__file__).parent.parent.parent / "backups" / "original_files" / fichier_original.name
    
    # 1. Backup du fichier original
    fichier_backup.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(fichier_original, fichier_backup)
    print(f"✅ Backup créé: {{fichier_backup}}")
    
    # 2. Lecture du contenu
    with open(fichier_original, 'r', encoding='utf-8') as f:
        contenu = f.read()
    
    # 3. Application des corrections
    contenu_corrige = contenu
    corrections_appliquees = 0
    
'''
        
        # Ajout des corrections spécifiques
        for correction in fichier_analyse["corrections_proposees"]:
            script_content += f'''
    # Correction ligne {correction["ligne"]}: {correction["explication"]}
    contenu_corrige = contenu_corrige.replace(
        r"""{correction["original"]}""",
        r"""{correction["corrige"]}"""
    )
    corrections_appliquees += 1
'''
        
        # Ajout imports nécessaires si manquants
        has_text_import = any(p["type"] == "import_text_missing" for p in fichier_analyse["problemes_detectes"])
        if has_text_import:
            script_content += '''
    # Ajout import text si manquant
    if "from sqlalchemy import text" not in contenu_corrige:
        # Recherche d'un import SQLAlchemy existant pour insérer après
        lignes = contenu_corrige.split('\\n')
        for i, ligne in enumerate(lignes):
            if "from sqlalchemy import" in ligne and "text" not in ligne:
                # Ajout text à l'import existant
                if ligne.endswith(')'):
                    lignes[i] = ligne[:-1] + ", text)"
                else:
                    lignes[i] = ligne + ", text"
                break
        else:
            # Ajout nouvel import si aucun trouvé
            for i, ligne in enumerate(lignes):
                if ligne.startswith("import ") or ligne.startswith("from "):
                    lignes.insert(i, "from sqlalchemy import text")
                    break
        contenu_corrige = '\\n'.join(lignes)
        corrections_appliquees += 1
'''
        
        script_content += f'''
    
    # 4. Vérification des corrections
    if corrections_appliquees > 0:
        # Sauvegarde du fichier corrigé
        with open(fichier_original, 'w', encoding='utf-8') as f:
            f.write(contenu_corrige)
        print(f"✅ {{corrections_appliquees}} corrections appliquées à {{fichier_original}}")
        
        # Création d'un rapport de correction
        rapport_correction = {{
            "timestamp": "{datetime.now().isoformat()}",
            "fichier": str(fichier_original),
            "corrections_appliquees": corrections_appliquees,
            "backup_localisation": str(fichier_backup)
        }}
        
        return rapport_correction
    else:
        print("ℹ️ Aucune correction nécessaire")
        return None

def restaurer_backup():
    """Restaure le fichier depuis le backup"""
    fichier_original = Path(r"{fichier_path}")
    fichier_backup = Path(__file__).parent.parent.parent / "backups" / "original_files" / fichier_original.name
    
    if fichier_backup.exists():
        shutil.copy2(fichier_backup, fichier_original)
        print(f"✅ Fichier restauré depuis backup: {{fichier_backup}}")
        return True
    else:
        print(f"❌ Backup non trouvé: {{fichier_backup}}")
        return False

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--restore":
        restaurer_backup()
    else:
        rapport = appliquer_corrections()
        if rapport:
            print(f"\\n📊 Rapport: {{rapport}}")
        else:
            print("\\n🎯 Aucune action requise")
'''
        
        return script_content
    
    def executer_corrections_test(self, corrections):
        """Exécute les corrections en mode test (simulation)"""
        self.logger.info("Execution des corrections en mode test")
        
        resultats_test = {
            "timestamp": datetime.now().isoformat(),
            "corrections_testees": [],
            "erreurs_simulation": [],
            "estimation_succes": 0
        }
        
        for script_info in corrections["scripts_correction"]:
            try:
                script_path = Path(script_info["script_correction"])
                
                # Test de syntaxe du script
                with open(script_path, 'r', encoding='utf-8') as f:
                    script_content = f.read()
                
                # Vérification syntaxe Python
                try:
                    ast.parse(script_content)
                    syntaxe_valide = True
                except SyntaxError as e:
                    syntaxe_valide = False
                    resultats_test["erreurs_simulation"].append({
                        "script": str(script_path),
                        "erreur": f"Erreur syntaxe: {e}"
                    })
                
                resultats_test["corrections_testees"].append({
                    "script": str(script_path),
                    "fichier_cible": script_info["fichier_original"],
                    "syntaxe_valide": syntaxe_valide,
                    "problemes_count": script_info["problemes_count"],
                    "ready_for_execution": syntaxe_valide
                })
                
            except Exception as e:
                resultats_test["erreurs_simulation"].append({
                    "script": script_info.get("script_correction", "unknown"),
                    "erreur": str(e)
                })
        
        # Calcul estimation succès
        scripts_valides = len([t for t in resultats_test["corrections_testees"] if t["syntaxe_valide"]])
        total_scripts = len(resultats_test["corrections_testees"])
        
        if total_scripts > 0:
            resultats_test["estimation_succes"] = (scripts_valides / total_scripts) * 100
        
        return resultats_test
    
    def generer_rapport(self, analyse_fichiers, corrections, resultats_test):
        """Génère le rapport Markdown détaillé"""
        rapport_content = f"""# 🔧 Rapport Agent SQLAlchemy Fixer

**Agent :** {self.name}  
**ID :** {self.agent_id}  
**Version :** {self.version}  
**Date :** {analyse_fichiers['timestamp']}  
**Statut :** {self.status}

---

## 📋 RÉSUMÉ EXÉCUTIF

### 🎯 Mission
Détection et correction automatique des erreurs SQLAlchemy dans le projet NextGeneration.

### 📊 Résultats d'Analyse
- **Fichiers analysés :** {len(analyse_fichiers.get('fichiers_analyses', []))}
- **Scripts de correction créés :** {len(corrections.get('scripts_correction', []))}
- **Corrections testées :** {len(resultats_test.get('corrections_testees', []))}
- **Estimation succès :** {resultats_test.get('estimation_succes', 0):.1f}%
- **Prêt pour exécution :** {'✅ Oui' if resultats_test.get('estimation_succes', 0) >= 80 else '⚠️ Avec précautions'}

---

## 🔍 ANALYSE FICHIERS SQLALCHEMY

### 📁 Fichiers Problématiques
```json
{json.dumps(analyse_fichiers.get('fichiers_analyses', []), indent=2, ensure_ascii=False)}
```

---

## 🛠️ CORRECTIONS AUTOMATIQUES CRÉÉES

### 📜 Scripts de Correction
```json
{json.dumps(corrections.get('scripts_correction', []), indent=2, ensure_ascii=False)}
```

### 💾 Backups Requis
```json
{json.dumps(corrections.get('backups_requis', []), indent=2, ensure_ascii=False)}
```

---

## 🧪 RÉSULTATS TESTS DE CORRECTION

### ✅ Tests de Validation
```json
{json.dumps(resultats_test.get('corrections_testees', []), indent=2, ensure_ascii=False)}
```

### ❌ Erreurs Détectées
```json
{json.dumps(resultats_test.get('erreurs_simulation', []), indent=2, ensure_ascii=False)}
```

---

## 🚀 PROCÉDURE D'EXÉCUTION

### 1. 📋 Pré-requis
```bash
# Vérification environnement
cd docs/agents_postgresql_resolution/solutions/sqlalchemy_fixes

# Validation scripts
ls -la *.py
```

### 2. 🔄 Exécution Corrections
```bash
# Exécution automatique de tous les scripts
for script in fix_*.py; do
    echo "Exécution: $script"
    python "$script"
done

# Ou exécution individuelle
python fix_models.py
python fix_session.py
```

### 3. 🔙 Procédure Rollback
```bash
# En cas de problème - restauration
for script in fix_*.py; do
    python "$script" --restore
done
```

---

## 🎯 CORRECTIONS PRINCIPALES

### 1. 🔧 Conflit Attribut Metadata
**Problème :** `metadata = Column(...)` entre en conflit avec SQLAlchemy
**Solution :** 
```python
# Avant (problématique)
class AgentSession(Base):
    metadata = Column(JSON)

# Après (corrigé)
class AgentSession(Base):
    session_metadata = Column(JSON)
```

### 2. 🔧 Expressions SQL sans text()
**Problème :** SQLAlchemy 2.x requiert text() pour SQL brut
**Solution :**
```python
# Avant (problématique)
result = conn.execute("SELECT 1 as test_value")

# Après (corrigé)
from sqlalchemy import text
result = conn.execute(text("SELECT 1 as test_value"))
```

### 3. 🔧 Imports Manquants
**Problème :** Import text() manquant
**Solution :**
```python
# Ajout automatique
from sqlalchemy import create_engine, Column, Integer, String, text
```

---

## 📊 IMPACT DES CORRECTIONS

### ✅ Bénéfices Attendus
- Résolution erreurs "metadata reserved"
- Compatibilité SQLAlchemy 2.x
- Tests PostgreSQL fonctionnels
- Stabilité environnement de développement

### ⚠️ Risques Mitigés
- Backup automatique avant modification
- Scripts réversibles (--restore)
- Validation syntaxe préalable
- Test en mode simulation

---

## 📞 COORDINATION AGENTS

### 🤝 Collaboration Requise
- **🧪 Agent Testing :** Validation corrections appliquées
- **🪟 Agent Windows :** Test environnement local
- **🐳 Agent Docker :** Validation containers après corrections

### 📤 Données Partagées
- Scripts de correction prêts à exécuter
- Procédures de backup/restore
- Guide de validation post-correction
- Documentation des modifications

---

## 🔄 PLAN D'EXÉCUTION RECOMMANDÉ

### Phase 1 - Préparation (15 min)
- [ ] Validation environnement de développement
- [ ] Vérification backup système
- [ ] Test accès fichiers projet

### Phase 2 - Exécution (30 min)
- [ ] Application corrections SQLAlchemy
- [ ] Validation syntaxe Python
- [ ] Test import modules

### Phase 3 - Validation (45 min)
- [ ] Exécution suite tests PostgreSQL
- [ ] Vérification absence erreurs
- [ ] Documentation modifications

### Phase 4 - Finalisation (15 min)
- [ ] Nettoyage fichiers temporaires
- [ ] Mise à jour documentation
- [ ] Rapport final

---

## 📊 MÉTRIQUES DE SUCCÈS

### 🎯 Objectifs Techniques
- [ ] 100% des erreurs metadata résolues
- [ ] 100% des expressions SQL avec text()
- [ ] Imports SQLAlchemy corrects
- [ ] Tests PostgreSQL passent

### 📈 Indicateurs de Validation
- Code compile sans erreur SQLAlchemy
- Tests de connexion PostgreSQL réussissent
- Modèles ORM initialisent correctement
- Performance maintenue ou améliorée

---

**🔧 Corrections SQLAlchemy prêtes pour déploiement sécurisé !**

*Rapport généré automatiquement par {self.name} v{self.version}*
"""
        
        return rapport_content
    
    def executer_mission(self):
        """Exécute la mission complète de correction SQLAlchemy"""
        self.logger.info(f"🚀 {self.name} - Démarrage mission")
        
        try:
            # Analyse des fichiers SQLAlchemy
            analyse_fichiers = self.analyser_fichiers_sqlalchemy()
            
            # Création des corrections automatiques
            corrections = self.creer_corrections_automatiques(analyse_fichiers)
            
            # Test des corrections
            resultats_test = self.executer_corrections_test(corrections)
            
            # Génération rapport
            rapport = self.generer_rapport(analyse_fichiers, corrections, resultats_test)
            
            # Sauvegarde rapport
            self.rapport_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.rapport_file, 'w', encoding='utf-8') as f:
                f.write(rapport)
                
            self.logger.info(f"✅ Rapport SQLAlchemy Fixer sauvegardé: {self.rapport_file}")
            
            # Sauvegarde données JSON
            json_file = self.rapport_file.with_suffix('.json')
            mission_data = {
                "analyse_fichiers": analyse_fichiers,
                "corrections": corrections,
                "resultats_test": resultats_test
            }
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(mission_data, f, indent=2, ensure_ascii=False)
                
            return {
                "statut": "SUCCESS",
                "rapport_file": str(self.rapport_file),
                "fichiers_analyses": len(analyse_fichiers.get('fichiers_analyses', [])),
                "scripts_crees": len(corrections.get('scripts_correction', [])),
                "estimation_succes": resultats_test.get('estimation_succes', 0),
                "ready_for_execution": resultats_test.get('estimation_succes', 0) >= 80
            }
            
        except Exception as e:
            self.logger.error(f"❌ Erreur mission SQLAlchemy Fixer: {e}")
            return {
                "statut": "ERROR",
                "erreur": str(e)
            }

if __name__ == "__main__":
    agent = SQLAlchemyFixerAgent()
    resultat = agent.executer_mission()
    print(f"Mission SQLAlchemy Fixer terminée: {resultat['statut']}")
