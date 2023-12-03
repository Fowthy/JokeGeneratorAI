import streamlit as st
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate
from langchain.schema import HumanMessage, BaseOutputParser
from typing import List

class ParseOutput(BaseOutputParser[List[str]]):
    def parse(self, text: str) -> List[str]:
        return text

st.title('Health and Fitness Advisor')

openai_api_key = st.sidebar.text_input('OpenAI API Key')

def health_advisor(input_text, vector_store):
    general_model = ChatOpenAI(openai_api_key=openai_api_key)

    template = "You are an AI health and fitness advisor. You answer with short, concrete answers, not general answers. You generalize the user's input and you create concrete goal for the user. Your prompt will be used in other AI model, so you must write to be understandable."

    # Construct the chat prompt with vector store information
    chat_prompt = ChatPromptTemplate.from_messages([
        template,
        f"User's input: {input_text}"
    ])

    # Invoke the model chain
    chain = chat_prompt | general_model | ParseOutput()
    response = chain.invoke(vector_store)


    nutritional_advice_model = ChatOpenAI(openai_api_key=openai_api_key)

    nutritional_model_template = "You are an AI nutritionist. Based on the user's goal, provide specific nutritional advice of what he should eat and what he should not eat, but no recipes. Only information about protein, vitamins, carbs, fat, etc."
    nutri_chat_prompt = ChatPromptTemplate.from_messages([
        nutritional_model_template,
        f"{response}"
    ])

    nutri_chain = nutri_chat_prompt | nutritional_advice_model | ParseOutput()
    nutri_response = nutri_chain.invoke(vector_store)

    recipe_model = ChatOpenAI(openai_api_key=openai_api_key)

    recipe_template = "You are an AI chef. Based on the user's goal, provide specific recipes of what he should eat and what he should not eat. You must use the nutritional advice from the previous model. You must write short and concrete list with quick foods that the user can eat to achieve his goal, nothing else. Only the list."
    recipe_chat_prompt = ChatPromptTemplate.from_messages([
        recipe_template,
        f"Nutritional AI model response: {nutri_response}"
    ])
    recipe_chain = recipe_chat_prompt | recipe_model | ParseOutput()
    recipe_response = recipe_chain.invoke(vector_store)

    combined = response | nutri_response | recipe_chat_prompt

    conclude_model = ChatOpenAI(openai_api_key=openai_api_key)

    conclude_template = "You are an AI health and fitness advisor. You answer with short, concrete answers, not general answers. You must take the response from the previous models and give concrete advice to the user with 2-3 sentences."

    # Construct the chat prompt with vector store information
    conclude_prompt = ChatPromptTemplate.from_messages([
        f"{conclude_template} Model response: {combined}",
        f"User's input: {input_text}"
    ])


    conclude_chain = conclude_prompt | conclude_model | ParseOutput()
    conclude_response = conclude_chain.invoke(vector_store)


    # Update vector store with new information
    vector_store['input_text'] = input_text


    vector_store.setdefault('message_history', []).append(f"Model's response: {response}")

    st.session_state.meal_vector_store = vector_store
    st.info(conclude_response)
    st.info(nutri_response)
    st.info(recipe_response)
    st.info("Opalqq, test")

with st.form('fitness_form'):
    text = st.text_area('Enter your body goal.')
    submitted = st.form_submit_button('Submit')

    # Initialize or retrieve vector store
    vector_store = st.session_state.get('health_vector_store', {})

    vector_store['message_history'] = []
    if submitted and openai_api_key.startswith('sk-'):
        health_advisor(text, vector_store)
        # Update the vector store for future conversations
        st.session_state.health_vector_store = vector_store
    elif not openai_api_key.startswith('sk-'):
        st.warning('Please enter your OpenAI API key!', icon='⚠')

















#    vector_store.setdefault('message_history', []).append(f"User's input: {input_text}")

#     # Construct the chat prompt with vector store information
#     chat_prompt = ChatPromptTemplate.from_messages([
#         template,
#         *vector_store.get('message_history')
#     ])

#     # Update vector store with new information
#     vector_store['input_text'] = input_text

#     # Invoke the model chain
#     chain = chat_prompt | chat_model | ParseOutput()
#     response = chain.invoke(vector_store)

#     vector_store.setdefault('message_history', []).append(f"Model's response: {response}")

#     st.session_state.meal_vector_store = vector_store