from fastapi import APIRouter, HTTPException, status, Query
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
    TeamWithMembersResponse
    )

# Router avec préfixe et tags
router = APIRouter(
    prefix="/api/teams",
    tags=["Teams"]
)

@router.get("/", response_model=TeamsResponse)
def get_teams():
    """Récupère toutes les équipes d'un tournoi"""
    try:
        # Appel du service
        teams = tournamentService.getTeams()
        
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

@router.get("/with-members", response_model=TeamWithMembersResponse)
def get_teams_with_members(tournament_id: str = Query(None, description="ID du tournoi")):
    """Récupère toutes les équipes avec leurs membres"""
    try:
        teams = tournamentService.getTeamsWithMembers(tournament_id)
        
        if teams is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erreur lors de la récupération des équipes avec membres"
            )
        
        return TeamWithMembersResponse(
            success=True,
            message=f"{len(teams)} équipe(s) récupérée(s) avec succès",
            data=teams
        )
    except Exception as e:
        print(f"❌ Erreur récupération équipes avec membres: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur interne lors de la récupération des équipes avec membres"
        )