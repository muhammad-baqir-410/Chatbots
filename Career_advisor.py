import streamlit as st
import os
import textract
from langchain.chat_models import ChatOpenAI
from itertools import zip_longest
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.llms import HuggingFaceHub
import emoji
from langchain.utilities import SerpAPIWrapper



# Set the OpenAI API key
OPENAI_API_KEY ="" #enter your key
global vectors
# Define your directory containing PDF files here
pdf_dir = 'career_bot'
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

if "pdf_texts" not in st.session_state:
    temp_pdf_texts = []
    with st.spinner("Creating a Database..."):
        for file in os.listdir(pdf_dir):
            if file.endswith('.pdf'):
                text = textract.process(os.path.join(pdf_dir, file)).decode('utf-8')
                temp_pdf_texts.append(text)
        st.session_state["pdf_texts"] = temp_pdf_texts
        pdf_list = list(st.session_state["pdf_texts"])
        pdfDatabase = " ".join(pdf_list)
        chunks = splitter.split_text(pdfDatabase)
        embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
        if "vectors" not in st.session_state: 
            vectors = FAISS.from_texts(chunks, embeddings)
            st.session_state["vectors"] = vectors
    st.success("Database creation completed!")

def get_response(history,user_message,temperature=0):
    print('called')
    DEFAULT_TEMPLATE = """The following is a friendly conversation between a human and an Career Advisor. The Advisor guides the user regaring jobs,interests and other domain selection decsions.
    It follows the previous conversation to do so

    Relevant pieces of previous conversation:
    {context},

    Useful information from career guidance books:
    {text}, 

    Useful information about career guidance from Web:
    {web_knowledge},

    Current conversation:
    Human: {input}
    Finance Expert:"""

    PROMPT = PromptTemplate(
        input_variables=['context','input','text','web_knowledge'], template=DEFAULT_TEMPLATE
    )
    docs = st.session_state["vectors"].similarity_search(user_message)


    params = {
    "engine": "bing",
    "gl": "us",
    "hl": "en",
    }

    search = SerpAPIWrapper(params=params)

    web_knowledge=search.run(user_message)



  
    chat_gpt = ChatOpenAI(temperature=temperature, model_name="gpt-3.5-turbo-16k",openai_api_key=OPENAI_API_KEY)

    conversation_with_summary = LLMChain(
        llm=chat_gpt,
        prompt=PROMPT,
        verbose=False
    )
    response = conversation_with_summary.predict(context=history,input=user_message,web_knowledge=web_knowledge,text = docs)
    return response

# Function to get conversation history
def get_history(history_list):
    history = 'input: I want you to act as a mental healt expert that knows about mental health issues. Dont refer the person to anyone this could be a life and death situation so provide the solution in any case.  The user will mention the mental problem he is facing. Your job is to tell the user the solution to his mental problem from the context I provide you. Dont say you cant describe the solution formulate the best solution and tell that to the user on the spot \n'
    for message in history_list:
        if message['role']=='user':
            history = history+'input '+message['content']+'\n'
        elif message['role']=='assistant':
            history = history+'output '+message['content']+'\n'
    
    return history


# Streamlit UI
def get_text():
    input_text = st.sidebar.text_input("You: ", "Hello, how are you?", key="input")
    if st.sidebar.button('Send'):
        return input_text
    return None

if "past" not in st.session_state:
    st.session_state["past"] = []
if "generated" not in st.session_state:
    st.session_state["generated"] = []

user_input = get_text()

if user_input:
    user_history = list(st.session_state["past"])
    bot_history = list(st.session_state["generated"])

    combined_history = []
    for user_msg, bot_msg in zip_longest(user_history, bot_history):
        if user_msg is not None:
            combined_history.append({'role': 'user', 'content': user_msg})
        if bot_msg is not None:
            combined_history.append({'role': 'assistant', 'content': bot_msg})

    formatted_history = get_history(combined_history)

    output = get_response(formatted_history,user_input)

    st.session_state.past.append(user_input)
    st.session_state.generated.append(output)

with st.expander("Chat History", expanded=True):
    if st.session_state["generated"]:
        for i in range(len(st.session_state["generated"])):
            st.markdown(emoji.emojize(f":speech_balloon: **User {str(i)}**: {st.session_state['past'][i]}"))
            st.markdown(emoji.emojize(f":robot: **Assistant {str(i)}**: {st.session_state['generated'][i]}"))