#!/usr/bin/env python3
"""
[SEARCH] VALIDATION JOURNAUX COMMUNICATION IA-1 & IA-2
Validation automatique des journaux quotidiens et communication inter-IA
Phase 4 - Excellence & Innovation
"""

import os
import re
import json
import yaml
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import argparse

class JournalValidator:
    """Validateur des journaux de communication IA-1 & IA-2"""
    
    def __init__(self, journals_dir: str = "journals"):
        self.journals_dir = Path(journals_dir)
        self.ia1_dir = self.journals_dir / "ia1"
        self.ia2_dir = self.journals_dir / "ia2"
        self.shared_dir = self.journals_dir / "shared"
        
        # Patterns de validation
        self.reference_patterns = {
            'task': r'PHASE4-IA[12]-S4[12]-[A-Z-]+',
            'message': r'PHASE4-MSG-IA[12]-TO-IA[12]-\d{3}-[A-Z]+',
            'blocker': r'PHASE4-BLOCKER-IA[12]-\d{3}',
            'joint': r'PHASE4-JOINT-[A-Z-]+'
        }
        
        # Sections obligatoires
        self.required_sections = {
            'ia1': [
                "OBJECTIFS JOUR",
                "RALISATIONS COMPLTES", 
                "EN COURS",
                "MTRIQUES JOUR",
                "OBJECTIFS DEMAIN",
                "MESSAGES POUR IA-2"
            ],
            'ia2': [
                "OBJECTIFS JOUR",
                "RALISATIONS COMPLTES", 
                "EN COURS", 
                "MTRIQUES JOUR",
                "OBJECTIFS DEMAIN",
                "MESSAGES POUR IA-1"
            ]
        }
        
        self.validation_results = {
            'journals_validated': 0,
            'errors': [],
            'warnings': [],
            'cross_references': 0,
            'missing_references': [],
            'communication_health': {},
            'compliance_score': 0.0
        }

    def validate_journal_structure(self, journal_path: Path, ia_type: str) -> Dict:
        """Valide la structure d'un journal"""
        result = {
            'valid': True,
            'missing_sections': [],
            'invalid_references': [],
            'cross_references_found': 0,
            'messages_count': 0
        }
        
        if not journal_path.exists():
            result['valid'] = False
            result['missing_sections'] = ['FILE_NOT_FOUND']
            return result
            
        try:
            with open(journal_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Vrifier sections obligatoires
            required = self.required_sections[ia_type]
            for section in required:
                if section not in content:
                    result['missing_sections'].append(section)
                    result['valid'] = False
                    
            # Valider rfrences
            references = self._extract_references(content)
            for ref in references:
                if not self._validate_reference_format(ref):
                    result['invalid_references'].append(ref)
                    result['valid'] = False
                    
            # Compter rfrences croises
            other_ia = 'IA2' if ia_type == 'ia1' else 'IA1'
            cross_refs = [r for r in references if other_ia in r]
            result['cross_references_found'] = len(cross_refs)
            
            # Compter messages
            messages = re.findall(r'MSG-\d{3}', content)
            result['messages_count'] = len(messages)
            
        except Exception as e:
            result['valid'] = False
            result['error'] = str(e)
            
        return result

    def _extract_references(self, content: str) -> List[str]:
        """Extrait toutes les rfrences du contenu"""
        references = []
        for pattern in self.reference_patterns.values():
            references.extend(re.findall(pattern, content))
        return references

    def _validate_reference_format(self, reference: str) -> bool:
        """Valide le format d'une rfrence"""
        for pattern in self.reference_patterns.values():
            if re.match(pattern, reference):
                return True
        return False

    def validate_cross_references(self, day: str) -> Dict:
        """Valide les rfrences croises entre IA-1 et IA-2"""
        result = {
            'valid': True,
            'ia1_references_to_ia2': [],
            'ia2_references_to_ia1': [],
            'missing_cross_refs': [],
            'orphan_references': []
        }
        
        ia1_journal = self.ia1_dir / f"JOURNAL-IA1-{day}.md"
        ia2_journal = self.ia2_dir / f"JOURNAL-IA2-{day}.md"
        
        if not (ia1_journal.exists() and ia2_journal.exists()):
            result['valid'] = False
            result['missing_cross_refs'] = ['JOURNALS_NOT_FOUND']
            return result
            
        try:
            # Lire les journaux
            with open(ia1_journal, 'r', encoding='utf-8') as f:
                ia1_content = f.read()
            with open(ia2_journal, 'r', encoding='utf-8') as f:
                ia2_content = f.read()
                
            # Extraire rfrences
            ia1_refs = self._extract_references(ia1_content)
            ia2_refs = self._extract_references(ia2_content)
            
            # Rfrences croises IA1  IA2
            ia1_to_ia2 = [r for r in ia1_refs if 'IA2' in r]
            result['ia1_references_to_ia2'] = ia1_to_ia2
            
            # Rfrences croises IA2  IA1  
            ia2_to_ia1 = [r for r in ia2_refs if 'IA1' in r]
            result['ia2_references_to_ia1'] = ia2_to_ia1
            
            # Vrifier cohrence des rfrences
            self._check_reference_consistency(ia1_content, ia2_content, result)
            
        except Exception as e:
            result['valid'] = False
            result['error'] = str(e)
            
        return result

    def _check_reference_consistency(self, ia1_content: str, ia2_content: str, result: Dict):
        """Vrifie la cohrence des rfrences entre journaux"""
        # Extraire les tches mentionnes
        ia1_tasks = re.findall(r'PHASE4-IA1-S4[12]-[A-Z-]+', ia1_content)
        ia2_tasks = re.findall(r'PHASE4-IA2-S4[12]-[A-Z-]+', ia2_content)
        
        # Vrifier que les tches IA-2 mentionnes par IA-1 existent
        ia1_mentions_ia2 = re.findall(r'PHASE4-IA2-S4[12]-[A-Z-]+', ia1_content)
        for task in ia1_mentions_ia2:
            if task not in ia2_tasks:
                result['orphan_references'].append(f"IA1 references {task} but not found in IA2")
                
        # Vrifier que les tches IA-1 mentionnes par IA-2 existent
        ia2_mentions_ia1 = re.findall(r'PHASE4-IA1-S4[12]-[A-Z-]+', ia2_content)
        for task in ia2_mentions_ia1:
            if task not in ia1_tasks:
                result['orphan_references'].append(f"IA2 references {task} but not found in IA1")

    def validate_message_flow(self, day: str) -> Dict:
        """Valide le flux de messages entre IA-1 et IA-2"""
        result = {
            'valid': True,
            'messages_ia1_to_ia2': [],
            'messages_ia2_to_ia1': [],
            'response_times': {},
            'unresponded_critical': [],
            'communication_score': 0.0
        }
        
        messages_log = self.shared_dir / "MESSAGES-LOG.md"
        if not messages_log.exists():
            result['valid'] = False
            result['error'] = 'MESSAGES_LOG_NOT_FOUND'
            return result
            
        try:
            with open(messages_log, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Extraire messages du jour
            day_section = self._extract_day_section(content, day)
            if not day_section:
                result['valid'] = False
                result['error'] = f'DAY_SECTION_NOT_FOUND_{day}'
                return result
                
            # Analyser messages IA1  IA2
            ia1_messages = self._extract_messages(day_section, 'IA-1', 'IA-2')
            result['messages_ia1_to_ia2'] = ia1_messages
            
            # Analyser messages IA2  IA1
            ia2_messages = self._extract_messages(day_section, 'IA-2', 'IA-1')
            result['messages_ia2_to_ia1'] = ia2_messages
            
            # Calculer temps de rponse
            self._calculate_response_times(ia1_messages, ia2_messages, result)
            
            # Vrifier messages critiques non rpondus
            self._check_critical_messages(ia1_messages, ia2_messages, result)
            
            # Score communication
            result['communication_score'] = self._calculate_communication_score(result)
            
        except Exception as e:
            result['valid'] = False
            result['error'] = str(e)
            
        return result

    def _extract_day_section(self, content: str, day: str) -> str:
        """Extrait la section d'un jour spcifique du log"""
        # Convertir J31 en format date
        day_num = int(day[1:])  # Enlever 'J'
        base_date = datetime(2025, 1, 27)  # J31 = 27 Janvier 2025
        target_date = base_date + timedelta(days=day_num - 31)
        date_str = target_date.strftime("%d %B %Y")
        
        pattern = f"## [CLIPBOARD] \\*\\*{day} - {date_str}\\*\\*"
        sections = re.split(r'## [CLIPBOARD] \*\*J\d+', content)
        
        for section in sections:
            if date_str in section:
                return section
        return ""

    def _extract_messages(self, content: str, from_ia: str, to_ia: str) -> List[Dict]:
        """Extrait les messages d'une IA vers une autre"""
        messages = []
        pattern = f"### \\*\\*Messages {from_ia}  {to_ia}\\*\\*"
        
        if pattern in content:
            section_start = content.find(pattern)
            section_end = content.find("### **Messages", section_start + 1)
            if section_end == -1:
                section_end = len(content)
                
            section = content[section_start:section_end]
            
            # Extraire chaque message
            msg_pattern = r'#### \*\*(\d{2}:\d{2}) - (MSG-\d{3}) : (.+?)\*\*'
            matches = re.finditer(msg_pattern, section)
            
            for match in matches:
                time, msg_id, subject = match.groups()
                
                # Extraire dtails YAML
                yaml_start = section.find('```yaml', match.end())
                yaml_end = section.find('```', yaml_start + 1)
                
                if yaml_start != -1 and yaml_end != -1:
                    yaml_content = section[yaml_start + 7:yaml_end]
                    try:
                        msg_data = yaml.safe_load(yaml_content)
                        msg_data['time'] = time
                        msg_data['msg_id'] = msg_id
                        msg_data['subject'] = subject
                        messages.append(msg_data)
                    except yaml.YAMLError:
                        pass
                        
        return messages

    def _calculate_response_times(self, ia1_messages: List[Dict], ia2_messages: List[Dict], result: Dict):
        """Calcule les temps de rponse entre messages"""
        for ia1_msg in ia1_messages:
            if 'rfrence' in ia1_msg:
                ref = ia1_msg['rfrence']
                
                # Chercher rponse correspondante
                for ia2_msg in ia2_messages:
                    if ia2_msg.get('rponse_') == ref:
                        # Calculer temps de rponse
                        ia1_time = datetime.strptime(ia1_msg['time'], '%H:%M')
                        ia2_time = datetime.strptime(ia2_msg['time'], '%H:%M')
                        
                        if ia2_time > ia1_time:
                            response_time = (ia2_time - ia1_time).seconds // 60
                        else:
                            # Message rponse le jour suivant
                            response_time = (ia2_time + timedelta(days=1) - ia1_time).seconds // 60
                            
                        result['response_times'][ref] = response_time
                        break

    def _check_critical_messages(self, ia1_messages: List[Dict], ia2_messages: List[Dict], result: Dict):
        """Vrifie les messages critiques non rpondus"""
        critical_ia1 = [msg for msg in ia1_messages if msg.get('priorit') == ' CRITIQUE']
        
        for critical_msg in critical_ia1:
            ref = critical_msg.get('rfrence')
            responded = any(msg.get('rponse_') == ref for msg in ia2_messages)
            
            if not responded:
                result['unresponded_critical'].append(ref)

    def _calculate_communication_score(self, result: Dict) -> float:
        """Calcule le score de communication"""
        score = 100.0
        
        # Pnalits pour messages critiques non rpondus
        score -= len(result['unresponded_critical']) * 20
        
        # Pnalits pour temps de rponse
        for ref, time in result['response_times'].items():
            if 'CRITICAL' in ref and time > 120:  # > 2h pour critique
                score -= 15
            elif 'NORMAL' in ref and time > 240:  # > 4h pour normal
                score -= 10
                
        return max(0.0, score)

    def generate_validation_report(self, days: List[str]) -> Dict:
        """Gnre un rapport de validation complet"""
        report = {
            'validation_date': datetime.now().isoformat(),
            'days_validated': days,
            'overall_score': 0.0,
            'journal_validation': {},
            'cross_reference_validation': {},
            'communication_validation': {},
            'compliance_summary': {},
            'recommendations': []
        }
        
        total_score = 0.0
        valid_days = 0
        
        for day in days:
            day_report = {
                'day': day,
                'journal_ia1': {},
                'journal_ia2': {},
                'cross_references': {},
                'communication': {},
                'day_score': 0.0
            }
            
            # Validation journaux
            day_report['journal_ia1'] = self.validate_journal_structure(
                self.ia1_dir / f"JOURNAL-IA1-{day}.md", 'ia1'
            )
            day_report['journal_ia2'] = self.validate_journal_structure(
                self.ia2_dir / f"JOURNAL-IA2-{day}.md", 'ia2'
            )
            
            # Validation rfrences croises
            day_report['cross_references'] = self.validate_cross_references(day)
            
            # Validation communication
            day_report['communication'] = self.validate_message_flow(day)
            
            # Score du jour
            day_score = self._calculate_day_score(day_report)
            day_report['day_score'] = day_score
            
            if day_score > 0:
                total_score += day_score
                valid_days += 1
                
            report[f'day_{day}'] = day_report
            
        # Score global
        if valid_days > 0:
            report['overall_score'] = total_score / valid_days
            
        # Rsum compliance
        report['compliance_summary'] = self._generate_compliance_summary(report)
        
        # Recommandations
        report['recommendations'] = self._generate_recommendations(report)
        
        return report

    def _calculate_day_score(self, day_report: Dict) -> float:
        """Calcule le score d'un jour"""
        score = 100.0
        
        # Journal IA-1
        if not day_report['journal_ia1']['valid']:
            score -= 25
        else:
            score -= len(day_report['journal_ia1']['missing_sections']) * 5
            score -= len(day_report['journal_ia1']['invalid_references']) * 3
            
        # Journal IA-2  
        if not day_report['journal_ia2']['valid']:
            score -= 25
        else:
            score -= len(day_report['journal_ia2']['missing_sections']) * 5
            score -= len(day_report['journal_ia2']['invalid_references']) * 3
            
        # Rfrences croises
        if not day_report['cross_references']['valid']:
            score -= 20
        else:
            score -= len(day_report['cross_references']['orphan_references']) * 5
            
        # Communication
        if day_report['communication']['valid']:
            comm_score = day_report['communication']['communication_score']
            score = score * 0.7 + comm_score * 0.3
        else:
            score -= 30
            
        return max(0.0, score)

    def _generate_compliance_summary(self, report: Dict) -> Dict:
        """Gnre un rsum de compliance"""
        summary = {
            'total_journals': 0,
            'valid_journals': 0,
            'compliance_rate': 0.0,
            'critical_issues': [],
            'warnings': []
        }
        
        for key, day_report in report.items():
            if key.startswith('day_'):
                summary['total_journals'] += 2  # IA-1 + IA-2
                
                if day_report['journal_ia1']['valid']:
                    summary['valid_journals'] += 1
                else:
                    summary['critical_issues'].append(f"{day_report['day']}: Journal IA-1 invalide")
                    
                if day_report['journal_ia2']['valid']:
                    summary['valid_journals'] += 1
                else:
                    summary['critical_issues'].append(f"{day_report['day']}: Journal IA-2 invalide")
                    
        if summary['total_journals'] > 0:
            summary['compliance_rate'] = summary['valid_journals'] / summary['total_journals'] * 100
            
        return summary

    def _generate_recommendations(self, report: Dict) -> List[str]:
        """Gnre des recommandations d'amlioration"""
        recommendations = []
        
        # Analyser score global
        if report['overall_score'] < 70:
            recommendations.append(" Score global faible - Rvision urgente du processus de communication")
            
        # Analyser compliance
        compliance = report['compliance_summary']
        if compliance['compliance_rate'] < 90:
            recommendations.append(" Taux de compliance faible - Renforcer validation journaux")
            
        # Analyser communication
        comm_issues = 0
        for key, day_report in report.items():
            if key.startswith('day_'):
                if day_report['communication']['unresponded_critical']:
                    comm_issues += len(day_report['communication']['unresponded_critical'])
                    
        if comm_issues > 0:
            recommendations.append(f" {comm_issues} messages critiques non rpondus - Amliorer ractivit")
            
        # Recommandations spcifiques
        if not recommendations:
            recommendations.append("[CHECK] Communication excellente - Maintenir le niveau")
            
        return recommendations

def main():
    """Fonction principale"""
    parser = argparse.ArgumentParser(description='Validation journaux communication IA-1 & IA-2')
    parser.add_argument('--days', nargs='+', default=['J31'], 
                       help='Jours  valider (ex: J31 J32 J33)')
    parser.add_argument('--output', default='validation_report.json',
                       help='Fichier de sortie du rapport')
    parser.add_argument('--journals-dir', default='journals',
                       help='Rpertoire des journaux')
    
    args = parser.parse_args()
    
    # Initialiser validateur
    validator = JournalValidator(args.journals_dir)
    
    # Gnrer rapport
    print(f"[SEARCH] Validation journaux communication IA-1 & IA-2")
    print(f" Jours: {', '.join(args.days)}")
    print(f"[FOLDER] Rpertoire: {args.journals_dir}")
    
    report = validator.generate_validation_report(args.days)
    
    # Sauvegarder rapport
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
        
    # Afficher rsum
    print(f"\n[CHART] RSULTATS VALIDATION")
    print(f"Score global: {report['overall_score']:.1f}%")
    print(f"Compliance: {report['compliance_summary']['compliance_rate']:.1f}%")
    print(f"Journaux valides: {report['compliance_summary']['valid_journals']}/{report['compliance_summary']['total_journals']}")
    
    # Afficher recommandations
    print(f"\n[BULB] RECOMMANDATIONS:")
    for rec in report['recommendations']:
        print(f"  {rec}")
        
    print(f"\n[DOCUMENT] Rapport dtaill: {args.output}")
    
    # Code de sortie
    if report['overall_score'] >= 80:
        print("[CHECK] VALIDATION RUSSIE")
        return 0
    elif report['overall_score'] >= 60:
        print(" VALIDATION PARTIELLE")
        return 1
    else:
        print("[CROSS] VALIDATION CHEC")
        return 2

if __name__ == "__main__":
    exit(main()) 



