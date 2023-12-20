import json
from typing import List
from pydantic import BaseModel
import streamlit as st
from PIL import Image
import os


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
            # TODO: This doesn't handle duplicate images; handle it or does it? I don't know
            if uploaded_file.name not in images_so_far.keys():
                images_so_far[uploaded_file.name] = uploaded_file
        st.session_state['images'] = images_so_far

    st.write("## Uploaded Images")
    if images_so_far:
        for index, image in enumerate(images_so_far):
            columns = st.columns([5,1])
            with columns[0]:
                with st.expander(image):
                    st.image(images_so_far[image], use_column_width=True)
            with columns[1]:
                if st.button("Delete", key="delete_image" + str(index)):
                    delete_image(image)

def toggle_ingredient(index):
    if index in st.session_state['selected_buttons']:
        st.session_state['selected_buttons'].remove(index)
    else:
        st.session_state['selected_buttons'].append(index)
    st.rerun()

def ingredients_container(dummy_data):
    st.header('Ingredients List')
    no_of_buttons_in_a_row = 6
    cols = st.columns(no_of_buttons_in_a_row)
    for i in range(0, len(dummy_data), no_of_buttons_in_a_row):
        for j in range(no_of_buttons_in_a_row):
            if i+j < len(dummy_data):
                if i+j in st.session_state['selected_buttons']:
                    type = "primary"
                else:
                    type = "secondary"
                # cols[j].button(dummy_data[i+j], key='dynamic_button_' + str(i)+ str(j) + dummy_data[i+j], type=type, on_click=on_click, args=(i+j,))
                if cols[j].button(dummy_data[i+j], key='dynamic_button_' + str(i)+ str(j) + dummy_data[i+j], type=type):
                    toggle_ingredient(i+j)

    new_data = ""
    cols = st.columns(2)
    with cols[0]:
        new_data = st.text_input("", label_visibility="collapsed")
    if cols[1].button('Add'):
        dummy_data.append(new_data)
        st.session_state["dummy_data"] = dummy_data
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
            option = st.selectbox(
            "Diet",
            ("Veg", "Non Veg", "Vegan")
            )
        with columns[1]:
            meal_type = st.selectbox(
            "Meal Type",
            ("Desert", "Main Course", "Appetizer")
            )
        cuisine = st.text_input("Enter cuisine")
        submitted = st.form_submit_button("Generate")
        if submitted:
            st.session_state["cuisine"] = cuisine
            st.session_state["meal_typ"] = meal_type
            st.session_state["option"] = option
            recipe = Recipe(name="Test", ingredients=["Onion", "Tomato"], steps=["Step 1", "Step 2", "Step 3"])
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
    if 'dummy_data' not in st.session_state.keys():
        st.session_state['dummy_data'] = ["Onion","Tomato","Carrot"]
    if 'images' not in st.session_state.keys():
        st.session_state['images'] = {}
    if 'selected_buttons' not in st.session_state.keys():
        st.session_state['selected_buttons'] = []


    st.title("HungerHack - Anyone can cook!")
    setup_file_uploader()
    ingredients_container(st.session_state["dummy_data"])
    setup_form() 

if __name__ == "__main__":
    main()
