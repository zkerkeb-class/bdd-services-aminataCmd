from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class GeneratePlanningRequest(BaseModel):
    """Requête pour générer un planning"""
    tournament_id: str = Field(..., description="ID du tournoi (UUID)")


class RegeneratePlanningRequest(BaseModel):
    """Requête pour régénérer un planning"""
    planning_id: str = Field(..., description="ID du planning à régénérer (UUID)")


class GetUserRequest(BaseModel):
    """Requête pour récupérer un utilisateur"""
    user_id: str = Field(..., description="ID de l'utilisateur (UUID)")


class UpdateUserProfileRequest(BaseModel):
    """Requête pour mettre à jour un profil utilisateur"""
    first_name: Optional[str] = Field(None, description="Prénom")
    last_name: Optional[str] = Field(None, description="Nom de famille") 
    display_name: Optional[str] = Field(None, description="Nom d'affichage")
    phone: Optional[str] = Field(None, description="Numéro de téléphone")
    bio: Optional[str] = Field(None, description="Biographie")
    preferred_language: Optional[str] = Field(None, description="Langue préférée")
    timezone: Optional[str] = Field(None, description="Fuseau horaire")
    email_notifications: Optional[bool] = Field(None, description="Notifications email")
    push_notifications: Optional[bool] = Field(None, description="Notifications push")

class AddTeamMemberRequest(BaseModel):
    """Requête pour ajouter un joueur à une équipe"""
    user_id: str = Field(..., description="ID de l'utilisateur (UUID)")
    status: str = Field('active', description="Statut du joueur") # active, inactive, pending
    role: Optional[str] = Field('player', description="Rôle du joueur") # captain, player
    position: Optional[str] = Field(None, description="Position du joueur")

class AddTeamMembersRequest(BaseModel):
    """Requête pour ajouter plusieurs joueurs à une équipe"""
    team_id: str = Field(..., description="ID de l'équipe (UUID)")
    players: list[AddTeamMemberRequest] = Field(..., description="Liste des joueurs à ajouter")
