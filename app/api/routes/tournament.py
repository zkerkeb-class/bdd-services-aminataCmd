from fastapi import APIRouter, HTTPException, status
from app.services.tournament_service import tournamentService
from app.schemas.response import (
    TournamentResponse, 
    CreateTournamentRequest,
    TournamentWithTeamsResponse,
    StandardResponse, 
    TeamsResponse,
    TeamResponse,
    UpdateTournamentStatusRequest,
    CreateTeamRequest,
    TeamMemberResponse,
    )
from app.schemas.requete import AddTeamMembersRequest

# Router avec préfixe et tags
router = APIRouter(
    prefix="/api/tournaments",
    tags=["Tournaments"]
)

@router.post("/", response_model=TournamentResponse, status_code=status.HTTP_201_CREATED)
def create_tournament(request: CreateTournamentRequest):
    """Crée un nouveau tournoi"""
    try:
        # Conversion en dict pour le service
        tournament_data = request.model_dump()
        
        # Appel du service Tournament
        tournament = tournamentService.createTournament(tournament_data)
        
        if not tournament:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Impossible de créer le tournoi. Vérifiez les données fournies."
            )
        
        return TournamentResponse(
            success=True,
            message="Tournoi créé avec succès",
            data=[tournament]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Erreur création tournoi: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur interne lors de la création du tournoi"
        )

@router.get("/", response_model=TournamentResponse, status_code=status.HTTP_200_OK)
def get_tournaments():
    """ Recupere tous les tournois"""
    try: 
        tournaments = tournamentService.getTournaments()
        if not tournaments:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tournois non trouvés"
            )
        return TournamentResponse(
            success=True,
            message="Tournoi récupéré avec succès",
            data=tournaments
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Erreur récupération tournoi: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur interne lors de la récupération du tournoi"
        )

@router.get("/{tournament_id}", response_model=TournamentResponse)
def get_tournament(tournament_id: str):
    """Récupère un tournoi par son ID"""
    try:
        # Appel du service
        tournament = tournamentService.getTournamentById(tournament_id)
        
        if not tournament:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tournoi non trouvé"
            )
        
        return TournamentResponse(
            success=True,
            message="Tournoi récupéré avec succès",
            data=[tournament]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Erreur récupération tournoi: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur interne lors de la récupération du tournoi"
        )

@router.get("/{tournament_id}/with-teams", response_model=TournamentWithTeamsResponse)
def get_tournament_with_teams(tournament_id: str):
    """Récupère un tournoi avec ses équipes"""
    try:
        # Appel du service
        tournament_data = tournamentService.getTournamentWithTeams(tournament_id)
        
        if not tournament_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tournoi non trouvé"
            )
        
        return TournamentWithTeamsResponse(
            success=True,
            message="Tournoi et équipes récupérés avec succès",
            data=tournament_data
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Erreur récupération tournoi avec équipes: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur interne lors de la récupération du tournoi"
        )

@router.get("/{tournament_id}/teams", response_model=TeamsResponse)
def get_tournament_teams(tournament_id: str):
    """Récupère toutes les équipes d'un tournoi"""
    try:
        # Appel du service
        teams = tournamentService.getTournamentTeams(tournament_id)
        
        return TeamsResponse(
            success=True,
            message=f"{len(teams)} équipe(s) récupérée(s) avec succès",
            data=teams
        )
        
    except Exception as e:
        print(f"❌ Erreur récupération équipes: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur interne lors de la récupération des équipes"
        )

@router.patch("/{tournament_id}/status", response_model=StandardResponse)
def update_tournament_status(tournament_id: str, request: UpdateTournamentStatusRequest):
    """Met à jour le statut d'un tournoi"""
    try:
        # Appel du service
        success = tournamentService.updateTournamentStatus(tournament_id, request.status)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Impossible de mettre à jour le statut du tournoi"
            )
        
        return StandardResponse(
            success=True,
            message=f"Statut du tournoi mis à jour vers '{request.status}'",
            data={"tournament_id": tournament_id, "new_status": request.status}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Erreur mise à jour statut: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur interne lors de la mise à jour du statut"
        )

@router.post("/{tournament_id}/teams", response_model=TeamResponse, status_code=status.HTTP_201_CREATED)
def create_team(tournament_id: str, request: CreateTeamRequest):
    """Crée une nouvelle équipe pour un tournoi"""
    try:
        # Vérifier que le tournament_id correspond
        if request.tournament_id != tournament_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="L'ID du tournoi dans l'URL ne correspond pas à celui dans la requête"
            )
        
        # Conversion en dict pour le service
        team_data = request.model_dump()
        
        # Appel du service
        team = tournamentService.createTeam(team_data)
        
        if not team:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Impossible de créer l'équipe. Vérifiez les données fournies."
            )
        
        return TeamResponse(
            success=True,
            message="Équipe créée avec succès",
            data=team
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Erreur création équipe: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur interne lors de la création de l'équipe"
        )

@router.get("/teams/{team_id}", response_model=TeamResponse)
def get_team(team_id: str):
    """Récupère une équipe par son ID"""
    try:
        # Appel du service
        team = tournamentService.getTeamById(team_id)
        
        if not team:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Équipe non trouvée"
            )
        
        return TeamResponse(
            success=True,
            message="Équipe récupérée avec succès",
            data=team
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Erreur récupération équipe: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur interne lors de la récupération de l'équipe"
        )
    
@router.delete("/teams/{team_id}", response_model=TeamResponse)
def delete_team(team_id: str):
    try:
        result = tournamentService.deleteTeamById(team_id)

        if result:
            return TeamResponse(
                success=True,
                message="Equipe supprimee avec succes"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur interne lors de la récupération de l'équipe"
        )
    
@router.get("/teams/add_teams/{tournament_id}")
def add_teams(tournament_id: str):
    from app.script.insert_teams import insert_16_teams
    insert_16_teams(tournament_id)

@router.post("/teams/{team_id}/members", response_model=TeamMemberResponse)
def add_team_members(team_id: str, request: AddTeamMembersRequest):
    """Ajoute un joueur à une équipe"""
    try:
        # verifier si team_id correspond au team_id de la requete

        if team_id != request.team_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="L'ID de l'équipe dans l'URL ne correspond pas à celui dans la requête"
            )
        
        # Appel du service
        team_member = tournamentService.addTeamMembers(request)
        
        if not team_member:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Impossible d'ajouter le joueur à l'équipe"
            )
        
        return TeamMemberResponse(
            success=True,
            message=f"{len(team_member)} joueur(s) ajouté(s) à l'équipe avec succès",
            data=team_member
        )

    except Exception as e:
        print(f"❌ Erreur ajout joueur: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur interne lors de l'ajout du joueur"
        )