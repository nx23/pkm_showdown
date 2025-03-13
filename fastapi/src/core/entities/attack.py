import random
from math import ceil, prod

from core.entities.type import Type


class Attack:
    def __init__(
        self,
        name: str,
        type: Type,
        accuracy: int,
        power: int,
        attack_status: str,
        effect=None,
    ):
        self.__name = name
        self.__type = type
        self.__accuracy = accuracy
        self.__power = power
        self.__attack_status = attack_status
        self.__effect = effect

    def __repr__(self) -> str:
        return f"Attack(name='{self.name}', type=Type(name='{self.type.name}'), accuracy={self.accuracy}, power={self.power}, attack_status='{self.attack_status}')"

    def __str__(self) -> str:
        return f"{self.name} ({self.type.name})"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Attack):
            return self.name == other.name
        elif isinstance(other, str):
            return self.name == other
        return False

    def __hash__(self) -> int:
        return hash(self.name)

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, name):
        Attack._check_for_valid_name(name)
        self.__name = name

    @property
    def type(self) -> Type:
        return self.__type

    @type.setter
    def type(self, type: Type):
        self._check_for_valid_type(type)
        self.__type = type

    @property
    def accuracy(self) -> int:
        return self.__accuracy

    @accuracy.setter
    def accuracy(self, accuracy):
        Attack._check_for_valid_accuracy(accuracy)
        self.__accuracy = accuracy

    @property
    def power(self) -> int:
        return self.__power

    @power.setter
    def power(self, power):
        Attack._check_for_valid_power(power)
        self.__power = power

    @property
    def attack_status(self) -> str:
        return self.__attack_status

    @attack_status.setter
    def attack_status(self, attack_status):
        self._check_for_valid_attack_status(attack_status)
        self.__attack_status = attack_status

    def calculate_damage(self, user: "Mon", target: "Mon"):
        messages = set()
        # Check if the attack hits based on accuracy
        if random.randint(1, 100) > self.accuracy:
            print(f"{user.name} used {self.name}, but it missed!")
            return 0

        # Calculate base damage considering attack and defense
        if self.type.name in [user.main_type, user.sub_type]:
            modifiers = [1.25]  # STAB (Same-Type Attack Bonus)
        else:
            modifiers = []

        # Check weaknesses, resistances, and immunities
        for target_type in [target.main_type, target.sub_type]:
            if target_type is None:
                continue
            if target_type.is_immune_to(self.type):
                messages.add(f"{self.name} had no effect on {target.main_type}")
                return 0
            elif target_type.is_resistant_to(self.type):
                messages.add(f"{self.name} was not very effective...")
                modifiers.append(0.5)
            elif target_type.is_weak_to(self.type):
                messages.add(f"{self.name} was super effective!")
                modifiers.append(2.0)

        if self.attack_status == "atk":
            base_damage = ceil(user.atk / target.df) * self.power
        elif self.attack_status == "satk":
            base_damage = ceil(user.satk / target.sdf) * self.power
        else:
            raise ValueError("Invalid attack_status value. Must be 'atk' or 'satk'.")

        damage = int(base_damage * prod(modifiers))

        # Apply damage to the target's HP
        target.current_hp = max(target.current_hp - damage, 0)
        print(f"{self.name} dealt {damage} damage to {target.name}!")

        for message in messages:
            print(message)

        return damage

    @classmethod
    def _check_for_valid_name(cls, name):
        if not isinstance(name, str):
            raise TypeError("name must be a string")

    @classmethod
    def _check_for_valid_type(cls, type):
        if not isinstance(type, Type):
            raise TypeError(f"{type} must be a Type instance")

    @classmethod
    def _check_for_valid_accuracy(cls, accuracy):
        if not isinstance(accuracy, int):
            raise TypeError("accuracy must be an integer")
        if not (0 <= accuracy <= 100):
            raise ValueError("accuracy must be between 0 and 100")

    @classmethod
    def _check_for_valid_power(cls, power):
        if not isinstance(power, int):
            raise TypeError("power must be an integer")
        if power < 0:
            raise ValueError("power must be greater than or equal to 0")

    @classmethod
    def _check_for_valid_attack_status(cls, attack_status):
        if attack_status not in ["atk", "satk"]:
            raise ValueError("attack_status must be 'atk' or 'satk'")
