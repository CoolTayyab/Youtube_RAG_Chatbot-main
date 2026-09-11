try:
    import streamlit as st
except ImportError as error:
    raise RuntimeError(
        "Streamlit is required to run this app. Install it with: pip install streamlit"
    ) from error
from src.pipeline.rag_pipeline import run_rag_pipeline, generate_answer

st.set_page_config(page_title="YouTube RAG Chatbot")
st.title("🎥 TubeTalks")

if "retriever" not in st.session_state:
    st.session_state.retriever = None
    st.session_state.llm = None

video_url = st.text_input("Enter YouTube URL")

if st.button("Process Video"):
    if not video_url.strip():
        st.error("Please enter a YouTube URL.")
    else:
        try:
            with st.spinner("Processing..."):
                retriever, llm = run_rag_pipeline(video_url)

            st.session_state.retriever = retriever
            st.session_state.llm = llm
            st.success("Video processed successfully!")

        except Exception as error:
            st.error(f"Could not process video: {error}")

query = st.text_input("Ask a question")

if st.button("Ask"):
    if st.session_state.retriever is None:
        st.warning("Please process a video first.")
    elif not query.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Thinking..."):
            answer = generate_answer(
                query,
                st.session_state.retriever,
                st.session_state.llm
            )
            st.write("### 🤖 Answer")
            st.write(answer)