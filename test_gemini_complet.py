#!/usr/bin/env python3
"""
Test simple et direct de Google Gemini avec différents types de tâches.
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
            raise ValueError("GOOGLE_API_KEY non trouvée dans .env")
    
    def call_gemini(self, prompt: str, model: str = "gemini-1.5-flash") -> dict:
        """Appel direct à l'API Gemini."""
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
                        "error": "Réponse inattendue",
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
        """Test une tâche créative."""
        print("🎨 Test créatif: Écriture d'un poème")
        print("-" * 40)
        
        prompt = """Écris un petit poème de 4 vers sur l'intelligence artificielle.
Le poème doit être optimiste et parler de collaboration entre humains et IA."""
        
        start_time = time.time()
        result = self.call_gemini(prompt)
        duration = time.time() - start_time
        
        if result["success"]:
            print(f"✅ Succès en {duration:.2f}s")
            print(f"📝 Poème généré:\n{result['text']}")
        else:
            print(f"❌ Échec: {result['error']}")
        
        return result["success"]
    
    def test_analysis_task(self):
        """Test une tâche d'analyse."""
        print("\n📊 Test analytique: Analyse comparative")
        print("-" * 40)
        
        prompt = """Analyse les avantages et inconvénients du télétravail.
Présente ta réponse sous forme de tableau avec:
- Avantages pour l'employé
- Inconvénients pour l'employé  
- Avantages pour l'employeur
- Inconvénients pour l'employeur"""
        
        start_time = time.time()
        result = self.call_gemini(prompt)
        duration = time.time() - start_time
        
        if result["success"]:
            print(f"✅ Succès en {duration:.2f}s")
            print(f"📝 Analyse générée:\n{result['text'][:300]}...")
        else:
            print(f"❌ Échec: {result['error']}")
        
        return result["success"]
    
    def test_technical_task(self):
        """Test une tâche technique."""
        print("\n🔧 Test technique: Explication concept")
        print("-" * 40)
        
        prompt = """Explique le concept de "blockchain" en termes simples.
Utilise une analogie avec la vie quotidienne et donne 3 exemples d'utilisation pratique."""
        
        start_time = time.time()
        result = self.call_gemini(prompt)
        duration = time.time() - start_time
        
        if result["success"]:
            print(f"✅ Succès en {duration:.2f}s")
            print(f"📝 Explication générée:\n{result['text'][:300]}...")
        else:
            print(f"❌ Échec: {result['error']}")
        
        return result["success"]
    
    def test_multilingual_task(self):
        """Test une tâche multilingue."""
        print("\n🌍 Test multilingue: Traduction et résumé")
        print("-" * 40)
        
        prompt = """Traduis ce texte en anglais et en espagnol, puis fais un résumé en français:

"L'intelligence artificielle transforme notre manière de travailler. Elle automatise les tâches répétitives et permet aux humains de se concentrer sur des activités créatives et stratégiques."

Format de réponse:
- Anglais: [traduction]
- Espagnol: [traduction] 
- Résumé français: [résumé en une phrase]"""
        
        start_time = time.time()
        result = self.call_gemini(prompt)
        duration = time.time() - start_time
        
        if result["success"]:
            print(f"✅ Succès en {duration:.2f}s")
            print(f"📝 Traductions générées:\n{result['text']}")
        else:
            print(f"❌ Échec: {result['error']}")
        
        return result["success"]
    
    def test_coding_task(self):
        """Test une tâche de programmation."""
        print("\n💻 Test programmation: Génération de code")
        print("-" * 40)
        
        prompt = """Écris une fonction Python qui:
1. Prend une liste de nombres en paramètre
2. Calcule la moyenne
3. Retourne True si la moyenne est supérieure à 50, False sinon
4. Gère le cas d'une liste vide

Inclus des commentaires et un exemple d'utilisation."""
        
        start_time = time.time()
        result = self.call_gemini(prompt)
        duration = time.time() - start_time
        
        if result["success"]:
            print(f"✅ Succès en {duration:.2f}s")
            print(f"💻 Code généré:\n{result['text']}")
        else:
            print(f"❌ Échec: {result['error']}")
        
        return result["success"]
    
    def run_all_tests(self):
        """Exécute tous les tests."""
        print("🚀 TESTS COMPLETS DE GOOGLE GEMINI")
        print("=" * 60)
        
        tests = [
            ("Créatif", self.test_creative_task),
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
                
                # Pause entre les tests pour éviter le rate limiting
                time.sleep(2)
                
            except Exception as e:
                print(f"❌ Erreur dans le test {test_name}: {e}")
                results[test_name] = False
        
        total_time = time.time() - total_start
        
        # Résumé final
        print("\n" + "=" * 60)
        print("📋 RÉSUMÉ DES TESTS GEMINI")
        print("=" * 60)
        
        successful_tests = sum(1 for success in results.values() if success)
        total_tests = len(results)
        
        print(f"📊 Résultats: {successful_tests}/{total_tests} tests réussis")
        print(f"⏱️ Temps total: {total_time:.2f}s")
        print(f"🎯 Taux de succès: {(successful_tests/total_tests)*100:.1f}%")
        
        print("\n📋 Détail par test:")
        for test_name, success in results.items():
            status = "✅" if success else "❌"
            print(f"   {status} {test_name}")
        
        if successful_tests == total_tests:
            print("\n🎉 EXCELLENT! Gemini fonctionne parfaitement!")
            print("💡 Gemini est prêt pour:")
            print("   - Tâches créatives (poèmes, histoires)")
            print("   - Analyses et résumés")
            print("   - Explications techniques")
            print("   - Traductions multilingues")
            print("   - Génération de code")
        else:
            print(f"\n⚠️ {total_tests - successful_tests} test(s) ont échoué")
            print("💡 Vérifiez:")
            print("   - La validité de votre clé GOOGLE_API_KEY")
            print("   - Les quotas et limites de votre compte")
            print("   - La connexion internet")
        
        return results

def main():
    """Point d'entrée principal."""
    try:
        tester = GeminiTester()
        results = tester.run_all_tests()
        
        # Sauvegarder les résultats
        with open("gemini_test_results.json", "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"\n💾 Résultats sauvegardés dans gemini_test_results.json")
        
    except ValueError as e:
        print(f"❌ Erreur de configuration: {e}")
        print("💡 Assurez-vous que GOOGLE_API_KEY est définie dans .env")
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")

if __name__ == "__main__":
    main()
