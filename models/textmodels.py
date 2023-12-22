# List of GeminiTextModel objects

from . import text

#TODO: Rename all the function names

#TODO: Rename this?
def get_zeroshot_model_limited_params(name = "text-zeroshot-limited-params"):
    system_prompt = """To do: Suggest a recipe which belongs to the {cuisine} cuisine that can be made within {time} with the following ingredients: {ingredients}.
    Don't count oil, salt, pepper in the ingredients
    Return the answer with json format with the following keys: name, ingredients, steps
    """
    gemini_zeroshot_model = text.GeminiTextModel(name, system_prompt)
    return gemini_zeroshot_model

#TODO: Rename this?
def get_fewshot_model_limited_params(name = "text-fewshot-limited-params"):
    system_prompt = """To do: Suggest a recipe which belongs to the {cuisine} cuisine that can be made within {time} with the following ingredients: {ingredients}.
    Don't count oil, salt, pepper in the ingredients
    For example cuisine:indian ingredients:onion, tomato, eggs, rice, milk time:1hr
    Good Answer: Egg curry with cooked rice because the dish follows all the constraints
    Bad Answer: Egg curry with paratha because ingredients does not have flour
    Another example: cuisine:italian ingredients:onion, tomato, eggs, parmesan, pasta, milk, garlic, red chilli peppers time:45mins
    Good Answer: Pasta Arrabbiata because the dish follows all the constraints
    Bad Answer: Egg curry with paratha because the dish is not from the given cuisine

    Return the answer with json format with the following keys: name, ingredients, steps
    """
    gemini_fewshot_model = text.GeminiTextModel(name, system_prompt)
    return gemini_fewshot_model

def get_zeroshot_model_all_params(name = "text-zeroshot-all-params"):
    system_prompt = """To do: Suggest a recipe for a {course} which belongs to the {cuisine} cuisine and should be {diet} that can be made within {time} with the following ingredients: {ingredients}. Don't count oil, salt, pepper in the ingredients
    Return the answer with json format with the following keys: name, ingredients, steps
    """
    gemini_zeroshot_model = text.GeminiTextModel(name, system_prompt)
    return gemini_zeroshot_model

#TODO: Add more example to few shot
def get_fewshot_model_all_params(name = "text-fewshot-all-params"):
    print("Model name", name)
    system_prompt = """To do: Suggest a recipe for a {course} which belongs to the {cuisine} cuisine and should be {diet} that can be made within {time} with the following ingredients: {ingredients}. Don't count oil, salt, pepper in the ingredients. 
    For example cuisine:indian ingredients:onion, tomato, eggs, rice, milk time:1hr
    Good Answer: Egg curry with cooked rice because the dish follows all the constraints
    Bad Answer: Egg curry with paratha because ingredients does not have flour
    Another example: cuisine:italian ingredients:onion, tomato, eggs, parmesan, pasta, milk, garlic, red chilli peppers time:45mins
    Good Answer: Pasta Arrabbiata because the dish follows all the constraints
    Bad Answer: Egg curry with paratha because the dish is not from the given cuisine

    Return the answer with json format with the following keys: name, ingredients, steps
    """
    gemini_fewshot_model = text.GeminiTextModel(name, system_prompt)
    return gemini_fewshot_model

def get_fewshot_model_all_params_with_reference(name = "text-fewshot-all-params-with-reference"):
    print("Model name", name)
    system_prompt = """To do: Suggest a recipe for a {course} which belongs to the {cuisine} cuisine and should be {diet} that can be made within {time} with the following ingredients: {ingredients}. Don't count oil, salt, pepper in the ingredients. 
    Don't get creative with the recipe or food suggestion. For example, if the user asks for a recipe for a dessert, don't suggest a main course.
    Also give me the reference for the recipe you suggest. 
    For example cuisine:indian ingredients:onion, tomato, eggs, rice, milk time:1hr
    Good Answer: Egg curry with cooked rice because the dish follows all the constraints
    Bad Answer: Egg curry with paratha because ingredients does not have flour
    Another example: cuisine:italian ingredients:onion, tomato, eggs, parmesan, pasta, milk, garlic, red chilli peppers time:45mins
    Good Answer: Pasta Arrabbiata because the dish follows all the constraints
    Bad Answer: Egg curry with paratha because the dish is not from the given cuisine

    Return the answer with json format with the following keys: name, ingredients, steps
    """
    gemini_fewshot_model = text.GeminiTextModel(name, system_prompt, text.RecipeWithReference)
    return gemini_fewshot_model


def get_fewshot_model_all_params_with_reference_with_temp(name = "text-fewshot-all-params-with-reference-v2-with-temp", temperature = 0.1):
    name = name + "-" + str(temperature)
    print("Model name", name)
    system_prompt = """To do: Suggest a recipe for a {course} which belongs to the {cuisine} cuisine and should be {diet} that can be made within {time} with the following ingredients: {ingredients}. Don't count oil, salt, pepper in the ingredients. 
    Don't get creative with the recipe or food suggestion. For example, if the user asks for a recipe for a dessert, don't suggest a main course.
    The recipe should be common in the given cuisine. 
    For example cuisine:indian ingredients:onion, tomato, eggs, rice, milk time:1hr
    Good Answer: Egg curry with cooked rice because the dish follows all the constraints
    Bad Answer: Egg curry with paratha because ingredients does not have flour
    Another example: cuisine:italian ingredients:onion, tomato, eggs, parmesan, pasta, milk, garlic, red chilli peppers time:45mins
    Good Answer: Pasta Arrabbiata because the dish follows all the constraints
    Bad Answer: Egg curry with paratha because the dish is not from the given cuisine

    Return the answer with json format with the following keys: name, ingredients, steps with the reference that I can use to verify the answer
    """
    gemini_fewshot_model = text.GeminiTextModel(name, system_prompt, text.RecipeWithReference, temperature = temperature)
    return gemini_fewshot_model


get_default_model = get_fewshot_model_all_params

