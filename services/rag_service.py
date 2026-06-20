from storage.vector_store import get_vector_store
from services.llm_service import get_llm
from services.memory_service import add_message, get_history
from config import TOP_K

def ask(question):

    vectordb = get_vector_store()
    retriever = vectordb.as_retriever(search_kwargs={"k": TOP_K})

    docs = retriever.invoke(question)
    context = "\n\n".join([d.page_content for d in docs])

    history = "\n".join(
        [f"{m['role']}: {m['content']}" for m in get_history()]
    )

    prompt = f"""
    Chat history:
    {history}

    Context:
    {context}

    User question:
    {question}
    """

    llm = get_llm()
    response = llm.invoke(prompt).content

    add_message("user", question)
    add_message("assistant", response)

    return response
