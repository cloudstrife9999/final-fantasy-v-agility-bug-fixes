#!/usr/bin/env python3

a_bonuses: list[int] = [0, 1, 2, 3]  # From the knives damage formula.

level: int = 7      # Bartz's level.
defence: int = 0    # Any enemy from random encounter outside the Wind Shrine.
agility: int = 41   # Bartz as a thief with no stat boosting equipment.
strength: int = 29  # Bartz as a thief with no stat boosting equipment.
atk: int = 14       # Dagger.

a_values: list[int] = [atk + a_bonus for a_bonus in a_bonuses]
d: int = defence
m: int = ((level * strength) >> 7) + ((level * agility) >> 7) + 2
bugged_m: int = ((level * strength) >> 7) + (((level * agility) % 256) >> 7) + 2

damages: list[int] = [min(9999, (a - d) * m) if a > d else 0 for a in a_values]
bugged_damages: list[int] = [min(9999, (a - d) * bugged_m) if a > d else 0 for a in a_values]

print("Character: Bartz.")
print("Job: Thief.")
print(f"Level: {level}.")
print("Job level: irrelevant.")
print(f"Strength: {strength}.")
print(f"Agility: {agility}.")
print(f"Enemy physical defence: {defence}.")
print(f"Weapon: Dagger (Atk: {atk}, random bonuses: {a_bonuses}).")
print("Other equipment: irrelevant, as long as it does not provide any Strength/Agility bonuses.")
print(f"Possible damage rolls: {damages}.")                # [70, 75, 80, 85]
print(f"Possible bugged damage rolls: {bugged_damages}.")  # [42, 45, 48, 51]
