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
    
    prompt_model = OpenAI(temperature=0.7, openai_api_key=openai_api_key)
    mood_model = OpenAI(temperature=0.7, openai_api_key=openai_api_key)
    # Model for generating responses
    vector_store.setdefault('moodanalyzer_history', []).append(f"User's input: {input_text}")

    chat_prompt = ChatPromptTemplate.from_messages([
        "You answer questions.",
        *vector_store.get('moodanalyzer_history')
    ])

    # Invoke the model chain
    chain = chat_prompt | prompt_model | ParseOutput()
    response = chain.invoke(vector_store)

    # Model for analyzing mood
    mood_prompt = f"Analyze the mood of: {input_text}. Use only one of three colorful emojis to describe the mood. Green, yellow or red., where green is friendly, yellow is neutral and red is angry. You output only the emoji, no quotes or other text. You output text only when the red is angry and there is something really wrong that must be pointed out."
    
    mood_analysis = mood_model(mood_prompt)



    st.info(response)

    st.info(mood_analysis)

with st.form('my_form'):
    text = st.text_area('Enter text:')
    submitted = st.form_submit_button('Submit')
    vector_store = st.session_state.get('moodanalyzer_vector_store', {})


    if not openai_api_key.startswith('sk-'):
        st.warning('Please enter your OpenAI API key!', icon='⚠')

    if submitted and openai_api_key.startswith('sk-'):
        st.session_state.health_vector_store = vector_store
        generate_response_and_analyze_mood(text)