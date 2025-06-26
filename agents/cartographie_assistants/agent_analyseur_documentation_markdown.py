# agents/cartographie_assistants/agent_analyseur_documentation_markdown.py
import logging
import re
from typing import Dict, Any, List, Optional, Tuple
from pathlib import Path

# Configuration du logging
# logger = logging.getLogger(__name__) # Remplacé par logger de classe
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s') # Configuré dans __main__ pour les tests

class AgentAnalyseurDocumentationMarkdown:
    """
    Agent responsable de l'analyse de fichiers de documentation Markdown (.md).
    Il peut extraire des informations telles que :
    - Le titre principal (H1)
    - Les sections (H2, H3, etc.)
    - La version de l'agent documenté (si mentionnée)
    - La description de l'agent.
    - Les listes d'objectifs, de capacités/tâches, et de dépendances.
    - Les blocs de code avec leur langage spécifié.
    """
    __version__ = "0.2.4" # Nettoyage plus robuste des nouvelles lignes

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        # Le niveau de logging sera configuré par l'application ou les tests
        # self.logger.info(f"Initialisation de {self.__class__.__name__} version {self.__version__}")

    def get_capabilities(self) -> Dict[str, Any]:
        """Retourne les capacités de l'agent."""
        return {
            "name": self.__class__.__name__,
            "version": self.__version__,
            "description": "Analyse des fichiers de documentation Markdown pour en extraire la structure et les informations clés sur les agents, y compris les blocs de code.",
            "tasks": [
                {
                    "name": "analyser_fichier_markdown",
                    "description": "Analyse un fichier Markdown et retourne un dictionnaire structuré d'informations."
                },
                {
                    "name": "extraire_version_documentee",
                    "description": "Tente d'extraire la version de l'agent telle que documentée dans le fichier Markdown."
                }
            ]
        }

    def _clean_section_content(self, text: str) -> str:
        """Nettoie les séquences de newline échappées.
        1. Remplace \\\\ (double backslash littéral) par \\ (simple backslash littéral).
        2. Remplace \\n (simple backslash littéral + n) par \\n (vrai newline).
        """
        if not text: return ""
        self.logger.debug(f"_clean_section_content: input (repr): {text!r}")
        # Étape 1: Gérer les doubles backslashes avant un 'n' ou seuls
        # Par exemple, "foo\\\\nbar" -> "foo\\nbar", "foo\\\\baz" -> "foo\\baz"
        cleaned_text = text.replace("\\\\\\\\", "\\\\") # Remplacer \\\\\\\\ par \\
        self.logger.debug(f"_clean_section_content: after replace('\\\\\\\\\\\\', '\\\\\\\\') (repr): {cleaned_text!r}")
        
        # Étape 2: Gérer les simples backslashes avant un 'n'
        # Par exemple, "foo\\nbar" (qui est maintenant le résultat de l'étape 1 ou l'original) -> "foo\nbar"
        final_cleaned_text = cleaned_text.replace("\\n", "\\n")
        self.logger.debug(f"_clean_section_content: after replace('\\\\n', '\\n') (repr): {final_cleaned_text!r}")
        return final_cleaned_text

    def _parse_list_items(self, text_content: str) -> List[str]:
        # Le text_content est supposé être déjà nettoyé par _clean_section_content 
        # via _parse_markdown_content avant d'être passé ici.
        self.logger.debug(f"_parse_list_items: Received text_content (supposément pré-nettoyé) (repr): {text_content!r}")

        items = []
        if not text_content:
            self.logger.debug("_parse_list_items: text_content is empty, returning empty list.")
            return items

        list_item_pattern = r"^\\s*([*\\-])\\s+(.*)"
        
        try:
            limit = min(30, len(text_content))
            char_ords = [ord(c) for c in text_content[:limit]]
            char_reprs = [repr(c) for c in text_content[:limit]]
            self.logger.debug(f"  _parse_list_items: text_content (PRE-SPLITLINES) - First {limit} char ords: {char_ords}")
            self.logger.debug(f"  _parse_list_items: text_content (PRE-SPLITLINES) - First {limit} char reprs: {char_reprs}")
        except Exception as e_log_char:
            self.logger.error(f"  _parse_list_items: Error logging text_content char details: {e_log_char}")

        processed_lines = []
        try:
            # Utiliser text_content directement, en supposant qu'il a de vrais newlines
            processed_lines = text_content.splitlines()
            self.logger.debug(f"_parse_list_items: text_content.splitlines() produced {len(processed_lines)} lines.")
            self.logger.debug(f"  _parse_list_items: processed_lines (POST-SPLITLINES) (repr): {processed_lines!r}")
            if processed_lines:
                 self.logger.debug(f"  _parse_list_items: First line from splitlines (repr): {processed_lines[0]!r}")
        except Exception as e_split:
            self.logger.error(f"_parse_list_items: Error during text_content.splitlines(): {e_split}", exc_info=True)
            return []

        list_item_regex = None
        try:
            list_item_regex = re.compile(list_item_pattern)
            self.logger.debug(f"_parse_list_items: Compiled list_item_regex pattern: {list_item_regex.pattern}")
        except re.error as e_re:
            self.logger.error(f"_parse_list_items: Erreur de compilation regex pour list_item: {e_re}", exc_info=True)
            return items

        for i, line_from_split in enumerate(processed_lines):
            self.logger.debug(f"  _parse_list_items: Processing line {i} from splitlines (repr): {line_from_split!r}")
            stripped_line = line_from_split.strip()
            if not stripped_line: 
                self.logger.debug(f"    _parse_list_items: Line {i} is empty after strip, skipping.")
                continue

            if list_item_regex: 
                match = list_item_regex.match(stripped_line)
                if match:
                    item_text = match.group(2).strip()
                    items.append(item_text)
                    self.logger.info(f"    _parse_list_items: Line {i} - LIST ITEM MATCH! Text: '{item_text}'")
                else:
                    self.logger.debug(f"    _parse_list_items: Line {i} - No list item match for stripped_line: {stripped_line!r}")
            else:
                self.logger.warning(f"    _parse_list_items: list_item_regex not compiled, cannot match line {i}")
            
        self.logger.debug(f"_parse_list_items: Returning {len(items)} items: {items!r}")
        return items

    def _parse_markdown_content(self, contenu: str) -> Dict[str, Any]:
        self.logger.debug(">>>> _parse_markdown_content CALLED <<<<")
        raw_sections: List[Dict[str, Any]] = []
        blocs_code: List[Dict[str, str]] = []
        current_section_data = None
        title_h1 = None
        version_documentee = None
        
        contenu_pour_splitlines = contenu.replace("\\\\n", "\\n") 
        initial_lines = contenu_pour_splitlines.splitlines()
        lines = [l.replace("\\\\n", "\\n") for l in initial_lines]
        self.logger.debug(f"Nombre de lignes à parser (après nettoyage double sécurité et splitlines): {len(lines)}")

        h1_regex_str = "^#\\s+(.*)" 
        h_regex_str = "^(#{2,6})\\s+(.*)" 
        code_block_start_regex_str = r"^```(\\w*)\\s*$" 
        code_block_end_regex_str = r"^```\\s*$"
        
        h1_regex = re.compile(h1_regex_str)
        h_regex = re.compile(h_regex_str)
        code_block_start_regex = re.compile(code_block_start_regex_str)
        code_block_end_regex = re.compile(code_block_end_regex_str)

        version_patterns_str = [
            "^\\*\\*\\s*Version\\s*:\\s*\\*\\*\\s*([\\w.\\-]+)", 
            "^Version\\s*:\\s*([\\w.\\-]+)",                  
            "^\\s*Version:\\s*([\\w.\\-]+)",                   
            "\\(\\s*v([\\w.\\-]+)\\s*\\)"                    
        ]
        version_regex_list = [re.compile(p, re.IGNORECASE) for p in version_patterns_str]

        content_buffer: List[str] = []
        in_code_block = False
        current_code_block_lang = ""
        current_code_block_content: List[str] = []

        for line_num, line in enumerate(lines):
            self.logger.debug(f"LIGNE {line_num} (parser principal) (type: {type(line)}, len: {len(line)}) (repr): {line!r}")

            if in_code_block:
                if code_block_end_regex.match(line):
                    self.logger.info(f"  Fin de bloc de code détectée à la ligne {line_num}.")
                    in_code_block = False
                    blocs_code.append({
                        "langage": current_code_block_lang,
                        "contenu": "\\n".join(current_code_block_content)
                    })
                    current_code_block_lang = ""
                    current_code_block_content = []
                else:
                    current_code_block_content.append(line)
                continue 
            
            code_block_start_match = code_block_start_regex.match(line)
            if code_block_start_match:
                self.logger.info(f"  Début de bloc de code détecté à la ligne {line_num} avec lang '{code_block_start_match.group(1)}'.")
                if current_section_data and content_buffer:
                     # Nettoyer le contenu de la section avant de le stocker
                     temp_buffered_content = "\\n".join(content_buffer).strip()
                     current_section_data["contenu"] = self._clean_section_content(temp_buffered_content)
                     self.logger.debug(f"      Section '{current_section_data['titre']}' contenu (avant bloc code) mis à jour et nettoyé: {current_section_data['contenu']!r}")
                     content_buffer = [] 
                in_code_block = True
                current_code_block_lang = code_block_start_match.group(1) or ""
                continue

            if version_documentee is None:
                for idx, v_regex in enumerate(version_regex_list):
                    v_match = v_regex.search(line) 
                    if v_match:
                        version_documentee = v_match.group(1) if v_match.group(1) else v_match.group(2)
                        self.logger.info(f"    LIGNE {line_num}: VERSION_MATCH! (Regex idx {idx}): '{version_documentee}'")
                        break 
            
            h1_match_obj = h1_regex.match(line)
            hx_match_obj = h_regex.match(line) 

            if title_h1 is None and h1_match_obj:
                title_h1 = h1_match_obj.group(1).strip()
                self.logger.info(f"    LIGNE {line_num}: H1_MATCH! Titre Principal: '{title_h1}'")

            elif hx_match_obj: 
                self.logger.info(f"    LIGNE {line_num}: HX_REGEX_MATCH! (Niveau {len(hx_match_obj.group(1))})")
                if current_section_data: 
                    temp_buffered_content = "\\n".join(content_buffer).strip()
                    current_section_data["contenu"] = self._clean_section_content(temp_buffered_content)
                    self.logger.debug(f"      Section '{current_section_data['titre']}' terminée. Contenu nettoyé (repr): {current_section_data['contenu']!r}")
                    raw_sections.append(current_section_data)
                
                content_buffer = [] 
                level = len(hx_match_obj.group(1)) 
                titre_section = hx_match_obj.group(2).strip()
                current_section_data = {"titre": titre_section, "level": level, "contenu": ""} # Contenu sera rempli et nettoyé
                self.logger.info(f"      Nouvelle section détectée (Niveau {level}): '{titre_section}'")
            
            elif current_section_data: 
                content_buffer.append(line)
            
            elif title_h1 and not current_section_data: 
                self.logger.debug(f"    Ligne de 'header' post-H1 (non capturée dans section): {line!r}")
        
        if current_section_data: 
            temp_buffered_content = "\\n".join(content_buffer).strip()
            current_section_data["contenu"] = self._clean_section_content(temp_buffered_content)
            self.logger.debug(f"Dernière section '{current_section_data['titre']}' terminée. Contenu nettoyé (repr): {current_section_data['contenu']!r}")
            raw_sections.append(current_section_data)

        extracted_data = {
            "titre_principal": title_h1,
            "version_documentee": version_documentee,
            "description_agent": None,
            "objectifs_agent": [],
            "capacites_agent": [],
            "dependances_agent": [],
            "blocs_code": blocs_code, 
            "sections_brutes": raw_sections
        }

        for section in raw_sections:
            titre_lower = section["titre"].lower().strip()
            # Le contenu de la section est déjà nettoyé lors de sa création/finalisation
            contenu_section = section.get("contenu", "") 
            
            self.logger.debug(f"Traitement section spécifique post-collecte: '{section['titre']}' (lower: '{titre_lower}')")
            self.logger.debug(f"  >>> contenu_section ('{titre_lower}') pour _parse_list_items (repr): {contenu_section!r}")
            # Les logs ord/repr pour contenu_section ici sont redondants si _parse_list_items les fait déjà.

            if titre_lower == "description":
                extracted_data["description_agent"] = contenu_section
                self.logger.info(f"  -> Description trouvée pour '{section['titre']}'.")
            elif titre_lower == "objectifs":
                extracted_data["objectifs_agent"] = self._parse_list_items(contenu_section)
                self.logger.info(f"  -> Objectifs trouvés ({len(extracted_data['objectifs_agent'])} items) pour '{section['titre']}'.")
            elif titre_lower in ["capacités", "capacites", "tâches", "taches"]: 
                extracted_data["capacites_agent"] = self._parse_list_items(contenu_section)
                self.logger.info(f"  -> Capacités/Tâches trouvées ({len(extracted_data['capacites_agent'])} items) pour '{section['titre']}'.")
            elif titre_lower in ["dépendances", "dependances"]: 
                extracted_data["dependances_agent"] = self._parse_list_items(contenu_section)
                self.logger.info(f"  -> Dépendances trouvées ({len(extracted_data['dependances_agent'])} items) pour '{section['titre']}'.")
            
        return extracted_data

    def analyser_fichier_markdown(self, chemin_fichier: str) -> Optional[Dict[str, Any]]:
        """
        Analyse un fichier Markdown donné et extrait sa structure.
        """
        self.logger.info(f"Début de l'analyse du fichier Markdown : {chemin_fichier}")
        try:
            fp = Path(chemin_fichier)
            if not fp.exists():
                self.logger.error(f"Fichier Markdown non trouvé : {chemin_fichier}")
                return None
            
            contenu_brut = fp.read_text(encoding='utf-8')
            contenu_normalise = contenu_brut.replace('\\r\\n', '\\n').replace('\\r', '\\n')
            
            analyse_resultat = self._parse_markdown_content(contenu_normalise)
            if analyse_resultat:
                analyse_resultat["chemin_fichier"] = str(fp.resolve()) 
            
            self.logger.info(f"Analyse Markdown terminée avec succès pour : {chemin_fichier}")
            return analyse_resultat

        except FileNotFoundError: 
            self.logger.error(f"Fichier Markdown non trouvé (exception) : {chemin_fichier}")
            return None
        except Exception as e:
            self.logger.error(f"Erreur inattendue lors de l'analyse de {chemin_fichier}: {e}", exc_info=True)
            return None

    def extraire_version_documentee(self, chemin_fichier: str) -> Optional[str]:
        """
        Tente d'extraire la version de l'agent telle que documentée dans le fichier Markdown.
        """
        analyse = self.analyser_fichier_markdown(chemin_fichier)
        if analyse and analyse.get("version_documentee"):
            return analyse["version_documentee"]
        self.logger.warning(f"Version non trouvée ou échec de l'analyse pour {chemin_fichier}")
        return None

    def execute_task(self, task_name: str, task_params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Exécute une tâche spécifique.
        """
        self.logger.info(f"Exécution de la tâche '{task_name}' avec les paramètres : {task_params}")
        if task_name == "analyser_fichier_markdown":
            chemin_fichier = task_params.get("chemin_fichier")
            if not chemin_fichier:
                return {"status": "erreur", "message": "Le paramètre 'chemin_fichier' est manquant."}
            resultat_analyse = self.analyser_fichier_markdown(chemin_fichier)
            if resultat_analyse:
                resultat_filtré = resultat_analyse.copy()
                resultat_filtré.pop("sections_brutes", None) 
                return {"status": "succes", "resultat": resultat_filtré}
            else:
                return {"status": "erreur", "message": f"Échec de l'analyse du fichier Markdown {chemin_fichier}."}
        
        elif task_name == "extraire_version_documentee":
            chemin_fichier = task_params.get("chemin_fichier")
            if not chemin_fichier:
                return {"status": "erreur", "message": "Le paramètre 'chemin_fichier' est manquant."}
            version = self.extraire_version_documentee(chemin_fichier)
            if version:
                return {"status": "succes", "version_documentee": version}
            else:
                return {"status": "erreur", "message": f"Impossible d'extraire la version du fichier {chemin_fichier}."}
            
        else:
            self.logger.warning(f"Tâche inconnue : {task_name}")
            return {"status": "erreur", "message": f"Tâche inconnue : {task_name}"}

if __name__ == '__main__':
    import json
    from pathlib import Path 
    
    # Configuration du logging pour les tests rapides
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    main_logger = logging.getLogger(__name__) # Logger pour ce bloc __main__
    
    analyseur_md = AgentAnalyseurDocumentationMarkdown()
    main_logger.info(f"Agent {analyseur_md.__class__.__name__} version {analyseur_md.__version__} instancié pour test.")

    dummy_md_path = Path("dummy_test_agent_doc.md")
    # dummy_content utilise des vrais sauts de ligne Python grâce aux triples guillemets
    dummy_content = """# Agent de Test Factice Alpha

**Version :** 1.2.3-beta (v1.2.3)

## Description

Ceci est la description de l'agent de test factice Alpha.
Il est conçu pour illustrer l'analyse de documentation Markdown.

```python
# Ceci est un bloc de code Python
def hello(name):
    print(f"Hello, {name}!")

hello("AADM")
```

## Objectifs

- Objectif principal 1
- Objectif secondaire 2
    - Sous-objectif 2.1 (ne sera pas extrait tel quel par _parse_list_items simple)

## Capacités

L'agent peut effectuer les tâches suivantes :

*   **Tâche 1 : Faire quelque chose**
    *   Sous-tâche 1.1 (sera extrait comme item séparé si commence par '*' ou '-')
    *   Sous-tâche 1.2
*   Tâche 2 : Analyser autre chose
*   Tâche 3 : Générer un rapport `important`

Ceci n'est pas un item de liste.

```text
Un autre bloc de code, sans langage spécifié.
Avec plusieurs lignes.
```

## Dépendances

-   Bibliothèque Externe (v4.5+)
-   Module Interne `utils.parser`

### Notes sur les dépendances
    Les dépendances sont cruciales.
    ```json
    { "key": "value", "another": 123 }
    ```

## Dépannage
    Contenu de la section dépannage.

## Tâches Spécifiques (Taches)
- Tâche A
- Tâche B
"""
    with open(dummy_md_path, "w", encoding="utf-8") as f:
        f.write(dummy_content)
    main_logger.info(f"Fichier Markdown factice '{dummy_md_path}' créé pour le test.")

    print(f"\n--- Capacités de l'agent AADM ({analyseur_md.__class__.__name__} v{analyseur_md.__version__}) ---")
    print(json.dumps(analyseur_md.get_capabilities(), indent=2, ensure_ascii=False))

    print(f"\n--- Analyse du fichier Markdown DUMMY : {dummy_md_path} ---")
    resultat_analyse_complet = analyseur_md.analyser_fichier_markdown(str(dummy_md_path))
    
    if resultat_analyse_complet:
        main_logger.info("Analyse directe du fichier MD factice réussie.")
        print(f"Titre Principal: {resultat_analyse_complet.get('titre_principal')}")
        print(f"Version Documentée: {resultat_analyse_complet.get('version_documentee')}")
        print(f"Description (repr): {resultat_analyse_complet.get('description_agent')!r}")
        print(f"Objectifs ({len(resultat_analyse_complet.get('objectifs_agent', []))} items): {resultat_analyse_complet.get('objectifs_agent')}")
        print(f"Capacités ({len(resultat_analyse_complet.get('capacites_agent', []))} items): {resultat_analyse_complet.get('capacites_agent')}")
        print(f"Dépendances ({len(resultat_analyse_complet.get('dependances_agent', []))} items): {resultat_analyse_complet.get('dependances_agent')}")
        
        blocs_code_extraits = resultat_analyse_complet.get('blocs_code', [])
        print(f"Blocs de code ({len(blocs_code_extraits)} items):")
        for i, bloc in enumerate(blocs_code_extraits):
            print(f"  Bloc {i+1} (lang: '{bloc.get('langage', 'non spécifié')}'):")
            contenu_bloc_indenté = "\\n    ".join(bloc.get('contenu', '').splitlines())
            print(f"    {contenu_bloc_indenté}") 
        
    else:
        main_logger.error("Échec de l'analyse directe du fichier MD factice.")
        print(f"Échec de l'analyse MD DUMMY.")

    print(f"\n--- Test de la tâche 'extraire_version_documentee' pour DUMMY : {dummy_md_path} ---")
    resultat_version_task = analyseur_md.execute_task("extraire_version_documentee", {"chemin_fichier": str(dummy_md_path)})
    print(json.dumps(resultat_version_task, indent=2, ensure_ascii=False))
    
    print(f"\n--- Test de la tâche 'analyser_fichier_markdown' (résultat filtré) pour DUMMY : {dummy_md_path} ---")
    resultat_analyser_task = analyseur_md.execute_task("analyser_fichier_markdown", {"chemin_fichier": str(dummy_md_path)})
    print(json.dumps(resultat_analyser_task, indent=2, ensure_ascii=False))

    print(f"\n--- Test avec un fichier Markdown inexistant ---")
    resultat_inexistant_task = analyseur_md.execute_task("analyser_fichier_markdown", {"chemin_fichier": "fichier_md_qui_n_existe_pas.md"})
    print(json.dumps(resultat_inexistant_task, indent=2, ensure_ascii=False))

    try:
        if dummy_md_path.exists():
            dummy_md_path.unlink()
            main_logger.info(f"Fichier '{dummy_md_path}' supprimé.")
    except Exception as e:
        main_logger.error(f"Erreur lors de la suppression du fichier '{dummy_md_path}': {e}")

    main_logger.info("Tests du bloc __main__ terminés.")