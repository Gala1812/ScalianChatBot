import getpass
import json
import os
import re

import emoji
import openai
import reflex as rx
import requests
import tiktoken
from dotenv import load_dotenv
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.text_splitter import (
    CharacterTextSplitter,
    RecursiveCharacterTextSplitter,
)
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.vectorstores import FAISS, Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
openai_api_key = os.getenv("OPENAI_API_KEY")
store = os.getenv("STORE")
database = os.getenv("DATABASE")
index = os.getenv("INDEX")

PROMPT_TEMPLATE = """
The following is a conversation with an AI assistant. The assistant is helpful, clever, and very friendly. After each dot, insert a new line. Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""


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

        text_splitter = CharacterTextSplitter(
            chunk_size=200, chunk_overlap=20, length_function=len, add_start_index=True
        )
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
            f"{folder_documents}/{index}"
        ):
            print("Database exists...")
            self.is_database_stored = True
        else:
            print("Database does not exist...")
            self.is_database_stored = False

    async def process_question(self, form_data: dict[str, str]):
        await self.check_database_stored()
        if not self.is_database_stored and not self.is_vector:
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

    # async def openai_process_question(self, question: str):
    #     """Get the response from the API."""

    #     # Add the question to the list of questions with a person emoji.
    #     qa = QA(question=question, answer="")
    #     self.chats[self.current_chat].append(qa)

    #     # llm = ChatOpenAI()
    #     # Clear the input and start the processing.
    #     self.processing = True
    #     yield

    #     embeddings = OpenAIEmbeddings()
    #     new_db = FAISS.load_local("scalian_database", embeddings)

    #     # retriever = new_db.as_retriever()
    #     # docs = retriever.invoke(question)

    #     results = new_db.similarity_search_with_relevance_scores(question, k=3)
    #     print("Len results: ", len(results))
    #     print("Results: ", results)
    #     if len(results) == 0 or results[0][1] < 0.75:
    #         prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE).format(
    #             context="",  # Remove context in this case
    #             question=question,
    #             additional_text="""\n\nI don't have that information in my database yet. Try rephrasing your question, or contact customer service at 911911911."""
    #         )
    #     else:

    #     # print(f"Found {len(results)} documents")
    #     # print(results)

    #         context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    #         prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    #         prompt = prompt_template.format(context=context_text, question=question)
    #         print(prompt)

    #     model = ChatOpenAI(temperature=0)
    #     response_text = model.invoke(prompt)
    #     formatted_response = f"🤖 {response_text} "

    #     # Use retrieved documents to generate response
    #     # response = ""

    #     # for doc in docs:
    #     #     response += "🤖 " + doc.page_content + "\n"
    #     #     print(f"🤓 {response}\n")

    #     # Update the last QA pair with the response
    #     self.chats[self.current_chat][-1].answer = formatted_response
    #     yield

    #     # Toggle the processing flag.
    #     self.processing = False

    # async def openai_process_question(self, question: str):
    #     """Get the response from the API."""

    #     # Add the question to the list of questions with a person emoji.
    #     qa = QA(question=question, answer="")
    #     self.chats[self.current_chat].append(qa)

    #     # llm = ChatOpenAI()
    #     # Clear the input and start the processing.
    #     self.processing = True
    #     yield

    #     embeddings = OpenAIEmbeddings()
    #     new_db = FAISS.load_local("scalian_database", embeddings)

    # retriever = new_db.as_retriever()
    # docs = retriever.invoke(question)

    #     results = new_db.similarity_search_with_relevance_scores(question, k=3)
    #     print("Len results: ", len(results))
    #     print("Results: ", results)
    #     if len(results) == 0 or results[0][1] < 0.5:
    #         prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE).format(
    #             context="",  # Remove context in this case
    #             question=question,
    #             additional_text="""I don't have that information in my database yet. Try rephrasing your question, or contact customer service at 911911911.""",
    #         )
    #     else:

    #         # print(f"Found {len(results)} documents")
    #         # print(results)

    #         context_text = "".join([doc.page_content for doc, _score in results])
    #         prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    #         prompt = prompt_template.format(context=context_text, question=question)
    #         print("PROMPT: ", prompt)

    #     model = ChatOpenAI(temperature=0)
    #     response_text = model.invoke(prompt)
    #     formatted_response = f"{response_text}"
    #     print("Texto: ", formatted_response[-1])

    #     # Use retrieved documents to generate response
    #     # response = ""

    #     # for doc in docs:
    #     #     response += "🤖 " + doc.page_content + "\n"
    #     #     print(f"🤓 {response}\n")

    #     # Update the last QA pair with the response
    #     self.chats[self.current_chat][-1].answer = formatted_response
    #     yield

    #     # Toggle the processing flag.
    #     self.processing = False

    async def openai_process_question(self, question: str):
        """Get the response from the API."""

        # Add the question to the list of questions with a person emoji.
        qa = QA(question=question, answer="")
        self.chats[self.current_chat].append(qa)

        llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0, max_tokens=1000)
        embeddings = OpenAIEmbeddings()
        new_db = FAISS.load_local("scalian_database", embeddings)

        # Clear the input and start the processing.
        retriever = new_db.as_retriever()

        prompt = ChatPromptTemplate.from_messages(
            [
                MessagesPlaceholder(variable_name="chat_history"),
                ("user", "{input}"),
                (
                    "user",
                    "Given the above conversation, generate a search query to look up in order to get information relevant to the conversation",
                ),
            ]
        )

        retriever_chain = create_history_aware_retriever(llm, retriever, prompt)

        promptb = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "Answer the user's questions based on the below context:\n\n{context}",
                ),
                MessagesPlaceholder(variable_name="chat_history"),
                ("user", "{input}"),
            ]
        )

        stuff_documents_chain = create_stuff_documents_chain(llm, promptb)

        conversation_rag_chain = create_retrieval_chain(
            retriever_chain, stuff_documents_chain
        )

        response = conversation_rag_chain.invoke(
            {
                "chat_history": [msg.answer for msg in self.chats[self.current_chat]],
                "input": question,
            }
        )

        self.processing = True
        yield

        self.chats[self.current_chat][-1].answer = response["answer"]
        yield

        # Toggle the processing flag.
        self.processing = False
