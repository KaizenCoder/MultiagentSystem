from datetime import datetime
from pathlib import Path

def generate_universal_audit_md(report: dict, agent_type: str, output_path: str, extra: dict = None):
    """
    Génère un rapport Markdown universel pour audit d'agent (sécurité, performance, qualité, etc.).
    - report : dict structuré (issues, score, recommandations...)
    - agent_type : 'sécurité', 'performance', 'qualité', etc.
    - output_path : chemin du fichier .md à générer
    - extra : dict optionnel pour injecter des sections spécifiques
      (doit contenir reviewer_name, reviewer_role, agent_name, agent_version, repo, etc. si disponibles)
    """
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    file_path = report.get('file_path', '')
    score = report.get('security_score') or report.get('performance_score') or report.get('quality_score') or 0
    risk_level = report.get('risk_level', 'N/A')
    nb_issues = report.get('total_issues', len(report.get('vulnerabilities', [])))
    # Zones obligatoires
    reviewer_name = (extra or {}).get('reviewer_name', 'Automatique')
    reviewer_role = (extra or {}).get('reviewer_role', 'Audit Automatisé')
    agent_name = (extra or {}).get('agent_name', '-')
    agent_version = (extra or {}).get('agent_version', '-')
    repo = (extra or {}).get('repo', '-')
    points_forts = (extra or {}).get('points_forts', '-')
    conclusion = (extra or {}).get('conclusion', '-')
    suggestions = report.get('secured_suggestions', []) or report.get('optimization_suggestions', [])
    issues = report.get('vulnerabilities', []) or report.get('antipatterns_detected', [])
    recommandations = report.get('recommendations', []) or report.get('optimizations_suggested', [])
    nblines = report.get('nblines', '-')
    nbfuncs = report.get('nbfuncs', '-')
    nbclasses = report.get('nbclasses', '-')

    md = [
        f"# 📋 RAPPORT D'AUDIT {agent_type.upper()} - {file_path}",
        "",
        "## 👤 Reviewer",
        f"- **Nom** : {reviewer_name}",
        f"- **Rôle** : {reviewer_role}",
        f"- **Date** : {now}",
        "",
        "## 🤖 Agent/Script Audité",
        f"- **Nom** : {agent_name}",
        f"- **Type** : {agent_type}",
        f"- **Version** : {agent_version}",
        "",
        "## 📂 Emplacement du Fichier Audité",
        f"- **Chemin** : {file_path}",
        f"- **Repository** : {repo}",
        "",
        "## 📈 Métriques de Code",
        "| Indicateur         | Valeur         |",
        "|--------------------|---------------|",
        f"| Lignes de code     | {nblines}     |",
        f"| Fonctions          | {nbfuncs}     |",
        f"| Classes            | {nbclasses}   |",
        f"| Score global       | {score}/100   |",
        f"| Niveau de risque   | {risk_level}  |",
        "",
        f"## ⚠️ Issues Détectées : {nb_issues}",
    ]
    if issues:
        for i, issue in enumerate(issues, 1):
            desc = issue.get('description') or issue.get('issue') or str(issue)
            line = issue.get('line', '?')
            severity = issue.get('severity', '')
            md.append(f"- Issue {i} (Ligne {line}) [{severity}] : {desc}")
    else:
        md.append("- Aucune issue critique détectée.")
    md.append("\n## ✅ Points Forts")
    md.append(points_forts)
    md.append("\n## 🛠️ Recommandations")
    if recommandations:
        for rec in recommandations:
            md.append(f"- {rec}")
    else:
        md.append("- RAS")
    md.append("\n## ✨ Suggestions de Code Sécurisé/Optimisé")
    if suggestions:
        for sugg in suggestions:
            if isinstance(sugg, dict):
                md.append(f"- Ligne {sugg.get('line', '?')}: {sugg.get('suggestion', '')}")
            else:
                md.append(f"- {sugg}")
    else:
        md.append("- Aucune suggestion spécifique.")
    md.append("\n## 🏆 Conclusion")
    md.append(conclusion)
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md)) 