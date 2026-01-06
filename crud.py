from sqlalchemy.orm import Session as DBSession
import models, schemas
from typing import List, Optional
from passlib.context import CryptContext
import time

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Users
def get_user_by_username(db: DBSession, username: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: DBSession, username: str, password: str) -> models.User:
    hashed = pwd_context.hash(password)
    user = models.User(username=username, hashed_password=hashed)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def authenticate_user(db: DBSession, username: str, password: str) -> Optional[models.User]:
    user = get_user_by_username(db, username)
    if not user:
        return None
    if not pwd_context.verify(password, user.hashed_password):
        return None
    return user

def save_spotify_tokens(db: DBSession, username: str, access_token: str, refresh_token: Optional[str], expires_in: Optional[int]) -> Optional[models.User]:
    """
    Persist Spotify tokens on the user record (by username).
    expires_in is seconds from now; we store absolute unix expires_at.
    """
    user = get_user_by_username(db, username)
    if not user:
        return None
    user.spotify_access_token = access_token
    if refresh_token:
        user.spotify_refresh_token = refresh_token
    if expires_in:
        user.spotify_expires_at = int(time.time()) + int(expires_in)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# Spotify state (nonces)
def create_spotify_state(db: DBSession, username: str, state: str, expires_in_seconds: int = 300) -> models.SpotifyState:
    expires_at = int(time.time()) + int(expires_in_seconds)
    st = models.SpotifyState(state=state, username=username, expires_at=expires_at)
    db.add(st)
    db.commit()
    db.refresh(st)
    return st

def get_spotify_state(db: DBSession, state: str) -> Optional[models.SpotifyState]:
    # also ensure not expired
    now = int(time.time())
    st = db.query(models.SpotifyState).filter(models.SpotifyState.state == state, models.SpotifyState.expires_at > now).first()
    return st

def delete_spotify_state(db: DBSession, state: str) -> None:
    db.query(models.SpotifyState).filter(models.SpotifyState.state == state).delete()
    db.commit()

# Songs
def create_song(db: DBSession, song_in: schemas.SongCreate) -> models.Song:
    song = models.Song(title=song_in.title, artist=song_in.artist, spotify_id=song_in.spotify_id, url=song_in.url)
    db.add(song)
    db.commit()
    db.refresh(song)
    return song

def list_songs(db: DBSession, skip: int = 0, limit: int = 100) -> List[models.Song]:
    return db.query(models.Song).offset(skip).limit(limit).all()

# Sessions
def create_session(db: DBSession, user: models.User, name: str, notes: Optional[str], song_ids: List[int]) -> models.Session:
    songs = db.query(models.Song).filter(models.Song.id.in_(song_ids)).all() if song_ids else []
    session = models.Session(name=name, user_id=user.id, notes=notes, songs=songs)
    db.add(session)
    db.commit()
    db.refresh(session)
    return session

def get_sessions_for_user(db: DBSession, user: models.User) -> List[models.Session]:
    return db.query(models.Session).filter(models.Session.user_id == user.id).order_by(models.Session.created_at.desc()).all()
