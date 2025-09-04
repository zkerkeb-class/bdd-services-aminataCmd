from app.services.tournament_service import tournamentService

def insert_16_teams(tournament_id: str):
    teams_data = [
        {
            "name": "Les Smasheuses",
            "description": "Équipe féminine expérimentée",
            "tournament_id": tournament_id,
            "contact_email": "smasheuses@volley.com",
            "contact_phone": "0123456789",
            "skill_level": "expert",
            "notes": "Championnes régionales 2024"
        },
        {
            "name": "Thunder Spikes",
            "description": "Équipe masculine explosive",
            "tournament_id": tournament_id,
            "contact_email": "thunder@volley.com",
            "contact_phone": "0123456790",
            "skill_level": "expert",
            "notes": "Spécialistes du contre-attaque"
        },
        {
            "name": "Beach Volley Stars",
            "description": "Équipe beach volley reconvertie",
            "tournament_id": tournament_id,
            "contact_email": "beach@volley.com",
            "contact_phone": "0123456791",
            "skill_level": "confirme",
            "notes": "Excellente technique de réception"
        },
        {
            "name": "Net Crushers",
            "description": "Équipe universitaire dynamique",
            "tournament_id": tournament_id,
            "contact_email": "crushers@volley.com",
            "contact_phone": "0123456792",
            "skill_level": "confirme",
            "notes": "Étudiants en sport-études"
        },
        {
            "name": "Fire Birds",
            "description": "Équipe vétéran passionnée",
            "tournament_id": tournament_id,
            "contact_email": "firebirds@volley.com",
            "contact_phone": "0123456793",
            "skill_level": "confirme",
            "notes": "Plus de 15 ans d'expérience moyenne"
        },
        {
            "name": "Speed Demons",
            "description": "Équipe rapide et technique",
            "tournament_id": tournament_id,
            "contact_email": "speed@volley.com",
            "contact_phone": "0123456794",
            "skill_level": "expert",
            "notes": "Jeu rapide et spectaculaire"
        },
        {
            "name": "Rising Phoenix",
            "description": "Jeune équipe prometteuse",
            "tournament_id": tournament_id,
            "contact_email": "phoenix@volley.com",
            "contact_phone": "0123456795",
            "skill_level": "debutant",
            "notes": "Équipe en progression constante"
        },
        {
            "name": "Golden Eagles",
            "description": "Équipe mixte expérimentée",
            "tournament_id": tournament_id,
            "contact_email": "eagles@volley.com",
            "contact_phone": "0123456796",
            "skill_level": "expert",
            "notes": "Excellente cohésion d'équipe"
        },
        {
            "name": "Wave Riders",
            "description": "Équipe côtière enjouée",
            "tournament_id": tournament_id,
            "contact_email": "wave@volley.com",
            "contact_phone": "0123456797",
            "skill_level": "confirme",
            "notes": "Ambiance décontractée mais compétitive"
        },
        {
            "name": "Storm Breakers",
            "description": "Équipe défensive solide",
            "tournament_id": tournament_id,
            "contact_email": "storm@volley.com",
            "contact_phone": "0123456798",
            "skill_level": "confirme",
            "notes": "Spécialistes de la défense"
        },
        {
            "name": "Sunset Warriors",
            "description": "Équipe de quartier unie",
            "tournament_id": tournament_id,
            "contact_email": "sunset@volley.com",
            "contact_phone": "0123456799",
            "skill_level": "debutant",
            "notes": "Esprit d'équipe exemplaire"
        },
        {
            "name": "Lightning Bolts",
            "description": "Équipe d'attaque puissante",
            "tournament_id": tournament_id,
            "contact_email": "lightning@volley.com",
            "contact_phone": "0123456800",
            "skill_level": "expert",
            "notes": "Attaques foudroyantes"
        },
        {
            "name": "Ocean Waves",
            "description": "Équipe fluide et harmonieuse",
            "tournament_id": tournament_id,
            "contact_email": "ocean@volley.com",
            "contact_phone": "0123456801",
            "skill_level": "confirme",
            "notes": "Jeu collectif remarquable"
        },
        {
            "name": "Mountain Peaks",
            "description": "Équipe de haute montagne",
            "tournament_id": tournament_id,
            "contact_email": "mountain@volley.com",
            "contact_phone": "0123456802",
            "skill_level": "confirme",
            "notes": "Endurance et ténacité"
        },
        {
            "name": "City Slickers",
            "description": "Équipe urbaine moderne",
            "tournament_id": tournament_id,
            "contact_email": "city@volley.com",
            "contact_phone": "0123456803",
            "skill_level": "debutant",
            "notes": "Première participation en tournoi"
        },
        {
            "name": "Wild Mustangs",
            "description": "Équipe libre et indépendante",
            "tournament_id": tournament_id,
            "contact_email": "mustangs@volley.com",
            "contact_phone": "0123456804",
            "skill_level": "confirme",
            "notes": "Style de jeu imprévisible"
        }
    ]
    
    print(f"🚀 Début insertion de 16 équipes pour le tournoi {tournament_id}")
    print("=" * 60)
    
    created_teams = []
    failed_teams = []
    
    for i, team_data in enumerate(teams_data, 1):
        print(f"📝 Insertion équipe {i}/16: {team_data['name']}")
        
        try:
            # Utiliser le service Tournament pour créer l'équipe
            team = tournamentService.createTeam(team_data)
            
            if team:
                created_teams.append(team)
                print(f"✅ {team.name} créée avec l'ID: {team.id}")
            else:
                failed_teams.append(team_data['name'])
                print(f"❌ Échec création de {team_data['name']}")
                
        except Exception as e:
            failed_teams.append(team_data['name'])
            print(f"❌ Erreur pour {team_data['name']}: {e}")
    
    print("=" * 60)
    print(f"🎯 RÉSULTATS:")
    print(f"✅ Équipes créées: {len(created_teams)}/16")
    print(f"❌ Équipes échouées: {len(failed_teams)}/16")
    
    if failed_teams:
        print(f"⚠️ Équipes en échec: {', '.join(failed_teams)}")
    
    if created_teams:
        print(f"\n🏆 Équipes créées avec succès:")
        for team in created_teams:
            print(f"   - {team.name} ({team.skill_level})")
    
    return created_teams, failed_teams


def insert_teams_with_new_tournament():
    """
    Crée un nouveau tournoi et y ajoute 16 équipes
    """
    print("🏆 Création d'un nouveau tournoi pour les équipes...")
    
    # Données du tournoi
    tournament_data = {
        "name": "Tournoi Test 16 Équipes",
        "description": "Tournoi créé pour tester 16 équipes",
        "tournament_type": "elimination_directe",
        "max_teams": 16,
        "courts_available": 4,
        "start_date": "2025-07-20",
        "start_time": "09:00",
        "match_duration_minutes": 20,
        "break_duration_minutes": 10,
        "constraints": {"pause_dejeuner": "12:00-13:00"},
        "organizer_id": "550e8400-e29b-41d4-a716-446655440001",
        "status": "ready"
    }
    
    # Créer le tournoi
    tournament = tournamentService.createTournament(tournament_data)
    
    if not tournament:
        print("❌ Impossible de créer le tournoi")
        return None, None
    
    print(f"✅ Tournoi créé: {tournament.name} (ID: {tournament.id})")
    print("-" * 40)
    
    # Ajouter les 16 équipes
    created_teams, failed_teams = insert_16_teams(tournament.id)
    
    return tournament, created_teams
