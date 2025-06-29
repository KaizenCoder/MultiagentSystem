# Documentation des Waves de Migration

Ce répertoire contient la documentation détaillée de chaque vague de migration des agents NextGeneration.

## Structure

- `wave1_niveau1/` : Agents de niveau 1 (faibles dépendances)
  - Agents maintenance niveau 1
  - Agents PostgreSQL documentation
  - Autres agents autonomes

- `wave2_niveau2/` : Agents de niveau 2 (dépendances moyennes)
  - Chef d'équipe maintenance
  - Diagnostic PostgreSQL
  - Auditeur qualité
  - Autres agents intermédiaires

- `wave3_piliers/` : Agents piliers (fortes dépendances)
  - Coordinateur principal
  - Meta-auditeur universel
  - Adaptateur de code
  - Autres agents critiques

## Format des Documents

Chaque wave doit contenir :
- Liste des agents à migrer (`AGENTS.md`)
- Analyse des dépendances (`DEPENDANCES.md`)
- Plan de migration (`PLAN_MIGRATION.md`)
- Tests Shadow Mode (`SHADOW_MODE.md`)
- Rapport de validation (`VALIDATION.md`)

## Règles de Migration

1. Validation en Shadow Mode obligatoire
2. Parité >99.9% requise pour activation
3. Documentation des dépendances exhaustive
4. Tests de non-régression complets
5. Monitoring post-activation 1 semaine minimum

## Workflow de Migration

1. **Préparation**
   - Analyse des dépendances
   - Plan de migration détaillé
   - Setup Shadow Mode

2. **Exécution**
   - Migration code par code
   - Tests en parallèle
   - Validation continue

3. **Validation**
   - Tests de non-régression
   - Vérification parité
   - Documentation résultats

4. **Activation**
   - Switch progressif
   - Monitoring intensif
   - Support réactif 