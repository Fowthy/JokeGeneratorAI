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


st.title('Task Planner')

openai_api_key = st.sidebar.text_input('OpenAI API Key')
joke_type = st.sidebar.text_input('Joke Type')

def generate_response(input_text):
    chat_model = ChatOpenAI(openai_api_key=openai_api_key)

    template = "You are an AI that generates {joke_type} jokes."
    human_template = "Generate a joke about {input_text}"

    chat_prompt = ChatPromptTemplate.from_messages([
    ("system", template),
    ("human", human_template),
    ])

    chain = chat_prompt | chat_model | ParseOutput()
    respomse = chain.invoke({"input_text": input_text, "joke_type": joke_type})

    st.info(respomse)




with st.form('my_form'):
    text = st.text_area('Enter keywords or topics for your joke.')
    submitted = st.form_submit_button('Submit')
    if not openai_api_key.startswith('sk-'):
        st.warning('Please enter your OpenAI API key!', icon='⚠')
    if submitted and openai_api_key.startswith('sk-'):
        generate_response(text)