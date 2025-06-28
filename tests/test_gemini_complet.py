#!/usr/bin/env python3
"""
Test simple et direct de Google Gemini avec diffrents types de tches.
"""

import os
import httpx
import json
import time
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

class GeminiTester:
    """Testeur simple pour Google Gemini."""
    
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY non trouve dans .env")
    
    def call_gemini(self, prompt: str, model: str = "gemini-1.5-flash") -> dict:
        """Appel direct  l'API Gemini."""
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={self.api_key}"
        
        payload = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }],
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 1000,
                "topP": 0.9
            }
        }
        
        try:
            with httpx.Client(timeout=60.0) as client:
                response = client.post(url, json=payload)
            
            if response.status_code == 200:
                result = response.json()
                if "candidates" in result and result["candidates"]:
                    text = result["candidates"][0]["content"]["parts"][0]["text"]
                    return {
                        "success": True,
                        "text": text,
                        "model": model
                    }
                else:
                    return {
                        "success": False,
                        "error": "Rponse inattendue",
                        "response": result
                    }
            else:
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}",
                    "response": response.text
                }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def test_creative_task(self):
        """Test une tche crative."""
        print(" Test cratif: criture d'un pome")
        print("-" * 40)
        
        prompt = """cris un petit pome de 4 vers sur l'intelligence artificielle.
Le pome doit tre optimiste et parler de collaboration entre humains et IA."""
        
        start_time = time.time()
        result = self.call_gemini(prompt)
        duration = time.time() - start_time
        
        if result["success"]:
            print(f"[CHECK] Succs en {duration:.2f}s")
            print(f" Pome gnr:\n{result['text']}")
        else:
            print(f"[CROSS] chec: {result['error']}")
        
        return result["success"]
    
    def test_analysis_task(self):
        """Test une tche d'analyse."""
        print("\n[CHART] Test analytique: Analyse comparative")
        print("-" * 40)
        
        prompt = """Analyse les avantages et inconvnients du tltravail.
Prsente ta rponse sous forme de tableau avec:
- Avantages pour l'employ
- Inconvnients pour l'employ  
- Avantages pour l'employeur
- Inconvnients pour l'employeur"""
        
        start_time = time.time()
        result = self.call_gemini(prompt)
        duration = time.time() - start_time
        
        if result["success"]:
            print(f"[CHECK] Succs en {duration:.2f}s")
            print(f" Analyse gnre:\n{result['text'][:300]}...")
        else:
            print(f"[CROSS] chec: {result['error']}")
        
        return result["success"]
    
    def test_technical_task(self):
        """Test une tche technique."""
        print("\n[TOOL] Test technique: Explication concept")
        print("-" * 40)
        
        prompt = """Explique le concept de "blockchain" en termes simples.
Utilise une analogie avec la vie quotidienne et donne 3 exemples d'utilisation pratique."""
        
        start_time = time.time()
        result = self.call_gemini(prompt)
        duration = time.time() - start_time
        
        if result["success"]:
            print(f"[CHECK] Succs en {duration:.2f}s")
            print(f" Explication gnre:\n{result['text'][:300]}...")
        else:
            print(f"[CROSS] chec: {result['error']}")
        
        return result["success"]
    
    def test_multilingual_task(self):
        """Test une tche multilingue."""
        print("\n Test multilingue: Traduction et rsum")
        print("-" * 40)
        
        prompt = """Traduis ce texte en anglais et en espagnol, puis fais un rsum en franais:

"L'intelligence artificielle transforme notre manire de travailler. Elle automatise les tches rptitives et permet aux humains de se concentrer sur des activits cratives et stratgiques."

Format de rponse:
- Anglais: [traduction]
- Espagnol: [traduction] 
- Rsum franais: [rsum en une phrase]"""
        
        start_time = time.time()
        result = self.call_gemini(prompt)
        duration = time.time() - start_time
        
        if result["success"]:
            print(f"[CHECK] Succs en {duration:.2f}s")
            print(f" Traductions gnres:\n{result['text']}")
        else:
            print(f"[CROSS] chec: {result['error']}")
        
        return result["success"]
    
    def test_coding_task(self):
        """Test une tche de programmation."""
        print("\n Test programmation: Gnration de code")
        print("-" * 40)
        
        prompt = """cris une fonction Python qui:
1. Prend une liste de nombres en paramtre
2. Calcule la moyenne
3. Retourne True si la moyenne est suprieure  50, False sinon
4. Gre le cas d'une liste vide

Inclus des commentaires et un exemple d'utilisation."""
        
        start_time = time.time()
        result = self.call_gemini(prompt)
        duration = time.time() - start_time
        
        if result["success"]:
            print(f"[CHECK] Succs en {duration:.2f}s")
            print(f" Code gnr:\n{result['text']}")
        else:
            print(f"[CROSS] chec: {result['error']}")
        
        return result["success"]
    
    def run_all_tests(self):
        """Excute tous les tests."""
        print("[ROCKET] TESTS COMPLETS DE GOOGLE GEMINI")
        print("=" * 60)
        
        tests = [
            ("Cratif", self.test_creative_task),
            ("Analytique", self.test_analysis_task),
            ("Technique", self.test_technical_task),
            ("Multilingue", self.test_multilingual_task),
            ("Programmation", self.test_coding_task)
        ]
        
        results = {}
        total_start = time.time()
        
        for test_name, test_func in tests:
            try:
                success = test_func()
                results[test_name] = success
                
                # Pause entre les tests pour viter le rate limiting
                time.sleep(2)
                
            except Exception as e:
                print(f"[CROSS] Erreur dans le test {test_name}: {e}")
                results[test_name] = False
        
        total_time = time.time() - total_start
        
        # Rsum final
        print("\n" + "=" * 60)
        print("[CLIPBOARD] RSUM DES TESTS GEMINI")
        print("=" * 60)
        
        successful_tests = sum(1 for success in results.values() if success)
        total_tests = len(results)
        
        print(f"[CHART] Rsultats: {successful_tests}/{total_tests} tests russis")
        print(f" Temps total: {total_time:.2f}s")
        print(f"[TARGET] Taux de succs: {(successful_tests/total_tests)*100:.1f}%")
        
        print("\n[CLIPBOARD] Dtail par test:")
        for test_name, success in results.items():
            status = "[CHECK]" if success else "[CROSS]"
            print(f"   {status} {test_name}")
        
        if successful_tests == total_tests:
            print("\n EXCELLENT! Gemini fonctionne parfaitement!")
            print("[BULB] Gemini est prt pour:")
            print("   - Tches cratives (pomes, histoires)")
            print("   - Analyses et rsums")
            print("   - Explications techniques")
            print("   - Traductions multilingues")
            print("   - Gnration de code")
        else:
            print(f"\n {total_tests - successful_tests} test(s) ont chou")
            print("[BULB] Vrifiez:")
            print("   - La validit de votre cl GOOGLE_API_KEY")
            print("   - Les quotas et limites de votre compte")
            print("   - La connexion internet")
        
        return results

def main():
    """Point d'entre principal."""
    try:
        tester = GeminiTester()
        results = tester.run_all_tests()
        
        # Sauvegarder les rsultats
        with open("gemini_test_results.json", "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"\n Rsultats sauvegards dans gemini_test_results.json")
        
    except ValueError as e:
        print(f"[CROSS] Erreur de configuration: {e}")
        print("[BULB] Assurez-vous que GOOGLE_API_KEY est dfinie dans .env")
    except Exception as e:
        print(f"[CROSS] Erreur inattendue: {e}")

if __name__ == "__main__":
    main()




