# �� Démarrage Rapide - Système d'Adaptation V4

*Dernière mise à jour : 2025-06-28*
*Statut : **Adaptateur V4 - Opérationnel avec Monitoring de Production***

---

## 🎯 Objectif

Lancer un cycle d'adaptation de code haute performance, incluant la correction automatique, les tests de performance et le monitoring en temps réel via l'**Adaptateur V4**.

## ⚡ ÉTAPE 1 : Lancer la Mission d'Adaptation

Le processus reste simple à initier. Ouvrez un terminal à la racine du projet et exécutez la commande suivante pour démarrer l'orchestrateur.

```bash
# Commande pour lancer le processus d'adaptation
# (Ex: python orchestrator/main.py --task adapt-codebase)
python lancer_mission_maintenance_agents_factory.py 
```

### Ce qui se passe en coulisses (Architecture V4)

L'exécution de ce script déclenche un workflow sophistiqué et performant :

1.  **Orchestration Parallèle** : Le **Chef d'Équipe Coordinateur** lance et supervise plusieurs instances de l'**Agent Adaptateur V4** pour traiter les tâches en parallèle, maximisant le débit.
2.  **Pipeline de Transformation Optimisé (LibCST)** : Chaque adaptateur utilise un pipeline de transformation de code basé sur LibCST, optimisé pour la performance et la précision.
3.  **Cache Intelligent (LRU + Redis)** : Un cache multi-niveau (mémoire locale + Redis partagé) avec une stratégie LRU adaptative (`AdaptiveCacheOptimizer`) accélère drastiquement les transformations répétitives. L'objectif est un hit rate supérieur à 80%.
4.  **Correction Intelligente** : Le moteur de correction gère des cas complexes (ex: indentation, imports) grâce à une classification fine des erreurs, permettant d'appliquer la bonne stratégie de réparation.
5.  **Monitoring en Temps Réel** : Pendant toute l'opération, des métriques de performance, de cache et d'erreurs sont collectées et exportées en continu vers **Prometheus**.

---

## 📊 ÉTAPE 2 : Consulter le Rapport de Mission

Comme pour l'ancien système, un rapport détaillé est généré à la fin de la mission, indiquant le succès ou l'échec et les actions effectuées.

- **Succès :** `rapport_maintenance_SUCCESS_YYYYMMDD_HHMMSS.json`
- **Échec :** `rapport_maintenance_ECHEC_YYYYMMDD_HHMMSS.json`

---

## 📈 ÉTAPE 3 : Consulter le Dashboard de Monitoring

Pour une vue en temps réel de la santé et des performances du système, accédez au dashboard Grafana.

- **URL :** `http://localhost:3000` (par défaut)
- **Dashboard :** "Adaptateur V4 - Performance"

#### Métriques clés à surveiller :
- **Latence des requêtes (P95)** : Temps de traitement des tâches.
- **Taux d'erreurs** : Pourcentage de tâches échouées.
- **Hit Rate du Cache (%)** : Efficacité de la mise en cache.
- **Utilisation Mémoire** : Consommation des ressources par les adaptateurs.

---

## 🚨 Dépannage (Système V4)

### ❌ Problème : Le cache ne semble pas fonctionner (hit rate bas)
**Solution :**
1.  Vérifiez que le service **Redis** est démarré et accessible par l'application.
2.  Inspectez les logs de `cache_optimizer.py` pour des messages d'erreur.
3.  Assurez-vous que les patterns de code traités sont répétitifs. Le cache est moins efficace sur des tâches uniques.

### ❌ Problème : Les métriques n'apparaissent pas dans Grafana
**Solution :**
1.  Vérifiez que **Prometheus** est en cours d'exécution et qu'il scrape bien la cible de l'application (configuré dans `prometheus.yml`).
2.  Examinez les logs de l'application pour des erreurs liées à `MetricsExporter`.
3.  Assurez-vous qu'aucun pare-feu ne bloque la communication entre l'application et Prometheus.

---
*Ce guide a été simplifié pour refléter le workflow de maintenance actuel, stable et unifié.* 