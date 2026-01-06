from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table, DateTime, Text, Index
from sqlalchemy.orm import relationship
from datetime import datetime
from db import Base

session_songs = Table(
    "session_songs",
    Base.metadata,
    Column("session_id", Integer, ForeignKey("sessions.id"), primary_key=True),
    Column("song_id", Integer, ForeignKey("songs.id"), primary_key=True),
)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    # Spotify tokens (nullable)
    spotify_access_token = Column(String, nullable=True)
    spotify_refresh_token = Column(String, nullable=True)
    spotify_expires_at = Column(Integer, nullable=True)
    sessions = relationship("Session", back_populates="user")

class Song(Base):
    __tablename__ = "songs"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    artist = Column(String, nullable=True)
    spotify_id = Column(String, nullable=True)
    url = Column(String, nullable=True)

class Session(Base):
    __tablename__ = "sessions"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="sessions")
    notes = Column(Text, nullable=True)
    songs = relationship("Song", secondary=session_songs, backref="sessions")

class SpotifyState(Base):
    """
    Server-side state nonce for Spotify Authorization Code flow.
    Single-use and expires quickly.
    """
    __tablename__ = "spotify_states"
    id = Column(Integer, primary_key=True, index=True)
    state = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(Integer, nullable=False)

Index("ix_spotify_state_expires_at", SpotifyState.expires_at)
