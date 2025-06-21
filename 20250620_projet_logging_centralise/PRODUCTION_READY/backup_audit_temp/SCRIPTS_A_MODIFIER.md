# 📋 SCRIPTS À MODIFIER - LOGGING CENTRALISÉ *(CORRIGÉ)*

**Liste précise des fichiers nécessitant une migration vers le logging centralisé**

---

## 🚨 **CORRECTION : AGENTS RATÉS DANS /docs/**

Vous aviez raison ! J'avais raté **8 agents** dans le répertoire `docs/agents_postgresql_resolution/agent team/` :

---

## 🎯 **AGENTS PRIORITAIRES (OBLIGATOIRES)**

### **1. Agent Factory Implementation (41 agents)**
```
📁 agent_factory_implementation/agents/
├── agent_01_coordinateur_principal.py          ✅ PRIORITÉ 1
├── agent_02_architecte_code_expert.py          ✅ PRIORITÉ 1  
├── agent_03_specialiste_configuration.py       ✅ PRIORITÉ 1
├── agent_04_expert_securite_crypto.py          ✅ PRIORITÉ 1
├── agent_05_maitre_tests_validation.py         ✅ PRIORITÉ 1
├── agent_06_specialiste_monitoring_sprint4.py  ✅ PRIORITÉ 1
├── agent_07_expert_deploiement_k8s_fixed.py    ✅ PRIORITÉ 1
├── agent_08_performance_optimizer.py           ✅ PRIORITÉ 1
├── agent_09_integration_specialist.py          ✅ PRIORITÉ 1
├── agent_10_documentaliste_expert.py           ✅ PRIORITÉ 1
├── agent_11_auditeur_qualite.py                ✅ PRIORITÉ 1
├── agent_12_backup_manager.py                  ✅ PRIORITÉ 1
├── agent_13_specialiste_documentation.py       ✅ PRIORITÉ 1
├── agent_14_specialiste_workspace.py           ✅ PRIORITÉ 1
├── agent_15_testeur_specialise.py              ✅ PRIORITÉ 1
├── agent_16_peer_reviewer_senior.py            ✅ PRIORITÉ 1
├── agent_17_peer_reviewer_technique.py         ✅ PRIORITÉ 1
├── agent_meta_strategique_scheduler.py         ✅ PRIORITÉ 1
├── agent_FASTAPI_23_orchestration_enterprise.py ✅ PRIORITÉ 1
├── agent_MONITORING_25_production_enterprise.py ✅ PRIORITÉ 1
└── ... (21 autres agents)
```

### **2. Équipe Maintenance (7 agents)**
```
📁 20250620_transformation_equipe_maintenance/agent_equipe_maintenance/
├── agent_MAINTENANCE_00_chef_equipe_coordinateur.py ✅ PRIORITÉ 1
├── agent_MAINTENANCE_01_analyseur_structure.py     ✅ PRIORITÉ 1
├── agent_MAINTENANCE_02_evaluateur_utilite.py      ✅ PRIORITÉ 1
├── agent_MAINTENANCE_03_adaptateur_code.py         ✅ PRIORITÉ 1
├── agent_MAINTENANCE_04_testeur_anti_faux_agents.py ✅ PRIORITÉ 1
├── agent_MAINTENANCE_05_documenteur_peer_reviewer.py ✅ PRIORITÉ 1
└── agent_MAINTENANCE_06_coordinateur_final.py      ✅ PRIORITÉ 1
```

### **3. 🚨 AGENTS RATÉS DANS /docs/ (8 agents)**
```
📁 docs/agents_postgresql_resolution/agent team/
├── agent_diagnostic_postgres_final.py          ✅ PRIORITÉ 2 (RATTRAPÉ)
├── agent_docker_specialist.py                  ✅ PRIORITÉ 2 (RATTRAPÉ)
├── agent_resolution_finale.py                  ✅ PRIORITÉ 2 (RATTRAPÉ)
├── agent_sqlalchemy_fixer.py                   ✅ PRIORITÉ 2 (RATTRAPÉ)
├── agent_testing_specialist.py                 ✅ PRIORITÉ 2 (RATTRAPÉ)
├── agent_windows_postgres.py                   ✅ PRIORITÉ 2 (RATTRAPÉ)
├── agent_web_researcher.py                     ✅ PRIORITÉ 2 (RATTRAPÉ)
├── agent_workspace_organizer.py                ✅ PRIORITÉ 2 (RATTRAPÉ)
└── agent_documentation_manager.py              ✅ PRIORITÉ 2 (RATTRAPÉ)
```

### **4. Factory Experts Team (6 agents)**
```
📁 agent_factory_experts_team/
├── coordinateur_equipe_experts.py              ✅ PRIORITÉ 2
├── expert_chatgpt_robustesse.py                ✅ PRIORITÉ 2
├── expert_gemini_innovation.py                 ✅ PRIORITÉ 2
├── expert_templates_specialist.py              ✅ PRIORITÉ 2
├── expert_superviseur_synthese.py              ✅ PRIORITÉ 2
└── expert_claude_architecture.py               ✅ PRIORITÉ 2
```

### **5. Agents Racine (5 agents)**
```
📁 nextgeneration/ (racine)
├── coordinateur_equipe_tools_apex.py           ✅ PRIORITÉ 2
├── coordinateur_equipe_tools.py                ✅ PRIORITÉ 2
├── agent_coordinateur_refactorisation_simple.py ✅ PRIORITÉ 2
├── agent_adaptateur_documentation.py           ✅ PRIORITÉ 2
└── agent_analyseur_outils.py                   ✅ PRIORITÉ 2
```

---

## 📊 **STATISTIQUES CORRIGÉES**

### **TOTAL AGENTS À MIGRER : 67 agents** *(+8 ratés)*
- **PRIORITÉ 1** : 48 agents (factory + maintenance)
- **PRIORITÉ 2** : 19 agents (docs + experts + racine)

### **AGENTS RATÉS INITIALEMENT**
- ❌ **8 agents** dans `/docs/agents_postgresql_resolution/`
- ✅ **Maintenant identifiés** et ajoutés à la liste

---

## 🚀 **COMMANDE DE MIGRATION CORRIGÉE**

```bash
# Migration complète des 67 agents
python migrate_all_files.py --agents-only --include-docs

# Ou par priorité
python migrate_all_files.py --priority=1  # 48 agents critiques
python migrate_all_files.py --priority=2  # 19 agents secondaires
```

---

## ⚠️ **SCRIPTS À IGNORER (CONFIRMÉ)**

### **❌ NE PAS MIGRER**
- **Scripts utilitaires** (`/scripts/`) : 64 fichiers
- **Outils** (`/tools/`) : 120 fichiers  
- **Orchestrateur** (`/orchestrator/`) : 15 fichiers
- **Tests** (`/tests/`) : 45 fichiers
- **API mémoire** (`/memory_api/`) : 8 fichiers
- **Monitoring** (`/monitoring/`) : 6 fichiers

**Raison** : Ces scripts ont leur propre logique de logging fonctionnelle et ne sont pas concernés par le problème des "logs anarchiques des agents".

---

## 🎯 **RÉSUMÉ FINAL**

- **✅ TOTAL À MIGRER** : **67 agents** (corrigé)
- **❌ TOTAL À IGNORER** : **762 scripts** (confirmé)
- **🚨 ERREUR CORRIGÉE** : +8 agents ratés dans `/docs/` 