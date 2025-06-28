# 🔌 **API DOCUMENTATION - AGENT FACTORY PATTERN**

## **Vue d'Ensemble**

L'API Agent Factory Pattern fournit des endpoints pour :
- Création et gestion templates optimisés
- Monitoring et métriques performance  
- Gestion backups et rollbacks
- Health checks et diagnostics

**Base URL :** `https://api.agentfactory.production`  
**Version :** 1.0.0  
**Authentification :** Bearer Token JWT

---

## **🔐 Authentification**

```bash
# Récupération token
curl -X POST https://auth.agentfactory.production/login \
  -H "Content-Type: application/json" \
  -d '{"username": "operator", "password": "secret"}'

# Utilisation token
curl -H "Authorization: Bearer <token>" \
  https://api.agentfactory.production/factory/create
```

---

## **📋 Endpoints**

### **GET /health**

**Description :** Health check système  
**Authentification :** None  
**Rate Limits :** 100/min

**Réponses :**

- **200** : Système opérationnel
- **503** : Système dégradé

**Exemple :**

```bash
GET /health
```

```json
{
  "status": "healthy",
  "uptime": 3600
}
```

---

### **GET /metrics**

**Description :** Métriques Prometheus  
**Authentification :** None  
**Rate Limits :** 10/min

**Réponses :**

- **200** : Métriques format Prometheus

**Exemple :**

```bash
GET /metrics
```

```json
"# HELP agent_factory_response_time_ms..."
```

---

### **POST /factory/create**

**Description :** Création template optimisée  
**Authentification :** Bearer token  
**Rate Limits :** 50/min

**Paramètres :**

- `id` (string) - **Requis** - ID unique template
- `name` (string) - **Requis** - Nom template
- `description` (string) - Optionnel - Description
- `type` (string) - Optionnel - 

**Réponses :**

- **201** : Template créé avec succès
- **400** : Paramètres invalides
- **500** : Erreur interne

**Exemple :**

```json
{
  "id": "test_template",
  "name": "Template Test",
  "type": "performance"
}
```

```json
{
  "template_id": "test_template",
  "performance_ms": 42.5,
  "compressed": true
}
```

---

### **GET /factory/templates/{id}**

**Description :** Récupération template par ID  
**Authentification :** Bearer token  
**Rate Limits :** 100/min

**Paramètres :**

- `id` (string) - **Requis** - ID template

**Réponses :**

- **200** : Template trouvé
- **404** : Template non trouvé

**Exemple :**

```bash
GET /factory/templates/test_template
```

```json
{
  "id": "test_template",
  "name": "Template Test",
  "created_at": "2025-01-28T10:00:00Z"
}
```

---

### **POST /backup/create**

**Description :** Création backup via Agent 12  
**Authentification :** Bearer token (admin)  
**Rate Limits :** 5/min

**Paramètres :**

- `source_path` (string) - **Requis** - Chemin source
- `backup_type` (string) - Optionnel - 

**Réponses :**

- **201** : Backup créé
- **400** : Paramètres invalides

**Exemple :**

```json
{
  "source_path": "/app/templates",
  "backup_type": "production"
}
```

```json
{
  "backup_id": "backup_1738024800_production",
  "size_bytes": 1048576
}
```

---

