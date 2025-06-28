# ADR-003: Système Dependency Injection

## Statut  
✅ **ACCEPTÉ ET IMPLÉMENTÉ** - 2025-06-18

## Contexte
Couplage fort entre composants dans architecture monolithique:
- Instanciation directe dépendances
- Tests difficiles (mocking complexe)
- Configuration centralisée impossible

## Décision
Adoption **Dependency Injection** avec FastAPI `Depends()`:
- **IoC Container**: Inversion contrôle
- **Injectable Services**: Services configurables
- **Scope Management**: Singleton/Request scope

## Implémentation
```python
# Container configuration
get_services_container() → ServiceContainer
get_database() → Database connection
get_cache_manager() → Redis connection

# Injection usage
@router.get("/endpoint")
async def endpoint(service: Service = Depends(get_service)):
    return await service.process()
```

## Architecture Impact
- **Testabilité**: Mock/stub facilités
- **Configuration**: Centralisée et flexible
- **Coupling**: Réduit significativement

## Métriques
- Dependencies configurées: 4 modules
- Services injectables: 12 services
- Routers utilisant DI: 3 routers

## Références
- [FastAPI Dependency Injection](https://fastapi.tiangolo.com/tutorial/dependencies/)
- [Inversion of Control Principle](https://en.wikipedia.org/wiki/Inversion_of_control)
