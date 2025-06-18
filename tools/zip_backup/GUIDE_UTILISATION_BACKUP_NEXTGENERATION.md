# 📚 Guide d'Utilisation - Système Backup NextGeneration

## 🎯 **Vue d'Ensemble**

Le système de sauvegarde NextGeneration est un outil automatisé enterprise-ready pour la sauvegarde quotidienne de vos projets de développement. Il génère des archives ZIP optimisées avec validation d'intégrité cryptographique.

### ✨ **Fonctionnalités Principales**
- 🗜️ **Compression ZIP optimisée** avec validation intégrité
- ⚙️ **Configuration multi-projets** user-friendly
- 📁 **Exclusions intelligentes** (.git, __pycache__, node_modules)
- 🔧 **Planificateur Windows** intégré
- 🔒 **Sécurité enterprise** (HMAC, checksums)
- 🧪 **Tests automatisés** et monitoring

## 📁 **Structure des Fichiers**

```
E:\DEV_BACKUP\
├── nextgeneration\                     ← Répertoire projet
│   ├── backup_nextgeneration_20241218_0200.zip
│   ├── backup_nextgeneration_20241218_1400.zip
│   └── backup_nextgeneration_20241219_0200.zip
├── autre_projet\                       ← Autre projet
│   ├── backup_autre_projet_20241218_0200.zip
│   └── backup_autre_projet_20241218_1400.zip
└── test_project_config\                ← Projet de test
    └── backup_test_project_config_20241218_1200.zip
```

**Pattern de nommage :**
- Format : `backup_{projet}_{YYYYMMDD}_{HHMM}.zip`
- Exemple : `backup_nextgeneration_20241218_1430.zip`
- **Organisation** : Chaque projet a son propre répertoire dans `E:\DEV_BACKUP\`

---

## 🚀 **Installation et Configuration**

### 📋 **Prérequis**
- Windows 10/11
- Python 3.8+
- PowerShell 5.1+
- Droits administrateur (pour planificateur)

### 🔧 **Configuration Initiale**

#### 1. **Configuration Globale**
```bash
cd C:\Dev\nextgeneration\tools\zip_backup
python agents/agent_configuration_manager.py
```

#### 2. **Configuration Interactive**
Le système vous guidera pour :
- ✅ Définir la destination backup (défaut: E:\DEV_BACKUP)
- ✅ Configurer les exclusions par défaut
- ✅ Paramétrer la rétention (défaut: 30 sauvegardes)
- ✅ Activer les notifications

---

## 📖 **Utilisation Quotidienne**

### 🎯 **Création d'un Nouveau Projet Backup**

#### **Méthode 1 : Interface CLI Interactive**
```bash
python agents/agent_configuration_manager.py --wizard
```

**Étapes guidées :**
1. Nom du projet
2. Chemin source du projet
3. Destination backup (optionnel)
4. Exclusions personnalisées
5. Planification (heure, fréquence)

#### **Méthode 2 : Configuration Manuelle**
```bash
python agents/agent_configuration_manager.py --create "mon_projet" --source "C:\Dev\mon_projet"
```

### 🗜️ **Exécution Backup Manuel**

#### **Backup Immédiat**
```bash
python agents/agent_backup_engine.py --project "nextgeneration"
```

#### **Test Backup (sans sauvegarde)**
```bash
python agents/agent_backup_engine.py --project "nextgeneration" --test
```

#### **Backup avec Exclusions Personnalisées**
```bash
python agents/agent_backup_engine.py --project "nextgeneration" --exclude "*.tmp,logs,temp"
```

---

## ⚙️ **Configuration Avancée**

### 📁 **Gestion des Exclusions**

#### **Exclusions par Défaut**
- `.git/` - Dépôt Git
- `__pycache__/` - Cache Python
- `node_modules/` - Dépendances Node.js
- `*.tmp` - Fichiers temporaires
- `.env` - Variables environnement
- `*.log` - Fichiers logs

#### **Ajout d'Exclusions Personnalisées**
```bash
python agents/agent_file_management.py --add-exclusion "*.bak,dist/,build/"
```

#### **Exclusions par Projet**
Éditer le fichier de configuration :
```json
{
  "name": "mon_projet",
  "exclusions": [
    "__pycache__",
    "node_modules",
    "*.tmp",
    "mon_exclusion_specifique/"
  ]
}
```

### 🔧 **Planification Windows**

#### **Création Tâche Planifiée**
```powershell
# Exécuter en tant qu'administrateur
python agents/agent_windows_integration.py --schedule "mon_projet" --time "02:00"
```

#### **Gestion des Tâches**
```powershell
# Lister les tâches backup
schtasks /query /fo table | findstr "NextGeneration"

# Exécuter manuellement
schtasks /run /tn "NextGeneration\BackupMonProjet"

# Désactiver temporairement
schtasks /change /tn "NextGeneration\BackupMonProjet" /disable
```

---

## 🧪 **Tests et Validation**

### 🔍 **Tests Système Complets**
```bash
python agents/agent_testing_specialist.py
```

**Tests Inclus :**
- ✅ Moteur backup (compression, intégrité)
- ✅ Gestionnaire configuration
- ✅ Gestion fichiers et exclusions
- ✅ Intégration système complète
- ✅ Performance sous charge

### 🔒 **Audit Sécurité**
```bash
python agents/agent_security_specialist.py
```

**Vérifications :**
- ✅ Intégrité clé secrète HMAC
- ✅ Permissions workspace
- ✅ Espace disque destination
- ✅ Protection fichiers sensibles

---

## 📊 **Monitoring et Maintenance**

### 📋 **Vérification État Système**
```bash
python agents/agent_configuration_manager.py --status
```

### 🔍 **Validation Intégrité Backup**
```bash
python agents/agent_security_specialist.py --verify "E:\DEV_BACKUP\backup_nextgeneration_20241218_0200.zip"
```

### 📈 **Rapports et Logs**

#### **Localisation des Logs**
- **Logs agents** : `C:\Dev\nextgeneration\tools\zip_backup\logs\`
- **Rapports** : `C:\Dev\nextgeneration\tools\zip_backup\reports\`
- **Résultats tests** : `C:\Dev\nextgeneration\tools\zip_backup\tests\results\`

#### **Consultation Logs**
```bash
# Logs récents
Get-Content logs\agent_backup_engine.log -Tail 50

# Rapports JSON
Get-Content reports\agent_backup_engine_rapport.json | ConvertFrom-Json
```

---

## 🛠️ **Dépannage**

### ❌ **Problèmes Courants**

#### **Erreur : "Destination inaccessible"**
```bash
# Vérifier destination
Test-Path "E:\DEV_BACKUP"

# Créer si nécessaire
New-Item -ItemType Directory -Path "E:\DEV_BACKUP" -Force
```

#### **Erreur : "Permissions insuffisantes"**
```powershell
# Exécuter PowerShell en administrateur
Start-Process powershell -Verb RunAs
```

#### **Backup Corrompu**
```bash
# Vérification intégrité
python agents/agent_security_specialist.py --verify "chemin_backup.zip"

# Re-création backup
python agents/agent_backup_engine.py --project "nom_projet" --force
```

#### **Tâche Planifiée Échoue**
```powershell
# Vérifier statut tâche
schtasks /query /tn "NextGeneration\BackupMonProjet"

# Consulter logs
Get-EventLog -LogName System -Source "Task Scheduler" -Newest 10
```

### 🔧 **Maintenance Préventive**

#### **Nettoyage Rétention**
```bash
python agents/agent_file_management.py --cleanup --retention 30
```

#### **Mise à Jour Configuration**
```bash
python agents/agent_configuration_manager.py --update "mon_projet"
```

#### **Régénération Clé Sécurité**
```bash
python agents/agent_security_specialist.py --regenerate-key
```

---

## 📋 **Commandes de Référence**

### 🎯 **Commandes Essentielles**

| Action | Commande |
|--------|----------|
| **Backup immédiat** | `python agents/agent_backup_engine.py --project "nom"` |
| **Configuration projet** | `python agents/agent_configuration_manager.py --wizard` |
| **Tests système** | `python agents/agent_testing_specialist.py` |
| **Audit sécurité** | `python agents/agent_security_specialist.py` |
| **Planification** | `python agents/agent_windows_integration.py --schedule` |

### ⚙️ **Options Avancées**

| Option | Description |
|--------|-------------|
| `--test` | Mode test sans sauvegarde |
| `--force` | Force backup même si récent |
| `--exclude "pattern"` | Exclusions personnalisées |
| `--verbose` | Logs détaillés |
| `--dry-run` | Simulation sans exécution |

---

## 🎯 **Exemples d'Utilisation**

### 📝 **Scenario 1 : Nouveau Projet**
```bash
# 1. Configuration
python agents/agent_configuration_manager.py --create "mon_app" --source "C:\Dev\mon_app"

# 2. Test backup
python agents/agent_backup_engine.py --project "mon_app" --test

# 3. Backup réel
python agents/agent_backup_engine.py --project "mon_app"

# 4. Planification
python agents/agent_windows_integration.py --schedule "mon_app" --time "03:00"
```

### 🔄 **Scenario 2 : Maintenance Hebdomadaire**
```bash
# 1. Tests système
python agents/agent_testing_specialist.py

# 2. Audit sécurité
python agents/agent_security_specialist.py

# 3. Nettoyage rétention
python agents/agent_file_management.py --cleanup

# 4. Vérification tâches
schtasks /query /fo table | findstr "NextGeneration"
```

### 🚨 **Scenario 3 : Récupération d'Urgence**
```bash
# 1. Vérification intégrité
python agents/agent_security_specialist.py --verify "backup.zip"

# 2. Extraction backup
python agents/agent_backup_engine.py --restore "backup.zip" --destination "C:\Recovery"

# 3. Validation restauration
python agents/agent_testing_specialist.py --validate-restore
```

---

## 📞 **Support et Ressources**

### 📚 **Documentation Technique**
- **Architecture** : `docs/class_diagram.puml`
- **Séquences** : `docs/sequence_diagram.puml`
- **Templates** : `templates/`

### 🔍 **Logs et Diagnostics**
- **Workspace** : `C:\Dev\nextgeneration\tools\zip_backup\`
- **Logs** : `logs/`
- **Rapports** : `reports/`
- **Tests** : `tests/results/`

### ⚡ **Performance**
- **Compression** : ~55% réduction taille
- **Vitesse** : ~150 fichiers/seconde
- **Intégrité** : Validation cryptographique systématique

---

## 🎉 **Félicitations !**

Votre système de sauvegarde NextGeneration est maintenant configuré et prêt à protéger vos projets de développement avec une fiabilité enterprise-grade !

**🔄 Backup automatique quotidien activé ✅**  
**🔒 Sécurité cryptographique garantie ✅**  
**📊 Monitoring et tests intégrés ✅** 