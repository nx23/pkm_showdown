import httpx


class Type:
    type_index = {
        "normal": 1,
        "fire": 2,
        "water": 3,
        "electric": 4,
        "grass": 5,
        "ice": 6,
        "fighting": 7,
        "poison": 8,
        "ground": 9,
        "flying": 10,
        "psychic": 11,
        "bug": 12,
        "rock": 13,
        "ghost": 14,
        "dragon": 15,
        "dark": 16,
        "steel": 17,
        "fairy": 18,
    }

    @classmethod
    async def create(cls, name: str):
        double_damage_from, half_damage_from, no_damage_from = await cls._async_init(
            name
        )

        return cls(name, double_damage_from, half_damage_from, no_damage_from)

    async def _async_init(name: str):
        await Type._check_for_valid_type(name)
        interactions = await Type._get_interactions(name)

        return (
            [type["name"] for type in interactions["double_damage_from"]],
            [type["name"] for type in interactions["half_damage_from"]],
            [type["name"] for type in interactions["no_damage_from"]],
        )

    @classmethod
    async def _check_for_valid_type(cls, type_name: str):
        """Check if the type name is present in the type_chart."""
        if not isinstance(type_name, str) or not type_name:
            raise TypeError(f"{type_name} must be a non-empty string")

        async with httpx.AsyncClient() as client:
            type_data = await client.get(
                f"https://pokeapi.co/api/v2/type/{cls.type_index[type_name]}"
            )

        if type_data.status_code == 404:
            raise ValueError(f"{type_name} is misspelled or is not a valid type.")

    @classmethod
    async def _get_interactions(cls, name: str):
        """Get the interactions for the given type."""
        async with httpx.AsyncClient() as client:
            type_data = await client.get(
                f"https://pokeapi.co/api/v2/type/{cls.type_index[name]}"
            )

        if type_data.status_code == 404:
            raise ValueError(f"{name} is misspelled or is not a valid type.")

        type_data = type_data.json()
        return type_data["damage_relations"]

    def __init__(
        self,
        name: str,
        double_damage_from: list[str],
        half_damage_from: list[str],
        no_damage_from: list[str],
    ):
        self.__name = name
        self.__weaknesses = double_damage_from
        self.__resistances = half_damage_from
        self.__immunities = no_damage_from

    def __repr__(self) -> str:
        return f"Type(name='{self.__name}')"

    def __str__(self) -> str:
        return self.__name

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Type):
            return self.__name == other.name
        elif isinstance(other, str):
            return self.__name == other
        return False

    def __hash__(self) -> int:
        return hash(self.__name)

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, name: str):
        Type._check_for_valid_type(name)
        self.__name = name

    @property
    def resistances(self) -> tuple[str]:
        return self.__resistances

    @property
    def weaknesses(self) -> tuple[str]:
        return self.__weaknesses

    @property
    def immunities(self) -> tuple[str]:
        return self.__immunities

    def is_weak_to(self, other_type):
        return other_type in self.weaknesses

    def is_resistant_to(self, other_type):
        return other_type in self.resistances

    def is_immune_to(self, other_type):
        return other_type in self.immunities
