import pytest
from unittest.mock import Mock, patch
from datetime import datetime
from app.services.database_service import databaseService
from app.models.models import AITournamentPlanning, AIGeneratedMatch, AIGeneratedPoule


class TestDatabaseService:
    """Tests pour le service Database"""
    
    def setup_method(self):
        """Setup avant chaque test"""
        self.service = databaseService
        self.service.supabase = Mock()  # Mock du client Supabase
    
    @pytest.fixture
    def sample_round_robin_planning(self):
        """Fixture planning round robin"""
        return {
            "type_tournoi": "round_robin",
            "matchs_round_robin": [
                {
                    "match_id": "rr_j1_m1",
                    "equipe_a": "Équipe 1",
                    "equipe_b": "Équipe 2",
                    "terrain": 1,
                    "horaire": "2024-06-15T09:00:00Z",
                    "journee": 1
                },
                {
                    "match_id": "rr_j1_m2",
                    "equipe_a": "Équipe 3", 
                    "equipe_b": "Équipe 4",
                    "terrain": 2,
                    "horaire": "2024-06-15T09:00:00Z",
                    "journee": 1
                }
            ],
            "final_ranking": [
                {"position": 1, "equipe_id": "team1", "nom_equipe": "Équipe 1"}
            ],
            "commentaires": "Planning test round robin"
        }
    
    @pytest.fixture
    def sample_poules_planning(self):
        """Fixture planning avec poules"""
        return {
            "type_tournoi": "poules_elimination",
            "poules": [
                {
                    "poule_id": "poule_a",
                    "nom_poule": "Poule A",
                    "equipes": ["Équipe 1", "Équipe 2"],
                    "matchs": [
                        {
                            "match_id": "poule_a_m1",
                            "equipe_a": "Équipe 1",
                            "equipe_b": "Équipe 2", 
                            "terrain": 1,
                            "horaire": "2024-06-15T09:00:00Z"
                        }
                    ]
                }
            ],
            "phase_elimination_apres_poules": {
                "finale": {
                    "match_id": "finale_1",
                    "equipe_a": "1er_poule_a",
                    "equipe_b": "1er_poule_b",
                    "terrain": 1,
                    "horaire": "2024-06-15T15:00:00Z"
                }
            },
            "final_ranking": [],
            "commentaires": "Planning test poules"
        }

    # ===== TESTS SAVE_PLANNING =====
    
    def test_save_planning_success(self, sample_round_robin_planning):
        """Test sauvegarde planning réussie"""
        # Mock réponse Supabase
        mock_response = Mock()
        mock_response.data = [{
            "id": "planning-123",
            "tournament_id": "tournament-456",
            "type_tournoi": "round_robin",
            "status": "generated",
            "total_matches": 2,
            "created_at": "2024-06-15T08:00:00Z"
        }]
        self.service.supabase.table.return_value.insert.return_value.execute.return_value = mock_response
        
        # Test
        result = self.service.savePlanning(
            tournamentId="tournament-456",
            planningData=sample_round_robin_planning,
            typeTournoi="round_robin"
        )
        
        # Vérifications
        assert result is not None
        assert isinstance(result, AITournamentPlanning)
        assert result.tournament_id == "tournament-456"
        assert result.type_tournoi == "round_robin"
        assert result.total_matches == 2
        
        # Vérifier que Supabase a été appelé
        self.service.supabase.table.assert_called_with("ai_tournament_planning")
    
    def test_save_planning_error(self, sample_round_robin_planning):
        """Test erreur lors de la sauvegarde"""
        # Mock erreur Supabase
        self.service.supabase.table.return_value.insert.return_value.execute.side_effect = Exception("DB Error")
        
        # Test
        result = self.service.savePlanning(
            tournamentId="tournament-456",
            planningData=sample_round_robin_planning,
            typeTournoi="round_robin"
        )
        
        # Vérifications
        assert result is None
    
    def test_save_planning_invalid_data(self):
        """Test avec données invalides"""
        invalid_data = {"type_tournoi": "invalid_type"}  # Données incomplètes
        
        # Test
        result = self.service.savePlanning(
            tournamentId="tournament-456",
            planningData=invalid_data,
            typeTournoi="round_robin"
        )
        
        # Vérifications
        assert result is None

    # ===== TESTS SAVE_MATCHES =====
    
    def test_save_matches_round_robin(self, sample_round_robin_planning):
        """Test sauvegarde matchs round robin"""
        # Mock réponse Supabase
        mock_response = Mock()
        mock_response.data = [
                {
                "id": "match-1", 
                "planning_id": "planning-123",
                "match_id_ai": "rr_j1_m1", 
                "equipe_a": "Équipe 1",
                "equipe_b": "Équipe 2",
                "terrain": 1,
                "horaire_prevu": "2024-06-15T09:00:00Z",
                "phase": "round_robin",
                "journee": 1,
                "status": "scheduled",
                "created_at": "2024-06-15T08:00:00Z"
            },
            {
                "id": "match-2", 
                "planning_id": "planning-123",
                "match_id_ai": "rr_j1_m2", 
                "equipe_a": "Équipe 3",
                "equipe_b": "Équipe 4",
                "terrain": 2,
                "horaire_prevu": "2024-06-15T09:00:00Z",
                "phase": "round_robin",
                "journee": 1,
                "status": "scheduled",
                "created_at": "2024-06-15T08:00:00Z"
            }
        ]
        self.service.supabase.table.return_value.insert.return_value.execute.return_value = mock_response
        
        # Test
        result = self.service.saveMatches("planning-123", sample_round_robin_planning)
        
        # Vérifications
        assert result is not None
        assert len(result) == 2
        assert all(isinstance(match, AIGeneratedMatch) for match in result)
        assert result[0].match_id_ai == "rr_j1_m1"
        assert result[0].phase == "round_robin"
        
        # Vérifier appel Supabase
        self.service.supabase.table.assert_called_with("ai_generated_match")
    
    def test_save_matches_poules(self, sample_poules_planning):
        """Test sauvegarde matchs avec poules + élimination"""
        # Mock réponse Supabase  
        mock_response = Mock()
        mock_response.data = [
            {
                "id": "match-1", 
                "planning_id": "planning-123",
                "match_id_ai": "poule_a_m1", 
                "equipe_a": "Équipe 1",
                "equipe_b": "Équipe 2",
                "terrain": 1,
                "horaire_prevu": "2024-06-15T09:00:00Z",
                "phase": "poules",
                "poule_id": "poule_a",
                "status": "scheduled",
                "created_at": "2024-06-15T08:00:00Z"
            },
            {
                "id": "match-2", 
                "planning_id": "planning-123",
                "match_id_ai": "finale_1", 
                "equipe_a": "1er_poule_a",
                "equipe_b": "1er_poule_b",
                "terrain": 1,
                "horaire_prevu": "2024-06-15T15:00:00Z",
                "phase": "finale",
                "status": "scheduled",
                "created_at": "2024-06-15T08:00:00Z"
            }
        ]
        self.service.supabase.table.return_value.insert.return_value.execute.return_value = mock_response
        
        # Test
        result = self.service.saveMatches("planning-123", sample_poules_planning)
        
        # Vérifications
        assert result is not None
        assert len(result) == 2
        phases = [match.phase for match in result]
        assert "poules" in phases
        assert "finale" in phases
    
    def test_save_matches_no_matches(self):
        """Test avec planning sans matchs"""
        empty_planning = {"type_tournoi": "round_robin", "matchs_round_robin": []}
        
        # Mock réponse vide
        mock_response = Mock()
        mock_response.data = []
        self.service.supabase.table.return_value.insert.return_value.execute.return_value = mock_response
        
        # Test
        result = self.service.saveMatches("planning-123", empty_planning)
        
        # Vérifications
        assert result == []
    
    def test_save_matches_error(self, sample_round_robin_planning):
        """Test erreur sauvegarde matchs"""
        # Mock erreur Supabase
        self.service.supabase.table.return_value.insert.return_value.execute.side_effect = Exception("DB Error")
        
        # Test
        result = self.service.saveMatches("planning-123", sample_round_robin_planning)
        
        # Vérifications
        assert result is None

    # ===== TESTS SAVE_POULES =====
    
    def test_save_poules_success(self, sample_poules_planning):
        """Test sauvegarde poules réussie"""
        # Mock réponse Supabase
        mock_response = Mock()
        mock_response.data = [{
            "id": "poule-1",
            "planning_id": "planning-123",
            "poule_id": "poule_a",
            "nom_poule": "Poule A",
            "equipes": ["Équipe 1", "Équipe 2"],
            "nb_equipes": 2,
            "nb_matches": 1
        }]
        self.service.supabase.table.return_value.insert.return_value.execute.return_value = mock_response
        
        # Test
        result = self.service.savePoules("planning-123", sample_poules_planning)
        
        # Vérifications
        assert result is not None
        assert len(result) == 1
        assert isinstance(result[0], AIGeneratedPoule)
        assert result[0].poule_id == "poule_a"
        assert result[0].nb_equipes == 2
        
        # Vérifier appel Supabase
        self.service.supabase.table.assert_called_with("ai_generated_poule")
    
    def test_save_poules_no_poules(self, sample_round_robin_planning):
        """Test avec planning sans poules"""
        # Test
        result = self.service.savePoules("planning-123", sample_round_robin_planning)
        
        # Vérifications
        assert result == []
    
    def test_save_poules_error(self, sample_poules_planning):
        """Test erreur sauvegarde poules"""
        # Mock erreur Supabase
        self.service.supabase.table.return_value.insert.return_value.execute.side_effect = Exception("DB Error")
        
        # Test
        result = self.service.savePoules("planning-123", sample_poules_planning)
        
        # Vérifications
        assert result is None

    # ===== TESTS GET_PLANNING_WITH_DETAILS =====
    
    def test_get_planning_with_details_success(self):
        """Test récupération planning avec détails"""
        # Mock réponses Supabase
        # 1. Planning principal
        planning_response = Mock()
        planning_response.data = {
            "id": "planning-123",
            "tournament_id": "tournament-456",
            "type_tournoi": "round_robin",
            "status": "generated",
            "total_matches": 2,
            "planning_data": {"type_tournoi": "round_robin"},
            "created_at": "2024-06-15T08:00:00Z"
        }
        
        # 2. Matchs
        matches_response = Mock()
        matches_response.data = [
            {
                "id": "match-1",
                "planning_id": "planning-123",
                "match_id_ai": "rr_j1_m1",
                "equipe_a": "Équipe 1",
                "equipe_b": "Équipe 2",
                "terrain": 1,
                "horaire_prevu": "2024-06-15T09:00:00Z",
                "phase": "round_robin",
                "status": "scheduled",
                "created_at": "2024-06-15T08:00:00Z"
            }
        ]
        
        # 3. Poules (vide)
        poules_response = Mock()
        poules_response.data = []
        
        # Setup mocks
        self.service.supabase.table.return_value.select.return_value.eq.return_value.single.return_value.execute.return_value = planning_response
        self.service.supabase.table.return_value.select.return_value.eq.return_value.order.return_value.execute.return_value = matches_response
        self.service.supabase.table.return_value.select.return_value.eq.return_value.execute.return_value = poules_response
        
        # Test
        result = self.service.getPlanningWithDetails("planning-123")
        
        # Vérifications
        assert result is not None
        assert "planning" in result
        assert "matches" in result
        assert "poules" in result
        
        assert isinstance(result["planning"], AITournamentPlanning)
        assert len(result["matches"]) == 1
        assert isinstance(result["matches"][0], AIGeneratedMatch)
        assert result["matches"][0].match_id_ai == "rr_j1_m1"
        assert result["poules"] == []
    
    def test_get_planning_with_details_not_found(self):
        """Test planning non trouvé"""
        # Mock réponse vide
        planning_response = Mock()
        planning_response.data = None
        self.service.supabase.table.return_value.select.return_value.eq.return_value.single.return_value.execute.return_value = planning_response
        
        # Test
        result = self.service.getPlanningWithDetails("planning-inexistant")
        
        # Vérifications
        assert result is None
    
    def test_get_planning_with_details_error(self):
        """Test erreur récupération planning"""
        # Mock erreur Supabase
        self.service.supabase.table.return_value.select.return_value.eq.return_value.single.return_value.execute.side_effect = Exception("DB Error")
        
        # Test
        result = self.service.getPlanningWithDetails("planning-123")
        
        # Vérifications
        assert result is None

    # ===== TESTS UPDATE_PLANNING_STATUS =====
    
    def test_update_planning_status_success(self):
        """Test mise à jour statut réussie"""
        # Mock réponse Supabase
        mock_response = Mock()
        mock_response.data = [{"id": "planning-123", "status": "active"}]
        self.service.supabase.table.return_value.update.return_value.eq.return_value.execute.return_value = mock_response
        
        # Test
        result = self.service.updatePlanningStatus("planning-123", "active")
        
        # Vérifications
        assert result is True
        
        # Vérifier appel Supabase
        self.service.supabase.table.assert_called_with("ai_tournament_planning")
        self.service.supabase.table.return_value.update.assert_called_once()
    
    def test_update_planning_status_error(self):
        """Test erreur mise à jour statut"""
        # Mock erreur Supabase
        self.service.supabase.table.return_value.update.return_value.eq.return_value.execute.side_effect = Exception("DB Error")
        
        # Test
        result = self.service.updatePlanningStatus("planning-123", "active")
        
        # Vérifications
        assert result is False


# ===== TESTS DES MÉTHODES PRIVÉES =====

class TestDatabaseServicePrivateMethods:
    """Tests des méthodes privées du service"""
    
    def setup_method(self):
        """Setup avant chaque test"""
        self.service = databaseService
        self.service.supabase = Mock()
    
    @pytest.fixture
    def sample_ai_planning_data(self):
        """Fixture AIPlanningData pour tests privés"""
        from app.models.models import AIPlanningData, RoundRobinMatch
        return AIPlanningData(
            type_tournoi="round_robin",
            matchs_round_robin=[
                RoundRobinMatch(
                    match_id="rr_j1_m1",
                    equipe_a="Équipe 1",
                    equipe_b="Équipe 2",
                    horaire=datetime(2024, 6, 15, 9, 0),
                    terrain=1,
                    journee=1
                )
            ]
        )
    
    def test_extract_round_robin_matches(self, sample_ai_planning_data):
        """Test extraction matchs round robin"""
        # Test
        matches = self.service._extractRoundRobinMatches("planning-123", sample_ai_planning_data)
        
        # Vérifications
        assert len(matches) == 1
        assert isinstance(matches[0], AIGeneratedMatch)
        assert matches[0].match_id_ai == "rr_j1_m1"
        assert matches[0].phase == "round_robin"
        assert matches[0].journee == 1
    
    def test_create_elimination_match_object(self):
        """Test création objet match élimination"""
        from app.models.models import EliminationMatch
        
        # Mock match élimination
        mock_match = EliminationMatch(
            match_id="finale_1",
            equipe_a="winner_demi_1",
            equipe_b="winner_demi_2",
            horaire=datetime(2024, 6, 15, 17, 0),
            terrain=1
        )
        
        # Test
        result = self.service._createEliminationMatchObject("planning-123", mock_match, "finale")
        
        # Vérifications
        assert result is not None
        assert isinstance(result, AIGeneratedMatch)
        assert result.match_id_ai == "finale_1"
        assert result.phase == "finale"
        assert result.equipe_a == "winner_demi_1"