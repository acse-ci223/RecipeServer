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
        if not isinstance(self.recipe_json, list):
            if isinstance(self.recipe_json, str):
                self.recipe_json = json.loads(self.recipe_json)
            elif isinstance(self.recipe_json, dict):
                return [self.recipe_json]
            self.to_dict()
        else:
            return self.recipe_json
