import uuid
from datetime import datetime
from typing import List, Optional
from app.core.database import getSupabase
from app.models.models import (
    AITournamentPlanning, 
    AIPlanningData, AIGeneratedMatch, AIGeneratedPoule,
    Match,
    Profile
)

class DatabaseService():

    def __init__(self):
        self.supabase = getSupabase()
    
    def savePlanning(self, 
                      tournamentId: str, 
                      planningData: dict, 
                      typeTournoi:str) -> Optional[AITournamentPlanning]:
        """
        Sauvegarde le planning principal en DB
        
        Args:
            tournament_id: ID du tournoi
            planning_data: JSON complet de l'IA
            type_tournoi: Type de tournoi
            
        Returns:
            AITournamentPlanning: Planning créé ou None si erreur
        """
        try: 
            print(f"💾 Sauvegarde planning pour tournoi {tournamentId}")
            
            # Générer ID unique
            planning_id = str(uuid.uuid4())
            
            # Valider les données avec Pydantic
            ai_planning_data = AIPlanningData(**planningData)
            total_matches = ai_planning_data.calculate_total_matches()
            
            # Créer l'objet Planning
            planning_obj = AITournamentPlanning(
                id=planning_id,
                tournament_id=tournamentId,
                type_tournoi=typeTournoi,
                status="generated",
                planning_data=planningData,
                total_matches=total_matches,
                ai_comments=ai_planning_data.commentaires,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            
            # Convertir en dict pour Supabase
            planning_dict = planning_obj.model_dump()
            planning_dict["created_at"] = planning_dict["created_at"].isoformat()
            planning_dict["updated_at"] = planning_dict["updated_at"].isoformat()
            
            # Sauvegarder
            result = self.supabase.table("ai_tournament_planning").insert(planning_dict).execute()
            
            print(f"✅ Planning {planning_id} sauvegardé ({total_matches} matchs)")
            
            # Retourner l'objet Planning créé
            return AITournamentPlanning(**result.data[0])
        except Exception as e:
            print(f"Erreur lors de la sauvegarde : {e}")
            return None
        
    def saveMatches(self, 
                    planningId: str, 
                    planningData: dict) -> Optional[List[AIGeneratedMatch]]:
        """
        Sauvegarde tous les matchs en lot
        
        Args:
            planning_id: ID du planning
            planning_data: Données JSON de l'IA
            
        Returns:
            List[AIGeneratedMatch]: Matchs sauvegardés ou None si erreur
        """

        try:
            print(f"Extraction et sauvegarde des matchs pour planning {planningId}")

            allMatches = []
            aiPlanningData = AIPlanningData(**planningData)

            roundRobinMatches = self._extractRoundRobinMatches(planningId, aiPlanningData)
            allMatches.extend(roundRobinMatches)

            poulesMatches = self._extractPoulesMatches(planningId, aiPlanningData)
            allMatches.extend(poulesMatches)

            eliminationMatches = self._extractEliminationMatches(planningId, aiPlanningData)
            allMatches.extend(eliminationMatches)

            if allMatches:
                matchesDicts = []
                for match in allMatches:
                    matchDict = match.model_dump()
                    matchDict["created_at"] = matchDict["created_at"].isoformat()
                    matchDict["debut_horaire"] = matchDict["debut_horaire"].isoformat()
                    matchDict["fin_horaire"] = matchDict["fin_horaire"].isoformat()

                    matchesDicts.append(matchDict)

                result = self.supabase.table("ai_generated_match").insert(matchesDicts).execute()
                print(f"{len(allMatches)} matchs sauvegardes en lot")
                print(f"result : {result.data}")
                return [AIGeneratedMatch(**data) for data in result.data]

            else:
                print("Aucun match à sauvegarder")
                return []

        except Exception as e:
            print(f"Erreur lors de la sauvegarde des matchs: {e}")
            return None

    def savePoules(self, 
                    planningId: str, 
                    planningData: dict) -> Optional[List[AIGeneratedPoule]]:
        """
        Sauvegarde les poules en lot
        
        Args:
            planning_id: ID du planning
            planning_data: Données JSON de l'IA
            
        Returns:
            List[AIGeneratedPoule]: Poules sauvegardées ou None si erreur
        """

        try:    
            aiPlanningData = AIPlanningData(**planningData)

            if not aiPlanningData.poules:
                print("Pas de poules à sauvegarder")
                return []
            
            print(f"Sauvegarde de {len(aiPlanningData.poules)} poules")

            allPoules = []

            for poule in aiPlanningData.poules:
                pouleObj = AIGeneratedPoule(
                    id=str(uuid.uuid4()),
                    planning_id=planningId,
                    poule_id=poule.poule_id,
                    nom_poule=poule.nom_poule,
                    equipes=poule.equipes,
                    nb_equipes=len(poule.equipes),
                    nb_matches=len(poule.matchs),
                    created_at=datetime.now()
                )
                allPoules.append(pouleObj)

            if allPoules:
                poulesDicts = []
                for poule in allPoules:
                    pouleDict = poule.model_dump()
                    pouleDict["created_at"] = pouleDict["created_at"].isoformat()
                    poulesDicts.append(pouleDict)
                
                result = self.supabase.table("ai_generated_poule").insert(poulesDicts).execute()
                print(f"{len(allPoules)} poules sauvegardees")

                return [AIGeneratedPoule(**data) for data in result.data]
            else:
                return []

        except Exception as e:
            print(f"Erreur lors de la sauvegarde des poules {e}")

    def getPlanningWithDetailsByPlanningId(self, planningId: str) -> Optional[dict]:
        """
        Récupère un planning avec tous ses détails
        
        Args:
            planningId: ID du planning
            
        Returns:
            dict: {
            "planning": AITournamentPlanning, 
            "matches": List[AIGeneratedMatch], 
            "poules": List[AIGeneratedPoule]
            } ou None si erreur
        """
        try:
            print(f"Recuperation planning {planningId}")

            planningResult = self.supabase.table("ai_tournament_planning")\
                .select("*")\
                .eq("id", planningId)\
                .single()\
                .execute()
            if not planningResult.data:
                print("Planning non trouve")
                return None
            planningObj = AITournamentPlanning(**planningResult.data)

            # matchesResult = self.supabase.table("ai_generated_match")\
            #     .select("*")\
            #     .eq("planning_id", planningId)\
            #     .order("debut_horaire")\
            #     .execute()
            # matchesObj = [AIGeneratedMatch(**matchData) for matchData in matchesResult.data or []]

            # poulesResult = self.supabase.table("ai_generated_poule")\
            #     .select("*")\
            #     .eq("planning_id", planningId)\
            #     .execute()
            # poulesObj = [AIGeneratedPoule(**pouleData) for pouleData in poulesResult.data or []]


            return planningObj
        
        except Exception as e:
            print(f"Erreur recuperation planning {e}")
            return None

    def getPlanningWithDetailsByTournamentId(self, tournamentId: str) -> Optional[dict]:
        """
        Récupère un planning avec tous ses détails par l'ID du tournoi
        """
        try:
            print(f"Recuperation planning par tournoi {tournamentId}")

            planningResult = self.supabase.table("ai_tournament_planning")\
                .select("*")\
                .eq("tournament_id", tournamentId)\
                .single()\
                .execute()
            
            if not planningResult.data:
                print("Planning non trouve")
                return None
            
            planningObj = AITournamentPlanning(**planningResult.data)
            
            return planningObj
        
        except Exception as e:
            print(f"Erreur recuperation planning par tournoi {e}")
            return None

    def updatePlanningStatus(self, 
                             planningId: str, 
                             newStatus: str) -> bool:
        """
        Met à jour le statut d'un planning
        
        Args:
            planningId: ID du planning
            newStatus: Nouveau statut
            
        Returns:
            bool: Succès de l'opération
        """
        try:
            print(f"Mise à jour statut planning {planningId} -> {newStatus}")
            result = self.supabase.table("ai_tournament_planning")\
            .update({
                "status": newStatus,
                "updated_at": datetime.now().isoformat()
            })\
            .eq("id", planningId)\
            .execute()

            print("Statut mis à jour")
            return True
        
        except Exception as e:
            print(f"Erreur mise à jour planning: {e}")
            return False

    def _extractRoundRobinMatches(self, 
                                  planningId: str, 
                                  aiPlanningData: AIPlanningData) -> List[AIGeneratedMatch]:
        """
        Extrait les matchs round robin
        """
        matches = []

        for match in aiPlanningData.matchs_round_robin:
            try:
                matchObj = AIGeneratedMatch(
                    id=str(uuid.uuid4()),
                    planning_id=planningId,
                    match_id_ai=match.match_id,
                    equipe_a=match.equipe_a,
                    equipe_b=match.equipe_b,
                    terrain=match.terrain,
                    debut_horaire=match.debut_horaire,
                    fin_horaire=match.fin_horaire,
                    phase="round_robin",
                    journee=match.journee,
                    status="scheduled",
                    created_at=datetime.now()
                )
                matches.append(matchObj)
            except Exception as e:
                print(f"Match round robin invalide ignore: {e}")
                continue
        
        return matches

    def _extractPoulesMatches(self, 
                              planningId: str, 
                              aiPlanningData: AIPlanningData) -> List[AIGeneratedPoule]:
        """
        Extrait les matchs de poules
        """
        matches = []

        for poule in aiPlanningData.poules:
            for match in poule.matchs:
                try:
                    matchObj = AIGeneratedMatch(
                        id=str(uuid.uuid4()),
                        planning_id=planningId,
                        match_id_ai=match.match_id,
                        equipe_a=match.equipe_a,
                        equipe_b=match.equipe_b,
                        terrain=match.terrain,
                        debut_horaire=match.debut_horaire,
                        fin_horaire=match.fin_horaire,
                        phase="poules",
                        poule_id=poule.poule_id,
                        status="scheduled",
                        created_at=datetime.now()
                    )
                    matches.append(matchObj)
                except Exception as e:
                    print(f"Match de poules invalide ignore: {e}")
                    continue
        return matches
    
    def _extractEliminationMatches(self,
                                   planningId: str, 
                                   aiPlanningData: AIPlanningData) -> List[AIGeneratedMatch]:
        """
        Extrait les matchs d'élimination apres les poules
        """

        matches = []

        if not aiPlanningData.phase_elimination_apres_poules:
            return matches
        
        elimination = aiPlanningData.phase_elimination_apres_poules

        # Quarts de finale
        for match in elimination.quarts:
            matchObj = self._createEliminationMatchObject(
                planningId,
                match, 
                "elimination"
            )
            if matchObj:
                matches.append(matchObj)

        # demi-finales
        for match in elimination.demi_finales:
            match_obj = self._createEliminationMatchObject(
                planningId, 
                match, 
                "elimination"
            )
            if match_obj:
                matches.append(match_obj)

        # Finale
        if elimination.finale:
            match_obj = self._createEliminationMatchObject(
                planningId, 
                elimination.finale, 
                "finale"
            )
            if match_obj:
                matches.append(match_obj)

        # Match 3e place
        if elimination.match_troisieme_place:
            match_obj = self._createEliminationMatchObject(
                planningId, 
                elimination.match_troisieme_place, 
                "elimination"
            )
            if match_obj:
                matches.append(match_obj)

        return matches
    
    def _createEliminationMatchObject(self, 
                                         planningId: str, 
                                         match: Match, 
                                         phase: str) -> Optional[AIGeneratedMatch]:
        """Crée un objet AIGeneratedMatch pour un match d'élimination"""
        try:
            return AIGeneratedMatch(
                id=str(uuid.uuid4()),
                planning_id=planningId,
                match_id_ai=match.match_id,
                equipe_a=match.equipe_a,
                equipe_b=match.equipe_b,
                terrain=match.terrain,
                debut_horaire=match.debut_horaire,
                fin_horaire=match.fin_horaire,
                phase=phase,
                status="scheduled",
                created_at=datetime.now()
            )
        except Exception as e:
            print(f"⚠️ Match élimination invalide ignore: {e}")
            return None
    
    def getUserById(self, userId: str) -> Optional[Profile]:
        """
        Récupère un utilisateur par son ID
        
        Args:
            userId: ID de l'utilisateur (UUID)
            
        Returns:
            Profile: Utilisateur trouvé ou None si erreur/non trouvé
        """
        try:
            print(f"🔍 Récupération utilisateur {userId}")
            
            # Récupérer l'utilisateur depuis la table profile
            result = self.supabase.table("profile")\
                .select("*")\
                .eq("id", userId)\
                .single()\
                .execute()
            
            if not result.data:
                print(f"❌ Aucun utilisateur trouvé avec l'ID {userId}")
                return None
            
            # Créer l'objet Profile
            user = Profile(**result.data)
            
            print(f"✅ Utilisateur {user.email} récupéré avec succès")
            return user
            
        except Exception as e:
            print(f"❌ Erreur lors de la récupération de l'utilisateur : {e}")
            return None

    def getUserByEmail(self, userEmail: str) -> Optional[Profile]:
        """
        Récupère un utilisateur par son email
        """
        try:
            print(f"🔍 Récupération utilisateur {userEmail}")
            
            # Récupérer l'utilisateur depuis la table profile
            result = self.supabase.table("profile")\
                .select("*")\
                .eq("email", userEmail)\
                .single()\
                .execute()
            
            if not result.data:
                print(f"❌ Aucun utilisateur trouvé avec l'email {userEmail}")
                return None
            
            # Créer l'objet Profile
            user = Profile(**result.data)
            
            print(f"✅ Utilisateur {user.email} récupéré avec succès")
            return user
            
        except Exception as e:
            print(f"❌ Erreur lors de la récupération de l'utilisateur : {e}")
            return None

    def sendInvitationEmail(self, email: str) -> bool:
        try:
            print(f"🔍 Envoi email d'invitation à {email}")
            result = self.supabase.auth.admin.invite_user_by_email(email)
            print(f"✅ Email d'invitation envoyé à {email}")
            return True
        except Exception as e:
            print(f"❌ Erreur envoi email d'invitation: {e}")
            return False
    
databaseService = DatabaseService()