# Nouvelle Architecture Modulaire

## Principes
- Single Responsibility Principle (SRP)
- Dependency Injection
- Separation of Concerns
- Testabilité maximale

## Structure
- `routers/`: Points d'entrée HTTP
- `services/`: Logique métier
- `repositories/`: Accès données
- `schemas/`: Modèles Pydantic
- `dependencies/`: Injection dépendances

## Migration
Chaque fichier god mode sera décomposé selon cette structure.
