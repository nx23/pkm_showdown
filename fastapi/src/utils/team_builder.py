import httpx

from fastapi import HTTPException, status


async def validate_member(member_name: str) -> dict:
    async with httpx.AsyncClient() as client:
        member = await client.get(f"https://pokeapi.co/api/v2/pokemon/{member_name}")

    if member.status_code == 404:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Member not found"
        )

    return member.json()
