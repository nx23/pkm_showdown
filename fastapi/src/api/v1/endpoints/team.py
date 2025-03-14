from typing import Optional

from core.entities import Mon, Type
from db.database import get_session
from db.models import Team_Members, Users
from pydantic import BaseModel
from sqlalchemy.orm import Session
from utils.security import get_current_user, is_user_authenticated
from utils.team_builder import validate_member

from fastapi import APIRouter, Depends, HTTPException, status


class Team(BaseModel):
    members: list[Team_Members]


router = APIRouter(prefix="/team")


@router.get("/", response_model=Team, status_code=status.HTTP_200_OK)
async def get_my_team(
    current_user: Users = Depends(get_current_user),
) -> Optional[Team]:
    is_user_authenticated(current_user)

    team_members = current_user.team_members
    if not team_members:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No team members found"
        )

    return Team(members=team_members)


@router.post("/", response_model=Team_Members, status_code=status.HTTP_201_CREATED)
async def add_team_member(
    member: Team_Members,
    db: Session = Depends(get_session),
    current_user: Users = Depends(get_current_user),
) -> Optional[Team]:
    is_user_authenticated(current_user)

    member.user_id = current_user.id

    if (
        db.query(Team_Members).filter(Team_Members.user_id == member.user_id).count()
        >= 6
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You can't have more than 6 members in your team",
        )

    member_data = await validate_member(member.name)

    pkm = Team_Members(
        user_id=member.user_id,
        name=member_data["species"]["name"],
        species=member_data["species"]["name"],
        hp=member_data["stats"][0]["base_stat"],
        atk=member_data["stats"][1]["base_stat"],
        df=member_data["stats"][2]["base_stat"],
        satk=member_data["stats"][3]["base_stat"],
        sdf=member_data["stats"][4]["base_stat"],
        spd=member_data["stats"][5]["base_stat"],
        type1=member_data["types"][0]["type"]["name"],
        type2=(
            member_data["types"][1]["type"]["name"]
            if len(member_data["types"]) > 1
            else None
        ),
    )

    db.add(pkm)
    db.commit()
    db.refresh(pkm)

    return pkm


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
