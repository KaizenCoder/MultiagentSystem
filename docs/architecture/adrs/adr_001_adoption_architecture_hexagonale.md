# ADR-001: Adoption Architecture Hexagonale

## Statut
✅ **ACCEPTÉ ET IMPLÉMENTÉ** - 2025-06-18

## Contexte
L'architecture monolithique originale (god mode files) présentait:
- 1110 lignes réparties dans 39 fichiers
- Couplage fort entre couches
- Difficultés de test et maintenance
- Violations principes SOLID

## Décision
Adoption du pattern **Architecture Hexagonale (Ports & Adapters)** avec:
- **Ports**: Interfaces métier (IOrchestratorService, IAgentService)
- **Adapters**: Implémentations concrètes (Repositories, Web API)
- **Core**: Logique métier pure (Services)

## Implémentation Réalisée
```
Services Layer (12 services):
- OrchestratorService: Coordination agents
- AgentService: Gestion cycle vie agents  
- HealthService: Monitoring santé

Routers Layer (3 routers):
- Séparation responsabilités par domaine
- Injection dépendances FastAPI

Dependencies Layer:
- IoC Container configuré
- Inversion contrôle effective
```

## Conséquences

### Positives ✅
- **Testabilité**: Isolation couches métier
- **Maintenabilité**: Responsabilités séparées
- **Flexibilité**: Changement d'adapteurs sans impact métier
- **Conformité SOLID**: Respect principes

### Négatives ⚠️
- **Complexité initiale**: Courbe apprentissage
- **Boilerplate**: Plus de fichiers/interfaces

## Métriques Impact
- **Réduction complexité**: 96.4% (1,990 → 71 lignes main.py)
- **Séparation**: 3 routers + 12 services
- **Patterns détectés**: Dependency Injection, FastAPI, Router Pattern, Pydantic Models

## Références
- [Hexagonal Architecture - Alistair Cockburn](https://alistair.cockburn.us/hexagonal-architecture/)
- [Ports & Adapters Pattern](https://herbertograca.com/2017/09/14/ports-adapters-architecture/)
