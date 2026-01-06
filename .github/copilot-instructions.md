# Copilot Instructions for Routine Music Backend

## Project Overview
This is a FastAPI-based backend application for managing music routines with Spotify integration. The application allows users to:
- Register and authenticate with JWT tokens
- Connect their Spotify accounts using OAuth2 Authorization Code flow
- Create and manage music sessions
- Add and track songs
- Search for tracks via Spotify API

## Technology Stack
- **Framework**: FastAPI
- **Database**: SQLAlchemy ORM with SQLite (configurable via DATABASE_URL)
- **Authentication**: JWT tokens using python-jose, OAuth2 with Password flow
- **Password Hashing**: passlib with bcrypt
- **External API**: Spotify Web API (Authorization Code flow and Client Credentials flow)
- **ASGI Server**: uvicorn
- **Python Version**: 3.8, 3.9, 3.10 (tested via CI)

## Project Structure
```
.
├── main.py                 # FastAPI app initialization and startup
├── config.py              # Environment configuration
├── db.py                  # Database session management
├── database.py            # Database initialization
├── models.py              # SQLAlchemy models (User, Song, Session, SpotifyState)
├── schema.py              # Pydantic schemas for request/response validation
├── crud.py                # Database operations (CRUD functions)
├── auth.py                # Auth utilities (token creation, password hashing)
├── auth_utils.py          # Auth dependencies (get_current_user, get_db)
├── deps.py                # Shared dependencies
├── spotify.py             # Spotify API client functions
└── routers/
    ├── auth.py            # Authentication and Spotify OAuth endpoints
    ├── songs.py           # Song management endpoints
    └── sessions.py        # Session management endpoints
```

## Database Models
- **User**: Stores user credentials and Spotify tokens
  - Fields: id, username, hashed_password, is_active, spotify_access_token, spotify_refresh_token, spotify_expires_at
- **Song**: Music track information
  - Fields: id, title, artist, spotify_id, url
- **Session**: User's music routine/session
  - Fields: id, name, created_at, user_id, notes, songs (many-to-many relationship)
- **SpotifyState**: Server-side state nonces for OAuth flow
  - Fields: id, state, username, created_at, expires_at

## Code Style and Conventions

### General Python
- Follow PEP 8 style guidelines
- Use type hints for function parameters and return types
- Keep functions focused and modular
- Use meaningful variable and function names

### FastAPI Patterns
- Use dependency injection with `Depends()` for database sessions and authentication
- Define response models using Pydantic schemas with `response_model` parameter
- Use appropriate HTTP status codes and exceptions
- Group related endpoints using `APIRouter` with prefixes and tags
- Use `orm_mode = True` in Pydantic Config for SQLAlchemy model serialization

### Database Operations
- All database operations go in `crud.py`
- Always commit and refresh after creating/updating records
- Use proper SQLAlchemy sessions (don't forget to pass `db` parameter)
- Close or properly manage database sessions to avoid leaks

### Authentication and Authorization
- Protected endpoints require `current_user = Depends(get_current_user)`
- JWT tokens are created with username in the `sub` claim
- Access tokens expire based on `ACCESS_TOKEN_EXPIRE_MINUTES` config
- Use `OAuth2PasswordRequestForm` for token endpoint (standard OAuth2 form)

### Spotify Integration
- **Client Credentials flow**: Used for public API calls (search_track)
- **Authorization Code flow**: Used for user-specific operations
- State parameter is a server-side nonce stored in SpotifyState table
- State expires after 5 minutes for security
- Tokens are stored on User model (plaintext - note security consideration)
- Always check if Spotify credentials are configured before making API calls

### Environment Variables
- Load environment variables using `python-dotenv`
- Provide sensible defaults for development (e.g., SECRET_KEY has default but should be changed)
- Required for Spotify: SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI
- Database: DATABASE_URL (defaults to SQLite)

### Error Handling
- Use `HTTPException` for API errors with appropriate status codes
- Return 400 for client errors (bad request, duplicate username)
- Return 401 for unauthorized access
- Return 404 for not found resources
- Return 500 for server/integration errors
- Provide clear error messages in the `detail` field

### Security Considerations
- Passwords are hashed using bcrypt via passlib
- JWT tokens use HS256 algorithm
- Spotify state nonces prevent CSRF attacks in OAuth flow
- State values are single-use and expire quickly (5 minutes)
- CORS is configured (currently allows all origins - adjust for production)
- **Important**: Spotify tokens are stored in plaintext on User model - consider encryption for production

### Testing and Development
- Use `uvicorn main:app --reload` for development
- Access API documentation at `/docs` (Swagger UI) or `/redoc`
- Health check available at `/health` endpoint
- Database readiness check at `/ready` endpoint
- Run pylint for code quality checks (configured in CI)

## Common Patterns

### Creating a New Protected Endpoint
```python
@router.get("/endpoint", response_model=schema.ResponseModel)
def endpoint_name(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Implementation
    pass
```

### Adding a New CRUD Function
```python
def function_name(db: DBSession, param: Type) -> ReturnType:
    # Query or modify database
    result = db.query(models.Model).filter(...).first()
    db.commit()  # If modifying
    db.refresh(result)  # If creating/updating
    return result
```

### Adding a New Model
1. Define in `models.py` using SQLAlchemy
2. Create corresponding Pydantic schemas in `schema.py` (Create, Out, Update if needed)
3. Add CRUD operations in `crud.py`
4. Create router endpoints in appropriate file under `routers/`

## Dependencies Installation
```bash
pip install -r requirements.txt
```

Required packages:
- fastapi
- uvicorn[standard]
- sqlalchemy
- python-dotenv
- python-jose[cryptography]
- passlib[bcrypt]
- requests

## Running the Application
```bash
# Set up environment
cp .env.example .env
# Edit .env with your configuration

# Run server
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

## Notes for Copilot
- When adding new endpoints, always consider authentication requirements
- Use existing patterns from the codebase for consistency
- Follow the separation of concerns: routers → crud → models
- Consider error cases and provide meaningful error messages
- Always validate input using Pydantic schemas
- Be mindful of security best practices, especially around authentication and token storage
- When working with Spotify API, handle cases where credentials might not be configured
- Remember to handle database session cleanup properly
