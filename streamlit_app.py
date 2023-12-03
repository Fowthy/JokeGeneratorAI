import streamlit as st
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate
from langchain.schema import HumanMessage, BaseOutputParser
from typing import List

class ParseOutput(BaseOutputParser[List[str]]):
    def parse(self, text: str) -> List[str]:
        return text.strip().split('\n')

st.title('Health and Fitness Advisor')

openai_api_key = st.sidebar.text_input('OpenAI API Key')

def health_advisor(input_text, vector_store):
    chat_model = ChatOpenAI(openai_api_key=openai_api_key)

    template = "You are an AI health and fitness advisor."

    # Construct the chat prompt with vector store information
    chat_prompt = ChatPromptTemplate.from_messages([
        HumanMessage(content=template),
        HumanMessage(content=f"Provide health and fitness advice based on: {input_text}")
    ])

    # Access vector store information
    if 'user_goals' in vector_store:
        chat_prompt.add_message(HumanMessage(content=f"User's goals: {vector_store['user_goals']}"))
    if 'user_progress' in vector_store:
        chat_prompt.add_message(HumanMessage(content=f"User's progress: {vector_store['user_progress']}"))
    if 'user_preferences' in vector_store:
        chat_prompt.add_message(HumanMessage(content=f"User's preferences: {vector_store['user_preferences']}"))

    # Update vector store with new information
    vector_store['input_text'] = input_text

    # Invoke the model chain
    chain = chat_prompt | chat_model | ParseOutput()
    response = chain.invoke(vector_store)

    st.info(response)

with st.form('fitness_form'):
    text = st.text_area('Enter your health and fitness query.')
    submitted = st.form_submit_button('Submit')

    # Initialize or retrieve vector store
    vector_store = st.session_state.get('health_vector_store', {})

    if submitted and openai_api_key.startswith('sk-'):
        health_advisor(text, vector_store)
        # Update the vector store for future conversations
        st.session_state.health_vector_store = vector_store
    elif not openai_api_key.startswith('sk-'):
        st.warning('Please enter your OpenAI API key!', icon='⚠')