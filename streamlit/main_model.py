#  import libraries
import os
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter # split text into characters
from langchain_openai import OpenAIEmbeddings, ChatOpenAI # vectorize text
from langchain_community.vectorstores import FAISS # store vectors
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage, HumanMessage
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
DATA = os.environ['DATA']
openai_api_key = os.environ["OPENAI_API_KEY"]

#  load data from the folder with TextLoader function and encode if necessary
class TextLoader:
    def __init__(self, folder_path):
        self.folder_path = folder_path

    def load(self):
        documents = []
        for root, _, files in os.walk(self.folder_path):
            for filename in files:
                if filename.endswith('.txt'):
                    file_path = os.path.join(root, filename)
                    with open(file_path, 'r', encoding='utf-8') as file:
                        documents.append(file.read())
        return documents

def load_doc(folder_path):
    # Load documents
    loader = TextLoader(folder_path)
    documents = loader.load()
    # concatenate all documents into one
    doc = ''.join(documents)
    # clean text
    doc = doc.replace('\n', ' ').replace('\xa0', ' ')
    # Split document in chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=0)
    texts = splitter.split_text(doc)
    # Vectorize the text
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key, model="text-embedding-3-small")
    # Create vectors
    vectorstore = FAISS.from_texts(texts, embeddings)
    # Persist the vectors locally on disk
    vectorstore.save_local("faiss_db_scilian")

    # Load from local storage
    vector_store = FAISS.load_local("faiss_db_scilian", embeddings)
    return vector_store

def get_context_retriever_chain(vector_store):
    llm = ChatOpenAI()

    retriever = vector_store.as_retriever()

    prompt = ChatPromptTemplate.from_messages([
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}"),
        ("user",
         "Given the above conversation, generate a search query to look up in order to get information relevant to the conversation")
    ])

    retriever_chain = create_history_aware_retriever(llm, retriever, prompt)

    return retriever_chain

def get_conversational_rag_chain(retriever_chain):
    llm = ChatOpenAI()

    prompt = ChatPromptTemplate.from_messages([
        ("system", "Answer the user's questions based on the below context:\n\n{context}"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}"),
    ])

    stuff_documents_chain = create_stuff_documents_chain(llm, prompt)

    return create_retrieval_chain(retriever_chain, stuff_documents_chain)

def get_response(user_input):


    retriever_chain = get_context_retriever_chain(st.session_state.vector_store)
    conversation_rag_chain = get_conversational_rag_chain(retriever_chain)

    response = conversation_rag_chain.invoke({
        "chat_history": st.session_state.chat_history,
        "input": user_query
    })

    return response['answer']


# app config
st.set_page_config(page_title="Chat with Scalian Assistant", page_icon=":robot:")
st.title("Chat with Scalian Assistant")

# sidebar
with st.sidebar:
    st.header("Settings")
    website_url = st.text_input("Website URL")

if website_url is None or website_url == "":
    st.info("Please enter a website URL")

else:
    # session state
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            AIMessage(content="Hello, I am your Assistant. How can I help you?"),
        ]
    if "vector_store" not in st.session_state:
        st.session_state.vector_store = load_doc(DATA)

        # user input
    user_query = st.chat_input("Type your message here...")
    if user_query is not None and user_query != "":
        response = get_response(user_query)
        st.session_state.chat_history.append(HumanMessage(content=user_query))
        st.session_state.chat_history.append(AIMessage(content=response))

    # conversation
    for message in st.session_state.chat_history:
        if isinstance(message, AIMessage):
            with st.chat_message("AI"):
                st.write(message.content)
        elif isinstance(message, HumanMessage):
            with st.chat_message("Human"):
                st.write(message.content)