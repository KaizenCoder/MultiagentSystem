# 🚀 Démarrage Rapide - Équipe d'Agents de Maintenance

*Dernière mise à jour : 2025-06-21*
*Statut : **Opérationnel et Stable***

---

## 🎯 Objectif

Lancer un cycle de maintenance complet sur l'équipe d'agents de l'Agent Factory. Le processus est **entièrement automatisé** et s'exécute avec **une seule commande**.

## ⚡ ÉTAPE 1 : Lancer la Mission

Il n'y a qu'une seule étape. Ouvrez un terminal à la racine du projet et exécutez la commande suivante.

```bash
python lancer_mission_maintenance_agents_factory.py
```

### Ce qui se passe en coulisses

L'exécution de ce script déclenche un workflow complet orchestré par l'agent **Chef d'Équipe Coordinateur** :

1.  **🤖 Analyse** : L'agent 01 scanne le répertoire `agents/` pour trouver tous les fichiers d'agents.
2.  **🤔 Évaluation** : L'agent 02 évalue chaque script pour déterminer s'il nécessite une maintenance.
3.  **✍️ Adaptation** : L'agent 03 corrige et refactorise le code de l'agent.
4.  **🔬 Test** : L'agent 04 exécute le code modifié pour s'assurer de son bon fonctionnement.
5.  **📚 Documentation** : L'agent 05 nettoie et documente le code final.
6.  **✅ Validation** : L'agent 06 effectue une validation finale avant de sauvegarder les modifications.

---

## 📊 ÉTAPE 2 : Consulter le Rapport

Une fois la mission terminée, un rapport détaillé au format JSON est généré à la racine du projet.

### Résultat attendu en cas de succès

Vous verrez ce message dans votre terminal :

```
✅ Mission de maintenance terminée avec succès!
📄 Rapport détaillé : rapport_maintenance_SUCCESS_YYYYMMDD_HHMMSS.json
```

Le fichier `rapport_maintenance_SUCCESS_...json` contient un compte-rendu détaillé de toutes les actions effectuées par chaque agent sur chaque fichier.

### En cas d'échec

Si la mission échoue, le message sera :
```
❌ Mission de maintenance échouée.
📄 Rapport d'erreur : rapport_maintenance_ECHEC_YYYYMMDD_HHMMSS.json
🔍 Erreur : [Message d'erreur]
```
Le fichier de rapport d'échec vous donnera des indices sur la cause du problème.

---

## 🚨 Dépannage

### ❌ Problème : `ModuleNotFoundError`
Si vous rencontrez une erreur indiquant qu'un module est manquant.

**Solution :**
Assurez-vous que toutes les dépendances sont installées. Il n'y a pas de `requirements.txt` global, vérifiez les imports dans les scripts pour les dépendances manquantes. Une dépendance qui a posé problème par le passé est `astor`.
```bash
pip install astor
```

### ❌ Problème : Le script échoue avec une erreur `SyntaxError` ou autre
Le système est conçu pour être robuste, mais des erreurs peuvent survenir.

**Solution :**
1.  Consultez le rapport d'échec JSON pour identifier l'agent et le fichier qui ont posé problème.
2.  Examinez les logs dans le terminal pour obtenir une trace complète de l'erreur (`traceback`).
3.  Si le problème persiste, il peut s'agir d'un cas non prévu par l'équipe de maintenance.

---
*Ce guide a été simplifié pour refléter le workflow de maintenance actuel, stable et unifié.* 