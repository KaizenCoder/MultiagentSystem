import asyncio
from agent_109_pattern_factory_version import PatternFactoryAgent
from datetime import datetime
from pathlib import Path
import os

# Détection automatique de tous les fichiers agents Python
AGENTS_DIR = Path(__file__).resolve().parent
AGENT_FILES = [f for f in os.listdir(AGENTS_DIR) if f.startswith('agent_') and f.endswith('.py')]

# Groupes de 5
def grouper(l, n):
    for i in range(0, len(l), n):
        yield l[i:i+n]

REPORTS_DIR = Path(__file__).resolve().parent.parent / "reports" / "factory_pattern"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

NON_CONFORMES = []

AGENT = ("Agent 04", "agent_04_expert_securite_crypto.py")

def generer_markdown_conformite(agent_label, result):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    compliant = result.get('compliant', False)
    issues = result.get('issues', [])
    score = 100 if compliant else max(0, 100 - 30*len(issues))
    statut = '✅ CONFORME' if compliant else '❌ NON CONFORME'
    color = '🟢' if compliant else '🔴'
    
    md = f"""# 🏗️ RAPPORT CONFORMITÉ PATTERN FACTORY : {agent_label}

**Date :** {now}
**Fichier analysé :** `{result.get('file_path','N/A')}`
**Score conformité :** {score}/100
**Statut global :** {statut}
**Issues critiques :** {len(issues)}

## 📋 Résumé des Checks

| Critère | Statut |
|---------|--------|
| Présence d'une classe | {'✅' if 'No class definition found.' not in issues else '❌'} |
| Méthode __init__ | {'✅' if 'No __init__ method found in class.' not in issues else '❌'} |
| Méthode run (async/sync) | {'✅' if 'No run method found for agent execution loop.' not in issues else '❌'} |

## 🚨 Issues Critiques
"""
    if issues:
        for i in issues:
            md += f"- 🔴 {i}\n"
    else:
        md += "- ✅ Aucun problème détecté\n"
    md += f"""

## 🔧 Recommandations
"""
    if compliant:
        md += "- L'agent respecte les standards du Pattern Factory.\n"
    else:
        md += "- Corriger les points listés dans les issues critiques ci-dessus.\n"
    md += f"""

## 🛠️ Détails Techniques
- Chemin du fichier : `{result.get('file_path','N/A')}`
- Date d'analyse : {now}
- Outil de validation : PatternFactoryAgent v2.0.0

---
*Rapport généré automatiquement par l'outil de conformité Pattern Factory.*
"""
    return md

async def main():
    agent = PatternFactoryAgent()
    label, path = AGENT
    result = await agent.validate_agent_compliance(path)
    print(f"\n---\n{label}:\n{result}\n")

if __name__ == "__main__":
    asyncio.run(main()) 