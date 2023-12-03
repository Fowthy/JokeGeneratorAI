import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts.chat import ChatPromptTemplate
from langchain.schema import HumanMessage, BaseOutputParser
from typing import List

class ParseOutput(BaseOutputParser[List[str]]):
    def parse(self, text: str) -> List[str]:
        return text

st.title('🎭 Mood Analyzer')

openai_api_key = st.sidebar.text_input('OpenAI API Key')

def generate_response_and_analyze_mood(input_text):
    
    prompt_model = OpenAI(temperature=0.7, openai_api_key=openai_api_key, model='gpt-3.5')
    mood_model = OpenAI(temperature=0.3, openai_api_key=openai_api_key, model='gpt-3.5-turbo-1106')
    # Model for generating responses
    vector_store.setdefault('moodanalyzer_history', []).append(f"{input_text}")

    chat_prompt = ChatPromptTemplate.from_messages([
        "You are an AI bot that responds to human text and nothing else. You just respond with text or question.",
        *vector_store.get('moodanalyzer_history')
    ])

    # Invoke the model chain
    chain = chat_prompt | prompt_model | ParseOutput()
    response = chain.invoke(vector_store)


    chat_mood_prompt = ChatPromptTemplate.from_messages([
        "You are an AI bot that analyzes the mood of the conversation so far. Use only one of three colorful emojis to describe the mood. Green, yellow or red., where green is friendly, yellow is neutral and red is angry. You output only the emoji, no quotes or other text. You output text only when the red is angry and there is something really wrong that must be pointed out. You output only the emoji, no quotes or other text.",
        *vector_store.get('moodanalyzer_history')
    ])

    # Model for analyzing mood

    chain_mood = chat_mood_prompt | mood_model | ParseOutput()
    mood_analysis = chain.invoke(vector_store)


    st.info(response)

    st.info(mood_analysis)
    vector_store.setdefault('moodanalyzer_history', []).append(f"Model's output: {response}. Mood Analysis: {mood_analysis}. ")

        # Update the vector_store for future interactions
    st.session_state.moodanalyzer_store = vector_store

with st.form('my_form'):
    text = st.text_area('Enter text:')
    submitted = st.form_submit_button('Submit')
    vector_store = st.session_state.get('moodanalyzer_store', {})

    vector_store['moodanalyzer_history'] = []

    if not openai_api_key.startswith('sk-'):
        st.warning('Please enter your OpenAI API key!', icon='⚠')

    if submitted and openai_api_key.startswith('sk-'):
        generate_response_and_analyze_mood(text)