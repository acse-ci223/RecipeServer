

__all__ = ['Grapher']


class Grapher:
    def __init__(self, recipe):
        self.recipe = recipe

    def graph(self):
        return self.recipe.graph()
