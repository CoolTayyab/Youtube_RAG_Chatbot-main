from langchain_chroma import Chroma

def create_vector_store(chunks, embedding_model, persist_dir="db"):
    vectordb = Chroma.from_texts(
        texts=chunks,
        embedding=embedding_model,
        persist_directory=persist_dir
    )
    return vectordb