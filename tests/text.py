# MODELS WITH LIMITED PARAMETERS: INGREDIENTS, TIME, CUISINE
from models.textmodels import get_fewshot_model_all_params_with_reference_v2, get_fewshot_model_limited_params, get_zeroshot_model_limited_params, get_fewshot_model_all_params, get_zeroshot_model_all_params, get_fewshot_model_all_params_with_reference


_variable_and_values = {
    "time": ["1hr", "30mins"],
    "cuisine": ["Mexican", "Italian", "Indian"],
    "diet": ["veg", "non-veg", "vegan"],
    "course": ["appetizer", "main course", "dessert"],
    "ingredients": [["Onion", "Tomato", "Chilli", "Milk", "Tortilla", "Chapathi", "Flour", "Potato", "Sauce", "Garlic", "Ginger", "Bread", "Chicken", "Bacon", "Mutton", "Pasta"],["Onion", "Tomato", "Milk", "Chapathi", "Flour", "Garlic", "Chicken", "Chapathi", "Tortilla"]]
}

variable_and_values = {
    "time": ["1hr"],
    "cuisine": ["Mexican", "Italian", "Indian"],
    "diet": ["veg", "non-veg"],
    "course": ["main course"],
    "ingredients": [["Onion", "Tomato", "Chilli", "Milk", "Tortilla", "Chapathi", "Flour", "Potato", "Sauce", "Garlic", "Ginger", "Bread", "Chicken", "Bacon", "Mutton", "Pasta"]]
}

# ZEROSHOT WITH LIMITED PARAMETERS: INGREDIENTS, TIME, CUISINE
def test_zero_shot_limited(suffix = "text", ingredients_list = variable_and_values["ingredients"], cuisine_list = variable_and_values["cuisine"], time_list = variable_and_values["time"]):
    print("going to create model")
    zero_shot_limited_model = get_zeroshot_model_limited_params("zero-shot-" + suffix + "-test")
    print("created model")

    test_cases = []
    for time_value in time_list:
        for cuisine_value in cuisine_list:
            for ingredients in ingredients_list:
                print("Created models")
                test_cases.append({"ingredients": ingredients, "time": time_value, "cuisine": cuisine_value})

    zero_shot_limited_model.run_multiple(test_cases)

# FEWSHOT WITH LIMITED PARAMETERS: INGREDIENTS, TIME, CUISINE
def test_few_shot_limited(suffix = "text", ingredients_list = variable_and_values["ingredients"], cuisine_list = variable_and_values["cuisine"], time_list = variable_and_values["time"]):
    print("going to create model")
    few_shot_limited_model = get_fewshot_model_limited_params("few-shot-" + suffix + "-test")
    print("created model")

    test_cases = []
    for time_value in time_list:
        for cuisine_value in cuisine_list:
            for ingredients in ingredients_list:
                print("Created models")
                test_cases.append({"ingredients": ingredients, "time": time_value, "cuisine": cuisine_value})

    few_shot_limited_model.run_multiple(test_cases)


# ZEROSHOT WITH ALL PARAMETERS: INGREDIENTS, TIME, CUISINE, DIET, COURSE
def test_zero_shot_all(suffix = "text", ingredients_list = variable_and_values["ingredients"], cuisine_list = variable_and_values["cuisine"], time_list = variable_and_values["time"], diet_list = variable_and_values["diet"], course_list = variable_and_values["course"]):
    print("going to create model")
    model = get_zeroshot_model_all_params("few-shot-" + suffix + "-test")
    print("created model")

    test_cases = []
    for time_value in time_list:
        for cuisine_value in cuisine_list:
            for ingredients in ingredients_list:
                for diet_value in diet_list:
                    for course_value in course_list:
                        test_cases.append({"ingredients": ingredients, "time": time_value, "cuisine": cuisine_value, "diet": diet_value, "course": course_value})

    model.run_multiple(test_cases)

# FEWSHOT WITH ALL PARAMETERS: INGREDIENTS, TIME, CUISINE, DIET, COURSE
def test_few_shot_all(suffix = "text", ingredients_list = variable_and_values["ingredients"], cuisine_list = variable_and_values["cuisine"], time_list = variable_and_values["time"], diet_list = variable_and_values["diet"], course_list = variable_and_values["course"]):
    print("going to create model")
    print("Suffix", suffix)
    few_shot_limited_model = get_fewshot_model_all_params("few-shot-" + suffix + "-test")
    print("created model")

    test_cases = []
    for time_value in time_list:
        for cuisine_value in cuisine_list:
            for ingredients in ingredients_list:
                for diet_value in diet_list:
                    for course_value in course_list:
                        test_cases.append({"ingredients": ingredients, "time": time_value, "cuisine": cuisine_value, "diet": diet_value, "course": course_value})

    few_shot_limited_model.run_multiple(test_cases)

def test_few_shot_all_with_reference(suffix = "text", ingredients_list = variable_and_values["ingredients"], cuisine_list = variable_and_values["cuisine"], time_list = variable_and_values["time"], diet_list = variable_and_values["diet"], course_list = variable_and_values["course"]):
    print("going to create model")
    print("Suffix", suffix)
    model = get_fewshot_model_all_params_with_reference("few-shot-reference-" + suffix + "-test")
    print("created model")

    test_cases = []
    for time_value in time_list:
        for cuisine_value in cuisine_list:
            for ingredients in ingredients_list:
                for diet_value in diet_list:
                    for course_value in course_list:
                        test_cases.append({"ingredients": ingredients, "time": time_value, "cuisine": cuisine_value, "diet": diet_value, "course": course_value})

    model.run_multiple(test_cases)

def test_few_shot_all_with_reference_v2(suffix = "text", ingredients_list = variable_and_values["ingredients"], cuisine_list = variable_and_values["cuisine"], time_list = variable_and_values["time"], diet_list = variable_and_values["diet"], course_list = variable_and_values["course"]):
    print("going to create model")
    print("Suffix", suffix)
    model = get_fewshot_model_all_params_with_reference_v2("few-shot-reference-" + suffix + "-test")
    print("created model")

    test_cases = []
    for time_value in time_list:
        for cuisine_value in cuisine_list:
            for ingredients in ingredients_list:
                for diet_value in diet_list:
                    for course_value in course_list:
                        test_cases.append({"ingredients": ingredients, "time": time_value, "cuisine": cuisine_value, "diet": diet_value, "course": course_value})

    model.run_multiple(test_cases)


