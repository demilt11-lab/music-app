from fastapi import FastAPI
from db import init_db, SessionLocal
from routers import auth as auth_router, sessions as sessions_router, songs as songs_router
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import SQLAlchemyError

app = FastAPI(title="Routine Music Backend")

app.include_router(auth_router.router)
app.include_router(sessions_router.router)
app.include_router(songs_router.router)

# CORS (adjust origins as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/ready")
def ready():
    try:
        db = SessionLocal()
        db.execute("SELECT 1")
        return {"status": "ready"}
    except SQLAlchemyError:
        from fastapi import Response, status
        return Response(content='{"status":"unready"}', media_type="application/json", status_code=status.HTTP_503_SERVICE_UNAVAILABLE)
    finally:
        try:
            db.close()
        except Exception:
            pass
