import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from PIL import Image

# Load environment variables
load_dotenv()

# Configure the generative AI model
api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
else:
    st.error("API key not found. Please check your environment variables.")

# Function to get response from Gemini API
def get_gemini_response(input_prompt, image):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash-latest")
        response = model.generate_content([input_prompt, image[0]])
        return response.text
    except Exception as e:
        return f"Error generating response: {str(e)}"

# Function to prepare image for API
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        try:
            bytes_data = uploaded_file.getvalue()
            image_parts = [
                {
                    "mime_type": uploaded_file.type,  # Get MIME type of the uploaded file
                    "data": bytes_data,
                }
            ]
            return image_parts
        except Exception as e:
            raise ValueError(f"Error processing image: {str(e)}")
    else:
        raise FileNotFoundError("No file uploaded.")

# Streamlit app setup
st.set_page_config(page_title="Gemini Health App", layout="centered")
st.header("Gemini Health App")

# File uploader
uploaded_file = st.file_uploader("Upload an Image of Food!", type=["jpg", "jpeg", "png"])
if uploaded_file:
    try:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_container_width=True)
    except Exception as e:
        st.error(f"Error displaying image: {str(e)}")

# Button to process the image
submit = st.button("Analyze Food & Get Calories")

# Define the input prompt
input_prompt = """
You are a nutrition expert. Analyze the image of the food provided, identify the food items, and calculate the total calories. 
Provide detailed information in the following format:
1. Item 1 - Number of calories
2. Item 2 - Number of calories
...
Additionally, determine:
- Whether the food is healthy or not
- The percentage split of macronutrients: carbohydrates, fats, proteins, fibers, and sugars.
"""

if submit:
    if uploaded_file:
        with st.spinner("Analyzing the image..."):
            try:
                image_data = input_image_setup(uploaded_file)
                response = get_gemini_response(input_prompt, image_data)
                st.success("Analysis Complete!")
                st.header("Calorie Information:")
                st.write(response)
            except FileNotFoundError as e:
                st.error("No image uploaded. Please upload an image.")
            except Exception as e:
                st.error(f"An unexpected error occurred: {str(e)}")
    else:
        st.warning("Please upload an image before submitting.")

