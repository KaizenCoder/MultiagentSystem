# 📚 Index de la Documentation - Équipe d'Agents de Maintenance

*Dernière mise à jour : 2025-06-28*
*Statut : **Opérationnel - Architecture Adaptateur V4 avec Monitoring de Production***

---

## 🎯 Navigation

Ce document sert de point d'entrée pour la documentation de l'**Équipe d'Agents de Maintenance**, désormais basée sur l'architecture haute performance **Adaptateur V4**.

### 📖 Documentation Clé

- **[Suivi d'Implémentation - Phase 2](./agents/PHASE2_SUIVI_IMPLEMENTATION.md)**
  - **À LIRE EN PRIORITÉ.** Détaille l'architecture, les optimisations (LibCST, cache) et la mise en place du monitoring.

- **[Démarrage Rapide - Système d'Adaptation V4](./QUICK_START_AGENTS_MAINTENANCE.md)**
  - **À lire pour :** Lancer une mission d'adaptation et comprendre le workflow V4.

- **[Guide d'Architecture (Legacy)](./AGENTS_MAINTENANCE_PATTERN_FACTORY.md)**
  - **Historique :** Décrit l'ancien workflow de maintenance à 6 étapes. Utile pour comprendre l'évolution du projet.

### 🚀 Fichiers et Systèmes Clés

- **[Script de Lancement](../lancer_mission_maintenance_agents_factory.py)**
  - Point d'entrée pour exécuter le workflow d'adaptation V4.

- **[Dossier des Agents](./agents/)**
  - Contient le code source des agents, notamment le `Chef d'Équipe Coordinateur` et les nouvelles versions des agents spécialisés.

- **[Monitoring - Dashboard Grafana](http://localhost:3000)**
  - Interface de visualisation en temps réel des performances du système.

- **[Monitoring - Configuration Prometheus](../2_Infrastructures_et_Technologies/monitoring/prometheus-production.yml)**
  - Fichier de configuration pour la collecte des métriques.

### 🗂️ Rapports et Journaux

- **[Rapports de Maintenance](../20250620_transformation_equipe_maintenance/reports/)**
  - Contient les rapports JSON générés après chaque mission.

- **[Journal des Opérations](../JOURNAL_EVOLUTION_EQUIPE.md)**
  - Suivi chronologique des décisions et des évolutions de l'équipe.

---
*Cet index a été mis à jour pour refléter l'architecture Adaptateur V4, axée sur la performance, la parallélisation et le monitoring.* 