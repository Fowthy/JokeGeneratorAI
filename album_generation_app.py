import streamlit as st
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate
from langchain.schema import HumanMessage, BaseOutputParser
from typing import List
from langchain.prompts import PromptTemplate
from langchain.utilities.dalle_image_generator import DallEAPIWrapper
from langchain.chains import LLMChain


class ParseOutput(BaseOutputParser[List[str]]):
    def parse(self, text: str) -> List[str]:
        return text

st.title('Album Generator')

openai_api_key = st.sidebar.text_input('OpenAI API Key')
songs_number = st.sidebar.text_input('How many songs?')


def health_advisor(input_text, vector_store):
    theme_generator_model = ChatOpenAI(openai_api_key=openai_api_key, temperature=0.2, model='gpt-3.5-turbo-1106')

    template = "You are an AI album generator. You generate an album theme based on the user prompt. This theme will be used for generating the album cover image and the album name, and will influence the lyrics."

    vector_store.setdefault('album_generator_history', []).append(f"User's prompt is {input_text}")

    # Construct the chat prompt with vector store information
    chat_prompt = ChatPromptTemplate.from_messages([
        template,
        *vector_store.get('album_generator_history')
    ])

    # Invoke the model chain
    chain = chat_prompt | theme_generator_model | ParseOutput()
    response = chain.invoke(vector_store)

    llm = OpenAI(temperature=0.9)
    prompt = PromptTemplate(
        input_variables={'album_theme': response},
        template=f"Generate a detailed prompt to generate an image based on the following description: {response}",
    )
    chain_cover = LLMChain(llm=llm, prompt=prompt)
    image_url = DallEAPIWrapper().run(chain_cover.run("halloween night at a haunted museum"))



    songs_generator_model = ChatOpenAI(openai_api_key=openai_api_key, temperature=0.8, model='gpt-3.5-turbo-1106')

    template_songs = f"You are an AI songs generator. You generate songs based on the album theme. You generate the lyrics only based on the album theme: {response}."


    # Construct the chat prompt with vector store information
    chat_prompt_songs = ChatPromptTemplate.from_messages([
        template_songs,
        f"Generate {songs_number} songs."
    ])

    vector_store.setdefault('album_generator_history', []).append(f"User's prompt is {input_text}")
    # Invoke the model chain
    chain_songs = chat_prompt_songs | songs_generator_model | ParseOutput()
    response_songs = chain_songs.invoke(vector_store)

    st.info(image_url)
    st.header('Album Theme')
    st.info(response, icon='🔥')
    st.header('Album Songs')
    st.info(response_songs)


with st.form('album_form'):
    text = st.text_area('Enter your prompt for your album.')
    submitted = st.form_submit_button('Submit')

    # Initialize or retrieve vector store
    vector_store = st.session_state.get('album_generator_store', {})

    if submitted and openai_api_key.startswith('sk-'):
        health_advisor(text, vector_store)
        # Update the vector store for future conversations
        st.session_state.album_generator_store = vector_store
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