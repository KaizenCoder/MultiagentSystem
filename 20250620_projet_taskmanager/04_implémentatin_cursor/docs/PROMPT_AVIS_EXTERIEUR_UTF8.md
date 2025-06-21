# 🆘 **DEMANDE D'AVIS EXTÉRIEUR - PROBLÈME UTF-8 POSTGRESQL WINDOWS**

## **CONTEXTE TECHNIQUE**

Nous développons **TaskMaster NextGeneration**, un système multi-agents avec PostgreSQL sur **Windows 10 français**. Nous rencontrons un **problème d'encodage UTF-8 persistant** qui résiste à toutes nos tentatives de résolution.

---

## 🔍 **PROBLÈME DÉTAILLÉ**

### **Erreur Constante**
```
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe9 in position 103: invalid continuation byte
```

### **Environnement Système**
- **OS** : Windows 10 (build 26100)
- **Python** : 3.12
- **PostgreSQL** : 17 (service Windows natif)
- **Locale système** : `fr_FR` avec `cp1252`
- **Encodage Python** : `utf-8` (préféré)

### **Configuration PostgreSQL Testée**
```sql
-- Configuration serveur
server_encoding = UTF8
client_encoding = UTF8
lc_collate = French_France.1252
lc_ctype = French_France.1252
```

---

## 🧪 **SOLUTIONS TESTÉES (TOUTES ÉCHOUÉES)**

### **1. Configuration SQLAlchemy**
```python
# URL avec encodage explicite
database_url = "postgresql://postgres:password@localhost:5432/db?client_encoding=utf8"

# Connect args renforcés
connect_args = {
    "client_encoding": "utf8",
    "options": "-c client_encoding=UTF8 -c lc_messages=C"
}
```

### **2. Configuration Docker UTF-8**
```yaml
# docker-compose.utf8.yml
environment:
  POSTGRES_INITDB_ARGS: "--encoding=UTF8 --lc-collate=C --lc-ctype=C"
  LC_ALL: C.UTF-8
  LANG: C.UTF-8
command: >
  postgres -c client_encoding=UTF8
```
**Résultat** : ❌ Même erreur exacte

### **3. Configuration Python Windows**
```python
# Forçage encodage système
if sys.platform == 'win32':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    locale.setlocale(locale.LC_ALL, 'C.UTF-8')
```

### **4. Connexion psycopg2 directe**
```python
conn = psycopg2.connect(
    host='localhost',
    user='postgres', 
    password='password',
    database='nextgeneration',
    client_encoding='UTF8'
)
conn.set_client_encoding('UTF8')
```

---

## 📊 **DIAGNOSTICS EFFECTUÉS**

### **Vérifications Système**
```python
import locale
print(locale.getpreferredencoding())  # utf-8
print(locale.getlocale())            # ('fr_FR', 'cp1252')
```

### **Tests PostgreSQL**
```sql
-- Tous retournent UTF8
SHOW server_encoding;
SHOW client_encoding; 
SELECT current_setting('lc_collate');
```

### **Analyse Erreur**
- **Byte 0xe9** = caractère français "é" 
- **Position 103** = dans réponse serveur PostgreSQL
- **Erreur systématique** même avec requêtes simples (`SELECT 1`)

---

## 🎯 **QUESTIONS SPÉCIFIQUES**

### **1. Diagnostic Root Cause**
Quel est le **véritable problème** ? Est-ce :
- Configuration PostgreSQL Windows ?
- Interaction Python/psycopg2/Windows ?
- Locale système française incompatible ?
- Driver PostgreSQL Windows ?

### **2. Solution Technique**
Comment résoudre **définitivement** ce problème sur Windows français ?
- Configuration PostgreSQL spécifique ?
- Paramètres Python/psycopg2 ?
- Variables environnement Windows ?
- Alternative technique ?

### **3. Workaround Production**
En attendant la résolution, quelle **alternative robuste** recommandez-vous ?
- SQLite avec migration ultérieure ?
- PostgreSQL distant (Linux) ?
- Configuration PostgreSQL minimale ?

---

## 💻 **CODE REPRODUCTIBLE**

### **Test Minimal Qui Échoue**
```python
import psycopg2

try:
    conn = psycopg2.connect(
        host='localhost',
        port=5432,
        user='postgres',
        password='SecurePostgresPassword2024!',
        database='nextgeneration',
        client_encoding='utf8'
    )
    cursor = conn.cursor()
    cursor.execute("SELECT version();")  # ❌ ÉCHOUE ICI
    result = cursor.fetchone()
    print(result)
except Exception as e:
    print(f"Erreur: {e}")
    # UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe9 in position 103
```

### **Configuration PostgreSQL.conf**
```ini
# Extraits pertinents
listen_addresses = 'localhost'
port = 5432
max_connections = 100
shared_buffers = 128MB
log_destination = 'stderr'
logging_collector = on
client_encoding = UTF8
default_text_search_config = 'pg_catalog.french'
```

---

## 🔧 **ENVIRONNEMENT DÉTAILLÉ**

### **Versions Exactes**
```
PostgreSQL: 17.2
Python: 3.12.0
psycopg2: 2.9.9
SQLAlchemy: 2.0.25
Windows: 10.0.26100
```

### **Installation PostgreSQL**
- **Source** : Installateur officiel PostgreSQL.org
- **Service** : Windows Service (postgresql-x64-17)
- **Port** : 5432 (actif, testé)
- **Authentification** : md5

### **Configuration Réseau**
```bash
netstat -an | findstr 5432
# TCP 0.0.0.0:5432 LISTENING ✅
```

---

## 🎯 **OBJECTIF FINAL**

Nous cherchons une **solution définitive** pour faire fonctionner PostgreSQL UTF-8 sur Windows français, ou une **alternative robuste** pour notre système de production.

**Toute expertise ou expérience similaire sera grandement appréciée !**

---

## 📎 **FICHIERS JOINTS**

- `memory_api/app/db/session.py` - Configuration SQLAlchemy
- `memory_api/test_postgres_setup.py` - Tests complets
- `docker-compose.utf8.yml` - Configuration Docker testée
- `docs/agents_postgresql_resolution/` - Historique tentatives

---

**🆘 Merci d'avance pour votre aide technique !** 