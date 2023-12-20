import streamlit as st
from PIL import Image
import os

def setup_file_uploader():
    uploaded_files = st.file_uploader("Upload an image of your ingredients...", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
    if uploaded_files:
            st.write("## Uploaded Images")
            columns = st.columns(10)
            for uploaded_file, column in zip(uploaded_files, columns):
                st.image(uploaded_file, use_column_width=True)
                img = Image.open(uploaded_file)

def checkbox_container(dummy_data):
    st.header('Ingredients List')
    for i in dummy_data:
        st.checkbox(i, key='dynamic_checkbox_' + i)
    new_data = ""
    cols = st.columns(2)
    with cols[0]:
        new_data = st.text_input("Enter ingredient to add")
    if cols[1].button('Add'):
        dummy_data.append(new_data)
        st.session_state["dummy_data"] = dummy_data
        st.rerun()

def generate_recepie():
    #to do call model to get a recipie
    st.text(st.session_state)
    
def setup_form():
    with st.form("params form"):
        columns = st.columns(2)
        with columns[0]:
            option = st.selectbox(
            "Veg/Non Veg/ Vegan",
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
            generate_recepie()                

def main():
    st.title("Multiple Image Upload and Display App")
    setup_file_uploader()
    if 'dummy_data' not in st.session_state.keys():
        st.session_state['dummy_data'] = ["a","b","c"]
    checkbox_container(st.session_state["dummy_data"])
    setup_form() 

if __name__ == "__main__":
    main()
