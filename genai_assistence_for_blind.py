
import streamlit as st
from PIL import Image
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
#from langchain_openai import OpenAI
from langchain.llms import OpenAI
import pytesseract
from gtts import gTTS
from tempfile import NamedTemporaryFile
import openai


# Configure the api key

f = open("keys/.openai.txt")
openai_key = f.read()


model = OpenAI(openai_api_key= openai_key )

prompt_template = PromptTemplate.from_template("What is in this image? {topic},Generate descriptive textual output that interprets the uploaded image, enabling users to understand the scene effectively.")

prompt_template_text_speech = PromptTemplate.from_template("Provide a detailed and informative speech on the topic: {text}")

prompt_template_object = PromptTemplate.from_template("Identify objects and obstacles within the image and highlight them: {topic}")


output_parser = StrOutputParser()

def scene_understanding():

    image_file_1 = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

    if image_file_1 is not None:

        image = Image.open(image_file_1).convert("RGB")

        st.image(image, caption='Uploaded Image')
        
        chain_1 = prompt_template | model | output_parser

        input_data = {"topic": image}

        response = chain_1.invoke(input_data)
        return response
        


def read_text():
        
    image_file_2 = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
    if image_file_2 is not None:
        image = Image.open(image_file_2).convert("RGB")
        st.image(image, caption='Uploaded Image')
        text = pytesseract.image_to_string(image)
        st.write("Extracted text: ")
        st.write(text)

        chain_2 = prompt_template_text_speech | model | output_parser
        input_data = {"text": text}
        response = chain_2.invoke(input_data)
        st.write("Speech text:")
        st.write(response)        
        audio_file =  text_to_speech(response)
        
        return audio_file


def text_to_speech(text):

    with NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
        tts = gTTS(text=text, lang='en')
        tts.save(temp_file.name)

    # Read the audio data from the temporary file
    with open(temp_file.name, 'rb') as audio_file:
        audio_data = audio_file.read()
        return audio_data


def object_detection():
    image_file_3 = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

    if image_file_3 is not None:

        image = Image.open(image_file_3).convert("RGB")

        st.image(image, caption='Uploaded Image')
        
        chain_3 = prompt_template_object | model | output_parser

        input_data = {"topic": image}

        response = chain_3.invoke(input_data)
        audio_response = text_to_speech(response)
        return audio_response

        

def main():
    st.title(":blue[Image Analyzer and Text-to-Speech Converter]")

    analysis = st.radio(
    "Select an analysis type",
    ["Real-time scene understanding", "Text to Speech", "Object and Obstacle Detection"],
    captions=[
        "Upload real time scene.",
        "Upload text based image.",
        "Upload real time image.",
    ],
    index=None,)

    if analysis == "Real-time scene understanding":
        description = scene_understanding()
        st.write("Image Description:")
        st.write(description)
    

    elif analysis == "Text to Speech":
        audio_file = read_text()
        st.audio(audio_file, format="audio/mpeg", loop=True)

    elif analysis == "Object and Obstacle Detection":
        audio_response = object_detection()
        st.audio(audio_response, format="audio/mpeg", loop=True)


if __name__ == "__main__":
    main()


    



    

    
