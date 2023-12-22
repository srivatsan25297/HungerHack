from typing import Dict, List, Optional, Union
from pydantic import BaseModel
import json
from llama_index.program import LLMTextCompletionProgram
from llama_index.llms import Gemini
from llama_index.output_parsers import PydanticOutputParser
from trulens_eval import Feedback, Tru, TruLlama, TruBasicApp, Select, Provider
from llama_index.llms import CustomLLM
import time

# Setting up Feedback provider
from trulens_eval.feedback.provider.openai import OpenAI as fOpenAI
from openai import OpenAI
openai_client = OpenAI()
fopenai = fOpenAI(client = openai_client)



def compare_ingredients(input, output):
    output = PydanticOutputParser(Recipe).parse(output)

    input_list = input["ingredients"]
    output_list = output.ingredients
    
    intersection = set(input_list) & set(output_list)
    differences = len(set(output_list) - intersection)

    return 1 - (float(differences) / len(output_list))

class Recipe(BaseModel):
    name: str
    ingredients: List[str]
    steps: List[str]

    def __str__(self):
        recipe_json = json.dumps(self.dict(), indent=4)
        return recipe_json

class RecipeWithReference(BaseModel):
    name: str
    ingredients: List[str]
    steps: List[str]
    reference: Optional[str]

    def __str__(self):
        recipe_json = json.dumps(self.dict(), indent=4)
        return recipe_json
    

class GeminiTextModel:
    def __init__(self, app_id: str, system_prompt: str, output_class = Recipe, temperature = 0.1):
        self.app_id = app_id
        self.system_prompt = system_prompt
        self.gemini_model = Gemini(temperature = temperature)
        self.output_class = output_class

    def set_model(self, model: CustomLLM):
        self.gemini_model = model

    def set_output_class(self, output_class):
        self.output_class = output_class

    def get_full_prompt(self, variable_dict: Dict[str, str]) -> str:
        filled_prompt = self.system_prompt
        for key in variable_dict:
            filled_prompt = filled_prompt.replace(f'{{{key}}}', str(variable_dict[key]))
        return filled_prompt

    def _run_model(self, user_variables: Dict[str, str]) -> Recipe:
        prompt = self.get_full_prompt(user_variables)
        program = LLMTextCompletionProgram.from_defaults(llm=self.gemini_model, output_parser=PydanticOutputParser(self.output_class), prompt_template_str = prompt, verbose = True)
        response = program()
        return response
    
    
    def run_multiple(self, cases: List[Dict[str, str]]):
        f_compare_ingredients = Feedback(compare_ingredients, name = "Ingredient correctness").on(
            input=Select.RecordInput, output=Select.RecordOutput
        )

        def custom_relevance(input, output):
            input = self.get_full_prompt(input)
            return fopenai.relevance_with_cot_reasons(input, output)

        
        fopenai_relevance = Feedback(custom_relevance, name = "Answer Relevance").on(input=Select.RecordInput, output=Select.RecordOutput)

        gemini_recorder_with_basic_feedback = TruBasicApp(self._run_model, app_id=self.app_id, feedbacks=[fopenai_relevance, f_compare_ingredients])
        responses = []
        with gemini_recorder_with_basic_feedback as recording:
            for case in cases:
                responses.append(gemini_recorder_with_basic_feedback.app(case))
        return responses
    
    def run_model(self, user_variables: Dict[str, str]) -> Recipe:
        responses = self.run_multiple([user_variables])
        return responses[0]
