# Modèles de réponse standardisés
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from app.models.models import (
    AITournamentPlanning, 
    Tournament, 
    Team, 
    Profile, 
    TeamMember, 
    TeamWithMembers
)  
from datetime import datetime, date, time

class StandardResponse(BaseModel):
    """Réponse standard de l'API"""
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None

class PlanningResponse(StandardResponse):
    """Réponse avec données de planning"""
    data: Optional[AITournamentPlanning] = None


class StatusResponse(StandardResponse):
    """Réponse avec statut de planning"""
    data: Optional[Dict[str, str]] = None

class HealthResponse(BaseModel):
    """Réponse du health check"""
    status: str
    timestamp: datetime
    version: str
    services: Dict[str, str]


class DetailedHealthResponse(BaseModel):
    """Réponse détaillée du health check"""
    status: str
    timestamp: datetime
    version: str
    uptime: str
    services: Dict[str, Dict[str, Any]]

class TournamentResponse(StandardResponse):
    """Réponse avec données de tournoi"""
    data: Optional[list[Tournament]] = None


class TournamentWithTeamsResponse(StandardResponse):
    """Réponse avec tournoi et équipes"""
    data: Optional[Dict[str, Any]] = None


class TeamsResponse(StandardResponse):
    """Réponse avec liste d'équipes"""
    data: Optional[List[Team]] = None


class TeamResponse(StandardResponse):
    """Réponse avec une équipe"""
    data: Optional[Team] = None

class CreateTournamentRequest(BaseModel):
    """Requête pour créer un tournoi"""
    name: str = Field(..., description="Nom du tournoi")
    description: Optional[str] = Field(None, description="Description du tournoi")
    tournament_type: str = Field(..., description="Type de tournoi (round_robin, elimination_directe, etc.)")
    max_teams: int = Field(..., ge=2, le=64, description="Nombre maximum d'équipes")
    courts_available: int = Field(..., ge=1, le=20, description="Nombre de terrains disponibles")
    start_date: date = Field(..., description="Date de début du tournoi")
    start_time: Optional[time] = Field(None, description="Heure de début")
    match_duration_minutes: int = Field(15, ge=5, le=120, description="Durée d'un match en minutes")
    break_duration_minutes: int = Field(5, ge=0, le=60, description="Pause entre matchs en minutes")
    constraints: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Contraintes spéciales")
    organizer_id: str = Field(..., description="ID de l'organisateur (UUID)")
    status: str = Field("draft", description="Statut du tournoi")


class CreateTeamRequest(BaseModel):
    """Requête pour créer une équipe"""
    name: str = Field(..., description="Nom de l'équipe")
    description: str = Field(..., description="Description de l'équipe")
    tournament_id: str = Field(..., description="ID du tournoi (UUID)")
    captain_id: Optional[str] = Field(None, description="ID du capitaine (UUID)")
    contact_email: Optional[str] = Field("", description="Email de contact")
    contact_phone: Optional[str] = Field("", description="Téléphone de contact")
    skill_level: Optional[str] = Field("debutant", description="Niveau de l'équipe ('debutant', 'amateur', 'confirme', 'expert', 'professionnel')")
    notes: Optional[str] = Field("", description="Notes sur l'équipe")


class UpdateTournamentStatusRequest(BaseModel):
    """Requête pour mettre à jour le statut d'un tournoi"""
    status: str = Field(..., description="Nouveau statut (draft, ready, active, completed, cancelled)")

class UserResponse(StandardResponse):
    """Réponse avec données d'un utilisateur"""
    data: Optional[Profile] = None

class UsersResponse(StandardResponse):
    """Réponse avec liste d'utilisateurs"""
    data: Optional[List[Profile]] = None

class TeamMemberResponse(StandardResponse):
    """Réponse avec données d'un membre d'équipe"""
    data: Optional[List[TeamMember]] = None

class TeamWithMembersResponse(StandardResponse):
    """Réponse avec données d'une équipe avec ses membres"""
    data: Optional[List[TeamWithMembers]] = None