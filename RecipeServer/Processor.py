import os
import json

import requests
from openai import OpenAI
from dotenv import load_dotenv

from .Recipe import Recipe


load_dotenv(override=True)

__all__ = ['Processor']


def validate_json_structure(data, structure):
    """
    Validate if the given data matches the expected structure.
    """
    if not isinstance(data, dict):
        return False

    for key, value in structure.items():
        if key not in data:
            return False

        if key == "time" and isinstance(value, list):
            # Expecting [minimum_time, maximum_time]
            if not (isinstance(data[key], list) and len(data[key]) == 2 and all(isinstance(item, (int, float)) for item in data[key])):
                return False
        elif key == "step_instruction" and isinstance(value, dict):
            # Recursive validation for step_instruction
            for sub_key, sub_structure in value.items():
                if not validate_json_structure({sub_key: data[key].get(sub_key, {})}, {sub_key: sub_structure}):
                    return False
        elif isinstance(value, dict):
            # General case for dictionary structures
            if not validate_json_structure(data[key], value):
                return False
    return True


def is_valid_json(json_string):
    try:
        data = json.loads(json_string)
        expected_structure = {
            "step_number": {
                "time": [0, 0],  # Placeholder for minimum and maximum time validation
                "step_instruction": {
                    "number": {
                        "instruction_number": "instruction",
                        "time": 0  # Placeholder for estimated time validation
                    }
                }
            }
        }
        return validate_json_structure(data, expected_structure)
    except json.JSONDecodeError:
        return False


class Processor:
    def __init__(self):
        self.__open_ai_key = os.getenv("OPENAI")
        self.__spoonacular_key = os.getenv("SPOONACULAR")
        self.client = OpenAI(api_key=self.__open_ai_key)
        self.seed = 100

    def download_recipe(self, recipe_name):
        sample_recipe = """
        A recipe for making a classic Italian lasagna.
        Ingredients:
        - 1 pound sweet Italian sausage
        - 3/4 pound lean ground beef
        - 1/2 cup minced onion
        - 2 cloves garlic, crushed
        - 1 (28 ounce) can crushed tomatoes
        - 2 (6 ounce) cans tomato paste
        - 2 (6.5 ounce) cans canned tomato sauce
        - 1/2 cup water
        - 2 tablespoons white sugar
        - 1 1/2 teaspoons dried basil leaves
        - 1/2 teaspoon fennel seeds
        - 1 teaspoon Italian seasoning
        - 1 tablespoon salt
        - 1/4 teaspoon ground black pepper
        - 4 tablespoons chopped fresh parsley
        - 12 lasagna noodles
        - 16 ounces ricotta cheese
        - 1 egg
        - 3/4 teaspoon salt
        - 3/4 pound mozzarella cheese, sliced
        - 3/4 cup grated Parmesan cheese
        Directions:
        1. In a Dutch oven, cook sausage, ground beef, onion, and garlic over medium heat until well browned. Stir in crushed tomatoes, tomato paste, tomato sauce, and water. Season with sugar, basil, fennel seeds, Italian seasoning, 1 tablespoon salt, pepper, and 2 tablespoons parsley. Simmer, covered, for about 1 1/2 hours, stirring occasionally.
        2. Bring a large pot of lightly salted water to a boil. Cook lasagna noodles in boiling water for 8 to 10 minutes. Drain noodles, and rinse with cold water. In a mixing bowl, combine ricotta cheese with egg, remaining parsley, and 1/2 teaspoon salt.
        3. Preheat oven to 375 degrees F (190 degrees C).
        4. To assemble, spread 1 1/2 cups of meat sauce in the bottom of a 9x13 inch baking dish. Arrange 6 noodles lengthwise over meat sauce. Spread with one half of the ricotta cheese mixture. Top with a third of mozzarella cheese slices. Spoon 1 1/2 cups meat sauce over mozzarella, and sprinkle with 1/4 cup Parmesan cheese. Repeat layers, and top with remaining mozzarella and Parmesan cheese. Cover with foil: to prevent sticking, either spray foil with cooking spray, or make sure the foil does not touch the cheese.
        5. Bake in preheated oven for 25 minutes. Remove foil, and bake an additional 25 minutes. Cool for 15 minutes before serving.
        """

        def get_recipes(ingredients, diet):
            url = "https://api.spoonacular.com/recipes/complexSearch"
            params = {
                "apiKey": self.__spoonacular_key,
                "query": ingredients,
                "diet": diet,
                "number": 1,
                "addRecipeInformation": True
            }
            response = requests.get(url, params=params)
            return response.json()

        recipe = get_recipes(recipe_name, "None")
        recipe = recipe["results"][0]
        source = recipe.get("sourceUrl")
        image = recipe.get("image")
        instructions = recipe.get("analyzedInstructions")[0]["steps"]
        instructions = "\n".join(list(map(lambda x: x["step"], instructions)))

        return instructions

    def process(self, recipe):
        inst = """
        Given a recipe, follow these steps to create a structured JSON object representing the recipe's instructions along with the estimated time for each step:

            1.	Break the recipe into many individual single steps.
            2.	For each step, identify the estimated time required to complete it in minutes. If the recipe provides a range, note both numbers in an array in the form of minutes, else estimate it in minutes.
            3.	Write a concise instruction for each step. Split that instruction into smaller parts and write each part in JSON format. Estimate each parts' time.
            4.	Format your JSON object with step numbers as keys and an object containing time and step_instruction as their values.
            5.	Ensure proper JSON formatting, including using double quotes for strings and keys, and correctly placing commas and brackets.”

        Convert all times from seconds to minutes. Critically evaluate the estimated times for each step. If you need to make any changes, do so now. All times should be in minutes.

        Example JSON Structure for a Single Step
        {
        "step_number": {
            "time": [minimum_time in minutes, maximum_time in minutes],
            "step_instruction": { "number": {"instruction_number":instruction, "time":estimated time in minutes} }
            }
        }

        Re-evaluate all steps and make sure everything is correct. If you need to make any changes, do so now. All times should be in minutes.
        """  # noqa

        response = self.client.chat.completions.create(
            model="gpt-4-0125-preview",
            seed=self.seed,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": inst},
                {"role": "user", "content": recipe}
            ]
        )

        res = response.choices[0].message.content
        if not is_valid_json(res):
            try:
                return Recipe(json.loads(res))
            except json.JSONDecodeError:
                raise ValueError("The response from the model is not a valid JSON object.")

        return Recipe(json.loads(res))

