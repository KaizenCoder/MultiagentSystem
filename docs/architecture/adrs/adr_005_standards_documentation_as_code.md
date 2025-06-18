# ADR-005: Documentation as Code

## Statut
✅ **ACCEPTÉ ET IMPLÉMENTÉ** - 2025-06-18

## Contexte
Documentation traditionnelle:
- Décalage code ↔ documentation
- Maintenance manuelle fastidieuse
- Obsolescence rapide

## Décision  
Adoption **Documentation as Code**:
- **PlantUML**: Diagrammes versionnés
- **OpenAPI**: Documentation API auto-générée
- **ADRs**: Architecture Decision Records
- **Markdown**: Documentation structurée

## Outils et Standards
```
Documentation Pipeline:
├── C4 Model (PlantUML)
│   ├── Context diagrams
│   ├── Container diagrams  
│   └── Component diagrams
├── API Documentation (OpenAPI)
│   ├── Schemas auto-générés
│   ├── Endpoints documentés
│   └── Examples interactifs
├── ADRs (Markdown)
│   ├── Décisions architecturales
│   ├── Contexte et conséquences
│   └── Historique décisions
└── Guides Opérationnels
    ├── Deployment guides
    ├── Runbooks incidents
    └── Best practices
```

## Automation Implémentée
- **CI/CD**: Génération automatique docs
- **Git hooks**: Validation syntaxe
- **Versioning**: Documentation synchrone code

## Métriques Couverture
- **Architecture**: 3 diagrammes
- **ADRs**: 5 décisions documentées
- **API**: Documentation auto FastAPI
- **Guides**: Procédures opérationnelles

## Bénéfices
- **Synchronisation**: Code ↔ docs automatique
- **Qualité**: Standards imposés
- **Maintenance**: Effort minimal
- **Accessibilité**: Formats standards

## Références
- [Docs as Code - GitLab](https://about.gitlab.com/handbook/engineering/ux/technical-writing/docs-as-code/)
- [PlantUML Documentation](https://plantuml.com/)
