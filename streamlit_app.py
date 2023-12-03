import streamlit as st
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate
from langchain.schema import HumanMessage, BaseOutputParser
from typing import List

class ParseOutput(BaseOutputParser[List[str]]):
    def parse(self, text: str) -> List[str]:
        return text.strip().split('\n')

st.title('Meal Planner and Tracker')

openai_api_key = st.sidebar.text_input('OpenAI API Key')

def meal_planner(input_text, vector_store):
    chat_model = ChatOpenAI(openai_api_key=openai_api_key)

    template = "You are an AI meal planner and tracker."

    chat_prompt = ChatPromptTemplate.from_messages([
        HumanMessage(content=template),
        HumanMessage(content=f"User's input: {input_text}")
    ])

    # Access vector store information (history)
    if 'meal_plan' in vector_store:
        chat_prompt.add_message(HumanMessage(content=f"User's meal plan: {vector_store['meal_plan']}"))
    if 'foods_eaten' in vector_store:
        chat_prompt.add_message(HumanMessage(content=f"Foods eaten: {vector_store['foods_eaten']}"))
    if 'remaining_foods' in vector_store:
        chat_prompt.add_message(HumanMessage(content=f"Remaining foods: {vector_store['remaining_foods']}"))

    vector_store['input_text'] = input_text

    chain = chat_prompt | chat_model | ParseOutput()
    response = chain.invoke(vector_store)

    st.session_state.meal_vector_store = vector_store

    st.info(response)

with st.form('meal_form'):
    text = st.text_area('Enter your meal-related query.')
    submitted = st.form_submit_button('Submit')

    # Initialize or retrieve vector store (history)
    vector_store = st.session_state.get('meal_vector_store', {})

    if submitted and openai_api_key.startswith('sk-'):
        meal_planner(text, vector_store)
    elif not openai_api_key.startswith('sk-'):
        st.warning('Please enter your OpenAI API key!', icon='⚠')