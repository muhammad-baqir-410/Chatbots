from PyPDF2 import PdfReader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.document_loaders import TextLoader

import pickle
from pathlib import Path
from dotenv import load_dotenv
import os
import streamlit as st
from streamlit_chat import message
import io
import asyncio
import requests
import requests
import html2text
from langchain import SQLDatabase, SQLDatabaseChain

st.set_page_config(
    page_title="Enhanced PDFChat",
    page_icon="📘",
    layout="wide",
    initial_sidebar_state="expanded",
)

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

async def main():

    async def storeDocEmbeds(file, filename):
        print("Inside the storedoc func")
        reader = PdfReader(file)
        print("reading content done")
        corpus = ''.join([p.extract_text() for p in reader.pages if p.extract_text()])

        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = splitter.split_text(corpus)

        embeddings = OpenAIEmbeddings(openai_api_key=api_key)
        vectors = FAISS.from_texts(chunks, embeddings)

        with open(filename + ".pkl", "wb") as f:
            pickle.dump(vectors, f)

    async def getDocEmbeds(file, filename):
        if not os.path.isfile(filename + ".pkl"):
            await storeDocEmbeds(file, filename)

        with open(filename + ".pkl", "rb") as f:
            vectors = pickle.load(f)

        return vectors
    
    async def storeStringEmbeds(input_string, filename):
        corpus = input_string

        with open(filename, 'w') as f:
            f.write(input_string)

        loader = TextLoader(filename)
        documents = loader.load()

        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = splitter.split_documents(documents)

        embeddings = OpenAIEmbeddings(openai_api_key=api_key)
        vectors = FAISS.from_documents(chunks, embeddings)

        with open(filename + ".pkl", "wb") as f:
            pickle.dump(vectors, f)

    async def getStringEmbeds(input_string, filename):
        if not os.path.isfile(filename + ".pkl"):
            await storeStringEmbeds(input_string, filename)

        with open(filename + ".pkl", "rb") as f:
            vectors = pickle.load(f)

        return vectors





    async def conversational_chat(query):



        
        result = qa({"question": query, "chat_history": st.session_state['history']})
        st.session_state['history'].append((query, result["answer"]))
        return result["answer"]

    # llm = ChatOpenAI(model_name="gpt-3.5-turbo")
    # chain = load_qa_chain(llm, chain_type="stuff")

    if 'history' not in st.session_state:
        st.session_state['history'] = []

    # Creating the chatbot interface
    st.title("PDFChat :")

    # option = st.selectbox("Select Option", ("PDF", "Blog",'database'))

    # if option == "PDF":
    uploaded_file = st.file_uploader("Choose a file", type="pdf")

    if uploaded_file is not None:
        with st.spinner("Processing..."):
            uploaded_file.seek(0)
            file = uploaded_file.read()
            vectors = await getDocEmbeds(io.BytesIO(file), uploaded_file.name)
            qa = ConversationalRetrievalChain.from_llm(
                ChatOpenAI(model_name="gpt-3.5-turbo"),
                retriever=vectors.as_retriever(),
                return_source_documents=True
            )

        st.session_state['ready'] = True




    if st.session_state.get('ready', False):
        if 'generated' not in st.session_state:
            st.session_state['generated'] = ["Welcome! You can now ask any questions"]

        if 'past' not in st.session_state:
            st.session_state['past'] = ["Hey!"]

        response_container = st.container()
        container = st.container()
       

        with container:
            with st.form(key='my_form', clear_on_submit=True):
                user_input = st.text_input("Query:", placeholder="e.g: Summarize the document", key='input')
                submit_button = st.form_submit_button(label='Send')

            if submit_button and user_input:
               
                output = await conversational_chat(user_input)
                st.session_state['past'].append(user_input)
                st.session_state['generated'].append(output)

        if st.session_state['generated']:
            with response_container:
                for i in range(len(st.session_state['generated'])):
                    if i < len(st.session_state['past']):
                        st.markdown(
                            "<div style='background-color: #90caf9; color: black; padding: 10px; border-radius: 5px; width: 70%; float: right; margin: 5px;'>"+ st.session_state["past"][i] +"</div>",
                            unsafe_allow_html=True
                        )
                    # st.markdown(
                    #     "<div style='background-color: #c5e1a5; color: black; padding: 10px; border-radius: 5px; width: 70%; float: left; margin: 5px;'>"+ st.session_state["generated"][i] +"</div>",
                    #     unsafe_allow_html=True
                    # )
                    # message(st.session_state["past"][i], is_user=True, key=str(i) + '_user', avatar_style="thumbs")
                    message(st.session_state["generated"][i], key=str(i), avatar_style="fun-emoji")

                    

if __name__ == "__main__":
    asyncio.run(main())