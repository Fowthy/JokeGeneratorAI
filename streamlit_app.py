import streamlit as st
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate


from langchain.schema import HumanMessage, BaseOutputParser
from langchain.prompts import PromptTemplate

from typing import List


class ParseOutput(BaseOutputParser[List[str]]):
    def parse(self, text: str) -> List[str]:
        return text.strip().split('\n')


st.title('Joke Generator')

openai_api_key = st.sidebar.text_input('OpenAI API Key')
joke_type = st.sidebar.text_input('Joke Type')

def generate_response(input_text):
    creative_model = ChatOpenAI(openai_api_key=openai_api_key)
    refinement_model = ChatOpenAI(openai_api_key=openai_api_key)
    criticism_model = ChatOpenAI(openai_api_key=openai_api_key)
    finalization_model = ChatOpenAI(openai_api_key=openai_api_key)

    template = "You are an AI that generates jokes."

    # Creative idea generation
    creative_prompt = ChatPromptTemplate.from_messages([
        ("system", template),
        ("human", f"Generate a creative joke about {input_text}")
    ])
    creative_output = creative_model(creative_prompt.format_prompt(input_text=input_text).to_messages())  # Get creative output

    # Language refinement
    refinement_prompt = ChatPromptTemplate.from_messages([
        ("system", template),
        ("human", f"Refine the language of the joke: {creative_output}")
    ])
    refined_output = refinement_model(refinement_prompt)  # Get refined output

    # Critique or sentiment analysis
    criticism_prompt = ChatPromptTemplate.from_messages([
        ("system", template),
        ("human", f"Critique the joke: {refined_output}")
    ])
    criticized_output = criticism_model(criticism_prompt)  # Get criticized output

    # Final output
    final_prompt = ChatPromptTemplate.from_messages([
        ("system", template),
        ("human", f"Finalize the joke: {criticized_output}")
    ])
    
    final_output = finalization_model(final_prompt)  # Get final output

    st.info(final_output)




with st.form('my_form'):
    text = st.text_area('Enter keywords or topics for your joke.')
    submitted = st.form_submit_button('Submit')
    if not openai_api_key.startswith('sk-'):
        st.warning('Please enter your OpenAI API key!', icon='⚠')
    if submitted and openai_api_key.startswith('sk-'):
        generate_response(text)