from typing import Dict, List, Union
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

# TODO: Invert high to low
def compare_ingredients(input, output):
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

class RecipeWithReference(BaseModel):
    name: str
    ingredients: List[str]
    steps: List[str]
    reference: str

    def __str__(self):
        recipe_json = json.dumps(self.dict(), indent=4)
        return recipe_json
    

class GeminiTextModel:
    def __init__(self, app_id: str, system_prompt: str, output_class = Recipe, temperature = 0.1):
        print("Model name", app_id)
        print("OUTPUT CLASS", output_class)
        print("TEMPERATURE", temperature)
        
        self.app_id = app_id
        self.system_prompt = system_prompt
        self.gemini_model = Gemini(temperature=temperature)
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

        # Feedbacks
        f_compare_ingredients = Feedback(compare_ingredients).on(
            input=Select.RecordInput, output=Select.RecordOutput
        )

        def custom_relevance(input, output):
            input = self.get_full_prompt(input)
            return fopenai.relevance_with_cot_reasons(input, output)
        
        from trulens_eval.feedback import GroundTruthAgreement
        golden_set = [
            {"query": "who invented the lightbulb?", "response": "Thomas Edison"},
            {"query": "¿quien invento la bombilla?", "response": "Thomas Edison"}
        ]
        ground_truth_collection = GroundTruthAgreement(golden_set)
        def custom_agreement_measure(input, output):
            input = self.get_full_prompt(input)
            print("Hey I am in Agreement measure")
            return_value = ground_truth_collection.agreement_measure(input, output)
            print("Return value", return_value)
            return return_value

        fopenai_relevance = Feedback(custom_relevance, name = "Answer Relevance").on(input=Select.RecordInput, output=Select.RecordOutput)
        fopenai_model_agreement = Feedback(custom_agreement_measure, name = "Agreement measure").on(input=Select.RecordInput, output=Select.RecordOutput)

        gemini_recorder_with_basic_feedback = TruBasicApp(self._run_model, app_id=self.app_id, feedbacks=[f_compare_ingredients, fopenai_model_agreement])
        
        responses = []
        with gemini_recorder_with_basic_feedback as recording:
            for case in cases:
                responses.append(gemini_recorder_with_basic_feedback.app(case))
                time.sleep(60)

        return responses
    
    def run_model(self, user_variables: Dict[str, str]) -> Recipe:
        responses = self.run_multiple([user_variables])
        return responses[0]
