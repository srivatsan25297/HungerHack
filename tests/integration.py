from models import textmodels
from models import visionmodels
from llama_index.schema import ImageDocument
from . import text


def test_ingredients_for_santy_fridge():
    print("going to create models")
    
    vision_model = visionmodels.get_default_model()
    print("Created models")

    test_img_paths = [
    "/Users/santy/Projects/HungerHack/tests/my_grocery_big.jpg",
    "/Users/santy/Projects/HungerHack/tests/my_grocery.jpg",
    "/Users/santy/Projects/HungerHack/tests/veggies-fridge.jpeg"
    ]

    images_local = []
    for pth in test_img_paths:
        images_local.append(ImageDocument(image_path=pth))
    
    ingredients = vision_model.run_model(images_local).items
    print("Got ingredients from vision model")

    # Run testing against all combinations
    text.test_few_shot_all(suffix = "vision-integration", ingredients_list = [ingredients])

def test_ingredients_for_santy_fridge_reference():
    print("going to create models")
    
    vision_model = visionmodels.get_default_model()
    print("Created models")

    test_img_paths = [
    "/Users/santy/Projects/HungerHack/tests/my_grocery_big.jpg",
    "/Users/santy/Projects/HungerHack/tests/my_grocery.jpg",
    "/Users/santy/Projects/HungerHack/tests/veggies-fridge.jpeg"
    ]

    images_local = []
    for pth in test_img_paths:
        images_local.append(ImageDocument(image_path=pth))
    
    ingredients = vision_model.run_model(images_local).items
    print("Got ingredients from vision model")

    # Run testing against all combinations
    text.test_few_shot_all_with_reference(suffix = "vision-integration-reference2", ingredients_list = [ingredients])

def test_ingredients_for_santy_fridge_reference_v2():
    print("going to create models")
    
    vision_model = visionmodels.get_default_model()
    print("Created models")

    test_img_paths = [
    "/Users/santy/Projects/HungerHack/tests/my_grocery_big.jpg",
    "/Users/santy/Projects/HungerHack/tests/my_grocery.jpg",
    "/Users/santy/Projects/HungerHack/tests/veggies-fridge.jpeg"
    ]

    images_local = []
    for pth in test_img_paths:
        images_local.append(ImageDocument(image_path=pth))
    
    ingredients = vision_model.run_model(images_local).items
    print("Got ingredients from vision model")

    # Run testing against all combinations
    text.test_few_shot_all_with_reference_v2(suffix = "vision-integration-referencev2", ingredients_list = [ingredients])
    



    