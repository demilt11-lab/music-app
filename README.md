[README.md](https://github.com/user-attachments/files/24460289/README.md)
```markdown
# Routine Music Backend (with Spotify Authorization Code flow)

Quick start

1. Create & activate virtualenv:
   python3 -m venv venv
   source venv/bin/activate

2. Install dependencies:
   pip install -r requirements.txt

3. Copy .env.example to .env and edit it:
   cp .env.example .env
   - Set SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET and ensure
     SPOTIFY_REDIRECT_URI exactly matches your Spotify app redirect URI
     (e.g. http://localhost:8000/auth/callback).

4. Run the server:
   uvicorn main:app --reload --host 127.0.0.1 --port 8000

Docs:
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

Important endpoints:
- POST /auth/register
  Body: { "username": "alice", "password": "secret" }

- POST /auth/token
  Form fields: username, password
  Returns: { "access_token": "...", "token_type": "bearer" }

- GET /auth/spotify/connect
  Simple local frontend page (paste your app JWT token) that starts Spotify login.

- Protected endpoints require an Authorization header: `Authorization: Bearer <APP_TOKEN>`

- GET /auth/spotify/login-url (protected)
  Returns a JSON { "url": "<spotify_auth_url>", "state": "..." } — the frontend opens the URL.

- Spotify callback:
  /auth/callback (Spotify will redirect here)

- GET /auth/spotify/token-info (protected)
  Returns masked token metadata for the logged-in user.

- POST /auth/spotify/refresh (protected)
  Refresh your stored Spotify access token (uses stored refresh token).

- Songs:
  - GET /songs (public)
  - POST /songs (protected)

- Sessions:
  - POST /sessions (protected)
  - GET /sessions (protected)

Test flow (minimal):
1) Register:
   curl -X POST "http://127.0.0.1:8000/auth/register" -H "Content-Type: application/json" -d '{"username":"alice","password":"secret"}'

2) Get app token:
   curl -X POST "http://127.0.0.1:8000/auth/token" -F "username=alice" -F "password=secret"

3) Open Spotify connect page in browser:
   http://127.0.0.1:8000/auth/spotify/connect
   - Paste APP_TOKEN (from step 2) into the page and click Connect.
   - A new tab will open for Spotify consent. After consenting, Spotify redirects
     to /auth/callback which stores tokens for the user.

4) Check token info:
   curl -H "Authorization: Bearer <APP_TOKEN>" http://127.0.0.1:8000/auth/spotify/token-info

Notes:
- This demo stores Spotify tokens on the user record (plaintext). For production
  consider encryption and secure token handling.
- State values are server-side single-use nonces with expiry (5 minutes).
```
