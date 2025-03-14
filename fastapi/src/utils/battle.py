import random
from math import ceil, prod

from core.entities.attack import Attack
from core.entities.mon import Mon


def calculate_damage(attack_move: Attack, user: Mon, target: Mon):
    messages = set()
    # Check if the attack hits based on accuracy
    if random.randint(1, 100) > attack_move.accuracy:
        print(f"{user.name} used {attack_move.name}, but it missed!")
        return 0

    # Calculate base damage considering attack and defense
    if attack_move.type.name in [user.main_type, user.sub_type]:
        modifiers = [1.25]  # STAB (Same-Type Attack Bonus)
    else:
        modifiers = []

    # Check weaknesses, resistances, and immunities
    for target_type in [target.main_type, target.sub_type]:
        if target_type is None:
            continue
        if target_type.is_immune_to(attack_move.type):
            messages.add(f"{attack_move.name} had no effect on {target.main_type}")
            return 0
        elif target_type.is_resistant_to(attack_move.type):
            messages.add(f"{attack_move.name} was not very effective...")
            modifiers.append(0.5)
        elif target_type.is_weak_to(attack_move.type):
            messages.add(f"{attack_move.name} was super effective!")
            modifiers.append(2.0)

    if attack_move.attack_status == "atk":
        base_damage = ceil(user.atk / target.df) * attack_move.power
    elif attack_move.attack_status == "satk":
        base_damage = ceil(user.satk / target.sdf) * attack_move.power
    else:
        raise ValueError("Invalid attack_status value. Must be 'atk' or 'satk'.")

    damage = int(base_damage * prod(modifiers))

    # Apply damage to the target's HP
    target.current_hp = max(target.current_hp - damage, 0)
    print(f"{attack_move.name} dealt {damage} damage to {target.name}!")

    for message in messages:
        print(message)

    return damage
