import os
import random
import reflex as rx
from dotenv import load_dotenv
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from openai import OpenAI

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
    is_database_loaded: bool = False

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
            chunk_size=1000, chunk_overlap=100, #length_function=len, add_start_index=True
        )
        docs = text_splitter.split_documents(documents)
        embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
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

    async def openai_process_question(self, question: str):
        """Get the response from the API."""

        # Add the question to the list of questions with a person emoji.

        qa = QA(question=question, answer="")
        self.chats[self.current_chat].append(qa)

        llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0.3, max_tokens=500)
        embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

        if not self.is_database_loaded:
            new_db = FAISS.load_local("scalian_database", embeddings)
            is_database_loaded = True

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
                    """
                    Hello! I'm Lian, your personal assistant. I can only answer questions related to Scalian. 
                    I cannot respond to questions beyond the information I have in the context {context}. 
                    My goal is to help you find answers quickly and in a friendly manner. To ensure smooth communication, 
                    I must always recognize the language of the question and respond in the same language in which 
                    I was asked. For example, if asked in English, I respond in English; if asked in French, 
                    I respond in French; if asked in Spanish, I respond in Spanish, and so on with all languages. 
                    I will provide comprehensive information in my responses. 
                    Additionally, I must always follow these rules with each question: If the question has no context, 
                    I will thoroughly investigate in my database with Scalian as a business reference. 
                    If I don't have the requested information about Scalian, I will offer a friendly apology message to the user. 
                    To add a friendly touch to our conversations, I will include some emojis that complement my responses. 
                    This is important: Whenever there is a URL, I will add it to my responses. I cannot invent or create it; 
                    the URL will be in bold and the title in markdown, indicating where I found the information. 
                    I must always respond in Markdown for better presentation!.
                    """
                    ),
                MessagesPlaceholder(variable_name="chat_history"),
                ("user", "{input}"),
            ]
        )

        stuff_documents_chain = create_stuff_documents_chain(llm, promptb)

        conversation_rag_chain = create_retrieval_chain(
            retriever_chain, stuff_documents_chain
        )

        self.processing = True
        yield

        # # Agrega algunos emojis para darle más personalidad al mensaje
        emojis = ["😬", "🧑🏻‍💻", "🙏", "🚀", "🧠", "⏳", "⏰", "⌛️"]

        thinking = f"{random.choice(emojis)} ..."
        self.chats[self.current_chat][-1].answer = thinking
        yield

        #Prepare chat_history by filtering out or replacing placeholders
        # prepared_chat_history = [
        #     msg.answer if msg.answer != estoy_pensando else msg.answer for msg in self.chats[self.current_chat]
        # ]

        response = await conversation_rag_chain.ainvoke(
            {
                "chat_history": [msg.answer for msg in self.chats[self.current_chat][:0]],
                "input": question,
            }
        )
# [msg.answer for msg in self.chats[self.current_chat]],
        answer_text = response["answer"]
        self.chats[self.current_chat][-1].answer = answer_text

        yield
        self.processing = False

