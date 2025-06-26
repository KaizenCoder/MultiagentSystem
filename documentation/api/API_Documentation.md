# 🔌 **API DOCUMENTATION - AGENT FACTORY PATTERN**

## **Vue d'Ensemble**
**Base URL :** `https://api.agentfactory.production`  
**Version :** 1.0.0  
**Authentification :** Bearer Token JWT

## **🔐 Authentification**
```bash
curl -X POST https://auth.agentfactory.production/login \
  -H "Content-Type: application/json" \
  -d '{"username": "operator", "password": "secret"}'
```

## **📋 Endpoints**
### **GET /health**
**Description :** Health check système  
**Authentification :** None  
**Rate Limits :** 100/min

**Exemple :**
```bash
curl -X GET http://localhost:8000/health
```

---
### **GET /metrics**
**Description :** Métriques Prometheus  
**Authentification :** None  
**Rate Limits :** 10/min

**Exemple :**
```bash
curl -X GET http://localhost:8000/metrics
```

---
### **POST /factory/create**
**Description :** Création template optimisée  
**Authentification :** Bearer token  
**Rate Limits :** 50/min

**Exemple :**
```bash
curl -X POST -H "Authorization: Bearer <token>" http://localhost:8000/factory/create
```

---
### **GET /factory/templates/{id}**
**Description :** Récupération template par ID  
**Authentification :** Bearer token  
**Rate Limits :** 100/min

**Exemple :**
```bash
curl -X GET -H "Authorization: Bearer <token>" http://localhost:8000/factory/templates/{id}
```

---
### **POST /backup/create**
**Description :** Création backup via Agent 12  
**Authentification :** Bearer token (admin)  
**Rate Limits :** 5/min

**Exemple :**
```bash
curl -X POST -H "Authorization: Bearer <token>" http://localhost:8000/backup/create
```

---

