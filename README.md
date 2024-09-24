# Hunger Hack

Hunger Hack is a web application that suggests recipes based on the contents of your fridge. 
Users can upload photos of their fridge, set some parameters, and receive suggestions on what to cook along with the steps based on their parameters and items.

## Project Structure

- `hunger_hack_ui.py`: This is the main file that contains the Streamlit-powered user interface.
- `models`: This directory contains the Text and Vision models which run the Gemini API.
- `tests`: This directory contains various test files that use TruLens to test different models.

## Setup

1. Clone the repository:
    ```
    git clone git@github.com:srivatsan25297/HungerHack.git
    ```
2. Navigate into the project directory:
    ```
    cd hungerhack
    ```
3. Install the required dependencies:
    ```
    pip install -r requirements.txt
    ```
    Note: It's recommended to use a virtual environment to avoid conflicts with other packages.

4. Export your Google API key:
    ```
    export GOOGLE_API_KEY=<your_google_api_key>
    ```
5. Export your OpenAI API key:
    ```
    export OPENAI_API_KEY=<your_openai_api_key>
    ```

## Running the Application

1. Run the Streamlit application:
    ```
    streamlit run hunger_hack_ui.py
    ```
2. Open your web browser and visit `http://localhost:8501` to view the application.

## Running the Tests

1. Run the tests:
    ```
    pytest tests
    ```
