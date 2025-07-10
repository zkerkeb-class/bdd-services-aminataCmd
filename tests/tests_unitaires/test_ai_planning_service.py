import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, date, time
from app.models.models import Tournament, Team, AITournamentPlanning


class TestAIPlanningService:
    """Tests pour AI Planning Service - méthodes publiques uniquement"""
    
    def setup_method(self):
        """Setup avant chaque test"""
        with patch('app.services.ai_planning_service.getSupabase'), \
            patch('app.services.ai_planning_service.tournamentService'), \
            patch('app.services.ai_planning_service.openai_service'), \
            patch('app.services.ai_planning_service.databaseService'):
            from app.services.ai_planning_service import AIPlanningService
            self.service = AIPlanningService()
    
    # FIXTURES
    @pytest.fixture
    def mock_tournament_data(self):
        """Fixture données complètes tournoi"""
        tournament = Tournament(
            id="550e8400-e29b-41d4-a716-446655440000",  # UUID valide
            name="Tournoi Test",
            description="Test",
            tournament_type="round_robin",
            max_teams=8,
            courts_available=2,
            start_date=date(2025, 7, 15),
            start_time=time(9, 0),
            match_duration_minutes=15,
            break_duration_minutes=5,
            constraints={},
            organizer_id="550e8400-e29b-41d4-a716-446655440001",  # UUID valide
            status="ready",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        teams = [
            Team(
                id="550e8400-e29b-41d4-a716-446655440010", name="Équipe A", description="Test",
                tournament_id="550e8400-e29b-41d4-a716-446655440000", captain_id="550e8400-e29b-41d4-a716-446655440011",
                status="registered", contact_email="a@test.com",
                contact_phone="0123456789", skill_level="intermediate",
                notes="Test", created_at=datetime.utcnow(), updated_at=datetime.utcnow()
            ),
            Team(
                id="550e8400-e29b-41d4-a716-446655440020", name="Équipe B", description="Test",
                tournament_id="550e8400-e29b-41d4-a716-446655440000", captain_id="550e8400-e29b-41d4-a716-446655440021",
                status="registered", contact_email="b@test.com",
                contact_phone="0123456788", skill_level="beginner",
                notes="Test", created_at=datetime.utcnow(), updated_at=datetime.utcnow()
            )
        ]
        
        return {
            "tournament": tournament,
            "teams": teams,
            "teams_count": 2,
            "has_minimum_teams": True,
            "can_start": True
        }
    
    @pytest.fixture
    def mock_ai_response(self):
        """Fixture réponse IA valide"""
        return {
            "type_tournoi": "round_robin",
            "matchs_round_robin": [
                {
                    "match_id": "rr_match_550e8400_001",
                    "equipe_a": "Équipe A",
                    "equipe_b": "Équipe B",
                    "horaire": datetime(2025, 7, 15, 9, 0),
                    "terrain": 1
                }
            ],
            "final_ranking": [],
            "commentaires": "Planning test"
        }
    
    @pytest.fixture
    def mock_planning(self):
        """Fixture planning sauvegardé"""
        return AITournamentPlanning(
            id="550e8400-e29b-41d4-a716-446655440100",  # UUID valide
            tournament_id="550e8400-e29b-41d4-a716-446655440000",  # UUID valide
            type_tournoi="round_robin",
            status="generated",
            planning_data={},
            total_matches=1,
            ai_comments="Test",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
    
    # TESTS GENERATE_PLANNING
    # 3 @patch = 3 paramètres mock (ordre inversé) + fixtures
    @patch('app.services.ai_planning_service.databaseService')      # 3ème patch
    @patch('app.services.ai_planning_service.openai_service')       # 2ème patch 
    @patch('app.services.ai_planning_service.tournamentService')    # 1er patch
    def test_generate_planning_success(self, 
                                     mock_tournament_service,  # 1er patch
                                     mock_openai_service,      # 2ème patch
                                     mock_db_service,          # 3ème patch
                                     mock_tournament_data,     # fixture
                                     mock_ai_response,         # fixture
                                     mock_planning):           # fixture
        """Test génération planning - succès complet"""
        # Setup mocks
        mock_tournament_service.getTournamentWithTeams.return_value = mock_tournament_data
        mock_openai_service.generatePlanning.return_value = mock_ai_response
        mock_db_service.savePlanning.return_value = mock_planning
        mock_db_service.saveMatches.return_value = []
        mock_db_service.savePoules.return_value = []
        
        # Appel
        result = self.service.generatePlanning("550e8400-e29b-41d4-a716-446655440000")
        
        # Vérifications
        assert result is not None
        assert result.id.id == "550e8400-e29b-41d4-a716-446655440100"
        assert result.tournament_id == "550e8400-e29b-41d4-a716-446655440000"
        
        # Vérifier les appels
        mock_tournament_service.getTournamentWithTeams.assert_called_once_with("tournament_123")
        mock_openai_service.generatePlanning.assert_called_once()
        mock_db_service.savePlanning.assert_called_once()
    
    # 1 @patch = 1 paramètre mock + fixtures
    @patch('app.services.ai_planning_service.tournamentService')
    def test_generate_planning_no_tournament(self, mock_tournament_service):
        """Test génération planning - tournoi non trouvé"""
        mock_tournament_service.getTournamentWithTeams.return_value = None
        
        result = self.service.generatePlanning("tournament_invalid")
        
        assert result is None
    
    # 1 @patch = 1 paramètre mock + 1 fixture
    @patch('app.services.ai_planning_service.tournamentService')
    def test_generate_planning_not_enough_teams(self, mock_tournament_service, mock_tournament_data):
        """Test génération planning - pas assez d'équipes"""
        # Modifier pour avoir 1 seule équipe
        mock_tournament_data["teams"] = [mock_tournament_data["teams"][0]]
        mock_tournament_service.getTournamentWithTeams.return_value = mock_tournament_data
        
        result = self.service.generatePlanning("tournament_123")
        
        assert result is None
    
    # 2 @patch = 2 paramètres mock + 1 fixture
    @patch('app.services.ai_planning_service.openai_service')       # 2ème patch
    @patch('app.services.ai_planning_service.tournamentService')     # 1er patch
    def test_generate_planning_openai_fails(self, 
                                          mock_tournament_service,  # 1er patch
                                          mock_openai_service,      # 2ème patch
                                          mock_tournament_data):    # fixture
        """Test génération planning - OpenAI échoue"""
        mock_tournament_service.getTournamentWithTeams.return_value = mock_tournament_data
        mock_openai_service.generatePlanning.return_value = None
        
        result = self.service.generatePlanning("tournament_123")
        
        assert result is None
    
    # 3 @patch = 3 paramètres mock + 2 fixtures
    @patch('app.services.ai_planning_service.databaseService')      # 3ème patch
    @patch('app.services.ai_planning_service.openai_service')       # 2ème patch
    @patch('app.services.ai_planning_service.tournamentService')     # 1er patch
    def test_generate_planning_save_fails(self, 
                                        mock_tournament_service,  # 1er patch
                                        mock_openai_service,      # 2ème patch
                                        mock_db_service,          # 3ème patch
                                        mock_tournament_data,     # fixture
                                        mock_ai_response):        # fixture
        """Test génération planning - sauvegarde échoue"""
        mock_tournament_service.getTournamentWithTeams.return_value = mock_tournament_data
        mock_openai_service.generatePlanning.return_value = mock_ai_response
        mock_db_service.savePlanning.return_value = None
        
        result = self.service.generatePlanning("tournament_123")
        
        assert result is None
    
    def test_generate_planning_exception(self):
        """Test génération planning - exception"""
        # 1 @patch dans le contexte = pas de paramètre additionnel
        with patch('app.services.ai_planning_service.tournamentService') as mock_service:
            mock_service.getTournamentWithTeams.side_effect = Exception("Erreur test")
            
            result = self.service.generatePlanning("tournament_123")
            
            assert result is None
    
    # TESTS GET_PLANNING_STATUS - Aucun @patch = aucun paramètre mock
    def test_get_planning_status_success(self):
        """Test récupération statut - succès"""
        mock_result = Mock()
        mock_result.data = [{"status": "completed"}]
        self.service.supabase.table.return_value.select.return_value.eq.return_value.execute.return_value = mock_result
        
        result = self.service.getPlanningStatus("planning_123")
        
        assert result == "completed"
    
    def test_get_planning_status_not_found(self):
        """Test récupération statut - non trouvé"""
        mock_result = Mock()
        mock_result.data = []
        self.service.supabase.table.return_value.select.return_value.eq.return_value.execute.return_value = mock_result
        
        result = self.service.getPlanningStatus("planning_invalid")
        
        assert result is None
    
    def test_get_planning_status_exception(self):
        """Test récupération statut - exception"""
        self.service.supabase.table.side_effect = Exception("Erreur DB")
        
        result = self.service.getPlanningStatus("planning_123")
        
        assert result is None
    
    # TESTS REGENERATE_PLANNING - Aucun @patch = aucun paramètre mock + 1 fixture
    def test_regenerate_planning_success(self, mock_planning):
        """Test régénération planning - succès"""
        # Mock get planning by id
        mock_result = Mock()
        mock_result.data = [mock_planning.model_dump()]
        self.service.supabase.table.return_value.select.return_value.eq.return_value.execute.return_value = mock_result
        
        # Mock delete planning
        self.service.supabase.table.return_value.delete.return_value.eq.return_value.execute.return_value = Mock()
        
        # Mock generate planning
        with patch.object(self.service, 'generatePlanning', return_value=mock_planning) as mock_generate:
            result = self.service.regeneratePlanning("planning_123")
            
            assert result is not None
            assert result.id == "planning_123"
            mock_generate.assert_called_once_with("tournament_123")
    
    def test_regenerate_planning_old_not_found(self):
        """Test régénération planning - ancien non trouvé"""
        mock_result = Mock()
        mock_result.data = []
        self.service.supabase.table.return_value.select.return_value.eq.return_value.execute.return_value = mock_result
        
        result = self.service.regeneratePlanning("planning_invalid")
        
        assert result is None
    
    def test_regenerate_planning_exception(self):
        """Test régénération planning - exception"""
        self.service.supabase.table.side_effect = Exception("Erreur test")
        
        result = self.service.regeneratePlanning("planning_123")
        
        assert result is None