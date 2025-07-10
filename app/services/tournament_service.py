import uuid
from datetime import datetime, date, time
from typing import List, Optional, Dict, Any
from app.core.database import getSupabase
from app.models.models import Tournament, Team, TeamMember, TeamWithMembers


class TournamentService():
    """
    Service pour gerer les tournois et equipes
    """

    def __init__(self):
        self.supabase = getSupabase()

    def getTournaments(self) -> list[Tournament]:
        try:

            result = self.supabase.table("tournament")\
                .select("*")\
                .execute()

            tournaments = []
            for tournament_data in result.data or []:
                try:
                    teams = self.getTournamentTeams(tournament_data["id"])
                    tournament_data["registered_teams"] = len(teams)

                    tournament = Tournament(**tournament_data)
                    tournaments.append(tournament)
                except Exception as e:
                    print(f"⚠️ Tournoi invalide ignorée: {e}")
                    continue
            return tournaments
        except Exception as e:
            print(f"❌ Erreur récupération tournois: {e}")
            return None 

    def getTournamentById(self, tournamentId: str) -> Optional[Tournament]:
        """
        Récupère un tournoi par son ID
        
        Args:
            tournamentId: ID du tournoi
            
        Returns:
            Tournament: Objet Tournament ou None si pas trouvé
        """
        try:
            print(f"🔍 Récupération tournoi {tournamentId}")
            
            result = self.supabase.table("tournament")\
                .select("*")\
                .eq("id", tournamentId)\
                .single()\
                .execute()
            print(f"result : {result}")
            if not result.data:
                print(f"❌ Tournoi {tournamentId} non trouvé")
                return None
            teams = self.getTournamentTeams(tournamentId)
            result.data["registered_teams"] = len(teams)
                
            # Convertir en objet Pydantic
            tournament = Tournament(**result.data)
            print(f"✅ Tournoi récupéré: {tournament.name}")
            return tournament
            
        except Exception as e:
            print(f"❌ Erreur récupération tournoi {tournamentId}: {e}")
            return None

    def getTournamentTeams(self, tournamentId: str) -> List[Team]:
        """
        Récupère toutes les équipes d'un tournoi
        
        Args:
            tournamentId: ID du tournoi
            
        Returns:
            List[Team]: Liste des équipes (vide si aucune)
        """
        try:
            print(f"👥 Récupération équipes du tournoi {tournamentId}")
            
            result = self.supabase.table("team")\
                .select("*")\
                .eq("tournament_id", tournamentId)\
                .order("name")\
                .execute()
            
            teams = []
            for team_data in result.data or []:
                try:
                    team = Team(**team_data)
                    teams.append(team)
                except Exception as e:
                    print(f"⚠️ Équipe invalide ignorée: {e}")
                    continue
            
            print(f"✅ {len(teams)} équipes récupérées")
            return teams
            
        except Exception as e:
            print(f"❌ Erreur récupération équipes: {e}")
            return []

    def createTournament(self, tournamentData: dict) -> Optional[Tournament]:
        """
        Crée un nouveau tournoi
        
        Args:
            tournamentData: Données du tournoi (dict)
            
        Returns:
            Tournament: Tournoi créé ou None si erreur
        """
        try:
            print(f"🏆 Création nouveau tournoi: {tournamentData.get('name', 'Sans nom')}")
            
            # Ajouter l'ID et timestamps
            temp_data = tournamentData.copy()
            temp_data.update({
                "id": "00000000-0000-0000-0000-000000000000",  # Temp pour validation
                "created_at": datetime.now(),  # Temp pour validation
                "updated_at": datetime.now()   # Temp pour validation
            })
            
            # Valider avec Pydantic
            tournament = Tournament(**temp_data)

            tournament_data_clean = tournamentData.copy()
            
            # Convertir les dates en ISO string pour Supabase
            if isinstance(tournament_data_clean.get("start_date"), date):
                tournament_data_clean["start_date"] = tournament_data_clean["start_date"].isoformat()
            
            if isinstance(tournament_data_clean.get("start_time"), time):
                tournament_data_clean["start_time"] = tournament_data_clean["start_time"].isoformat()
            
            # Sauvegarder en DB
            result = self.supabase.table("tournament").insert(tournament_data_clean).execute()
            
            if not result.data:
                print("❌ Erreur lors de l'insertion en DB")
                return None
            
            print(f"✅ Tournoi créé avec ID: {tournament_data_clean}")
            return Tournament(**result.data[0])
            
        except Exception as e:
            print(f"❌ Erreur création tournoi: {e}")
            return None

    def getTournamentWithTeams(self, tournamentId: str) -> Optional[Dict[str, Any]]:
        """
        Récupère un tournoi avec ses équipes
        
        Args:
            tournmentId: ID du tournoi
            
        Returns:
            dict: {"tournament": Tournament, "teams": List[Team]} ou None si erreur
        """
        try:
            print(f"🔍 Récupération tournoi + équipes {tournamentId}")
            
            tournament = self.getTournamentById(tournamentId)
            if not tournament:
                return None
            teams = self.getTournamentTeams(tournamentId)
            if len(teams) < 1:
                return None
            result = {
                "tournament": tournament,
                "teams": teams,
                "teams_count": len(teams),
                "has_minimum_teams": len(teams) >= 2,
                "can_start": len(teams) >= 2 and tournament.status == "ready"
            }
            
            print(f"✅ Tournoi + {len(teams)} équipes récupérés")
            return result
            
        except Exception as e:
            print(f"❌ Erreur récupération tournoi avec équipes: {e}")
            return None

    def updateTournamentStatus(self, tournamentId: str, newStatus: str) -> bool:
        """
        Met à jour le statut d'un tournoi
        
        Args:
            tournamentId: ID du tournoi
            newStatus: Nouveau statut
            
        Returns:
            bool: Succès de l'opération
        """
        try:
            print(f"🔄 Mise à jour statut tournoi {tournamentId} → {newStatus}")
            
            result = self.supabase.table("tournament")\
                .update({
                    "status": newStatus,
                    "updated_at": datetime.now().isoformat()
                })\
                .eq("id", tournamentId)\
                .execute()
            
            print(f"✅ Statut tournoi mis à jour")
            return True
            
        except Exception as e:
            print(f"❌ Erreur mise à jour statut tournoi: {e}")
            return False

    def createTeam(self, teamData: dict) -> Optional[Team]:
        """
        Crée une nouvelle équipe
        
        Args:
            teamData: Données de l'équipe (dict)
            
        Returns:
            Team: Équipe créée ou None si erreur
        """
        try:
            print(f"👥 Création nouvelle équipe: {teamData.get('name', 'Sans nom')}")
            # Ajouter l'ID et timestamps
            team_data_temp = teamData.copy()
            team_data_temp.update({
                "id": "00000000-0000-0000-0000-000000000000",
                "created_at": datetime.now(),
                "updated_at": datetime.now()
            })
            
            # Valider avec Pydantic
            team = Team(**team_data_temp)
            
            # Convertir en dict pour Supabase
            team_dict = teamData.copy()
            if team_dict.get("created_at"):
                team_dict["created_at"] = team_dict["created_at"].isoformat()
            if team_dict.get("updated_at"):
                team_dict["updated_at"] = team_dict["updated_at"].isoformat()
            
            # Sauvegarder en DB
            result = self.supabase.table("team").insert(team_dict).execute()

            if not result.data:
                print("❌ Erreur lors de l'insertion équipe en DB")
                return None
            
            # Ajouter automatiquement le captain dans team_member si captain_id existe
            created_team = result.data[0]
            if created_team.get("captain_id"):
                try:
                    print(f"👑 Ajout du capitaine à team_member: {created_team['captain_id']}")
                    team_member_data = {
                        "team_id": created_team["id"],
                        "user_id": created_team["captain_id"],
                        "role": "captain",
                        "status": "active"
                    }
                    team_member_result = self.supabase.table("team_member").insert(team_member_data).execute()
                    print(f"✅ Capitaine ajouté à team_member")
                except Exception as member_error:
                    print(f"⚠️ Erreur ajout capitaine à team_member (équipe créée): {member_error}")
                    # L'équipe est créée même si l'ajout du capitaine échoue
            
            print(f"✅ Équipe créée avec ID: {created_team['id']}")
            return Team(**created_team)
            
        except Exception as e:
            print(f"❌ Erreur création équipe: {e}")
            return None

    def getTeamById(self, teamId: str) -> Optional[Team]:
        """
        Récupère une équipe par son ID
        
        Args:
            team_id: ID de l'équipe
            
        Returns:
            Team: Objet Team ou None si pas trouvé
        """
        try:
            print(f"🔍 Récupération équipe {teamId}")
            
            result = self.supabase.table("team")\
                .select("*")\
                .eq("id", teamId)\
                .single()\
                .execute()
            
            if not result.data:
                print(f"❌ Équipe {teamId} non trouvée")
                return None
            
            # Convertir en objet Pydantic
            team = Team(**result.data)
            print(f"✅ Équipe récupérée: {team.name}")
            return team
            
        except Exception as e:
            print(f"❌ Erreur récupération équipe {teamId}: {e}")
            return None

    def deleteTeamById(self, teamId: str) -> bool:
        try:
            team = self.getTeamById(teamId)

            result = self.supabase.table("team")\
                .delete()\
                .eq("id", team.id)\
                .execute()
            if result:
                return True
        except Exception as e:
            print(f"Erreur lors de la suppression: {e}")
            return False

    def _validateTournamentData(self, tournamentData: Dict[str, Any]) -> bool:
        """Valide si le tournoi peut avoir un planning généré"""
        try:
            tournament = tournamentData["tournament"]
            teams = tournamentData["teams"]
            
            print(f"🔍 Validation: {len(teams)} équipes, {tournament.courts_available} terrains")
            
            # Vérifier nombre minimum d'équipes
            if len(teams) < 2:
                print("❌ Pas assez d'équipes (minimum 2)")
                return False
            
            # Vérifier nombre maximum d'équipes
            if len(teams) > tournament.max_teams:
                print(f"❌ Trop d'équipes ({len(teams)} > {tournament.max_teams})")
                return False
            
            # Vérifier terrains
            if tournament.courts_available <= 0:
                print("❌ Nombre de terrains invalide")
                return False
            
            # Vérifier type de tournoi
            if not tournament.tournament_type:
                print("❌ Type de tournoi manquant")
                return False
            
            print("✅ Validation réussie")
            return True
            
        except Exception as e:
            print(f"❌ Erreur validation: {e}")
            return False

    def getTeams(self, tournamentId: str = None) -> list[Team]:
        try:
            if not tournamentId:
                result = self.supabase.table("team")\
                    .select("*")\
                    .execute()
            else:
                result = self.supabase.table("team")\
                    .select("*")\
                    .eq("tournament_id", tournamentId)\
                    .execute()

            teams = []
            for team_data in result.data or []:
                try:
                    team = Team(**team_data)
                    teams.append(team)
                except Exception as e:
                    print(f"⚠️ Team invalide ignorée: {e}")
                    continue
            return teams
        except Exception as e:
            print(f"❌ Erreur récupération teams : {e}")
            return None 
    
    def _getTeamMembers(self, teamId: str) -> List[TeamMember]:
        """Récupère les membres d'une équipe et les convertit en objets TeamMember"""
        try:
            result = self.supabase.from_("team_member")\
                .select("*, profile(email)")\
                .eq("team_id", teamId)\
                .execute()
            
            members = []
            for member_data in result.data or []:
                try:
                    # Créer l'objet TeamMember avec validation Pydantic
                    email = member_data.pop("profile")["email"]
                    team_member = TeamMember(**member_data, email=email)
                    members.append(team_member)
                except Exception as e:
                    print(f"⚠️ Membre d'équipe invalide ignoré: {e}")
                    continue
            
            return members
            
        except Exception as e:
            print(f"❌ Erreur récupération membres équipe: {e}")
            return []
        
    def getTeamsWithMembers(self, tournamentId: str = None) -> Optional[List[TeamWithMembers]]:
        """Récupère toutes les équipes avec leurs membres"""
        try:
            teams = self.getTeams(tournamentId)
            if not teams:
                print("❌ Aucune équipe trouvée")
                return []
                
            teams_with_members = []
            for team in teams:
                try:
                    team_members = self._getTeamMembers(team.id)
                    team_with_members = TeamWithMembers(
                        **team.model_dump(), 
                        members=team_members
                    )
                    teams_with_members.append(team_with_members)
                except Exception as e:
                    print(f"⚠️ Erreur lors du traitement de l'équipe {team.id}: {e}")
                    continue
                    
            print(f"✅ {len(teams_with_members)} équipe(s) avec membres récupérée(s)")
            return teams_with_members
            
        except Exception as e:
            print(f"❌ Erreur récupération teams avec membres: {e}")
            return None
    
    def addTeamMembers(self, teamMembersData: dict) -> Optional[List[TeamMember]]:
        try:
                        
            # Préparer les données pour insertion en lot
            team_members_data = []
            for player in teamMembersData.players:
                team_member_data = {
                    "team_id": teamMembersData.team_id,
                    "user_id": player.user_id,
                    "role": player.role or "player",
                    "position": player.position or "",
                    "status": player.status or "active",
                }
                team_members_data.append(team_member_data)
            
            # Insertion en lot dans la DB
            result = self.supabase.table("team_member")\
                .insert(team_members_data)\
                .execute()
            
            if not result.data:
                print("❌ Aucun joueur ajouté")
                return None
            
            # Convertir en objets TeamMember
            added_members = []
            for member_data in result.data:
                try:
                    team_member = TeamMember(**member_data)
                    added_members.append(team_member)
                except Exception as e:
                    print(f"⚠️ Erreur conversion TeamMember: {e}")
                    continue
            
            print(f"✅ {len(added_members)} joueur(s) ajouté(s) à l'équipe avec succès")
            return added_members
            
        except Exception as e:
            print(f"❌ Erreur ajout joueurs: {e}")
            return None
    
tournamentService = TournamentService()