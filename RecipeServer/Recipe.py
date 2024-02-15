import json


__all__ = ["Recipe"]


class Recipe:
    def __init__(self, recipe):
        self.recipe_json = recipe

    def __repr__(self) -> str:
        return json.dumps(self.recipe_json)

    def __str__(self) -> str:
        return json.dumps(self.recipe_json)

    def to_dict(self):
        return self.recipe_json
