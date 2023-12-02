import streamlit as st
from langchain.llms import OpenAI, GPT3, DialoGPT
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate


from langchain.schema import HumanMessage
from langchain.prompts import PromptTemplate






st.title('Task Planner')

openai_api_key = st.sidebar.text_input('OpenAI API Key')
joke_type = st.sidebar.text_input('Joke Type')

def generate_response(input_text):
    llm = OpenAI(temperature=0.7, openai_api_key=openai_api_key)
    chat_model = ChatOpenAI()

    template = "You are an AI that generates {joke_type} jokes."
    human_template = "Generate a joke about {input_text}"

    chat_prompt = ChatPromptTemplate.from_messages([
    ("system", template),
    ("human", human_template),
    ])

    chat_prompt.format_messages(joke_type=joke_type, input_text=input_text)

    chain = chat_prompt | chat_model
    respomse = chain.invoke()

    st.info(respomse)




with st.form('my_form'):
    text = st.text_area('Enter keywords or topics for your joke.')
    submitted = st.form_submit_button('Submit')
    if not openai_api_key.startswith('sk-'):
        st.warning('Please enter your OpenAI API key!', icon='⚠')
    if submitted and openai_api_key.startswith('sk-'):
        generate_response(text)