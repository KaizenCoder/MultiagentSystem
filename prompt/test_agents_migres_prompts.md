# 🧪 Prompts de Test des Agents Migrés NextGeneration

## 📋 Instructions Générales pour l'IA de Test

En tant qu'IA de test, votre mission est de valider rigoureusement les agents migrés vers l'architecture NextGeneration. Vous devez :
- Tester TOUS les cas d'usage existants
- Ne faire AUCUN compromis sur la complexité
- Valider la non-régression ABSOLUE
- Documenter exhaustivement les résultats

## 🔍 Protocole de Test par Agent

### 🤖 Agent 05 - Maître Tests Validation

#### 1️⃣ Test Parallélisation Tests
```prompt
CONTEXTE:
Vous êtes en charge de valider les capacités de parallélisation de l'Agent 05.

MISSION:
1. Générer une suite de tests complexe avec 1000+ cas
2. Exiger une exécution parallèle sur 8 workers
3. Injecter des dépendances complexes entre tests
4. Simuler des timeouts et erreurs aléatoires

VALIDATION REQUISE:
- Parallélisation efficace maintenue
- Gestion correcte des dépendances
- Résolution des conflits de ressources
- Reporting détaillé maintenu

CRITÈRES ÉCHEC:
- Perte de parallélisation
- Simplification des dépendances
- Dégradation reporting
```

#### 2️⃣ Test Formats Legacy
```prompt
CONTEXTE:
Validation support des formats de test historiques.

MISSION:
1. Soumettre tests aux formats:
   - JUnit 3.8 (2002)
   - TestNG 5.14 (2010)
   - Ancien format propriétaire XYZ
   - Formats mixtes et malformés

VALIDATION REQUISE:
- Support 100% formats legacy
- Conversion bidirectionnelle exacte
- Préservation métadonnées historiques
- Compatibilité totale rapports

CRITÈRES ÉCHEC:
- Perte support ancien format
- Conversion inexacte
- Simplification structure
```

#### 3️⃣ Test Intégration CI/CD
```prompt
CONTEXTE:
Vérification intégration pipeline CI/CD complexe.

MISSION:
1. Configurer pipeline avec:
   - 15 stages interdépendants
   - Hooks pre/post complexes
   - Conditions branch spécifiques
   - Matrix builds multi-OS

VALIDATION REQUISE:
- Intégration tous stages
- Exécution hooks complexes
- Support matrix complet
- Reporting temps réel

CRITÈRES ÉCHEC:
- Simplification pipeline
- Perte fonctionnalité hooks
- Dégradation reporting
```

### 🤖 Agent 111 - Auditeur Qualité

#### 1️⃣ Test Analyse Projets Volumineux
```prompt
CONTEXTE:
Validation analyse code base >1M LOC.

MISSION:
1. Analyser projet avec:
   - 1.2M LOC Java/Kotlin mixte
   - 50K fichiers répartis
   - Dépendances cycliques
   - Dette technique complexe

VALIDATION REQUISE:
- Analyse complète maintenue
- Performance temps réel
- Détection patterns complexes
- Rapport exhaustif

CRITÈRES ÉCHEC:
- Simplification analyse
- Perte détection patterns
- Dégradation performance
```

#### 2️⃣ Test Multi-Langages
```prompt
CONTEXTE:
Validation support multi-langages avec interdépendances.

MISSION:
1. Analyser projet hybride:
   - Frontend: TS/JS/Vue/React
   - Backend: Java/Kotlin/Scala
   - Scripts: Python/Bash/Perl
   - Legacy: COBOL/Fortran

VALIDATION REQUISE:
- Support tous langages
- Analyse inter-langages
- Détection anti-patterns
- Validation cross-langage

CRITÈRES ÉCHEC:
- Perte support langage
- Simplification analyse
- Manque détection patterns
```

#### 3️⃣ Test Règles Qualité Custom
```prompt
CONTEXTE:
Validation règles qualité personnalisées complexes.

MISSION:
1. Implémenter règles:
   - Patterns architecturaux custom
   - Métriques complexes custom
   - Validations business rules
   - Contraintes legacy

VALIDATION REQUISE:
- Support règles complexes
- Extensibilité maintenue
- Performance temps réel
- Reporting détaillé

CRITÈRES ÉCHEC:
- Simplification règles
- Perte extensibilité
- Dégradation précision
```

### 🤖 Agent MAINTENANCE_00 - Chef Équipe

#### 1️⃣ Test Gestion Conflits
```prompt
CONTEXTE:
Validation gestion conflits équipe maintenance.

MISSION:
1. Simuler scénarios complexes:
   - 20 devs concurrent access
   - Conflits ressources multiples
   - Priorités changeantes
   - Deadlines critiques

VALIDATION REQUISE:
- Résolution conflits maintenue
- Priorisation intelligente
- Communication équipe
- Adaptation temps réel

CRITÈRES ÉCHEC:
- Simplification gestion
- Perte fonctionnalité
- Dégradation communication
```

#### 2️⃣ Test Priorisation Dynamique
```prompt
CONTEXTE:
Validation système priorisation maintenance.

MISSION:
1. Tester scénarios:
   - 100+ tickets simultanés
   - Dépendances complexes
   - Changements priorité live
   - Contraintes ressources

VALIDATION REQUISE:
- Priorisation intelligente
- Adaptation temps réel
- Gestion contraintes
- Reporting temps réel

CRITÈRES ÉCHEC:
- Simplification algorithme
- Perte adaptation
- Dégradation précision
```

#### 3️⃣ Test Workflows Legacy
```prompt
CONTEXTE:
Validation support workflows maintenance historiques.

MISSION:
1. Exécuter workflows:
   - Procédures 2010-2020
   - Scripts maintenance legacy
   - Formats rapport historiques
   - Intégrations anciennes

VALIDATION REQUISE:
- Support total workflows
- Compatibilité maintenue
- Performance préservée
- Documentation exacte

CRITÈRES ÉCHEC:
- Perte compatibilité
- Simplification workflow
- Dégradation support
```

## 📊 Métriques de Validation

### 📈 Exigences Quantitatives
```prompt
CONTEXTE:
Validation métriques performance et qualité.

VALIDATION REQUISE:
1. Performance:
   - Temps réponse ≤ baseline
   - Utilisation CPU ≤ baseline
   - Mémoire utilisée ≤ baseline
   
2. Qualité:
   - Précision = 100% baseline
   - Couverture = 100% baseline
   - Fiabilité ≥ baseline

3. Fonctionnalités:
   - Support = 100% existant
   - Complexité = maintenue
   - Extensions = validées

CRITÈRES ÉCHEC:
- Métrique < baseline
- Simplification détectée
- Perte fonctionnalité
```

## 🔍 Instructions de Reporting

### 📝 Format Rapport
```prompt
CONTEXTE:
Génération rapport test exhaustif.

STRUCTURE REQUISE:
1. Résumé Exécutif:
   - Status global (PASS/FAIL)
   - Métriques clés
   - Blockers identifiés

2. Détails Tests:
   - Cas testés (100% requis)
   - Résultats détaillés
   - Preuves non-régression
   - Documentation bugs

3. Validation Complexité:
   - Preuve maintien
   - Comparaison baseline
   - Points attention

4. Recommandations:
   - Actions requises
   - Risques identifiés
   - Prochaines étapes

CRITÈRES ÉCHEC:
- Documentation incomplète
- Manque preuve
- Simplification non-documentée
```

## ⚠️ Règles d'Or

1. **Interdiction Absolue**:
   - Aucune simplification acceptée
   - Aucun contournement toléré
   - Aucune régression permise

2. **Validation Obligatoire**:
   - Tests production uniquement
   - Charge réelle x1.5 minimum
   - Documentation exhaustive

3. **Reporting Strict**:
   - Preuve non-régression
   - Validation complexité
   - Documentation complète

## 📝 Notes Importantes

1. Ces prompts doivent être exécutés:
   - En production uniquement
   - Sur 1 semaine minimum
   - Avec charge réelle x1.5
   
2. Tout échec nécessite:
   - Rollback immédiat
   - Investigation complète
   - Correction totale

3. La validation requiert:
   - 100% cas testés
   - 0 simplification
   - Documentation exhaustive 