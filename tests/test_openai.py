from app.services.openai_client_service import openai_service

def test_openai_connection():
    print("Test connection Openai")
    print('-' * 40)

    # test connection
    if not openai_service.test_connection():
        print("Impossible de se connecter à OpenAI")
        return False
    
    # test generation simple
    print("\n Test génération planning simple ...")

    simple_prompt = """
    Génère un planning simple pour un tournoi de volley :
    
    - 4 équipes : Équipe 1, Équipe 2, Équipe 3, Équipe 4
    - 2 terrains disponibles
    - Type : round_robin
    - Date : 2024-06-15
    - Heure début : 09:00
    - Durée match : 10 minutes
    
    Retourne uniquement le JSON selon ton format habituel.
    """

    try:
        planning = openai_service.generate_planning(simple_prompt)

        print("✅ Planning généré !")
        print(f"Type: {planning.get('type_tournoi')}")
        print(f"Matchs: {len(planning.get('matchs_round_robin', []))}")
        print(f"Commentaires: {planning.get('commentaires', '')[:100]}...")

        return True
    except Exception as e:
        print(f"Erreur génération {e}")
        return False
    
if __name__ == "__main__":
    test_openai_connection()