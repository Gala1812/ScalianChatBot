import gradio as gr
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import ConversationalRetrievalChain
from langchain_community.document_loaders import DirectoryLoader
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

# Set your OpenAI API key
os.getenv("OPENAI_API_KEY")

# Initialize the language model
llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

# Data Ingestion for .txt files
txt_loader = DirectoryLoader('../server/chatbot/TextDocuments', glob="**/*.txt")
loaders = [txt_loader]
documents = []
for loader in loaders:
    documents.extend(loader.load())

# Chunk and Embeddings
text_splitter = CharacterTextSplitter(chunk_size=1500, chunk_overlap=0)
documents = text_splitter.split_documents(documents)

embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(documents, embeddings)

# Initialise Langchain - Conversation Retrieval Chain
qa = ConversationalRetrievalChain.from_llm(llm, vectorstore.as_retriever())

def user(user_message, history):
    """Handles user input and retrieves response from QA chain."""
    formatted_history = [(f"User: {msg}", f"Bot: {response}") for msg, response in history]
    response = qa({"question": user_message, "chat_history": formatted_history})
    history.append((user_message, response["answer"]))
    return gr.update(value=""), history

with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    msg = gr.Textbox()
    clear = gr.Button("Clear")
    chat_history = []
    
    msg.submit(user, inputs=[msg, chatbot], outputs=[msg, chatbot])
    clear.click(lambda: None, inputs=None, outputs=chatbot)

if __name__ == "__main__":
    demo.launch(debug=True)
