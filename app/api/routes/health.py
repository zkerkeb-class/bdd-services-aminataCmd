from fastapi import APIRouter, HTTPException, status
from datetime import datetime
import os
from app.schemas.response import HealthResponse, DetailedHealthResponse

router = APIRouter(
    prefix="/api/health",
    tags=["Health Check"]
)

@router.get("/", response_model=HealthResponse)
async def health_check():
    """Health check basique de l'API"""
    try:
        # Vérification basique des services
        services_status = {}
        
        # Vérifier les services principaux
        try:
            from app.services.ai_planning_service import aiPlanningService
            services_status["ai_planning"] = "healthy"
        except Exception:
            services_status["ai_planning"] = "unhealthy"
        
        try:
            from app.services.tournament_service import tournamentService
            services_status["tournament"] = "healthy"
        except Exception:
            services_status["tournament"] = "unhealthy"
        
        try:
            from app.services.database_service import databaseService
            services_status["database"] = "healthy"
        except Exception:
            services_status["database"] = "unhealthy"
        
        try:
            from app.services.openai_client_service import openai_service
            services_status["openai"] = "healthy"
        except Exception:
            services_status["openai"] = "unhealthy"
        
        # Déterminer le statut global
        global_status = "healthy" if all(s == "healthy" for s in services_status.values()) else "degraded"
        
        return HealthResponse(
            status=global_status,
            timestamp=datetime.utcnow(),
            version=os.getenv("APP_VERSION", "1.0.0"),
            services=services_status
        )
        
    except Exception as e:
        print(f"❌ Erreur health check: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors du health check"
        )


@router.get("/detailed", response_model=DetailedHealthResponse)
async def detailed_health_check():
    """Health check détaillé avec informations étendues"""
    try:
        # Informations système
        import psutil
        import time
        
        # Calcul uptime approximatif
        uptime_seconds = time.time() - psutil.boot_time()
        uptime_hours = int(uptime_seconds // 3600)
        uptime_minutes = int((uptime_seconds % 3600) // 60)
        uptime_str = f"{uptime_hours}h {uptime_minutes}m"
        
        # Vérification détaillée des services
        detailed_services = {}
        
        # AI Planning Service
        try:
            from app.services.ai_planning_service import aiPlanningService
            detailed_services["ai_planning"] = {
                "status": "healthy",
                "last_check": datetime.utcnow().isoformat(),
                "details": "Service disponible"
            }
        except Exception as e:
            detailed_services["ai_planning"] = {
                "status": "unhealthy",
                "last_check": datetime.utcnow().isoformat(),
                "details": str(e)
            }
        
        # Tournament Service
        try:
            from app.services.tournament_service import tournamentService
            detailed_services["tournament"] = {
                "status": "healthy",
                "last_check": datetime.utcnow().isoformat(),
                "details": "Service disponible"
            }
        except Exception as e:
            detailed_services["tournament"] = {
                "status": "unhealthy",
                "last_check": datetime.utcnow().isoformat(),
                "details": str(e)
            }
        
        # Database Service
        try:
            from app.services.database_service import databaseService
            detailed_services["database"] = {
                "status": "healthy",
                "last_check": datetime.utcnow().isoformat(),
                "details": "Service disponible"
            }
        except Exception as e:
            detailed_services["database"] = {
                "status": "unhealthy",
                "last_check": datetime.utcnow().isoformat(),
                "details": str(e)
            }
        
        # OpenAI Service
        try:
            from app.services.openai_client_service import openai_service
            detailed_services["openai"] = {
                "status": "healthy",
                "last_check": datetime.utcnow().isoformat(),
                "details": "Service disponible"
            }
        except Exception as e:
            detailed_services["openai"] = {
                "status": "unhealthy",
                "last_check": datetime.utcnow().isoformat(),
                "details": str(e)
            }
        
        # Vérification Supabase
        try:
            from app.core.database import getSupabase
            supabase = getSupabase()
            # Test de connexion simple
            result = supabase.table("tournament").select("id").limit(1).execute()
            detailed_services["supabase"] = {
                "status": "healthy",
                "last_check": datetime.utcnow().isoformat(),
                "details": "Connexion base de données OK"
            }
        except Exception as e:
            detailed_services["supabase"] = {
                "status": "unhealthy",
                "last_check": datetime.utcnow().isoformat(),
                "details": f"Erreur connexion DB: {str(e)}"
            }
        
        # Statut global
        healthy_count = sum(1 for s in detailed_services.values() if s["status"] == "healthy")
        total_count = len(detailed_services)
        
        if healthy_count == total_count:
            global_status = "healthy"
        elif healthy_count > 0:
            global_status = "degraded"
        else:
            global_status = "unhealthy"
        
        return DetailedHealthResponse(
            status=global_status,
            timestamp=datetime.utcnow(),
            version=os.getenv("APP_VERSION", "1.0.0"),
            uptime=uptime_str,
            services=detailed_services
        )
        
    except Exception as e:
        print(f"❌ Erreur health check détaillé: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors du health check détaillé"
        )


@router.get("/ping")
async def ping():
    """Ping simple pour vérifier que l'API répond"""
    return {"status": "pong", "timestamp": datetime.utcnow()}