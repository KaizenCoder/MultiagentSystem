### Volet 1 : Classification des erreurs & Routage (Adaptateur)
* **Date :** 2024-06-24 00:27 CET
* **Analyse Comparative :**  
L'Adaptateur actuel ne distingue pas les types d'erreurs ; la réparation est peu ciblée. L'ajout d'une classification des exceptions permettra de router la correction vers la bonne stratégie (ex : indentation, nommage, import…).  
Limite : sans classification, la boucle de réparation tourne à vide sur certains cas (notamment l'indentation).
* **Proposition :**  
1. Ajouter une fonction `classify_exception` pour déterminer le type d'erreur.  
2. Modifier le coordinateur pour utiliser cette classification et transmettre `error_type` à l'Adaptateur.  
3. Adapter l'Adaptateur pour appliquer la stratégie de réparation adaptée selon `error_type`.  
4. Tester le workflow complet (M-T-D) : commit/push si succès, rollback si échec.
* **Décision avant test :** GO
* **Résultat du Test :** ÉCHEC initial (TypeError: `Task` object n'accepte pas l'argument `data`), suivi d'un SUCCÈS après correction.
* **Observations post-test :** L'erreur initiale était due à une mauvaise utilisation de l'API de la classe `Task` (`data` au lieu de `params`). Après rollback et correction, le workflow s'exécute correctement. La classification d'erreur est maintenant fonctionnelle et le `error_type` est bien transmis à l'adaptateur.
* **Décision Finale :** GO - Le Volet 1 est implémenté, testé et validé.

### Volet 2 : Amélioration du moteur de correction d'indentation
* **Date :** <à compléter>
* **Analyse Comparative :**
L'Adaptateur actuel utilise une méthode `_pre_check_and_repair_syntax` limitée qui ne corrige qu'un seul type d'erreur d'indentation. C'est insuffisant pour garantir une réparation robuste.
* **Proposition :**
1.  Remplacer la logique existante par une nouvelle fonction `_fix_indentation_errors` plus complète, capable de gérer `unexpected indent` et `unindent does not match`.
2.  Modifier la méthode `execute_task` de l'Adaptateur pour router les erreurs de type `indentation` vers cette nouvelle fonction.
3.  Valider la correction via le cycle M-T-D en utilisant un fichier de test contenant une erreur d'indentation.
* **Décision avant test :**
En attente de validation utilisateur.
* **Résultat du Test :**
—
* **Observations post-test :**
—
* **Décision Finale :**
—
--- 