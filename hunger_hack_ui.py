# Description: This file contains the streamlit UI code for the HungerHack project

# Imports
import streamlit as st
from PIL import Image
import os
with st.spinner("Setting up the application... Please wait :)"):
    from models import visionmodels, textmodels

#TODO: Setting Globally is okay? I don't evem know anymore lol
if "vision_model" not in st.session_state:
    st.session_state["vision_model"] = visionmodels.get_default_model()
if "text_model" not in st.session_state:
    st.session_state["text_model"] = textmodels.get_default_model()

VISION_MODEL = st.session_state["vision_model"]
TEXT_MODEL = st.session_state["text_model"]


def delete_image(name):
    ingredients_in_image = st.session_state['images'][name]['ingredients']
    for ingredient in ingredients_in_image:
        ingredient_count = st.session_state['ingredients'][ingredient]['count']
        if ingredient_count == 1:
            st.session_state['ingredients'].pop(ingredient)
        else:
            st.session_state['ingredients'][ingredient]['count'] -= 1

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
                    if ingredient not in st.session_state['ingredients']:
                        st.session_state['ingredients'][ingredient] = {}
                        st.session_state['ingredients'][ingredient]['count'] = 1
                        st.session_state['ingredients'][ingredient]['selected'] = True
                    else:
                        st.session_state['ingredients'][ingredient]['count'] += 1
                        st.session_state['ingredients'][ingredient]['selected'] = True
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

def toggle_ingredient(ingredient):
    st.session_state['ingredients'][ingredient]['selected'] = not st.session_state['ingredients'][ingredient]['selected']
    st.rerun()

def ingredients_container(ingredients):
    st.header('Ingredients List')
    no_of_buttons_in_a_row = 6
    cols = st.columns(no_of_buttons_in_a_row)
    ingredients_list = list(ingredients.keys())
    for row_start_index in range(0, len(ingredients_list), no_of_buttons_in_a_row):
        for col_index in range(no_of_buttons_in_a_row):
            if row_start_index + col_index < len(ingredients_list):
                ingredient = ingredients_list[row_start_index + col_index]
                selected = ingredients[ingredient]['selected']
                if selected:
                    type = "primary"
                else:
                    type = "secondary"
                if cols[col_index].button(ingredients_list[row_start_index + col_index], key='dynamic_button_' + str(row_start_index)+ str(col_index) + ingredients_list[row_start_index + col_index], type=type):
                    toggle_ingredient(ingredient)

    new_ingredient = ""
    cols = st.columns(2)
    with cols[0]:
        new_ingredient = st.text_input("", label_visibility="collapsed")
    if cols[1].button('Add'):
        if new_ingredient not in ingredients:
            ingredients[new_ingredient] = {}
            ingredients[new_ingredient]['count'] = 1
            ingredients[new_ingredient]['selected'] = True
            st.rerun()


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
            selected_ingredients = []
            for ingredient in st.session_state['ingredients']:
                if st.session_state['ingredients'][ingredient]['selected']:
                    selected_ingredients.append(ingredient)
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