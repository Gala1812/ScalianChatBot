from rich.console import Console
from utils import get_openai_api_key
from text_processing import load_documents
from dotenv import load_dotenv
import os
from langchain_openai import OpenAIEmbeddings
from vector_database import get_chroma_db
from langchain_openai import ChatOpenAI
from conversation import run_conversation


load_dotenv()
data_path = os.getenv("DATA")
data_path = "dataprueba"
recreate_chroma_db = False


def main():
    console = Console()
    # console.clear()
    console.print("\n[blue]Informacion:[/blue] iniciando la ejecucion")
    get_openai_api_key()
    data = load_documents(data_path)
    # embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
    vectorstore_chroma = get_chroma_db(
        embeddings, data, "chroma_docs", recreate_chroma_db
    )
    llm = ChatOpenAI(
        model_name="gpt-3.5-turbo",
        temperature=0.2,
        max_tokens=1000,
    )
    run_conversation(vectorstore_chroma, llm)


if __name__ == "__main__":
    main()
