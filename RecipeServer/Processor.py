import os
import json

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
        open_ai_key = os.getenv("OPENAI")
        self.client = OpenAI(api_key=open_ai_key)
        self.seed = 100

    def process(self, recipe):
        inst = """
        Given a recipe, follow these steps to create a structured JSON object representing the recipe's instructions along with the estimated time for each step:

            1.	Break the recipe into many individual single steps.
            2.	For each step, identify the estimated time required to complete it. If the recipe provides a range, note both numbers in an array, else estimate it.
            3.	Write a concise instruction for each step. Split that instruction into smaller parts and write each part in JSON format. Estimate each parts' time.
            4.	Format your JSON object with step numbers as keys and an object containing time and step_instruction as their values.
            5.	Ensure proper JSON formatting, including using double quotes for strings and keys, and correctly placing commas and brackets.”

        Example JSON Structure for a Single Step
        {
        "step_number": {
            "time": [minimum_time, maximum_time],
            "step_instruction": { "number": {"instruction_number":instruction, "time":estimated time} }
            }
        }
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
            raise ValueError("The response from the model is not a valid JSON object.")

        return Recipe(json.loads(res))

