import csv
import folium

class Node:
    
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None
        self.height = 1

    def matches_criteria(self, criteria):
        for key, value in criteria.items():
            if key not in self.data:
                return False
            if isinstance(value, tuple):
                operator, target_value = value
                if operator == '>':
                    if self.data[key] <= target_value:
                        return False
                elif operator == '<':
                    if self.data[key] >= target_value:
                        return False
                elif operator == '>=':
                    if self.data[key] < target_value:
                        return False
                elif operator == '<=':
                    if self.data[key] > target_value:
                        return False
                elif operator == '=':
                    if self.data[key] != target_value:
                        return False
                else:
                    raise ValueError(f"Invalid operator: {operator}")
            else:
                if self.data[key] != value:
                    return False
        return True


