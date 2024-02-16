import os
import re
import getpass
import requests
import json
import openai
import emoji
import tiktoken
import reflex as rx
from openai import OpenAI
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
openai_api_key = os.getenv("OPENAI_API_KEY")
store = os.getenv("STORE")
database = os.getenv("DATABASE")
index = os.getenv("INDEX")


class QA(rx.Base):
    """A question and answer pair."""

    question: str
    answer: str


DEFAULT_CHATS = {
    "Main": [],
}


class State(rx.State):
    """The app state."""

    chats: dict[str, list[QA]] = DEFAULT_CHATS
    current_chat = "Main"
    question: str
    processing: bool = False
    new_chat_name: str = ""
    drawer_open: bool = False
    modal_open: bool = False
    api_type: str = "openai"
    is_vector: bool = False
    is_empty: bool = True
    is_database_stored: bool = False

    def create_chat(self):
        """Create a new chat."""
        # Add the new chat to the list of chats.
        self.current_chat = self.new_chat_name
        self.chats[self.new_chat_name] = []

        # Toggle the modal.
        self.modal_open = False

    def toggle_modal(self):
        """Toggle the new chat modal."""
        self.modal_open = not self.modal_open

    def toggle_drawer(self):
        """Toggle the drawer."""
        self.drawer_open = not self.drawer_open

    def delete_chat(self):
        """Delete the current chat."""
        del self.chats[self.current_chat]
        if len(self.chats) == 0:
            self.chats = DEFAULT_CHATS
        self.current_chat = list(self.chats.keys())[0]
        self.toggle_drawer()

    def set_chat(self, chat_name: str):
        """Set the name of the current chat.

        Args:
            chat_name: The name of the chat.
        """
        self.current_chat = chat_name
        self.toggle_drawer()

    @rx.var
    def chat_titles(self) -> list[str]:
        """Get the list of chat titles.

        Returns:
            The list of chat names.
        """
        return list(self.chats.keys())

    async def load_documents(self):
        folder_path = store

        text_loader_kwargs = {"autodetect_encoding": True}
        loader = DirectoryLoader(
            folder_path,
            loader_cls=TextLoader,
            loader_kwargs=text_loader_kwargs,
            show_progress=True,
            silent_errors=True,
        )
        documents = loader.load()

        text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=10)
        docs = text_splitter.split_documents(documents)
        embeddings = OpenAIEmbeddings()
        db = FAISS.from_documents(docs, embeddings)
        db.save_local("scalian_database")
        self.is_vector = True

    async def check_store_documents(self):
        try:
            if not os.path.exists(store):
                os.makedirs(store)
            if len(os.listdir(store)) != 0:
                self.is_empty = False
                print("Documents are already stored...")
                if not self.is_empty and not self.is_vector:
                    print("Building vector store...")
                    await self.load_documents()
                    await self.check_database_stored()
            else:
                self.is_empty = True
                print("No documents are stored...")
        except Exception as e:
            print(e)

    async def check_database_stored(self):
        current_dir = os.path.dirname(__file__)
        folder_documents = os.path.join(current_dir, "..", database)

        if os.path.exists(folder_documents) and os.path.exists(
            folder_documents + "/" + index
        ):
            print("Database exists...")
            self.is_database_stored = True
        else:
            print("Database does not exist...")
            self.is_database_stored = False

    async def process_question(self, form_data: dict[str, str]):
        await self.check_database_stored()
        if not self.is_database_stored:
            if not self.is_vector:
                await self.check_store_documents()
        if self.is_database_stored:
            # Get the question from the form
            question = form_data["question"]

            # Check if the question is empty
            if question == "":
                return

            model = self.openai_process_question

            async for value in model(question):
                yield value

    async def openai_process_question(self, question: str):
        """Get the response from the API."""

        # Add the question to the list of questions with a person emoji.
        qa = QA(question=emoji.emojize("👨🏼‍💼 ") + question, answer="")
        self.chats[self.current_chat].append(qa)

        llm = ChatOpenAI()
        # Clear the input and start the processing.
        self.processing = True
        yield

        embeddings = OpenAIEmbeddings()
        new_db = FAISS.load_local("scalian_database", embeddings)

        retriever = new_db.as_retriever()
        docs = retriever.invoke(question)
        # Use retrieved documents to generate response
        response = ""

        for doc in docs:
            response += "🤖 " + doc.page_content + "\n"
            print(f"🤓 {response}\n")

        # Update the last QA pair with the response
        self.chats[self.current_chat][-1].answer = response
        yield

        # Toggle the processing flag.
        self.processing = False
