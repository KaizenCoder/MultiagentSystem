# 📋 **CONVENTIONS NOMMAGE - PATTERN FACTORY**
## **Guide Standardisation Nomenclature Enterprise**

---

## 📊 **MÉTADONNÉES DOCUMENT**

**📅 Création :** 19 juin 2025 - 16h15 (Paris)  
**🎯 Objectif :** Standardisation nomenclature Pattern Factory Enterprise  
**📍 Scope :** Tous fichiers, agents, rapports, répertoires  
**🔄 Version :** 1.0.0 - Standard Enterprise  

---

## 🏗️ **ARCHITECTURE GÉNÉRALE NOMMAGE**

### **📋 PRINCIPES FONDAMENTAUX**

1. **🕐 Horodatage** : `YYYYMMDD_HH_MM` obligatoire pour traçabilité
2. **🏷️ Préfixes typés** : Identification immédiate du type
3. **📝 Description claire** : Fonction/objectif explicite
4. **🔤 Casse cohérente** : Snake_case pour fichiers, PascalCase pour classes
5. **📊 Métadonnées** : Tags et version intégrés

---

## 📁 **CONVENTIONS PAR TYPE DE FICHIER**

### **🤖 AGENTS PATTERN FACTORY**

#### **📋 Format Standard**
```
agent_[XX]_[nom_descriptif_fonctionnel]_[version_optionnelle].py
```

#### **🎯 Exemples Conformes**
```
✅ agent_21_pattern_control_plane_enterprise.py
✅ agent_22_data_plane_claude_implementation.py
✅ agent_23_fastapi_enterprise_orchestrator.py
✅ agent_24_storage_enterprise_vault.py
✅ agent_25_monitoring_production_telemetry.py
```

#### **❌ Exemples Non-Conformes**
```
❌ Agent21.py (casse incorrecte)
❌ pattern_control.py (préfixe manquant)
❌ agent21pattern.py (underscore manquant)
❌ agentPatternControl.py (convention mixte)
```

#### **🏷️ Conventions Spécialisées**
- **Enterprise** : `agent_[21-25]_enterprise_[fonction].py`
- **Core** : `agent_[01-20]_[fonction]_core.py`
- **Tools** : `agent_[26+]_tools_[specialite].py`
- **Deprecated** : `DEPRECATED_agent_XX_[raison].py`

### **📊 RAPPORTS AUDIT**

#### **📋 Format Standard**
```
YYYYMMDD_HH_MM_[type_rapport]_[description_contexte].md
```

#### **🎯 Exemples Conformes**
```
✅ 20250619_14_39_rapport_audit_independant_claude_implementation_initial.md
✅ 20250619_15_00_audit_code_effectif_analyse_directe.md
✅ 20250620_09_30_milestone_conformite_75_percent.md
✅ 20250621_16_45_certification_enterprise_final.md
```

#### **🏷️ Types Rapports Reconnus**
- **`rapport_audit`** : Audit général conformité
- **`audit_code_effectif`** : Analyse directe code source
- **`milestone_conformite`** : Jalons progression
- **`certification_enterprise`** : Validation production
- **`rapport_catastrophe`** : Issues critiques
- **`analyse_gap`** : Écarts identifiés

### **📁 RÉPERTOIRES ET STRUCTURE**

#### **📋 Format Standard**
```
[prefixe_fonctionnel]/[sous_categorie]/[type_contenu]/
```

#### **🎯 Exemples Structure**
```
✅ reports/audit_post_phase_6_confomite_code_claude/
✅ agents/enterprise/production_ready/
✅ documentation/conventions/nommage/
✅ backups/YYYYMMDD_HHMM_[type]/
✅ logs/YYYY/MM/DD/
```

#### **🏷️ Préfixes Répertoires**
- **`reports/`** : Tous rapports et analyses
- **`agents/`** : Code agents Pattern Factory
- **`documentation/`** : Docs technique et user
- **`backups/`** : Sauvegardes horodatées
- **`logs/`** : Journaux système
- **`tests/`** : Tests unitaires et intégration
- **`monitoring/`** : Métriques et observabilité

---

## 🏷️ **SYSTÈME TAGS ET MÉTADONNÉES**

### **📋 Tags Standards**

#### **🎯 Tags Fonctionnels**
```
#enterprise #production #core #tools #deprecated
#pattern_factory #claude_implementation #async_agent
#control_plane #data_plane #api_endpoint #monitoring
```

#### **🔍 Tags Audit**
```
#audit #conformite #baseline #milestone #certification
#score_XX_100 #agent_XX_status #gap_critique #validation
```

#### **📊 Tags Priorité**
```
#P0_urgent #P1_haute #P2_moyenne #P3_basse
#critique #important #normal #optionnel
```

#### **🕐 Tags Temporels**
```
#YYYYMMDD #phase_X #sprint_X #version_X_Y_Z
#initial #progress #final #archived
```

### **📝 Métadonnées Obligatoires**

#### **📋 En-tête Standard**
```markdown
**📅 Création :** DD mois YYYY - HHhMM (Paris)
**🎯 Objectif :** [Description claire objectif]
**📍 Localisation :** [Chemin relatif]
**🔍 Nomenclature :** [Pattern utilisé]
**🏷️ Tags :** #tag1 #tag2 #tag3
**📊 Version :** X.Y.Z - [Statut]
```

---

## 🔢 **CONVENTIONS VERSIONING**

### **📋 Semantic Versioning**

#### **🎯 Format Standard**
```
MAJOR.MINOR.PATCH-[STAGE]
```

#### **🏷️ Définitions**
- **MAJOR** : Changements incompatibles API
- **MINOR** : Fonctionnalités compatibles
- **PATCH** : Corrections bugs
- **STAGE** : alpha, beta, rc, stable

#### **🎯 Exemples**
```
✅ 1.0.0-stable (Production ready)
✅ 2.1.3-beta (Feature en test)
✅ 1.2.0-rc (Release candidate)
✅ 3.0.0-alpha (Développement)
```

### **📊 Versioning Agents**

#### **📋 Pattern Agents Enterprise**
```
Version 2.0.0+ : Agents Enterprise production
Version 1.X.X : Agents Core stable
Version 0.X.X : Agents développement/test
```

---

## 📊 **NOMENCLATURE SPÉCIALISÉE**

### **🤖 Classes et Fonctions Python**

#### **📋 Conventions Code**
```python
# Classes : PascalCase
class PatternFactoryAgent:
class EnterpriseControlPlane:
class ClaudeImplementationCore:

# Fonctions : snake_case
async def execute_enterprise_task():
def validate_agent_conformity():
def generate_audit_report():

# Constantes : UPPER_SNAKE_CASE
ENTERPRISE_AGENT_COUNT = 5
PATTERN_FACTORY_VERSION = "2.0.0"
CLAUDE_API_ENDPOINT = "https://api.anthropic.com"

# Variables : snake_case
agent_status = "production_ready"
conformity_score = 87.4
enterprise_agents_list = [21, 22, 23, 24, 25]
```

### **🔧 Configuration et Variables**

#### **📋 Variables d'Environnement**
```bash
# Préfixe PATTERN_FACTORY_
PATTERN_FACTORY_ENV=production
PATTERN_FACTORY_AGENT_COUNT=25
PATTERN_FACTORY_CLAUDE_API_KEY=sk-xxx

# Préfixe ENTERPRISE_
ENTERPRISE_MODE=enabled
ENTERPRISE_SECURITY_LEVEL=high
ENTERPRISE_MONITORING=prometheus

# Préfixe AUDIT_
AUDIT_ENABLED=true
AUDIT_SCORE_THRESHOLD=75
AUDIT_REPORT_FREQUENCY=daily
```

---

## 🔍 **OUTILS RECHERCHE ET INDEXATION**

### **📋 Patterns Recherche**

#### **🎯 Par Date**
```bash
# Recherche par date complète
find . -name "*20250619*"

# Recherche par mois
find . -name "*202506*"

# Recherche par année
find . -name "*2025*"
```

#### **🏷️ Par Type**
```bash
# Agents enterprise
find . -name "agent_2[1-5]_*enterprise*.py"

# Rapports audit
find . -name "*rapport_audit*.md"

# Fichiers conformité
grep -r "conformite" --include="*.md"
```

#### **📊 Par Score/Métrique**
```bash
# Score conformité
grep -r "score.*[0-9][0-9]/100" --include="*.md"

# Agents validés
grep -r "✅.*agent" --include="*.md"

# Issues critiques
grep -r "❌.*critique" --include="*.md"
```

---

## ⚠️ **ANTI-PATTERNS À ÉVITER**

### **❌ Nomenclature Incorrecte**

#### **🚫 Erreurs Fréquentes**
```
❌ Agent21Pattern.py (casse mixte)
❌ rapport-audit-19-06.md (tirets au lieu underscores)
❌ PatternFactory_Agent21.py (ordre inversé)
❌ agent21.py (numéro sans underscore)
❌ auditreport20250619.md (pas de séparateurs)
```

#### **🚫 Caractères Interdits**
```
❌ Espaces : "agent 21.py"
❌ Caractères spéciaux : "agent@21.py"
❌ Accents : "rapport_créé.md"
❌ Majuscules anarchiques : "AgEnT_21.py"
```

### **❌ Métadonnées Manquantes**

#### **🚫 En-têtes Insuffisantes**
```markdown
❌ Pas de date de création
❌ Pas d'objectif défini
❌ Pas de tags métadonnées
❌ Pas de version/statut
❌ Pas de localisation
```

---

## ✅ **VALIDATION CONFORMITÉ**

### **📋 Checklist Validation**

#### **🎯 Avant Commit**
- [ ] **Horodatage** : Format YYYYMMDD_HH_MM présent
- [ ] **Préfixe** : Type de fichier identifiable
- [ ] **Description** : Fonction claire et explicite
- [ ] **Casse** : Convention respectée (snake_case/PascalCase)
- [ ] **Métadonnées** : En-tête complet avec tags
- [ ] **Version** : Semantic versioning appliqué
- [ ] **Localisation** : Répertoire approprié

#### **🔍 Outils Validation**
```bash
# Script validation nomenclature
./scripts/validate_naming_convention.py

# Vérification patterns
grep -E "^[a-z0-9_]+\.py$" --include="*.py"

# Validation horodatage
grep -E "20[0-9]{6}_[0-9]{2}_[0-9]{2}" --include="*.md"
```

---

## 📊 **MÉTRIQUES CONFORMITÉ**

### **🎯 KPIs Nomenclature**

#### **📋 Métriques de Base**
- **Conformité Agents** : XX/25 agents conformes (XX%)
- **Conformité Rapports** : XX/XX rapports conformes (XX%)
- **Métadonnées Complètes** : XX/XX fichiers avec en-têtes (XX%)
- **Tags Présents** : XX/XX fichiers tagués (XX%)

#### **📊 Objectifs Cibles**
- **Conformité Globale** : 95%+ pour production
- **Métadonnées** : 100% pour tous fichiers
- **Horodatage** : 100% pour rapports/logs
- **Versioning** : 100% pour agents enterprise

---

## 🚀 **ÉVOLUTION CONVENTIONS**

### **📅 Roadmap**

#### **🎯 Version 1.1.0**
- Extension conventions APIs
- Standards Kubernetes manifests
- Nomenclature Docker images

#### **🎯 Version 1.2.0**
- Conventions bases de données
- Standards monitoring/alerting
- Nomenclature CI/CD pipelines

#### **🎯 Version 2.0.0**
- Migration vers conventions cloud-native
- Standards multi-environnements
- Nomenclature microservices

---

## 📚 **RÉFÉRENCES**

### **🔗 Standards Externes**
- **PEP 8** : Style Guide Python
- **Semantic Versioning** : semver.org
- **ISO 8601** : Standards dates/heures
- **RFC 3986** : URI Generic Syntax

### **📖 Documentation Interne**
- [Pattern Factory Architecture](./PATTERN_FACTORY_ARCHITECTURE.md)
- [Agent Development Guide](./AGENT_DEVELOPMENT_GUIDE.md)
- [Audit Standards](./AUDIT_STANDARDS.md)

---

**📅 Dernière mise à jour :** 19 juin 2025 - 16h30 (Paris)  
**👥 Responsable :** Équipe Architecture Pattern Factory  
**🔄 Prochaine révision :** Phase 7 (Juillet 2025)  

---

*Ce document fait autorité pour toute nomenclature Pattern Factory Enterprise* 