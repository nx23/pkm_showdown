from typing import Optional

from db.database import get_session
from db.models import Team_Members, Users
from pydantic import BaseModel
from sqlalchemy.orm import Session
from utils.security import get_current_user, is_user_authenticated

from fastapi import APIRouter, Depends, HTTPException, status


class Team(BaseModel):
    member: list[Team_Members]


router = APIRouter(prefix="/team")


@router.get("/", response_model=Team, status_code=status.HTTP_200_OK)
def get_my_team(current_user: Users = Depends(get_current_user)) -> Optional[Team]:
    is_user_authenticated(current_user)

    team_members = current_user.team_members
    if not team_members:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No team members found"
        )

    return Team(member=team_members)


@router.post("/", response_model=Team, status_code=status.HTTP_201_CREATED)
def add_team_member(
    member: Team_Members,
    db: Session = Depends(get_session),
    current_user: Users = Depends(get_current_user),
) -> Optional[Team]:
    is_user_authenticated(current_user)

    member.user_id = current_user.id

    db.add(member)
    db.commit()
    db.refresh(member)

    return Team(member=[member])


@router.delete("/", status_code=status.HTTP_200_OK)
def remove_team_member(
    member: Team_Members,
    db: Session = Depends(get_session),
    current_user: Users = Depends(get_current_user),
) -> Optional[Team]:
    is_user_authenticated(current_user)

    member = db.query(Team_Members).filter(Team_Members.id == member.id).first()

    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Team member not found"
        )

    if member.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to delete this member",
        )

    db.query(Team_Members).filter(Team_Members.id == member.id).delete()
    db.commit()
