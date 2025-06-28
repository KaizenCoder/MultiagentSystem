# Guide d'Installation - Outils Apex_VBA_FRAMEWORK

## 🚀 Installation Rapide

1. **Vérifier les prérequis**
   ```bash
   python --version  # Python 3.8+
   ```

2. **Installer les dépendances** (si nécessaire)
   ```bash
   pip install -r requirements.txt
   ```

3. **Tester l'installation**
   ```bash
   python run_apex_tool.py
   ```

## 🔧 Configuration

### Variables d'Environnement

Les outils Apex utilisent la détection automatique du projet NextGeneration.
Aucune configuration manuelle n'est requise.

### PowerShell (Windows)

Pour les outils PowerShell, assurez-vous que l'exécution de scripts est autorisée:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## 🧪 Tests

### Test Global
```bash
python -m pytest tests/  # Si des tests sont disponibles
```

### Test Individuel
```bash
python run_apex_tool.py <nom_outil> --help
```

## 🔍 Dépannage

### Erreurs Communes

1. **Outil introuvable**
   - Vérifiez que le nom est correct avec `python run_apex_tool.py`

2. **Erreur d'importation Python**
   - Installez les dépendances: `pip install -r requirements.txt`

3. **Erreur PowerShell**
   - Vérifiez la politique d'exécution
   - Utilisez: `powershell -ExecutionPolicy Bypass -File ...`

## 📞 Support

Pour les problèmes spécifiques aux outils Apex:
1. Consultez la documentation individuelle de chaque outil
2. Vérifiez les logs dans le répertoire `logs/`
3. Référez-vous à la documentation NextGeneration

## 📚 Ressources

- [Documentation NextGeneration](../docs/)
- [Apex_VBA_FRAMEWORK Original](G:/Dev/Apex_VBA_FRAMEWORK/)
