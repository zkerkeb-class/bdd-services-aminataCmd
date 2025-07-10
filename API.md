# API Documentation

## Base URL
```
http://localhost:8000
```

## Health Check

### GET `/api/health/`
Status basique de l'API

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-06-25T14:30:00Z",
  "version": "1.0.0",
  "services": {
    "ai_planning": "healthy",
    "tournament": "healthy", 
    "database": "healthy",
    "openai": "healthy"
  }
}
```

### GET `/api/health/detailed`
Health check détaillé avec informations sur tous les services

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-06-25T14:30:00Z",
  "version": "1.0.0",
  "uptime": "2h 45m",
  "services": {
    "database": {
      "status": "healthy",
      "last_check": "2025-06-25T14:30:00Z",
      "details": "Service disponible"
    },
    "openai": {
      "status": "healthy",
      "last_check": "2025-06-25T14:30:00Z",
      "details": "Service disponible"
    },
    "ai_planning": {
      "status": "healthy",
      "last_check": "2025-06-25T14:30:00Z",
      "details": "Service disponible"
    },
    "tournament": {
      "status": "healthy",
      "last_check": "2025-06-25T14:30:00Z",
      "details": "Service disponible"
    }
  }
}
```

### GET `/api/health/ping`
Ping simple
```json
{
  "status": "pong",
  "timestamp": "2025-06-25T14:30:00Z"
}
```

## AI Planning

### POST `/api/planning/generate`
Génère un planning IA pour un tournoi

**Request:**
```json
{
  "tournament_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Planning généré avec succès",
  "data": {
    "id": "planning-uuid",
    "tournament_id": "tournament-uuid",
    "type_tournoi": "round_robin",
    "status": "completed",
    "total_matches": 12,
    "planning_data": {...},
    "created_at": "2025-06-25T14:30:00Z"
  }
}
```

### GET `/api/planning/{planning_id}/status`
Récupère le statut d'un planning

**Response:**
```json
{
  "success": true,
  "message": "Statut récupéré avec succès",
  "data": {
    "status": "completed",
    "planning_id": "planning-uuid"
  }
}
```

### POST `/api/planning/{planning_id}/regenerate`
Régénère un planning existant

**Response:**
```json
{
  "success": true,
  "message": "Planning régénéré avec succès",
  "data": {
    "id": "new-planning-uuid",
    "tournament_id": "tournament-uuid",
    "status": "completed"
  }
}
```

### GET `/api/planning/{planning_id}`
Récupère un planning complet par son ID

**Response:**
```json
{
  "success": true,
  "message": "Planning récupéré avec succès",
  "data": {
    "planning": {...},
    "matches": [...],
    "poules": [...]
  }
}
```

### GET `/api/planning/tournament/{tournament_id}`
Récupère le planning d'un tournoi par l'ID du tournoi

**Response:**
```json
{
  "success": true,
  "message": "Planning récupéré avec succès",
  "data": {
    "planning": {
      "id": "planning-uuid",
      "tournament_id": "tournament-uuid",
      "type_tournoi": "round_robin",
      "status": "completed",
      "total_matches": 12,
      "planning_data": {...},
      "created_at": "2025-06-25T14:30:00Z"
    },
    "matches": [
      {
        "id": "match-uuid-1",
        "planning_id": "planning-uuid",
        "team1_id": "team-uuid-1",
        "team2_id": "team-uuid-2",
        "round": 1,
        "match_order": 1,
        "start_time": "09:00:00",
        "duration_minutes": 30,
        "court": "Court 1",
        "referee": null,
        "status": "scheduled"
      }
    ],
    "poules": [
      {
        "id": "poule-uuid-1",
        "planning_id": "planning-uuid",
        "poule_id": "poule_a",
        "nom_poule": "Poule A",
        "equipes": ["Équipe 1", "Équipe 2", "Équipe 3"],
        "nb_equipes": 3,
        "nb_matches": 3
      }
    ]
  }
}
```

## Tournaments

### GET `/api/tournaments/`
Récupère tous les tournois

**Response:**
```json
{
  "success": true,
  "message": "Tournoi récupéré avec succès",
  "data": [
    {
      "id": "tournament-uuid-1",
      "name": "Tournoi été 2025", 
      "tournament_type": "round_robin",
      "max_teams": 8,
      "registered_teams": 4,
      "status": "ready",
      "start_date": "2025-07-15",
      "start_time": "09:00:00",
      "created_at": "2025-06-25T14:30:00Z"
    },
    {
      "id": "tournament-uuid-2",
      "name": "Coupe de France",
      "tournament_type": "elimination_directe", 
      "max_teams": 16,
      "registered_teams": 12,
      "status": "draft",
      "start_date": "2025-08-01",
      "created_at": "2025-06-25T15:00:00Z"
    }
  ]
}
```

### POST `/api/tournaments/`
Crée un nouveau tournoi

**Request:**
```json
{
  "name": "Tournoi été 2025",
  "description": "Tournoi de volley-ball",
  "tournament_type": "round_robin",
  "max_teams": 8,
  "courts_available": 2,
  "start_date": "2025-07-15",
  "start_time": "09:00",
  "match_duration_minutes": 15,
  "break_duration_minutes": 5,
  "constraints": {},
  "organizer_id": "550e8400-e29b-41d4-a716-446655440001",
  "status": "draft"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Tournoi créé avec succès",
  "data": {
    "id": "auto-generated-uuid",
    "name": "Tournoi été 2025",
    "tournament_type": "round_robin",
    "max_teams": 8,
    "courts_available": 2,
    "start_date": "2025-07-15",
    "start_time": "09:00:00",
    "status": "draft",
    "created_at": "2025-06-25T14:30:00Z",
    "updated_at": "2025-06-25T14:30:00Z"
  }
}
```

### GET `/api/tournaments/{tournament_id}`
Récupère un tournoi par son ID

**Response:**
```json
{
  "success": true,
  "message": "Tournoi récupéré avec succès",
  "data": {
    "id": "tournament-uuid",
    "name": "Tournoi été 2025",
    "tournament_type": "round_robin",
    "max_teams": 8,
    "status": "ready"
  }
}
```

### GET `/api/tournaments/{tournament_id}/with-teams`
Récupère un tournoi avec ses équipes

**Response:**
```json
{
  "success": true,
  "message": "Tournoi et équipes récupérés avec succès",
  "data": {
    "tournament": {...},
    "teams": [...],
    "teams_count": 4,
    "has_minimum_teams": true,
    "can_start": true
  }
}
```

### GET `/api/tournaments/{tournament_id}/teams`
Récupère toutes les équipes d'un tournoi

**Response:**
```json
{
  "success": true,
  "message": "4 équipe(s) récupérée(s) avec succès",
  "data": [
    {
      "id": "team-uuid",
      "name": "Les Champions",
      "tournament_id": "tournament-uuid",
      "contact_email": "champions@email.com",
      "skill_level": "intermediate",
      "status": "registered"
    }
  ]
}
```

### PATCH `/api/tournaments/{tournament_id}/status`
Met à jour le statut d'un tournoi

**Request:**
```json
{
  "status": "ready"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Statut du tournoi mis à jour vers 'ready'",
  "data": {
    "tournament_id": "tournament-uuid",
    "new_status": "ready"
  }
}
```

### POST `/api/tournaments/{tournament_id}/teams`
Crée une nouvelle équipe pour un tournoi

**Request:**
```json
{
  "name": "Les Champions",
  "description": "Équipe championne",
  "tournament_id": "tournament-uuid",
  "captain_id": "captain-uuid",
  "contact_email": "champions@email.com",
  "contact_phone": "0123456789",
  "skill_level": "intermediate",
  "notes": "Équipe expérimentée"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Équipe créée avec succès",
  "data": {
    "id": "auto-generated-uuid",
    "name": "Les Champions",
    "tournament_id": "tournament-uuid",
    "contact_email": "champions@email.com",
    "skill_level": "intermediate",
    "status": "registered",
    "created_at": "2025-06-25T14:30:00Z"
  }
}
```

### GET `/api/tournaments/teams/{team_id}`
Récupère une équipe par son ID

**Response:**
```json
{
  "success": true,
  "message": "Équipe récupérée avec succès",
  "data": {
    "id": "team-uuid",
    "name": "Les Champions",
    "tournament_id": "tournament-uuid",
    "contact_email": "champions@email.com",
    "skill_level": "intermediate"
  }
}
```

### DELETE `/api/tournaments/teams/{team_id}`
Supprime une équipe par son ID

**Response:**
```json
{
  "success": true,
  "message": "Equipe supprimee avec succes",
  "data": null
}
```

### POST `/api/tournaments/teams/{team_id}/members`
Ajoute plusieurs joueurs à une équipe en lot

**Request:**
```json
{
  "team_id": "team-uuid",
  "players": [
    {
      "user_id": "user-uuid-1",
      "role": "player",
      "position": "Attaquant",
      "status": "active"
    },
    {
      "user_id": "user-uuid-2", 
      "role": "player",
      "position": "Libéro",
      "status": "active"
    },
    {
      "user_id": "user-uuid-3",
      "role": "captain",
      "position": "Passeur",
      "status": "active"
    }
  ]
}
```

**Response:**
```json
{
  "success": true,
  "message": "3 joueur(s) ajouté(s) à l'équipe avec succès",
  "data": [
    {
      "id": "member-uuid-1",
      "team_id": "team-uuid",
      "user_id": "user-uuid-1",
      "role": "player",
      "position": "Attaquant",
      "status": "active",
      "joined_at": "2025-06-25T14:30:00Z",
      "created_at": "2025-06-25T14:30:00Z"
    },
    {
      "id": "member-uuid-2",
      "team_id": "team-uuid", 
      "user_id": "user-uuid-2",
      "role": "player",
      "position": "Libéro",
      "status": "active",
      "joined_at": "2025-06-25T14:30:00Z",
      "created_at": "2025-06-25T14:30:00Z"
    },
    {
      "id": "member-uuid-3",
      "team_id": "team-uuid",
      "user_id": "user-uuid-3", 
      "role": "captain",
      "position": "Passeur",
      "status": "active",
      "joined_at": "2025-06-25T14:30:00Z",
      "created_at": "2025-06-25T14:30:00Z"
    }
  ]
}
```

## Teams

### GET `/api/teams/`
Récupère toutes les équipes de tous les tournois

**Response:**
```json
{
  "success": true,
  "message": "8 équipe(s) récupérée(s) avec succès",
  "data": [
    {
      "id": "team-uuid-1",
      "name": "Les Champions",
      "description": "Équipe expérimentée",
      "tournament_id": "tournament-uuid-1",
      "captain_id": "user-uuid-1",
      "status": "registered",
      "contact_email": "champions@email.com",
      "contact_phone": "0123456789",
      "skill_level": "intermediate",
      "notes": "Équipe motivée",
      "created_at": "2025-06-25T14:30:00Z",
      "updated_at": "2025-06-25T14:30:00Z"
    },
    {
      "id": "team-uuid-2",
      "name": "Les Aigles",
      "description": "Jeune équipe prometteuse",
      "tournament_id": "tournament-uuid-1",
      "captain_id": "user-uuid-2",
      "status": "registered",
      "contact_email": "aigles@email.com",
      "contact_phone": "0987654321",
      "skill_level": "beginner",
      "notes": "Première participation",
      "created_at": "2025-06-25T15:00:00Z",
      "updated_at": "2025-06-25T15:00:00Z"
    }
  ]
}
```

### GET `/api/teams/with-members`
Récupère toutes les équipes avec leurs membres

**Response:**
```json
{
  "success": true,
  "message": "2 équipe(s) récupérée(s) avec succès",
  "data": [
    {
      "id": "team-uuid-1",
      "name": "Les Champions",
      "description": "Équipe expérimentée",
      "tournament_id": "tournament-uuid-1",
      "captain_id": "user-uuid-1",
      "status": "registered",
      "contact_email": "champions@email.com",
      "contact_phone": "0123456789",
      "skill_level": "intermediate",
      "notes": "Équipe motivée",
      "created_at": "2025-06-25T14:30:00Z",
      "updated_at": "2025-06-25T14:30:00Z",
      "members": [
        {
          "id": "member-uuid-1",
          "team_id": "team-uuid-1",
          "user_id": "user-uuid-1",
          "role": "captain",
          "email": "member-1@example.com",
          "position": null,
          "status": "active",
          "joined_at": "2025-06-25T14:30:00Z",
          "created_at": "2025-06-25T14:30:00Z"
        },
        {
          "id": "member-uuid-2",
          "team_id": "team-uuid-1",
          "user_id": "user-uuid-3",
          "role": "player",
          "position": "Attaquant",
          "email": "member-2@example.com",
          "status": "active",
          "joined_at": "2025-06-25T14:35:00Z",
          "created_at": "2025-06-25T14:35:00Z"
        }
      ]
    }
  ]
}
```

## Users

### GET `/api/users/{user_id}`
Récupère un utilisateur par son ID

**Response:**
```json
{
  "success": true,
  "message": "Utilisateur user@example.com récupéré avec succès",
  "data": {
    "id": "user-uuid",
    "email": "user@example.com",
    "first_name": "Jean",
    "last_name": "Dupont",
    "display_name": "Jean D.",
    "role": "player",
    "phone": "+33123456789",
    "avatar_url": "https://example.com/avatar.jpg",
    "bio": "Passionné de volleyball",
    "preferred_language": "fr",
    "timezone": "Europe/Paris",
    "email_notifications": true,
    "push_notifications": true,
    "is_active": true,
    "email_verified": true,
    "metadata": {},
    "created_at": "2025-06-25T14:30:00Z",
    "updated_at": "2025-06-25T14:30:00Z",
    "last_login": "2025-06-25T14:00:00Z"
  }
}
```

### GET `/api/users/?email={email}`
Récupère un utilisateur par son email

**Paramètres:**
- `email` (query parameter): Email de l'utilisateur à rechercher

**Response (utilisateur trouvé):**
```json
{
  "success": true,
  "message": "Utilisateur user@example.com récupéré avec succès",
  "data": {
    "id": "user-uuid",
    "email": "user@example.com",
    "first_name": "Jean",
    "last_name": "Dupont",
    "display_name": "Jean D.",
    "role": "player",
    "phone": "+33123456789",
    "avatar_url": "https://example.com/avatar.jpg",
    "bio": "Passionné de volleyball",
    "preferred_language": "fr",
    "timezone": "Europe/Paris",
    "email_notifications": true,
    "push_notifications": true,
    "is_active": true,
    "email_verified": true,
    "metadata": {},
    "created_at": "2025-06-25T14:30:00Z",
    "updated_at": "2025-06-25T14:30:00Z",
    "last_login": "2025-06-25T14:00:00Z"
  }
}
```

**Response (utilisateur non trouvé - invitation envoyée):**
```json
{
  "success": true,
  "message": "Utilisateur avec l'email newuser@example.com non trouvé, invitation envoyée",
  "data": null
}
```

## Error Responses

### 400 Bad Request
```json
{
  "success": false,
  "message": "Données invalides",
  "data": null
}
```

### 404 Not Found
```json
{
  "success": false,
  "message": "Ressource non trouvée",
  "data": null
}
```

### 500 Internal Server Error
```json
{
  "success": false,
  "message": "Erreur interne du serveur",
  "data": null
}
```

## Data Types

### Tournament Types
- `round_robin`
- `elimination_directe`
- `poules_elimination`

### Tournament Status
- `draft`
- `ready`
- `active`
- `completed`
- `cancelled`

### Team Skill Levels
- `beginner`
- `intermediate`
- `advanced`

### Team Status
- `registered`
- `confirmed`
- `cancelled`

### Team Member Roles
- `captain`
- `player`

### Team Member Status
- `active`
- `inactive`
- `pending`

### Team Member Positions (Volleyball)
- `Attaquant`
- `Passeur`
- `Libéro`
- `Central`
- `Réceptionneur-Attaquant`

### Planning Status
- `generating`
- `completed`
- `error`
- `cancelled`

## Rate Limits
- 100 requests/minute per IP
- 1000 requests/hour per IP

## Authentication
Currently no authentication required (MVP version)