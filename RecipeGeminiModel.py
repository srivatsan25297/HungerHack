from typing import Dict, List, Union
from pydantic import BaseModel
import json
from llama_index.program import LLMTextCompletionProgram
from llama_index.llms import Gemini
from llama_index.output_parsers import PydanticOutputParser
from trulens_eval import Feedback, Tru, TruLlama, TruBasicApp, Select, Provider


class GeminiFeedbackProvider(Provider):
    # metric A 
    def compare_ingredients(self, input, output):
        output = PydanticOutputParser(Recipe).parse(output)

        input_list = input["ingredients"]
        output_list = output.ingredients
        
        intersection = set(input_list) & set(output_list)
        differences = len(set(output_list) - intersection)

        return float(differences)

class Recipe(BaseModel):
    name: str
    ingredients: List[str]
    steps: List[str]

    def __str__(self):
        recipe_json = json.dumps(self.dict(), indent=4)
        return recipe_json
    

class GeminiModel:
    def __init__(self, app_id: str, system_prompt: str):
        self.app_id = app_id
        self.system_prompt = system_prompt


    def get_full_prompt(self, variable_dict: Dict[str, str]) -> str:
        filled_prompt = self.system_prompt #TODO: Better name
        for key in variable_dict:
            filled_prompt = filled_prompt.replace(f'{{{key}}}', str(variable_dict[key]))
        return filled_prompt

    # TODO: Currently in function; but, seperate it to another function with unittest package?
    def run_test_cases(self, test_cases: List[Dict[str, str]]):
        gemini_provider = GeminiFeedbackProvider()
        f_compare_ingredients = Feedback(gemini_provider.compare_ingredients).on(
            input=Select.RecordInput, output=Select.RecordOutput
        )
        gemini_recorder_with_basic_feedback = TruBasicApp(self.run_model, app_id=self.app_id, feedbacks=[f_compare_ingredients])
        with gemini_recorder_with_basic_feedback as recording:
            for test_case in test_cases:
                gemini_recorder_with_basic_feedback.app(test_case)

    def run_model(self, user_variables: Dict[str, str]) -> Recipe:
        prompt = self.get_full_prompt(user_variables)
        gemini_model = Gemini()
        program = LLMTextCompletionProgram.from_defaults(llm=gemini_model, output_parser=PydanticOutputParser(Recipe), prompt_template_str = prompt, verbose = True)
        response = program()
        return response
    
    

    

gemini_zeroshot_system_prompt = """To do: Suggest a recipe which belongs to the {cuisine} cuisine that can be made within {time} with the following ingredients: {ingredients}.
    Return the answer with json format with the following keys: name, ingredients, steps
    """

gemini_zeroshot_model = GeminiModel("gemini-zeroshot", gemini_zeroshot_system_prompt)


test_cases = [
    {"ingredients":["Onion", "Tomato", "Chilli powder", "Milk", "Paneer", "Garlic", "Ginger"], "time": "1hr", "cuisine": "Indian"},
    {"ingredients":["Onion", "Garlic", "Bread", "Chilli powder", "Milk", "Potato"], "time": "1hr", "cuisine": "Italian"},
    {"ingredients":["Onion", "Garlic", "Bread", "Chilli powder", "Milk", "Potato"], "time": "30mins", "cuisine": "Indian"},
    {"ingredients":["Onion", "Garlic", "Bread", "Chilli powder", "Milk", "Potato"], "time": "30mins", "cuisine": "Mexican"},
    {"ingredients":["Onion", "Garlic", "Bread", "Chilli powder", "Milk", "Potato"], "time": "30mins", "cuisine": "Japanese"},
]

gemini_zeroshot_model.run_test_cases(test_cases)





import time
time.sleep(60) # Wait for the recording to finish
