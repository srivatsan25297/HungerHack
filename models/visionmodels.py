from . import vision

def get_vanilla_model(name = "vanilla-vision"):
    return vision.GeminiVisionModel(name, "Identify the items in the fridge and return it as a list")

get_default_model = get_vanilla_model