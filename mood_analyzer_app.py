import streamlit as st
from langchain.llms import OpenAI

st.title('🎭 Mood Analyzer')

openai_api_key = st.sidebar.text_input('OpenAI API Key')
prompt_model = OpenAI(temperature=0.7, openai_api_key=openai_api_key)
mood_model = OpenAI(temperature=0.7, openai_api_key=openai_api_key)

def generate_response_and_analyze_mood(input_text):
    # Model for generating responses
    response_prompt = f"Generate a response to: {input_text}"
    response = prompt_model(response_prompt)

    # Model for analyzing mood
    mood_prompt = f"Analyze the mood of: {input_text}. Use only one of three colorful emojis to describe the mood. Green, yellow or red., where green is friendly, yellow is neutral and red is angry. You output only the emoji, no quotes or other text. You output text only when the red is angry and there is something really wrong that must be pointed out."
    mood_analysis = mood_model(mood_prompt)

    st.info(response)

    st.info(mood_analysis)

with st.form('my_form'):
    text = st.text_area('Enter text:')
    submitted = st.form_submit_button('Submit')

    if not openai_api_key.startswith('sk-'):
        st.warning('Please enter your OpenAI API key!', icon='⚠')

    if submitted and openai_api_key.startswith('sk-'):
        generate_response_and_analyze_mood(text)