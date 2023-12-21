import json
from typing import List
from pydantic import BaseModel
import streamlit as st
from PIL import Image
import os
from models import visionmodels, textmodels

VISION_MODEL = visionmodels.get_default_model()
TEXT_MODEL = textmodels.get_default_model()

def delete_image(name):
    st.session_state['images'].pop(name)
    st.session_state["file_uploader_key"] += 1
    st.rerun()

def setup_file_uploader():
    
    st.write('''<style>
        .uploadedFile {
                display: none;
        }
    </style>''', unsafe_allow_html=True)

    images_so_far = st.session_state['images']
    uploaded_files = st.file_uploader("Upload an image of your ingredients...", type=["jpg", "jpeg", "png"], accept_multiple_files=True, key=st.session_state["file_uploader_key"])
    if uploaded_files:
        for uploaded_file in uploaded_files:
            if uploaded_file.name not in images_so_far.keys():
                image = Image.open(uploaded_file)
                # TODO: Maybe we can save the image to a temporary directory and then delete it after the session ends?
                image_path = os.path.join(os.getcwd(), uploaded_file.name)
                image.save(image_path)
                images_so_far[uploaded_file.name] = {"filepath": image_path, "image": image} 
    
    images_to_process = []
    for image in images_so_far.keys():
        if "ingredients" not in images_so_far[image]:
            images_to_process.append(image)

    with st.spinner("Processing image(s)..."):
        if images_to_process:
            # TODO: Maybe we can do bulk processing of images? but then, we also need image -> ingredients mapping so that we remove ingredients when we delete an image
            for image in images_to_process:
                image_path = images_so_far[image]["filepath"]
                ingredients = VISION_MODEL.run_model(image_path = image_path).items
                images_so_far[image]["ingredients"] = ingredients
                for ingredient in ingredients:
                    ingredient_count = st.session_state['ingredients'].get(ingredient, 0)
                    st.session_state['ingredients'][ingredient] = ingredient_count + 1
            st.rerun()
            
        

    st.write("## Uploaded Images")
    if images_so_far:
        for index, image in enumerate(images_so_far):
            columns = st.columns([5,1])
            with columns[0]:
                with st.expander(image):
                    st.image(images_so_far[image]['image'], use_column_width=True)
            with columns[1]:
                if st.button("Delete", key="delete_image" + str(index)):
                    delete_image(image)

def toggle_ingredient(index):
    if index in st.session_state['selected_buttons']:
        st.session_state['selected_buttons'].remove(index)
    else:
        st.session_state['selected_buttons'].append(index)
    st.rerun()

def ingredients_container(ingredients):
    st.header('Ingredients List')
    no_of_buttons_in_a_row = 6
    cols = st.columns(no_of_buttons_in_a_row)
    ingredients_list = list(ingredients.keys())
    for row_start_index in range(0, len(ingredients_list), no_of_buttons_in_a_row):
        for col_index in range(no_of_buttons_in_a_row):
            if row_start_index + col_index < len(ingredients_list):
                if row_start_index + col_index in st.session_state['selected_buttons']:
                    type = "primary"
                else:
                    type = "secondary"
                # cols[j].button(dummy_data[i+j], key='dynamic_button_' + str(i)+ str(j) + dummy_data[i+j], type=type, on_click=on_click, args=(i+j,))
                if cols[col_index].button(ingredients_list[row_start_index + col_index], key='dynamic_button_' + str(row_start_index)+ str(col_index) + ingredients_list[row_start_index + col_index], type=type):
                    toggle_ingredient(row_start_index + col_index)

    new_ingredient = ""
    cols = st.columns(2)
    with cols[0]:
        new_ingredient = st.text_input("", label_visibility="collapsed")
    if cols[1].button('Add'):
        if new_ingredient not in ingredients:
            ingredients[new_ingredient] = 1
            st.rerun()

class Recipe(BaseModel):
    name: str
    ingredients: List[str]
    steps: List[str]

    def __str__(self):
        recipe_json = json.dumps(self.dict(), indent=4)
        return recipe_json

def setup_form():
    with st.form("params form"):
        columns = st.columns(2)
        with columns[0]:
            diet = st.selectbox(
            "Diet",
            ("Veg", "Non Veg", "Vegan")
            )
        with columns[1]:
            course = st.selectbox(
            "Course",
            ("Dessert", "Main Course", "Appetizer")
            )
        columns = st.columns(2)
        with columns[0]:
            cuisine = st.text_input("Enter cuisine")
        with columns[1]:
            time_to_cook = st.slider("Time to cook - mins", 0, 120, 30)
        submitted = st.form_submit_button("Generate")
        if submitted:
            total_ingredients = list(st.session_state['ingredients'].keys())
            selected_ingredients = [total_ingredients[i] for i in st.session_state['selected_buttons']]
            print("Details: ", cuisine, course, diet, time_to_cook, selected_ingredients)
            with st.spinner("Generating recipe..."):
                data = {}
                data["cuisine"] = cuisine
                data["time"] = time_to_cook
                data["ingredients"] = selected_ingredients
                data["diet"] = diet
                data["course"] = course
                recipe = TEXT_MODEL.run_model(data)
                print("Returned recipe: ", recipe)
    if submitted:
        st.write("## Generated Recipe: " + recipe.name)

        st.write('''<style> div[data-testid="stExpander"] div[data-testid="stMarkdownContainer"] {
                    font-size: 1.5rem;
                    } </style>''', 
                    unsafe_allow_html=True)
        
        with st.expander(" ### Video"):
            st.video("https://www.youtube.com/watch?v=c2E1P_UN58I")

        with st.expander(" ### Ingredients"):
            for ingredient in recipe.ingredients:
                    st.write("- " + ingredient)
        
        with st.expander(" ### Steps"):
            for index, step in enumerate(recipe.steps):
                st.write(str(index + 1) + ". " + step)

def main():
    if "file_uploader_key" not in st.session_state:
        st.session_state["file_uploader_key"] = 0
    if 'ingredients' not in st.session_state.keys():
        st.session_state['ingredients'] = {}
    if 'images' not in st.session_state.keys():
        st.session_state['images'] = {}
    if 'selected_buttons' not in st.session_state.keys():
        st.session_state['selected_buttons'] = []


    st.title("HungerHack - Anyone can cook!")
    setup_file_uploader()
    ingredients_container(st.session_state["ingredients"])
    setup_form() 

if __name__ == "__main__":
    main()