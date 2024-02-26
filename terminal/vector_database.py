from langchain_community.vectorstores import Chroma
from rich.console import Console

console = Console()


def get_chroma_db(embeddings, documents, path, vectorize):

    if vectorize:
        console.print("Creando CHROMA DB")
        return Chroma.from_documents(
            documents=documents, embedding=embeddings, persist_directory=path
        )
    else:
        console.print("CARGANDO CHROMA EXISTENTE")
        return Chroma(persist_directory=path, embedding_function=embeddings)
