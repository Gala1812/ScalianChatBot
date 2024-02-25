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
            chunk_size=1000, chunk_overlap=0, #length_function=len, add_start_index=True
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
                    You are an assistant named Lian, you are polite, 
                    Answer the user's questions based on the context: 
                    {context}
                    You must answer the question on the language of the question:
                    the question on English must answer on English,
                    the question on Spanish must answer on Spanish,
                    question on French must answer on French.
                    
                    If you are asked a question that out of context, check if you can answer it by adding Scalian as a reference company.
                    Always answer providing complete information, if you can't answer, you can say that you do not have that information and 
                    provide them with a phone number or the address of the office in Madrid, or you can ask the user for additional information.
                    Add some emojis as you answer to give meaning to the responses, and don't forget to be kind and polite.
                    Whenever possible, end with the URL in bold to direct them to the place where you found the information,.
                    don't forget to highlight the link in bold. Answer in Markdown.
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

        # Prepare chat_history by filtering out or replacing placeholders
        # prepared_chat_history = [
        #     msg.answer if msg.answer != estoy_pensando else msg.answer for msg in self.chats[self.current_chat]
        # ]

        response = await conversation_rag_chain.ainvoke(
            {
                "chat_history": [msg.answer for msg in self.chats[self.current_chat]],
                "input": question,
            }
        )

        answer_text = response["answer"]
        self.chats[self.current_chat][-1].answer = answer_text

        yield
        self.processing = False

