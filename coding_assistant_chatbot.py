import streamlit as st


st.set_page_config(page_title="LangChain Demo", page_icon=":robot:")
st.header("LangChain Demo")



# from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatOpenAI



import streamlit as st
from streamlit_chat import message




"""Python file to serve as the frontend"""
from streamlit_chat import message

from itertools import zip_longest
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain




global bot_history,user_history


def get_response(history,user_message,temperature=0):
   



    DEFAULT_TEMPLATE = """The following is a friendly conversation between a human and an AI. The AI is teaching the user how to program.
    It folows the previous conversation to do so

    Relevant pieces of previous conversation:
    {context}


    (You do not need to use these pieces of information if not relevant)


    Current conversation:
    Human: {input}
    AI:"""

    PROMPT = PromptTemplate(
   input_variables=['context','input'], template=DEFAULT_TEMPLATE
    )



    chat_gpt = ChatOpenAI(temperature=temperature, model_name="gpt-4")
    conversation_with_summary = LLMChain(
    llm=chat_gpt,
    prompt=PROMPT,
    verbose=False
    )
    response =conversation_with_summary.predict(context=history,input=user_message)
    return response

def get_history(history_list):
    history = 'input: I want you to act as an chatbot that teaches coding. The user will mention the topic and language in the specific language he wants to learn. your job is to create a small interactive tutorials in which you break a problem into small coding tasks. Ask the user to complete each task, evaluate its code and then give the next task \n'
    for message in history_list:
        if message['role']=='user':
            history=history+'input '+message['content']+'\n'
        elif message['role']=='assistant':
            history=history+'output '+message['content']+'\n'
    
    return history



# chain = load_chain()

# From here down is all the StreamLit UI.


if "generated" not in st.session_state:
    st.session_state["generated"] = []

if "past" not in st.session_state:
    st.session_state["past"] = []


def get_text():
    input_text = st.text_area("You: ", "Hello, how are you?", key="input")
    return input_text


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

if st.session_state["generated"]:
    for i in range(len(st.session_state["generated"])):
        message(st.session_state["past"][i], is_user=True, key=str(i) + "_user")

        message(st.session_state["generated"][i], key=str(i))

