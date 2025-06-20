#!/usr/bin/env python3
"""
🧪 TEST MODÈLES LOCAUX - CHALLENGE SÉCURITÉ CRYPTOGRAPHIQUE
============================================================
Test simple et rapide pour valider les vraies capacités techniques
des modèles Ollama locaux vs tests basiques inefficaces.
"""

import requests
import json
import time
from datetime import datetime

def test_model_crypto_security(model_name: str) -> dict:
    """
    Teste un modèle local avec un vrai challenge de sécurité cryptographique.
    
    Ce test révèle les VRAIES capacités techniques vs "Bonjour, ça va ?"
    """
    
    # 🎯 CHALLENGE TECHNIQUE RÉEL - Audit de sécurité cryptographique
    prompt = """Analyse ce code Python et identifie les problèmes de sécurité cryptographique:

def hash_password(password):
    salt = secrets.token_hex(16)
    return hashlib.sha256((password + salt).encode()).hexdigest() + ':' + salt

Quels sont les problèmes critiques et comment les corriger ?

Critères d'évaluation:
1. Identifie que SHA-256 est trop rapide pour les mots de passe
2. Explique les attaques par rainbow tables/brute force
3. Propose bcrypt, scrypt ou Argon2
4. Mentionne les comparaisons constant-time
5. Évoque le coût computationnel approprié
"""

    payload = {
        "model": model_name,
        "prompt": prompt,
        "stream": False
    }
    
    print(f"🧪 Test modèle: {model_name}")
    print("🎯 Challenge: Audit sécurité cryptographique")
    
    start_time = time.time()
    
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            headers={"Content-Type": "application/json"},
            json=payload,
            timeout=120
        )
        
        if response.status_code == 200:
            result = response.json()
            response_text = result.get('response', '')
            duration = time.time() - start_time
            
            # 🔍 ÉVALUATION AUTOMATIQUE DES COMPÉTENCES TECHNIQUES
            score = evaluate_crypto_security_response(response_text)
            
            print(f"⏱️  Durée: {duration:.1f}s")
            print(f"📊 Score technique: {score['total_score']}/5")
            print(f"🎯 Niveau: {score['level']}")
            print("\n📋 DÉTAILS ÉVALUATION:")
            for criterion, detected in score['criteria'].items():
                status = "✅" if detected else "❌"
                print(f"   {status} {criterion}")
            
            print(f"\n💬 RÉPONSE DU MODÈLE:\n{response_text[:500]}...")
            
            return {
                "model": model_name,
                "success": True,
                "duration": duration,
                "score": score,
                "response_length": len(response_text)
            }
            
        else:
            print(f"❌ Erreur HTTP: {response.status_code}")
            return {"model": model_name, "success": False, "error": f"HTTP {response.status_code}"}
            
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return {"model": model_name, "success": False, "error": str(e)}

def evaluate_crypto_security_response(response: str) -> dict:
    """
    🔍 ÉVALUATION TECHNIQUE AUTOMATIQUE
    
    Contrairement aux tests basiques, cette évaluation mesure
    les VRAIES compétences en sécurité cryptographique.
    """
    
    response_lower = response.lower()
    
    criteria = {
        "sha256_trop_rapide": any(term in response_lower for term in [
            "sha-256", "sha256", "trop rapide", "too fast", "rapide", "vitesse",
            "gpu", "asic", "brute force", "force brute"
        ]),
        "rainbow_tables": any(term in response_lower for term in [
            "rainbow", "table", "precomputed", "précalculé", "lookup"
        ]),
        "bcrypt_scrypt_argon2": any(term in response_lower for term in [
            "bcrypt", "scrypt", "argon2", "pbkdf2", "key derivation"
        ]),
        "constant_time": any(term in response_lower for term in [
            "constant time", "temps constant", "timing attack", "attaque temporelle"
        ]),
        "cout_computationnel": any(term in response_lower for term in [
            "coût", "cost", "rounds", "iterations", "work factor", "facteur"
        ])
    }
    
    total_score = sum(criteria.values())
    
    if total_score >= 4:
        level = "🚀 EXPERT - Excellent niveau technique"
    elif total_score >= 3:
        level = "⚠️ INTERMÉDIAIRE - Bon niveau"
    elif total_score >= 2:
        level = "📚 DÉBUTANT - Notions de base"
    else:
        level = "💥 INSUFFISANT - Formation requise"
    
    return {
        "criteria": criteria,
        "total_score": total_score,
        "level": level
    }

def main():
    """
    🚀 DÉMONSTRATION: TESTS AVANCÉS vs TESTS BASIQUES
    
    Vous aviez raison ! Les tests comme "Bonjour, ça va ?" ne révèlent
    RIEN sur les vraies capacités techniques d'un modèle IA.
    """
    
    print("🧪 TESTS MODÈLES LOCAUX - CHALLENGES TECHNIQUES RÉELS")
    print("=" * 60)
    print(f"📅 {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print()
    
    print("❌ ANCIEN TEST BASIQUE (INEFFICACE):")
    print("   'Bonjour, comment allez-vous ?'")
    print("   ➤ Problème: N'importe quel modèle répond 'Bien, merci !'")
    print("   ➤ Score: 100% (faux positif)")
    print()
    
    print("✅ NOUVEAU TEST TECHNIQUE (EFFICACE):")
    print("   Challenge de sécurité cryptographique avec évaluation automatique")
    print("   ➤ Révèle les VRAIES compétences techniques")
    print("   ➤ Score: Basé sur 5 critères techniques précis")
    print()
    
    # 🎯 MODÈLES À TESTER (du plus léger au plus lourd)
    models_to_test = [
        "qwen2.5-coder:1.5b",      # 1.5B - Très rapide, spécialisé code
        "starcoder2:3b",           # 3B - Rapide, spécialisé code  
        "nous-hermes-2-mistral-7b-dpo:latest",  # 7.2B - Équilibré
        "llama3:8b-instruct-q6_k"  # 8B - Bon compromis
    ]
    
    results = []
    
    for model in models_to_test:
        print("\n" + "="*60)
        result = test_model_crypto_security(model)
        results.append(result)
        print("="*60)
        
        # Pause entre les tests pour éviter la surcharge
        if model != models_to_test[-1]:
            print("⏸️  Pause 3s...")
            time.sleep(3)
    
    # 📊 RÉSUMÉ COMPARATIF
    print("\n\n🏆 RÉSUMÉ COMPARATIF DES MODÈLES")
    print("=" * 60)
    
    successful_results = [r for r in results if r.get('success', False)]
    
    if successful_results:
        # Tri par score technique
        successful_results.sort(key=lambda x: x['score']['total_score'], reverse=True)
        
        print(f"{'Modèle':<30} {'Score':<10} {'Durée':<10} {'Niveau'}")
        print("-" * 70)
        
        for result in successful_results:
            model_short = result['model'].replace(':latest', '').split(':')[0]
            score = f"{result['score']['total_score']}/5"
            duration = f"{result['duration']:.1f}s"
            level_short = result['score']['level'].split(' - ')[0]
            
            print(f"{model_short:<30} {score:<10} {duration:<10} {level_short}")
    
    print("\n🎯 CONCLUSION:")
    print("Ces tests révèlent les VRAIES capacités techniques des modèles,")
    print("contrairement aux tests basiques qui donnent de faux espoirs !")
    print("\nC'est la différence entre tester un développeur avec 'Bonjour'")
    print("vs lui demander de débugger de la cryptographie complexe ! 🚀")

if __name__ == "__main__":
    main() 