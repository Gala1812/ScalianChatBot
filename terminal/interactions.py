from rich.console import Console
from langchain.chains import ConversationalRetrievalChain

console = Console()


# def process_memory_query():
#     return "proceso de memoria"


def process_memory_query(query, retriever, llm, chat_history):
    conversation = ConversationalRetrievalChain.from_llm(
        llm=llm, retriever=retriever, verbose=True
    )
    console.print("[yellow]La IA está pensando...[/yellow]")
    print(f"La historia antes de esta respuesta es: {chat_history}")
    result = conversation({"question": query, "chat_history": chat_history})
    chat_history.append((query, result["answer"]))
    return result["answer"]


def get_query_from_user() -> str:
    """
    Solicita una consulta al usuario.

    Returns:
        La consulta ingresada por el usuario.
    """
    try:
        query = input()
        return query
    except EOFError:
        print("Error: Input no esperado. Por favor intenta de nuevo.")
        return get_query_from_user()
