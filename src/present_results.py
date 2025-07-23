from pokemon_class import Pokemon
from config import damage_altering_abilities
from wrap_text import wrap_text

def format_effectiveness_list(type_list):
    if len(type_list) > 0:
        final_string = ", ".join(type_list)
    else:
        final_string = "None"
    return final_string

def has_only_altering_ability(pokemon, return_warning=True):
    if len(pokemon.abilities) == 1 and pokemon.abilities[0] in damage_altering_abilities:
        warning = f"Warning! Pokémon has only 1 ability and it changes its defensive properties. Below are its defensive properties with this ability ({pokemon.abilities[0]}) taken into account."
        ability = pokemon.abilities[0]
        condition = damage_altering_abilities[ability].get("condition")
    else:
        return None
    
    if condition == "super effective":
        for key, multiplier in pokemon.defensive_damage_multipliers.items():
            if multiplier > 1:
                pokemon.defensive_damage_multipliers[key] *= damage_altering_abilities[ability]["multiplier"]
    elif condition == "not super effective":
        for key, multiplier in pokemon.defensive_damage_multipliers.items():
            if multiplier <= 1:
                pokemon.defensive_damage_multipliers[key] *= damage_altering_abilities[ability]["multiplier"]
    else:
        for key in damage_altering_abilities[ability]:
            pokemon.defensive_damage_multipliers[key] *= damage_altering_abilities[ability][key]
    if return_warning == True:
        return warning
    
def possible_altering_abilities(pokemon, altering_abilities):
    if len(pokemon.abilities) > 1 and len(altering_abilities) > 0:
        print(wrap_text(f"Warning! Pokémon {pokemon.name} may have an ability ({', '.join(altering_abilities)}), which changes type effectiveness."))
    for each in altering_abilities:
        print(wrap_text(f"{each} changes effectiveness of {', '.join(damage_altering_abilities[each].keys())}"))
        print(wrap_text("When planning matchup for this Pokémon, please take into account possibility of effectivenes of these type(s) to change."))
    
def display_search_results(pokemon):
    types = ", ".join(pokemon.types)
    abilities = ", ".join(pokemon.abilities)

    warning = has_only_altering_ability(pokemon)

    x4_defensive = []
    x2_defensive = []
    x1_defensive = []
    x0_5_defensive = []
    x0_25_defensive = []
    x0_defensive = []
    for key in pokemon.defensive_damage_multipliers:
        if pokemon.defensive_damage_multipliers[key] == 4:
            x4_defensive.append(key)
        elif pokemon.defensive_damage_multipliers[key] == 2:
            x2_defensive.append(key)
        elif pokemon.defensive_damage_multipliers[key] == 1:
            x1_defensive.append(key)
        elif pokemon.defensive_damage_multipliers[key] == 0.5:
            x0_5_defensive.append(key)
        elif pokemon.defensive_damage_multipliers[key] == 0.25:
            x0_25_defensive.append(key)
        else:
            x0_defensive.append(key)

    defensive_4 = format_effectiveness_list(x4_defensive)
    defensive_2 = format_effectiveness_list(x2_defensive)
    defensive_1 = format_effectiveness_list(x1_defensive)
    defensive_0_5 = format_effectiveness_list(x0_5_defensive)
    defensive_0_25 = format_effectiveness_list(x0_25_defensive)
    defensive_0 = format_effectiveness_list(x0_defensive)
    
    x2_offensive = []
    x1_offensive = []
    x0_5_offensive = []
    x0_offensive = []
    for key in pokemon.offensive_damage_multipliers:
        if pokemon.offensive_damage_multipliers[key] == 2:
            x2_offensive.append(key)
        elif pokemon.offensive_damage_multipliers[key] == 1:
            x1_offensive.append(key)
        elif pokemon.offensive_damage_multipliers[key] == 0.5:
            x0_5_offensive.append(key)
        else:
            x0_offensive.append(key)
    offensive_2 = format_effectiveness_list(x2_offensive)
    offensive_1 = format_effectiveness_list(x1_offensive)
    offensive_0_5 = format_effectiveness_list(x0_5_offensive)
    offensive_0 = format_effectiveness_list(x0_offensive)

    altering_abilities = []
    for ability in pokemon.abilities:
        if ability in damage_altering_abilities:
            altering_abilities.append(ability)

    print(wrap_text(f"Searched Pokémon: {pokemon.number}. {pokemon.name}."))

    print(wrap_text(f"Its type(s) are: {types}. | Its possible abilities: {abilities}."))

    if warning:
        print(wrap_text(warning))
    print()
    print(wrap_text("Defensive type effectiveness of Pokémon:"))
    print(wrap_text(f"\t4x weaknesses: {defensive_4}"))
    print(wrap_text(f"\t2x weaknesses: {defensive_2}"))
    print(wrap_text(f"\tNeutral damage: {defensive_1}"))
    print(wrap_text(f"\tx0.5 resistance: {defensive_0_5}"))
    print(wrap_text(f"\tx0.25 resistance: {defensive_0_25}"))
    print(wrap_text(f"\tImmunities: {defensive_0}"))
    possible_altering_abilities(pokemon, altering_abilities)
    
    print()
    print(wrap_text("Offensive type effectiveness of Pokémon:"))
    print(wrap_text(f"\tSuper effective (x2): {offensive_2}"))
    print(wrap_text(f"\tNeutral (x1): {offensive_1}"))
    print(wrap_text(f"\tNot very effective (x0.5): {offensive_0_5}"))
    print(wrap_text(f"\tNo effect (x0): {offensive_0}"))
    print()
    print(wrap_text("Pokémon base stats:"))
    print(wrap_text(f"HP: {pokemon.stats["HP"]} | Attack: {pokemon.stats["Attack"]} | Defense: {pokemon.stats["Defense"]} | Special Attack: {pokemon.stats["Special-attack"]} | Special Defense: {pokemon.stats["Special-defense"]} | Speed: {pokemon.stats["Speed"]}"))
    print(wrap_text(f"Pokémon base stats total: {pokemon.bst}"))