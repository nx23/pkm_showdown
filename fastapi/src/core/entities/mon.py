from __future__ import annotations

from math import ceil
from typing import Optional

from core.entities.attack import Attack
from core.entities.type import Type


class Mon:
    MAX_ATTACKS = 4
    MAX_STAT = 255
    MIN_STAT = 1

    def __init__(
        self,
        species: str,
        hp: int,
        atk: int,
        df: int,
        satk: int,
        sdf: int,
        spd: int,
        main_type: Type,
        sub_type: Optional[Type] = None,
        attacks: Optional[list[Attack]] = None,
        name: Optional[str] = None,
    ):
        self.__name = name or species
        self.__species = species
        self.__stats = {}
        self.__main_type = main_type
        self.__sub_type = sub_type
        self.__attacks = []

        # Validation and initialization of stats
        for stat_name, value in {
            "hp": hp,
            "atk": atk,
            "df": df,
            "satk": satk,
            "sdf": sdf,
            "spd": spd,
        }.items():
            self._check_for_valid_stat(value, stat_name)
            self.__stats[stat_name] = value

        # Maximum and current HP
        self.__max_hp = self._calculate_max_hp(self.__stats["hp"])
        self.__current_hp = self.__max_hp

        if attacks:
            for attack in attacks:
                self.add_attack(attack)

    def __str__(self):
        type_info = (
            f"{self.main_type.name}{'/' + self.sub_type.name if self.sub_type else ''}"
        )
        attacks = ", ".join(attack.name for attack in self.attacks) or "No attacks"
        return (
            f"{self.name} ({self.species}) - Type: {type_info}, "
            f"HP: {self.current_hp}/{self.max_hp}, ATK: {self.atk}, DF: {self.df}, "
            f"SATK: {self.satk}, SDEF: {self.sdf} SPD: {self.spd}, "
            f"Known Attacks: {attacks}"
        )

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value

    @property
    def species(self) -> str:
        return self.__species

    @species.setter
    def species(self, value: str):
        self.__species = value

    @property
    def current_hp(self) -> int:
        """Returns the current HP"""
        return self.__current_hp

    @property
    def max_hp(self) -> int:
        """Returns the maximum HP"""
        return self.__max_hp

    @current_hp.setter
    def current_hp(self, value: int):
        """Sets the current HP"""
        if value < 0:
            raise ValueError("HP value cannot be less than 0")
        if value > self.max_hp:
            raise ValueError(f"Current HP cannot exceed the maximum ({self.max_hp})")
        self.__current_hp = value

    @property
    def hp(self) -> int:
        """Returns the HP stat"""
        return self.__stats["hp"]

    @hp.setter
    def hp(self, value: int):
        self._check_for_valid_stat(value, "HP")
        self.__stats["hp"] = value

    @property
    def atk(self) -> int:
        return self.__stats["atk"]

    @atk.setter
    def atk(self, value: int):
        self._check_for_valid_stat(value, "ATK")
        self.__stats["atk"] = value

    @property
    def df(self) -> int:
        return self.__stats["df"]

    @df.setter
    def df(self, value: int):
        self._check_for_valid_stat(value, "DEF")
        self.__stats["df"] = value

    @property
    def satk(self) -> int:
        return self.__stats["satk"]

    @satk.setter
    def satk(self, value: int):
        self._check_for_valid_stat(value, "SATK")
        self.__stats["satk"] = value

    @property
    def sdf(self) -> int:
        return self.__stats["sdf"]

    @sdf.setter
    def sdf(self, value: int):
        self._check_for_valid_stat(value, "SDEF")
        self.__stats["sdf"] = value

    @property
    def spd(self) -> int:
        return self.__stats["spd"]

    @spd.setter
    def spd(self, value: int):
        self._check_for_valid_stat(value, "SPD")
        self.__stats["spd"] = value

    @property
    def main_type(self) -> Type:
        return self.__main_type

    @property
    def sub_type(self) -> Optional[Type]:
        return self.__sub_type

    @property
    def attacks(self) -> list[Attack]:
        """Returns the attacks known by the Mon"""
        return list(self.__attacks)

    def _calculate_max_hp(self, base_hp: int) -> int:
        return ceil(base_hp * 1.5)

    def attack(self, target: Mon, attack: Attack):
        """
        Performs an attack on another Mon.
        Args:
            target (Mon): The Mon being attacked.
            attack (Attack): The attack being used.
        """
        print(f"{self.name} is attacking {target.name}!")

        if attack not in self.attacks:
            raise ValueError(f"{self.name} does not know {attack.name}")

        calculate_damage(self, target)

    async def _check_valid_type(self, type_name: str):
        await Type._check_for_valid_type(type_name)

    def _check_for_valid_stat(self, stat: int, name: str):
        if not isinstance(stat, int):
            raise TypeError(f"{name} must be an integer")
        if not Mon.MIN_STAT <= stat <= Mon.MAX_STAT:
            raise ValueError(
                f"{name} must be between {Mon.MIN_STAT} and {Mon.MAX_STAT}"
            )

    def _check_for_valid_attack(self, attack: Attack):
        from src.core.entities.attack import Attack

        if not isinstance(attack, Attack):
            raise TypeError("Attack must be an instance of the Attack class")

    def add_attack(self, attack: Attack):
        from src.core.entities.attack import Attack

        if attack in self.__attacks:
            raise ValueError(f"Attack '{attack.name}' is already added to {self.name}")
        if len(self.__attacks) >= Mon.MAX_ATTACKS:
            raise ValueError(f"A Mon can have at most {Mon.MAX_ATTACKS} attacks")
        if not isinstance(attack, Attack):
            raise TypeError("Attack must be an instance of the Attack class")

        self.__attacks.append(attack)


from utils.battle import calculate_damage
