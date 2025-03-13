import httpx
from core.entities import Mon, Type

from fastapi import HTTPException, status


async def validate_member(member_name: str):
    async with httpx.AsyncClient() as client:
        member = await client.get(f"https://pokeapi.co/api/v2/pokemon/{member_name}")

    if member.status_code == 404:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Member not found"
        )

    member_data = member.json()

    mon = Mon(
        species=member_data["species"]["name"],
        hp=member_data["stats"][0]["base_stat"],
        atk=member_data["stats"][1]["base_stat"],
        df=member_data["stats"][2]["base_stat"],
        satk=member_data["stats"][3]["base_stat"],
        sdf=member_data["stats"][4]["base_stat"],
        spd=member_data["stats"][5]["base_stat"],
        main_type=Type(member_data["types"][0]["type"]["name"]),
        sub_type=(
            Type(member_data["types"][1]["type"]["name"])
            if len(member_data["types"]) > 1
            else None
        ),
        attacks=None,
        name=member_data["species"]["name"],
    )

    print(mon)
