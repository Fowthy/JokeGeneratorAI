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

    template = "You are an AI that generates jokes. You answer only what you were asked, in short, concrete answers. You output only the joke, no quotes or other text. You make the joke about goverment."

    template2 = f"{template} You analyse the joke and refine it in understandable way."

    template3 = f"{template2} You critisize the joke and give feedback on what is funny and what is not funny. You output your answer with the joke first and then the feedback."

    template4 = f"{template} You will get the joke, followed with a critique of the joke. You will then finalize the joke and output the final joke. Your goal is to make it as funny as possible."

    # Creative idea generation
    creative_prompt = ChatPromptTemplate.from_messages([
        ("system", template),
        ("human", f"Generate a creative joke about {input_text}")
    ])
    creative_output = creative_model(creative_prompt.format_prompt(input_text=input_text).to_messages()) 

    # Language refinement
    refinement_prompt = ChatPromptTemplate.from_messages([
        ("system", template2),
        ("human", f"Refine the the joke: {creative_output}")
    ])
    refined_output = refinement_model(refinement_prompt.format_prompt(input_text=input_text).to_messages()) 

    # Critique or sentiment analysis
    criticism_prompt = ChatPromptTemplate.from_messages([
        ("system", template3),
        ("human", f"Critique the joke: {refined_output}")
    ])
    criticized_output = criticism_model(criticism_prompt.format_prompt(input_text=input_text).to_messages()) 

    # Final output
    final_prompt = ChatPromptTemplate.from_messages([
        ("system", template4),
        ("human", f"Finalize the joke: {criticized_output}")
    ])
    
    final_output = finalization_model(final_prompt.format_prompt(input_text=input_text).to_messages())

    st.info(final_output)




with st.form('my_form'):
    text = st.text_area('Enter keywords or topics for your joke.')
    submitted = st.form_submit_button('Submit')
    if not openai_api_key.startswith('sk-'):
        st.warning('Please enter your OpenAI API key!', icon='⚠')
    if submitted and openai_api_key.startswith('sk-'):
        generate_response(text)