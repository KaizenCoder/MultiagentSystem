# ✅ Plan de test qualité - TaskMaster Pool

## Objectif
Garantir la stabilité, la scalabilité et la traçabilité du système de lancement multi-agents TaskMaster.

---

## 🔬 Tests unitaires

- [ ] Initialisation d’un TaskMaster individuel
- [ ] Logging spécifique par agent
- [ ] Rechargement dynamique de template

## ⚙️ Tests fonctionnels

- [ ] Lancement via REST API (`/launch`)
- [ ] Affichage des agents (`/instances`)
- [ ] Suppression d’un agent (`/instances/{id}`)
- [ ] Spawn via CLI (`launch_taskmaster.py`)
- [ ] Validation via `session_validator.py`

## 🔄 Tests de robustesse

- [ ] Lancement de 10 agents en parallèle
- [ ] Crash volontaire d’un agent (tester isolation)
- [ ] Surcharge I/O logging (stress test)

## 📊 Audit

- [ ] Métriques exposées par agent
- [ ] Logs horodatés / versionnés
- [ ] Session ID unique
- [ ] Absence de conflit template

---

## 🚦Critères de validation

| Axe         | Seuil     |
|-------------|-----------|
| Latence API | < 300ms   |
| Temps création agent | < 500ms |
| Uptime pool | > 99.9%   |
| Traçabilité logs | 100% identifiables par agent_id |
