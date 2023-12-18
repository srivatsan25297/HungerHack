from llama_index.multi_modal_llms.gemini import GeminiMultiModal

from llama_index.multi_modal_llms.generic_utils import (
    load_image_urls,
)
from PIL import Image
import requests
from io import BytesIO
import matplotlib.pyplot as plt
import os
from llama_index.schema import ImageDocument

image_urls = [
    # "https://www.shutterstock.com/image-photo/vegetables-open-fridge-drawer-260nw-1328050283.jpg",
    # "https://www.shutterstock.com/image-photo/vegetables-open-fridge-drawer-260nw-1328050280.jpg",
    # "https://i.pinimg.com/736x/1c/7b/fa/1c7bfa9ce50a91209e5e168389eb839f.jpg"
    "https://www.simplyrecipes.com/thmb/-Ho-gm887tBPpcqjOSoxUFtWiHo=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/SimplyRecipesVegetablesinCrisperDrawer-e7a15e56190846cc8c6d61cee75493f0.jpg"
    # Add yours here!
]

img_folder = "./gopal fridge"

files = [f for f in os.listdir(img_folder)]

# print(files)

img_paths = [
    # "/Users/srivatsan/Desktop/HungerHack/onion-fridge.webp",
    # "/Users/srivatsan/Desktop/HungerHack/onion-potato-fridge.webp",
    "/Users/srivatsan/Desktop/HungerHack/gopal fridge/IMG_1291.jpg",
    "/Users/srivatsan/Desktop/HungerHack/gopal fridge/IMG_1292.jpg"
]

image_documents = load_image_urls(image_urls)

gemini_pro = GeminiMultiModal(model_name="models/gemini-pro-vision")

img_response = requests.get(image_urls[0])
print(image_urls[0])
img = Image.open(BytesIO(img_response.content))
plt.imshow(img)
images_local = []
for pth in img_paths:
    # full_pth = img_folder+"/"+pth
    # print(full_pth)
    images_local.append(ImageDocument(image_path=pth))
print(f"local imgs = {images_local}")
# cuisine = input("Enter the cuisine:")
# time = input("Enter time you have to cook the dish")
# few_shot_prompt = f"""To do: Suggest a recipe which belongs to the {cuisine} cuisine that can be made within {time} with only the ingredients present in the given image. Assume only salt, pepper and oil as extra ingredients.
#     For example cuisine:indian ingredients:onion, tomato, eggs, rice, milk time:1hr
#     Good Answer: Egg curry with cooked rice because the dish follows all the constraints
#     Bad Answer: Egg curry with paratha because ingredients does not have flour
#     Another example: cuisine:italian ingredients:onion, tomato, eggs, parmesan, pasta, milk, garlic, red chilli peppers time:45mins
#     Good Answer: Pasta Arrabbiata because the dish follows all the constraints
#     Bad Answer: Egg curry with paratha because the dish is not from the given cuisine
#     Return the answer with json format with the following keys: name, ingredients, steps, ingredients identified from the image
#     """
complete_response = gemini_pro.complete(
    prompt="Identify the items in the fridge and return it as a list",
    image_documents=images_local,
)
print(complete_response)