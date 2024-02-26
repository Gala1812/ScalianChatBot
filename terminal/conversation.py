from rich.console import Console
from interactions import process_memory_query, get_query_from_user

console = Console()


def run_conversation(vectorstore, llm):

    console.print("\n[blue]IA:[/blue] Hola 🚀! Qué quieres preguntarme sobre Scalian?")
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    chat_history = []

    while True:
        console.print("\n[blue]Tú:[/blue]")
        query = get_query_from_user()

        if query.lower() == "salir":
            break
        response = process_memory_query(
            query=query, retriever=retriever, llm=llm, chat_history=chat_history
        )
        # response = process_memory_query()
        console.print(f"[red]IA:[/red] {response}")
