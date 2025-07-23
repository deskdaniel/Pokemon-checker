import json
import csv
from database import create_type_list
from config import types_path


class Pokemon():
    def __init__(self, number, name, types, abilities, stats, bst):
        self.number = number
        self.name = name
        self.types = types
        self.abilities = abilities
        self.stats = stats
        self.bst = bst
        types_list = create_type_list()
        self.defensive_damage_multipliers = self._set_defensive_multipliers(types_list)
        self.offensive_damage_multipliers = self._set_offensive_multipliers(types_list)
    
    def _set_defensive_multipliers(self, types_list):
        defensive_values = {}
        for each in types_list:
            defensive_values[each] = 1
        with open(types_path, mode='r', newline='', encoding='utf-8') as file:
            type_file = csv.reader(file)
            next(type_file)
            for row in type_file:
                if row[0] in self.types:
                    type_multipiers = json.loads(row[1])
                    for key in defensive_values:
                        defensive_values[key] *= type_multipiers[key]
        return defensive_values
    
    def _set_offensive_multipliers(self, types_list):
        offensive_values = {}
        for each in types_list:
            offensive_values[each] = 0
        with open(types_path, mode='r', newline='', encoding='utf-8') as file:
            type_file = csv.reader(file)
            next(type_file)
            for row in type_file:
                if row[0] in self.types:
                    type_multipiers = json.loads(row[2])
                    for key in offensive_values:
                        offensive_values[key] = max(offensive_values[key], type_multipiers[key])
        return offensive_values