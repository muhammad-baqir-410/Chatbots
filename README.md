# Interactive Chatbot Applications

This repository contains several interactive chatbot applications that utilize OpenAI's GPT-3.5-turbo language model for natural language processing and conversational interactions. The chatbots are built using the LangChain library, which provides tools and utilities for creating conversational agents.

## Blog.py

The application creates an interactive chatbot interface with Streamlit. Users can input a URL of a blog or any webpage, and the application will extract the text content from that URL.

## Db.py

This code creates an interactive chatbot web application that utilizes OpenAI's GPT-3.5-turbo model for conversational interactions and SQL database interactions to provide useful and informative responses to user queries.

## Pdf.py

This code creates a web-based chatbot interface that allows users to interact with OpenAI GPT-3.5-turbo model for conversational question-answering based on uploaded PDF documents. The chatbot maintains context and history, providing responses to user queries in a user-friendly chat format.

## Coding_assistant_chatbot.py

This code creates a simple interactive chatbot interface using Streamlit, allowing users to engage in a conversation with an LLM model powered by OpenAI. The chatbot responds to user messages based on the conversation history, maintaining context and providing natural-sounding responses in a chat format.

## Career_advisor.py

This code creates a simple interactive chatbot interface using Streamlit, allowing users to engage in a conversation with an LLM model powered by OpenAI. The chatbot responds to user messages based on the conversation history and uses FAISS for similarity search to provide relevant career guidance information from PDF files and web knowledge obtained using the SerpAPIWrapper.

## Financial_advisor.py

This updated code creates an interactive chatbot interface using Streamlit, allowing users to engage in a conversation with an LLM model powered by OpenAI. The chatbot responds to user messages based on the conversation history, relevant financial literature, and information from the web, providing financial advice and guidance to the user.

## Requirements

To run the applications, you will need to install the following dependencies:

aiohttp==3.8.5
aiosignal==1.3.1
altair==5.0.1
argcomplete==1.10.3
async-timeout==4.0.2
attrs==23.1.0
beautifulsoup4==4.8.2
blinker==1.6.2
cachetools==5.3.1
certifi==2023.7.22
chardet==3.0.4
charset-normalizer==3.2.0
click==8.1.6
colorama==0.4.6
compressed-rtf==1.0.6
dataclasses-json==0.5.14
decorator==5.1.1
docx2txt==0.8
ebcdic==1.1.1
emoji==2.7.0
extract-msg==0.28.7
frozenlist==1.4.0
gitdb==4.0.10
GitPython==3.1.32
greenlet==2.0.2
html2text==2020.1.16
idna==3.4
IMAPClient==2.1.0
importlib-metadata==6.8.0
Jinja2==3.1.2
jsonschema==4.18.4
jsonschema-specifications==2023.7.1
langchain==0.0.239
langsmith==0.0.16
lxml==4.9.3
markdown-it-py==3.0.0
MarkupSafe==2.1.3
marshmallow==3.20.1
mdurl==0.1.2
multidict==6.0.4
mypy-extensions==1.0.0
numexpr==2.8.4
numpy==1.25.2
olefile==0.46
openai==0.27.8
openapi-schema-pydantic==1.2.4
packaging==23.1
pandas==2.0.3
pdfminer.six==20191110
Pillow==9.5.0
protobuf==4.23.4
pyarrow==12.0.1
pycryptodome==3.18.0
pydantic==1.10.12
pydeck==0.8.0
Pygments==2.15.1
Pympler==1.0.1
PyPDF2==3.0.1
python-dateutil==2.8.2
python-dotenv==1.0.0
python-pptx==0.6.21
pytz==2023.3
pytz-deprecation-shim==0.1.0.post0
PyYAML==6.0.1
referencing==0.30.0
requests==2.31.0
rich==13.5.1
rpds-py==0.9.2
six==1.12.0
smmap==5.0.0
sortedcontainers==2.4.0
soupsieve==2.4.1
SpeechRecognition==3.8.1
SQLAlchemy==2.0.19
streamlit==1.25.0
streamlit-chat==0.1.1
tenacity==8.2.2
textract==1.6.5
toml==0.10.2
toolz==0.12.0
tornado==6.3.2
tqdm==4.65.0
typing-inspect==0.9.0
typing_extensions==4.7.1
tzdata==2023.3
tzlocal==4.3.1
urllib3==2.0.4
validators==0.20.0
watchdog==3.0.0
xlrd==1.2.0
XlsxWriter==3.1.2
yarl==1.9.2
zipp==3.16.2

You will also need an OpenAI API key for the GPT-3.5-turbo model.

