# 🔗 GIT HOOKS NEXTGENERATION
## Validation Automatique et Workflows Git

---

**Projet :** NextGeneration AI Platform  
**Version :** 1.0  
**Date :** Décembre 2024  
**Référence :** Transposition SuperWhisper_V6 → NextGeneration adaptée  

---

## 🎯 **OBJECTIF**

Automatiser la validation qualité et les workflows Git pour NextGeneration avec hooks personnalisés qui garantissent la conformité avant commit/push.

## 📋 **HOOKS DISPONIBLES**

### 🔍 **pre-commit** - Validation Avant Commit
**Fichier :** `pre-commit`  
**Déclencheur :** Avant chaque `git commit`  
**Fonction :** Validation qualité automatique  

**Validations effectuées :**
- ✅ **Syntaxe Python** : Compilation sans erreurs
- ✅ **Standards PEP8** : Avec flake8 si disponible
- ✅ **Syntaxe PowerShell** : Avec pwsh si disponible
- ✅ **Fichiers Markdown** : Validation basique
- ✅ **GPU RTX 3090** : Si modifications GPU détectées
- ✅ **Documentation** : Vérification âge CODE-SOURCE.md
- ✅ **Outils matures** : Intégrité tools/ critiques

**Temps d'exécution :** ~10-30 secondes selon modifications

### 🚀 **pre-push** (Futur)
**Fichier :** `pre-push`  
**Déclencheur :** Avant `git push`  
**Fonction :** Tests complets avant push  

**Validations prévues :**
- 🧪 **Tests unitaires** complets
- 📊 **Génération documentation** automatique
- 🎮 **Validation GPU** complète
- 📈 **Métriques performance**

## 🛠️ **INSTALLATION**

### 📥 **Installation Automatique**

```bash
# Script d'installation rapide
cd /c/Dev/nextgeneration
chmod +x git_hooks/install_hooks.sh
./git_hooks/install_hooks.sh
```

### 📝 **Installation Manuelle**

#### **Étape 1 : Copie des Hooks**
```bash
# Naviguer vers le projet
cd /c/Dev/nextgeneration

# Copier les hooks dans .git/hooks/
cp git_hooks/pre-commit .git/hooks/
chmod +x .git/hooks/pre-commit

# Vérifier installation
ls -la .git/hooks/
```

#### **Étape 2 : Configuration Environnement**
```bash
# Créer dossier logs
mkdir -p logs/git_hooks

# Vérifier permissions
chmod +x .git/hooks/*

# Test hook
.git/hooks/pre-commit
```

#### **Étape 3 : Validation Installation**
```bash
# Test avec commit vide
git commit --allow-empty -m "Test hook pre-commit"

# Vérifier logs
ls -la logs/git_hooks/
```

## ⚙️ **CONFIGURATION**

### 🔧 **Variables d'Environnement**

```bash
# Optionnel : Configuration personnalisée
export NEXTGEN_HOOK_VERBOSE=1          # Mode verbeux
export NEXTGEN_HOOK_SKIP_GPU=1          # Ignorer validation GPU
export NEXTGEN_HOOK_SKIP_DOCS=1         # Ignorer vérification documentation
```

### 📋 **Fichier de Configuration**

**Créer :** `git_hooks/config.json`
```json
{
    "validation": {
        "python_syntax": true,
        "pep8_standards": true,
        "powershell_syntax": true,
        "markdown_validation": true,
        "gpu_validation": true,
        "documentation_check": true,
        "tools_integrity": true
    },
    "thresholds": {
        "documentation_age_hours": 24,
        "max_validation_time_seconds": 60
    },
    "logging": {
        "level": "INFO",
        "save_detailed_logs": true,
        "log_retention_days": 7
    }
}
```

## 🔍 **UTILISATION**

### ✅ **Commit Standard**
```bash
# Modification fichiers
git add .

# Commit avec validation automatique
git commit -m "feat: nouvelle fonctionnalité"

# Hook pre-commit s'exécute automatiquement
# ✅ Validation réussie → Commit accepté
# ❌ Validation échouée → Commit refusé
```

### ⚠️ **Bypass d'Urgence**
```bash
# ATTENTION : Uniquement en cas d'urgence
git commit --no-verify -m "fix: correction critique"

# Ou pour pre-push
git push --no-verify
```

### 🔧 **Mode Debug**
```bash
# Exécution manuelle avec debug
NEXTGEN_HOOK_VERBOSE=1 .git/hooks/pre-commit

# Consulter logs détaillés
cat logs/git_hooks/pre-commit_*.log
```

## 📊 **RÉSULTATS ET LOGS**

### 📋 **Format Output Standard**
```
[10:30:15] INFO: 🚀 DÉBUT PRE-COMMIT HOOK NEXTGENERATION
[10:30:15] INFO: 🔍 Validation fichiers modifiés
[10:30:16] SUCCESS: 🐍 Python syntaxe OK: tools/exemple.py
[10:30:17] SUCCESS: 📝 Markdown validé: docs/nouveau-guide.md
[10:30:18] SUCCESS: 🎮 Validation GPU RTX 3090 réussie
[10:30:19] SUCCESS: ✅ PRE-COMMIT VALIDATION RÉUSSIE
[10:30:19] INFO: Commit autorisé pour NextGeneration
```

### 📄 **Logs Détaillés**
**Localisation :** `logs/git_hooks/pre-commit_YYYYMMDD_HHMMSS.log`

**Contenu :**
- Timestamp précis de chaque validation
- Détails des fichiers analysés
- Résultats de chaque test
- Métriques de performance
- Conseils d'amélioration

### 🎯 **Métriques Collectées**
- Nombre de fichiers validés par type
- Temps d'exécution par phase
- Taux de réussite des validations
- Fréquence des bypasses d'urgence

## 🚨 **DÉPANNAGE**

### ❌ **Erreurs Courantes**

#### **Hook ne s'exécute pas**
```bash
# Vérifier permissions
ls -la .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit

# Tester manuellement
.git/hooks/pre-commit
```

#### **Erreur Python non trouvé**
```bash
# Vérifier PATH Python
which python
python --version

# Alternative avec python3
sed -i 's/python /python3 /g' .git/hooks/pre-commit
```

#### **Erreur validation GPU**
```bash
# Désactiver validation GPU temporairement
export NEXTGEN_HOOK_SKIP_GPU=1
git commit -m "correction"

# Ou ignorer dans config
echo '{"validation": {"gpu_validation": false}}' > git_hooks/config.json
```

#### **Hook trop lent**
```bash
# Mode rapide uniquement
git config hooks.pre-commit.mode quick

# Ou bypass ponctuel
git commit --no-verify -m "commit rapide"
```

### 🔧 **Optimisations**

#### **Réduire Temps d'Exécution**
```bash
# Exclure certains fichiers
echo "*.log" >> .git/info/exclude
echo "*.tmp" >> .git/info/exclude

# Validation partielle
export NEXTGEN_HOOK_SKIP_DOCS=1
```

#### **Logs Détaillés**
```bash
# Activer mode verbeux
git config hooks.verbose true

# Consulter logs récents
tail -f logs/git_hooks/pre-commit_*.log
```

## 🎓 **BONNES PRATIQUES**

### ✅ **Recommandations Développeur**

1. **Validation Locale** : Toujours tester en local avant commit
2. **Commits Atomiques** : Un commit = une fonctionnalité/correction
3. **Messages Clairs** : Utiliser prefixes (feat:, fix:, docs:)
4. **Code Propre** : Respecter PEP8 et standards NextGeneration
5. **Documentation** : Maintenir CODE-SOURCE.md à jour

### 🔄 **Workflow Recommandé**
```bash
# 1. Développement local
# ... modification code ...

# 2. Validation manuelle
python -m pytest tests/
python tools/documentation_generator/generate_bundle_nextgeneration.py --mode validation

# 3. Commit avec validation automatique
git add .
git commit -m "feat: nouvelle fonctionnalité agents"

# 4. Push avec validation complète (futur)
git push origin main
```

### 📈 **Métriques Qualité**
- **Taux commits validés** : > 95%
- **Temps moyen validation** : < 30 secondes
- **Bypasses d'urgence** : < 5%
- **Régressions détectées** : 0

## 🔄 **MAINTENANCE**

### 🧹 **Nettoyage Logs**
```bash
# Nettoyage automatique (7 jours)
find logs/git_hooks/ -name "*.log" -mtime +7 -delete

# Nettoyage manuel
rm logs/git_hooks/pre-commit_*.log
```

### 🔄 **Mise à Jour Hooks**
```bash
# Sauvegarder configuration
cp git_hooks/config.json git_hooks/config.json.bak

# Mettre à jour hooks
git pull origin main
./git_hooks/install_hooks.sh

# Restaurer configuration
cp git_hooks/config.json.bak git_hooks/config.json
```

### 📊 **Statistiques d'Usage**
```bash
# Analyser logs
grep "SUCCESS" logs/git_hooks/*.log | wc -l
grep "ERROR" logs/git_hooks/*.log | wc -l

# Temps moyen d'exécution
grep "VALIDATION TERMINÉE" logs/git_hooks/*.log
```

## 🚀 **ÉVOLUTIONS FUTURES**

### 🔮 **Roadmap Hooks**
- **pre-push** : Validation complète avant push
- **post-commit** : Notifications et métriques
- **pre-receive** : Validation côté serveur
- **Integration CI/CD** : Hooks pour GitHub Actions

### 🎯 **Améliorations Prévues**
- Validation incrémentale (uniquement fichiers modifiés)
- Cache de validation pour performance
- Intégration avec outils externes (SonarQube, etc.)
- Rapports de qualité automatiques

---

**🎯 Objectif : Commits 100% validés, Zero défaut en production**  
**🚀 Vision : Workflows Git NextGeneration = Référence qualité**  
**📊 Standard : Validation automatique transparente et rapide** 