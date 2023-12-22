from . import vision

def get_vanilla_model(name = "vanilla-vision"):
    return vision.GeminiVisionModel(name, "Identify the groceries in the fridge and return it as a list. If you could not find any groceries return an empty list ")

get_default_model = get_vanilla_model