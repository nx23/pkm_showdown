from sqlalchemy.orm import Session
from utils.security import hash_password # type: ignore
from db.models import User, Team # type: ignore
from schemas.user import UserCreate # type: ignore
from schemas.teams import TeamMemberCreate # type: ignore

# User CRUD Operations

def get_user(db: Session, user_id: int):
    """Get a user by ID."""
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    """Get a user by username."""
    return db.query(User).filter(User.username == username).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    """Get a list of users with pagination."""
    return db.query(User).offset(skip).limit(limit).all()

def create_user(db: Session, user: UserCreate):
    """Create a new user."""
    db_user = User(
        username=user.username,
        hashed_password=hash_password(user.password),  # Hash the password before saving
        is_active=user.is_active,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user_update: dict):
    """Update an existing user."""
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        for key, value in user_update.items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    """Delete a user."""
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user

# Team CRUD Operations
def get_team(db: Session, team_id: int):
    """Get a team by ID."""
    return db.query(Team).filter(Team.id == team_id).first()

def get_teams(db: Session, skip: int = 0, limit: int = 100):
    """Get a list of teams with pagination."""
    return db.query(Team).offset(skip).limit(limit).all()

def create_team(db: Session, team: TeamMemberCreate):
    """Create a new team."""
    db_team = Team(
        owner_id=team.owner_id,
        member=team.member,
    )
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team

def update_team(db: Session, team_id: int, team_update: dict):
    """Update an existing team."""
    db_team = db.query(Team).filter(Team.id == team_id).first()
    if db_team:
        for key, value in team_update.items():
            setattr(db_team, key, value)
        db.commit()
        db.refresh(db_team)
    return db_team

def delete_team(db: Session, team_id: int):
    """Delete a team."""
    db_team = db.query(Team).filter(Team.id == team_id).first()
    if db_team:
        db.delete(db_team)
        db.commit()
    return db_team