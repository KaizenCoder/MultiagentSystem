# 📋 Contraintes de Travail - Vision Stratégique

## 🎯 Directives Obligatoires

**Date d'application** : 29 Juin 2025  
**Statut** : 🔒 OBLIGATOIRE ET NON NÉGOCIABLE  
**Workspace principal** : `/mnt/c/Dev/nextgeneration/stubs/Vision_strategique/`

---

## 📁 Centralisation Obligatoire

### 1. **Tests et Validation**
```
OBLIGATOIRE : /stubs/Vision_strategique/suivi_plan_implementation/tests/
├── agents/ ← Tests spécifiques agents
├── migration/ ← Tests de migration 
├── performance/ ← Tests de performance
├── regression/ ← Tests de régression
└── shadow_mode/ ← Tests shadow mode
```

### 2. **Rapports et Documentation**
```
OBLIGATOIRE : /stubs/Vision_strategique/suivi_plan_implementation/docs/rapports/
├── validation/ ← Rapports de validation
├── migration/ ← Rapports de migration
├── performance/ ← Rapports de performance
└── audit/ ← Rapports d'audit
```

### 3. **Outils et Utilitaires**
```
OBLIGATOIRE : /stubs/Vision_strategique/suivi_plan_implementation/tools/
├── validation/ ← Outils de validation
├── migration/ ← Outils de migration
├── monitoring/ ← Outils de monitoring
└── analysis/ ← Outils d'analyse
```

---

## 📝 Mise à Jour Progressive

### **Journal de Développement**
- **Localisation** : `/stubs/Vision_strategique/suivi_plan_implementation/docs/journal/JOURNAL_DEVELOPPEMENT.md`
- **Fréquence** : Mise à jour quotidienne OBLIGATOIRE
- **Format** : Horodatage UTC + actions détaillées
- **Contenu** : Toutes analyses, décisions, insights techniques

### **Suivi d'Implémentation**
- **Localisation** : `/stubs/Vision_strategique/suivi_plan_implementation/docs/journal/SUIVI_IMPLEMENTATION_NEXTGENERATION.md`
- **Synchronisation** : Avec `/docs/SUIVI_PRINCIPAL.md`
- **Métriques** : Cohérentes entre tous documents
- **Références** : Liens bidirectionnels obligatoires

---

## 🔄 Workflow de Travail

### **Processus Standard**
```python
# Workflow obligatoire pour tout travail
def workflow_vision_strategique():
    # 1. Travail dans Vision_strategique uniquement
    workspace = "/stubs/Vision_strategique/suivi_plan_implementation/"
    
    # 2. Tests dans /tests/
    run_tests(f"{workspace}tests/")
    
    # 3. Rapports dans /docs/rapports/
    generate_reports(f"{workspace}docs/rapports/")
    
    # 4. Mise à jour journal quotidien
    update_journal(f"{workspace}docs/journal/JOURNAL_DEVELOPPEMENT.md")
    
    # 5. Synchronisation documentation principale
    sync_with_main_docs()
```

### **Règles d'Organisation**
1. **Pas de duplication** : Information unique par emplacement
2. **Références croisées** : Liens vers autres documents
3. **Horodatage** : Tous changements datés UTC
4. **Cohérence** : Métriques alignées entre documents

---

## 🚫 Interdictions

### **Localisation du Travail**
- ❌ **Tests en dehors Vision_strategique** : Tous tests doivent être dans `/tests/`
- ❌ **Rapports dispersés** : Tous rapports dans `/docs/rapports/`
- ❌ **Outils externes** : Tous outils dans `/tools/`
- ❌ **Documentation déconnectée** : Liens obligatoires

### **Mise à Jour Documentation**
- ❌ **Journal obsolète** : Mise à jour quotidienne obligatoire
- ❌ **Métriques incohérentes** : Alignement obligatoire
- ❌ **Références cassées** : Validation liens requise
- ❌ **Horodatage manquant** : Timestamp UTC obligatoire

---

## ✅ Validation Contraintes

### **Checklist Quotidienne**
- [ ] Journal mis à jour avec horodatage UTC
- [ ] Tests exécutés dans `/tests/`
- [ ] Rapports générés dans `/docs/rapports/`
- [ ] Métriques synchronisées avec documentation principale
- [ ] Liens de références validés

### **Validation Hebdomadaire**
- [ ] Structure Vision_strategique respectée
- [ ] Aucun travail en dehors du workspace
- [ ] Documentation complètement synchronisée
- [ ] Outils centralisés dans `/tools/`
- [ ] Cohérence globale maintenue

---

## 📊 Bénéfices Attendus

### **Efficacité**
- **Localisation unique** : Tout le travail au même endroit
- **Réduction context switching** : Focus sur Vision_strategique
- **Amélioration productivité** : Structure organisée

### **Qualité**
- **Documentation centralisée** : Source unique de vérité
- **Cohérence** : Métriques et références alignées
- **Traçabilité** : Historique complet dans journal

### **Maintenance**
- **Facilité mise à jour** : Structure prévisible
- **Collaboration** : Workspace partagé standardisé
- **Évolutivité** : Architecture extensible

---

## 🔧 Outils de Support

### **Scripts de Validation**
```bash
# Validation structure (à créer)
./tools/validation/validate_constraints.py

# Synchronisation documentation (à créer)
./tools/validation/sync_documentation.py

# Vérification liens (à créer)
./tools/validation/check_references.py
```

### **Templates de Travail**
- **Test template** : `/tests/template_test.py`
- **Rapport template** : `/docs/rapports/template_rapport.md`
- **Journal template** : Format standardisé UTC

---

## 📞 Support et Questions

**Référence principale** : Ce document  
**Validation** : Scripts dans `/tools/validation/`  
**Documentation** : Journal quotidien obligatoire  
**Cohérence** : Synchronisation avec `/docs/SUIVI_PRINCIPAL.md`

---

*Contraintes établies le 29 Juin 2025 - Application immédiate et obligatoire*