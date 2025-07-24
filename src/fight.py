import math
from present_results import possible_altering_abilities
from config import damage_altering_abilities
from wrap_text import wrap_text

def pokemon_effective(pokemon1, pokemon2):
    best_multiplier = 0
    best_type = []
    for key in pokemon1.types:
        try:
            multiplier = pokemon2.defensive_damage_multipliers[key]
        except KeyError:
            print(wrap_text(f"Error: type {key} from {pokemon1.name} not found in {pokemon2.name}'s defensive multipiers: {pokemon2.defensive_damage_multipliers}."))
            print(wrap_text("Please check and consider updating the database or report the issue to the author."))
        if multiplier > best_multiplier:
            best_type = [key]
            best_multiplier = multiplier
        elif multiplier == best_multiplier:
            best_type.append(key)
    
    if len(best_type) == 1:
        type_string = best_type[0]
    else:
        type_string = ", ".join(best_type[:-1]) + " and " + best_type[-1]
    
    if best_multiplier > 1:
        print(wrap_text(f"{pokemon1.name} is very effective on {pokemon2.name} (x{best_multiplier} damage) using {type_string} type attacks."))
    elif best_multiplier < 1 and best_multiplier > 0:
        print(wrap_text(f"{pokemon1.name} is not very effective on {pokemon2.name} (x{best_multiplier} damage) using {type_string} type attacks."))
    elif best_multiplier == 0:
        print(wrap_text(f"{pokemon2.name} is immune to {type_string} type attack from {pokemon1.name}."))
    elif best_multiplier == 1:
        print(wrap_text(f"{pokemon1.name} deals neutral damage against {pokemon2.name} (x{best_multiplier} damage)  using {type_string} type attacks."))
    else:
        print(wrap_text(f"Unexpected damage multiplier. Please check {pokemon2.name} data and consider updating data to correct this issue."))
    return best_multiplier, best_type

def determine_attack(pokemon1, pokemon2):
    if pokemon1.stats["Attack"] > pokemon1.stats["Special-attack"]:
        pokemon1_offense = pokemon1.stats["Attack"]
        print(wrap_text(f"{pokemon1.name} has more Attack({pokemon1.stats["Attack"]}) than Special Attack({pokemon1.stats["Special-attack"]}). It will be used for further calculations."))
        return pokemon1_offense, "Attack"
    elif pokemon1.stats["Special-attack"] > pokemon1.stats["Attack"]:
        pokemon1_offense = pokemon1.stats["Special-attack"]
        print(wrap_text(f"{pokemon1.name} has more Special Attack({pokemon1.stats["Special-attack"]}) than Attack({pokemon1.stats["Attack"]}). It will be used for further calculations."))
        return pokemon1_offense, "Special Attack"
    else:
        print(wrap_text(f"{pokemon1.name} has equal Attack and Special Attack. Checking Defences of {pokemon2.name} to determine which Attack to use."))
        if pokemon2.stats["Defense"] > pokemon2.stats["Special-defense"]:
            pokemon1_offense = pokemon1.stats["Special-attack"]
            print(wrap_text(f"{pokemon2.name} has more Defense({pokemon2.stats["Defense"]}) than Special Defense({pokemon2.stats["Special-defense"]}). {pokemon1.name}'s Special Attack will be used."))
            return pokemon1_offense, "Special Attack"
        elif pokemon2.stats["Special-defense"] > pokemon2.stats["Defense"]:
            pokemon1_offense = pokemon1.stats["Attack"]
            print(wrap_text(f"{pokemon2.name} has more Special Defense({pokemon2.stats["Special-defense"]}) than Defense({pokemon2.stats["Defense"]}). {pokemon1.name}'s Attack will be used."))
            return pokemon1_offense, "Attack"
        else:
            pokemon1_offense = pokemon1.stats["Attack"]
            print(wrap_text(f"Both of {pokemon1.name} attack types (Attack or Special Attack) will have the same effect on {pokemon2.name}."))
            return pokemon1_offense, "Attack"
        
def effective_hp(pokemon1, pokemon2_effective_on_pokemon1, pokemon2_attack_type):
    if pokemon1.name == "Shedinja":
        effective_hp = 1
        return effective_hp
    if pokemon2_attack_type == "Attack":
        effective_hp = pokemon1.stats["HP"] * pokemon1.stats["Defense"] / pokemon2_effective_on_pokemon1
    else:
        effective_hp = pokemon1.stats["HP"] * pokemon1.stats["Special-defense"] / pokemon2_effective_on_pokemon1
    return effective_hp

def turns_to_knock_out(level, pokemon1_base_attack, pokemon2_base_defense, pokemon2_base_health, pokemon1_effective_on_pokemon2, shedinja_flag=False):
    level = int(level)
    if level < 16:
        power = 40
    elif level < 30:
        power = 60
    else:
        power = 80
    
    stab_multiplier = 1.5
    random_factor = (0.85 + 1) / 2
    pokemon1_attack = ((2 * pokemon1_base_attack) * level)//100 + 5
    pokemon2_defense = ((2 * pokemon2_base_defense) * level)//100 + 5
    if shedinja_flag == False:
        pokemon2_health = (((2 * pokemon2_base_health) * level)//100) + level + 10
    else:
        pokemon2_health = 1
    
    damage = ((((2 * level) / 5 + 2) * power * (pokemon1_attack / pokemon2_defense)) / 50 + 2) * stab_multiplier * pokemon1_effective_on_pokemon2 * random_factor
    rounded = math.ceil(damage - 0.5)

    if rounded > 0:
        turns_to_knock_out = -(-pokemon2_health // rounded)
    elif rounded == 0:
        turns_to_knock_out = float("inf")
    else:
        raise ValueError(wrap_text("Incorrect damage value. Terminating program. Please report the issue to the author."))
    return turns_to_knock_out

def ability_warning(pokemon):
    if len(pokemon.abilities) == 1 and pokemon.abilities[0] in damage_altering_abilities:
        warning = f"Warning! {pokemon.name} has only 1 ability and it changes its defensive properties. This simulatio takes this ability ({pokemon.abilities[0]})into account.\nIf you have a way to ignore this ability you can change its defensive properties."
        print(wrap_text(warning))
    possible_altering_abilities(pokemon)

def fight(pokemon1, pokemon2, level=50, max_attemps=5):
    level = str(level)
    attempts = 0
    while attempts < max_attemps:
        if not level.isdigit() or int(level) < 1 or int(level) > 100:
            attempts += 1
            if attempts == max_attemps:
                print(wrap_text("Too many failed attempts. Terminating function."))
                return
            print(wrap_text("Pokémon level range is 1-100. Please enter level congruent with this range."))
            print(wrap_text("Please enter correct Pokémon level:"))
            level = input(">>")
            level = level.strip().lstrip("0")
        else:
            break


    print(wrap_text(f"{pokemon1.name} VS {pokemon2.name}"))
    print(wrap_text(f"{pokemon1.name} types: {pokemon1.types}"))
    print(wrap_text(f"{pokemon2.name} types: {pokemon2.types}"))

    ability_warning(pokemon1)
    ability_warning(pokemon2)

    pokemon1_effective_on_pokemon2 = pokemon_effective(pokemon1, pokemon2)
    pokemon2_effective_on_pokemon1 = pokemon_effective(pokemon2, pokemon1)

    if pokemon1.bst > pokemon2.bst:
        print(wrap_text(f"{pokemon1.name} has more base stats total (BST) than {pokemon2.name}({pokemon1.bst} vs {pokemon2.bst})."))
    elif pokemon2.bst > pokemon1.bst:
        print(wrap_text(f"{pokemon2.name} has more base stats total (BST) than {pokemon1.name}({pokemon2.bst} vs {pokemon1.bst})."))
    else:
        print(wrap_text(f"{pokemon1.name} and {pokemon2.name} have the same base stats total (BST: {pokemon1.bst})."))

    pokemon1_attack, pokemon1_attack_type = determine_attack(pokemon1, pokemon2)
    pokemon1_offense = pokemon1_attack * pokemon1_effective_on_pokemon2[0]
    pokemon2_attack, pokemon2_attack_type = determine_attack(pokemon2, pokemon1)
    pokemon2_offense = pokemon2_attack * pokemon1_effective_on_pokemon2[0]

    if pokemon1_offense > pokemon2_offense:
        print(wrap_text(f"{pokemon1.name}'s offensive power is higher than {pokemon2.name}'s offensive power."))
    elif pokemon2_offense > pokemon1_offense:
        print(wrap_text(f"{pokemon2.name}'s offensive power is higher than {pokemon1.name}'s offensive power."))
    else:
        print(wrap_text("Both Pokémon have the same offensive power."))

    pokemon1_effective_hp = effective_hp(pokemon1, pokemon2_effective_on_pokemon1[0], pokemon2_attack_type)
    pokemon2_effective_hp = effective_hp(pokemon2, pokemon1_effective_on_pokemon2[0], pokemon1_attack_type)

    if pokemon1_effective_hp > pokemon2_effective_hp:
        print(wrap_text(f"{pokemon1.name} has more effective HP in this fight than {pokemon2.name}."))
    elif pokemon2_effective_hp > pokemon1_effective_hp:
        print(wrap_text(f"{pokemon2.name} has more effective HP in this fight than {pokemon1.name}."))
    else:
        print(wrap_text("Both Pokémon have the same effective HP."))

    if pokemon1_attack_type == "Attack":
        pokemon2_defense = pokemon2.stats["Defense"]
    else:
        pokemon2_defense = pokemon2.stats["Special-defense"]
    
    if pokemon2_attack_type == "Attack":
        pokemon1_defense = pokemon1.stats["Defense"]
    else:
        pokemon1_defense = pokemon1.stats["Special-defense"]
                                
    pokemon1_knockout_turns = turns_to_knock_out(level, pokemon1_attack, pokemon2_defense, pokemon2.stats["HP"], pokemon1_effective_on_pokemon2[0])
    pokemon2_knockout_turns = turns_to_knock_out(level, pokemon2_attack, pokemon1_defense, pokemon1.stats["HP"], pokemon2_effective_on_pokemon1[0])
    if pokemon1_knockout_turns == float("inf"):
        if pokemon2_knockout_turns == float("inf"):
            print(wrap_text("Both Pokémon can't damage each other using only moves corresponding to their types. Fight will end in draw."))
            return
        print(wrap_text(f"{pokemon1.name} can't deal any damage to {pokemon2.name} using only moves corresponding to its types"))
        print(wrap_text(f"{pokemon2.name} will win the fight in {pokemon2_knockout_turns} turns."))
    elif pokemon2_knockout_turns == float("inf"):
        print(wrap_text(f"{pokemon2.name} can't deal any damage to {pokemon1.name} using only moves corresponding to its types"))
        print(wrap_text(f"{pokemon1.name} will win the fight in {pokemon1_knockout_turns} turns."))

    if pokemon1.stats["Speed"] > pokemon2.stats["Speed"]:
        print(wrap_text(f"{pokemon1.name} is faster than {pokemon2.name}."))
        if pokemon1_knockout_turns <= pokemon2_knockout_turns:
            winner_name = pokemon1.name
            winner_turns = pokemon1_knockout_turns
        else:
            winner_name = pokemon2.name
            winner_turns = pokemon2_knockout_turns
    elif pokemon2.stats["Speed"] > pokemon1.stats["Speed"]:
        print(wrap_text(f"{pokemon2.name} is faster than {pokemon1.name}."))
        if pokemon2_knockout_turns <= pokemon1_knockout_turns:
            winner_name = pokemon2.name
            winner_turns = pokemon2_knockout_turns
        else:
            winner_name = pokemon1.name
            winner_turns = pokemon1_knockout_turns
    else:
        print(wrap_text(f"Both Pokémon have the same speed ({pokemon1.stats["Speed"]}). Outcome of the battle may be determined by RNG!!"))
        if pokemon1_knockout_turns < pokemon2_knockout_turns:
            winner_name = pokemon1.name
            winner_turns = pokemon1_knockout_turns
        elif pokemon2_knockout_turns < pokemon1_knockout_turns:
            winner_name = pokemon2.name
            winner_turns = pokemon2_knockout_turns
        else:
            print(wrap_text(f"Both Pokémon have equal speed, as a result outcome of this fight is random - Pokémon that will act first in turn number: {pokemon1_knockout_turns} will win. Beware that damage formula in Pokémon has random factor, which may change outcome of the fight."))
            print(wrap_text("Remember that in real Pokémon fight outcome may also change because of IVs, EVs, natures, held items and other factors."))
            return

    print(wrap_text(f"{winner_name} will win this fight. The fight will end in {winner_turns} turns. Beware that damage formula in Pokémon has random factor, which may change outcome of the fight."))   
    print(wrap_text("Remember that in real Pokémon fight outcome may also change because of IVs, EVs, natures, held items and other factors."))