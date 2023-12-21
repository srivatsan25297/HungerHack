
from llama_index.multi_modal_llms.gemini import GeminiMultiModal
from llama_index.program import MultiModalLLMCompletionProgram
from llama_index.schema import ImageDocument
from pydantic import BaseModel

from typing import Dict, List, overload
from llama_index.output_parsers import PydanticOutputParser

class Ingredients(BaseModel):
    items: List[str]


class GeminiVisionModel:
    def __init__(self, app_id: str, system_prompt: str):
        self.model = GeminiMultiModal(model_name="models/gemini-pro-vision")
        self.app_id = app_id
        self.system_prompt = system_prompt


    def run_model(self, image_path: str = None, image_paths: List[str] = None, image_documents: List[ImageDocument] = None) -> Ingredients:
        if image_path:
            image_documents = [ImageDocument(image_path = image_path)]
        elif image_paths:
            image_documents = [ImageDocument(image_path = image_path) for image_path in image_paths]
        elif image_documents:
            image_documents = image_documents
        
        llm_program = MultiModalLLMCompletionProgram.from_defaults(
            output_parser=PydanticOutputParser(Ingredients),
            image_documents=image_documents,
            prompt_template_str=self.system_prompt,
            multi_modal_llm=self.model,
            verbose=True,
        )
        
        ingredients = llm_program()
        return ingredients