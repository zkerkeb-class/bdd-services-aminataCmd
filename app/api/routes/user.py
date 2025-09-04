from fastapi import APIRouter, HTTPException, status, Path, Query
from app.services.database_service import DatabaseService
from app.schemas.response import UserResponse

# Router avec préfixe et tags
router = APIRouter(
    prefix="/api/users",
    tags=["Users"]
)

# Instance globale du service database (style établi)
databaseService = DatabaseService()

@router.get("/{user_id}", response_model=UserResponse)
def get_user_by_id(user_id: str = Path(..., description="ID de l'utilisateur (UUID)")):
    """Récupère un utilisateur par son ID"""
    try:
        # Appel du service
        user = databaseService.getUserById(user_id)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Utilisateur avec l'ID {user_id} non trouvé"
            )
        
        return UserResponse(
            success=True,
            message=f"Utilisateur {user.email} récupéré avec succès",
            data=user
        )
    except Exception as e:
        print(f"❌ Erreur récupération utilisateur: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur interne lors de la récupération de l'utilisateur"
        )
    
@router.get("/", response_model=UserResponse)
def get_user_by_email(email: str = Query(..., description="Email de l'utilisateur")):
    """Récupère un utilisateur par son email"""
    try:
        # Appel du service
        user = databaseService.getUserByEmail(email)
        
        if not user:
            # send invitation email
            databaseService.sendInvitationEmail(email)
            return UserResponse(
                success=True,
                message=f"Utilisateur avec l'email {email} non trouvé, invitation envoyée",
                data=None
            )
        
        return UserResponse(
            success=True,
            message=f"Utilisateur {user.email} récupéré avec succès",
            data=user
        )
    except Exception as e:
        print(f"❌ Erreur récupération utilisateur: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur interne lors de la récupération de l'utilisateur"
        )