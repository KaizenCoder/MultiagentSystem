def get_capabilities(self) -> List[str]:
    """Retourne les capacités de l'agent de test"""
    return [
        "test_models_integration",
        "validate_ollama_connection", 
        "benchmark_performance",
        "test_agent_model_compatibility",
        "generate_validation_report"
    ] 