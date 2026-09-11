from src.ingestion.youtube_loader import get_full_transcript
from src.ingestion.text_splitters import split_text
from src.embeddings.hf_embeddings import get_embedding_model
from src.vectorstore.chroma_store import create_vector_store
from src.retrieval.retriever import get_retriever
from src.llm.gemini_llm import GeminiModel


def run_rag_pipeline(video_url):

    text = get_full_transcript(video_url)

    chunks = split_text(text)

    embedding_model = get_embedding_model()

    vectordb = create_vector_store(chunks, embedding_model)

    retriever = get_retriever(vectordb)

    llm = GeminiModel()

    return retriever, llm


def generate_answer(query, retriever, llm):

    docs = retriever.invoke(query)

    context = "\n".join([doc.page_content for doc in docs])

    prompt = f"""
    Answer ONLY from the context and write the answer in English.
    Translate relevant information from the context into English when necessary.

    Context:
    {context}

    Question:
    {query}
    """

    return llm.generate(prompt)