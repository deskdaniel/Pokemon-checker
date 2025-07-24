import unittest
from unittest.mock import patch, call

from search import search_by_name, search_by_number, search_by_type
from wrap_text import wrap_text

class TestHTMLNode(unittest.TestCase):
    @patch('builtins.print')
    def test_search_mega_aggron(self, mock_print):
        query = "Aggron Mega"
        result = search_by_name(query)
        expected_bst = 630
        expected_number = 306
        expected_defensive_fire = 1.5
        expected_defensive_fighting = 1.5
        self.assertEqual(int(result.bst), expected_bst)
        self.assertEqual(int(result.number), expected_number)
        self.assertEqual(result.defensive_damage_multipliers["Fire"], expected_defensive_fire)
        self.assertEqual(result.defensive_damage_multipliers["Fighting"], expected_defensive_fighting)

    @patch('builtins.print')
    def test_search_shedinja(self, mock_print):
        query = "292"
        result = search_by_number(query)
        expected_name = "Shedinja"
        expected_abilities = ["Wonder Guard"]
        expected_defensive = {"Normal": 0, "Fighting": 0, "Flying": 2, "Poison": 0, "Ground": 0, "Rock": 2, "Bug": 0, "Ghost": 2, "Steel": 0, "Fire": 2, "Water": 0, "Grass": 0, "Electric": 0, "Psychic": 0, "Ice": 0, "Dragon": 0, "Dark": 2, "Fairy": 0, "Stellar": 0}
        self.assertEqual(result.name, expected_name)
        self.assertEqual(result.abilities, expected_abilities)
        self.assertEqual(result.defensive_damage_multipliers, expected_defensive)

    @patch('builtins.print')
    def test_search_eelekross(self, mock_print):
        query = "Eelektross"
        result = search_by_name(query)
        expected_abilities = ["Levitate"]
        expected_speed = 50
        expected_defensive_ground = 0
        self.assertEqual(result.abilities, expected_abilities)
        self.assertEqual(result.stats["Speed"], expected_speed)
        self.assertEqual(result.defensive_damage_multipliers["Ground"], expected_defensive_ground)

    @patch('builtins.print')
    def test_search_vaporeon(self, mock_print):
        query = "134"
        result = search_by_number(query)
        expected_name = "Vaporeon"
        expected_abilities = ['Water Absorb', 'Hydration']
        expected_defensive_water = 0.5
        self.assertEqual(result.name, expected_name)
        self.assertEqual(result.abilities, expected_abilities)
        self.assertEqual(result.defensive_damage_multipliers["Water"], expected_defensive_water)

    @patch('builtins.print')
    def test_search_walrein(self, mock_print):
        query = "Walrein"
        result = search_by_name(query)
        expected_defensive_fire = 1
        expected_defensive_ice = 0.25
        self.assertEqual(result.defensive_damage_multipliers["Fire"], expected_defensive_fire)
        self.assertEqual(result.defensive_damage_multipliers["Ice"], expected_defensive_ice)

    @patch('builtins.print')
    def test_search_lanturn(self, mock_print):
        query = "Lanturn"
        result = search_by_name(query)
        expected_defensive_water = 0.5
        expected_defensive_electric = 1
        self.assertEqual(result.defensive_damage_multipliers["Electric"], expected_defensive_electric)
        self.assertEqual(result.defensive_damage_multipliers["Water"], expected_defensive_water)

    @patch('builtins.print')
    def test_search_abomasnow(self, mock_print):
        query = "Abomasnow Mega"
        result = search_by_name(query)
        expected_defensive_fire = 4
        expected_defensive_ice = 1
        self.assertEqual(result.defensive_damage_multipliers["Fire"], expected_defensive_fire)
        self.assertEqual(result.defensive_damage_multipliers["Ice"], expected_defensive_ice)

    @patch('builtins.print')
    def test_search_magnezone(self, mock_print):
        query = "462"
        result = search_by_number(query)
        expected_name = "Magnezone"
        expected_defensive_ground = 4
        expected_defensive_steel = 0.25
        expected_defensive_poison = 0
        self.assertEqual(result.name, expected_name)
        self.assertEqual(result.defensive_damage_multipliers["Ground"], expected_defensive_ground)
        self.assertEqual(result.defensive_damage_multipliers["Steel"], expected_defensive_steel)
        self.assertEqual(result.defensive_damage_multipliers["Poison"], expected_defensive_poison)

    @patch('builtins.print')
    def test_search_crobat(self, mock_print):
        query = "Crobat"
        result = search_by_name(query)
        expected_defensive_ground = 0
        expected_defensive_fighting = 0.25
        self.assertEqual(result.defensive_damage_multipliers["Ground"], expected_defensive_ground)
        self.assertEqual(result.defensive_damage_multipliers["Fighting"], expected_defensive_fighting)

    @patch('builtins.print')
    def test_search_sableye(self, mock_print):
        query = "Sableye Mega"
        result = search_by_name(query)
        expected_defensive_fighting = 0
        expected_defensive_normal = 0
        expected_defensive_psychic = 0
        expected_defensive_dark = 1
        self.assertEqual(result.defensive_damage_multipliers["Fighting"], expected_defensive_fighting)
        self.assertEqual(result.defensive_damage_multipliers["Normal"], expected_defensive_normal)
        self.assertEqual(result.defensive_damage_multipliers["Psychic"], expected_defensive_psychic)
        self.assertEqual(result.defensive_damage_multipliers["Dark"], expected_defensive_dark)

    @patch('builtins.print')
    def test_search_fearow(self, mock_print):
        query = "22"
        result = search_by_name(query)
        expected_name = "Fearow"
        expected_defensive = {"Normal": 1, "Fighting": 1, "Flying": 1, "Poison": 1, "Ground": 0, "Rock": 2, "Bug": 0.5, "Ghost": 0, "Steel": 1, "Fire": 1, "Water": 1, "Grass": 0.5, "Electric": 2, "Psychic": 1, "Ice": 2, "Dragon": 1, "Dark": 1, "Fairy": 1, "Stellar": 1}
        self.assertEqual(result.name, expected_name)
        self.assertEqual(result.defensive_damage_multipliers, expected_defensive)

    @patch('builtins.print')
    def test_search_golduck(self, mock_print):
        query = "Golduck"
        result = search_by_name(query)
        expected_name = "Golduck"
        expected_defensive = {"Normal": 1, "Fighting": 1, "Flying": 1, "Poison": 1, "Ground": 1, "Rock": 1, "Bug": 1, "Ghost": 1, "Steel": 0.5, "Fire": 0.5, "Water": 0.5, "Grass": 2, "Electric": 2, "Psychic": 1, "Ice": 0.5, "Dragon": 1, "Dark": 1, "Fairy": 1, "Stellar": 1}
        self.assertEqual(result.name, expected_name)
        self.assertEqual(result.defensive_damage_multipliers, expected_defensive)

    @patch('builtins.print')
    def test_search_fairy_fire(self, mock_print):
        query = "Fairy Fire"
        result = search_by_type(query)
        expected_result = None
        self.assertEqual(result, expected_result)

    @patch('builtins.print')
    def test_search_fire_water(self, mock_print):
        query = "Fire Water"
        result = search_by_type(query)
        expected_result = "721. Volcanion"
        self.assertEqual(result, expected_result)

    @patch('builtins.print')
    def test_search_grass_electric(self, mock_print):
        query = "Grass Electric"
        result = search_by_type(query)
        expected_result = "100. Voltorb Hisui\n101. Electrode Hisui\n479. Rotom Mow"
        self.assertEqual(result, expected_result)

    @patch('builtins.input', side_effect=['Rattata Alola'])
    @patch('builtins.print')
    def test_search_multiple_results(self, mock_print, mock_input):
        query = "Rattata"
        result = search_by_name(query)
        expected_name = "Rattata Alola"
        self.assertEqual(result.name, expected_name)

        expected_message_1 = wrap_text(f"Found more than 1 match for this search term(\"{query}\").")
        choices_content = "1 Rattata\n2 Rattata Alola"
        expected_message_2 = wrap_text(f"Pick one(write a name from list or number corresponding to choosen name) from the following list:\n{choices_content}")
        expected_message_3 = wrap_text("Waiting for name or number input:")
        mock_print.assert_any_call(expected_message_1)
        mock_print.assert_any_call(expected_message_2)
        mock_print.assert_any_call(expected_message_3)

        mock_input.assert_called_once_with(">>")

    @patch('builtins.input', side_effect=['3', '1'])
    @patch('builtins.print')
    def test_search_multiple_results_first_error(self, mock_print, mock_input):
        query = "Rattata"
        result = search_by_name(query)
        expected_name = "Rattata"
        self.assertEqual(result.name, expected_name)

        expected_message_1 = wrap_text(f"Found more than 1 match for this search term(\"{query}\").")
        choices_content = "1 Rattata\n2 Rattata Alola"
        expected_message_2 = wrap_text(f"Pick one(write a name from list or number corresponding to choosen name) from the following list:\n{choices_content}")
        expected_message_3 = wrap_text("Waiting for name or number input:")
        mock_print.assert_has_calls([call(expected_message_1), call(expected_message_2), call(expected_message_3)])
        expected_message_4 = wrap_text(f"Specified number is out of list's range. Please try again(attempt 1 out of 5). Here's the list once again:\n{choices_content}")
        mock_print.assert_any_call(expected_message_4)

        mock_input.assert_has_calls([unittest.mock.call(">>"), unittest.mock.call(">>")])
        self.assertEqual(mock_input.call_count, 2)

    @patch('builtins.input', side_effect=['3', '3', '3', '3', '3', '3'])
    @patch('builtins.print')
    def test_search_multiple_results_too_many_attempts(self, mock_print, mock_input):
        query = "Rattata"
        result = search_by_name(query)
        expected_result = None
        self.assertEqual(result, expected_result)

        expected_message_1 = wrap_text(f"Found more than 1 match for this search term(\"{query}\").")
        choices_content = "1 Rattata\n2 Rattata Alola"
        expected_message_2 = wrap_text(f"Pick one(write a name from list or number corresponding to choosen name) from the following list:\n{choices_content}")
        expected_message_3 = wrap_text("Waiting for name or number input:")
        mock_print.assert_has_calls([call(expected_message_1), call(expected_message_2), call(expected_message_3)])
        expected_message_4 = wrap_text(f"Specified number is out of list's range. Please try again(attempt 1 out of 5). Here's the list once again:\n{choices_content}")
        mock_print.assert_any_call(expected_message_4)

        mock_input.assert_has_calls([unittest.mock.call(">>"), unittest.mock.call(">>")])
        self.assertEqual(mock_input.call_count, 5)

    @patch('builtins.input', side_effect=['Bulbasaur'])
    @patch('builtins.print')
    def test_search_wrong_prefix_then_correct(self, mock_print, mock_input):
        query = "Xyz"
        result = search_by_name(query)
        expected_name = "Bulbasaur"
        self.assertEqual(result.name, expected_name)

        expected_message_1 = wrap_text(f"No Pokémon matching prefix: \"{query}\" found.")
        expected_message_2 = wrap_text("Please try again. You can type \"exit\" to return to main menu.")
        expected_message_3 = wrap_text("Waiting for Pokémon name or Pokédex number input:")
        mock_print.assert_has_calls([call(expected_message_1), call(expected_message_2), call(expected_message_3)])
        expected_message_4 = wrap_text("Found Pokémon")
        mock_print.assert_any_call(expected_message_4)

        mock_input.assert_called_once_with(">>")

    @patch('builtins.input', side_effect=['Bulbasaur'])
    @patch('builtins.print')
    def test_search_empty_input_then_correct(self, mock_print, mock_input):
        query = ""
        result = search_by_name(query)
        expected_name = "Bulbasaur"
        self.assertEqual(result.name, expected_name)

        expected_message_1 = wrap_text("Empty input detected.")
        expected_message_2 = wrap_text("Please try again. You can type \"exit\" to return to main menu.")
        expected_message_3 = wrap_text("Waiting for Pokémon name or Pokédex number input:")
        mock_print.assert_has_calls([call(expected_message_1), call(expected_message_2), call(expected_message_3)])
        expected_message_4 = wrap_text("Found Pokémon")
        mock_print.assert_any_call(expected_message_4)

        mock_input.assert_called_once_with(">>")

    @patch('builtins.input', side_effect=['Bulbasaur'])
    @patch('builtins.print')
    def test_search_00_input_then_correct(self, mock_print, mock_input):
        query = "00"
        result = search_by_number(query)
        expected_name = "Bulbasaur"
        self.assertEqual(result.name, expected_name)

        expected_message_1 = wrap_text(f"Invalid input, {query} is not a valid Pokédex number.")
        expected_message_2 = wrap_text("Please try again. You can type \"exit\" to return to main menu.")
        expected_message_3 = wrap_text("Waiting for Pokémon name or Pokédex number input:")
        mock_print.assert_has_calls([call(expected_message_1), call(expected_message_2), call(expected_message_3)])
        expected_message_4 = wrap_text("Found Pokémon")
        mock_print.assert_any_call(expected_message_4)

        mock_input.assert_called_once_with(">>")

    @patch('builtins.input', side_effect=['abc', '1'])
    @patch('builtins.print')
    def test_search_multiple_results_first_error2(self, mock_print, mock_input):
        query = "Rattata"
        result = search_by_name(query)
        expected_name = "Rattata"
        self.assertEqual(result.name, expected_name)

        expected_message_1 = wrap_text(f"Found more than 1 match for this search term(\"{query}\").")
        choices_content = "1 Rattata\n2 Rattata Alola"
        expected_message_2 = wrap_text(f"Pick one(write a name from list or number corresponding to choosen name) from the following list:\n{choices_content}")
        expected_message_3 = wrap_text("Waiting for name or number input:")
        mock_print.assert_has_calls([call(expected_message_1), call(expected_message_2), call(expected_message_3)])
        expected_message_4 = wrap_text(f"Incorrect name. Please try again(attempt 1 out of 5). Here's the list once again:\n{choices_content}")
        mock_print.assert_any_call(expected_message_4)

        mock_input.assert_has_calls([unittest.mock.call(">>"), unittest.mock.call(">>")])
        self.assertEqual(mock_input.call_count, 2)

    