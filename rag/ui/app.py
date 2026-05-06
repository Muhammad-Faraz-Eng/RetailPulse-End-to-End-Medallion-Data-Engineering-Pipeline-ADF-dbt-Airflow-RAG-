import streamlit as st
import sys
import os
from pathlib import Path

# Add parent directory to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from rag.ingestion.index_builder import build_index
from rag.chains.qa_chain import build_qa_chain


def init_session_state():
    """Initialize session state variables."""
    if "qa_chain" not in st.session_state:
        st.session_state.qa_chain = None
    if "index_built" not in st.session_state:
        st.session_state.index_built = False
    if "messages" not in st.session_state:
        st.session_state.messages = []


def load_qa_chain():
    """Load the QA chain."""
    if st.session_state.qa_chain is None:
        with st.spinner("Loading QA chain..."):
            st.session_state.qa_chain = build_qa_chain()
    return st.session_state.qa_chain


def main():
    """Main Streamlit app."""
    st.set_page_config(
        page_title="RetailPulse RAG System",
        page_icon="🔍",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    init_session_state()

    # Header
    st.title("🔍 RetailPulse RAG System")
    st.markdown(
        "Ask questions about your retail data using AI-powered retrieval and generation."
    )

    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")

        tab1, tab2 = st.tabs(["Index Management", "Chat Settings"])

        with tab1:
            st.subheader("Vector Index")

            col1, col2 = st.columns(2)

            with col1:
                if st.button("🔨 Build Index", use_container_width=True):
                    try:
                        with st.spinner("Building vector index from database..."):
                            build_index()
                            st.session_state.index_built = True
                            st.success(
                                "✅ Vector index built successfully! You can now ask questions."
                            )
                    except Exception as e:
                        st.error(f"❌ Error building index: {str(e)}")

            with col2:
                if st.button("🔄 Refresh QA Chain", use_container_width=True):
                    st.session_state.qa_chain = None
                    st.success("QA chain refreshed!")

            status_col1, status_col2 = st.columns(2)
            with status_col1:
                if st.session_state.index_built:
                    st.info("✅ Index: Ready")
                else:
                    st.warning("⚠️ Index: Not built")

            with status_col2:
                if st.session_state.qa_chain is not None:
                    st.info("✅ QA Chain: Loaded")
                else:
                    st.warning("⚠️ QA Chain: Not loaded")

        with tab2:
            st.subheader("Model Settings")
            model_name = st.selectbox(
                "Select Model",
                options=["mistral"],
                help="The Ollama model to use for answering questions",
            )
            st.info(f"Currently using: **{model_name}** model via Ollama")

            temperature = st.slider(
                "Response Temperature",
                min_value=0.0,
                max_value=1.0,
                value=0.7,
                step=0.1,
                help="Higher values make responses more creative",
            )

    # Main content area
    if not st.session_state.index_built:
        st.warning(
            "📌 **Please build the vector index first.** Click 'Build Index' in the sidebar to get started."
        )
        st.info(
            "The index will extract data from your database and create vector embeddings for semantic search."
        )
    else:
        # Chat interface
        st.subheader("💬 Ask Questions About Your Data")

        # Load QA chain
        qa_chain = load_qa_chain()

        # Chat input
        user_query = st.text_input(
            "Your question:",
            placeholder="e.g., What were the total sales last month? Which products had the highest demand?",
            key="user_input",
        )

        col1, col2 = st.columns([4, 1])

        with col2:
            submit_button = st.button("🚀 Ask", use_container_width=True)

        # Process query
        if submit_button and user_query:
            # Add user message to history
            st.session_state.messages.append({"role": "user", "content": user_query})

            # Generate response
            with st.spinner("Thinking..."):
                try:
                    response = qa_chain.run(user_query)

                    # Add assistant message to history
                    st.session_state.messages.append(
                        {"role": "assistant", "content": response}
                    )

                except Exception as e:
                    st.error(f"❌ Error generating response: {str(e)}")

        # Display chat history
        if st.session_state.messages:
            st.subheader("📚 Conversation History")

            for i, message in enumerate(st.session_state.messages):
                if message["role"] == "user":
                    with st.chat_message("user", avatar="🧑"):
                        st.markdown(message["content"])
                else:
                    with st.chat_message("assistant", avatar="🤖"):
                        st.markdown(message["content"])

            # Clear history button
            if st.button("🗑️ Clear Conversation", use_container_width=True):
                st.session_state.messages = []
                st.rerun()

        # Additional info
        with st.expander("ℹ️ About This System"):
            st.markdown(
                """
                **RetailPulse RAG (Retrieval-Augmented Generation)** uses:
                - **Vector Database**: Chroma for semantic search
                - **Embeddings**: Ollama's Mistral model
                - **LLM**: Ollama for natural language generation
                - **Framework**: LangChain for orchestration

                ### How it works:
                1. **Index Building**: Extracts data from your database and creates vector embeddings
                2. **Query Processing**: When you ask a question, it searches for relevant data using semantic similarity
                3. **Generation**: An LLM uses the retrieved context to generate a natural language answer

                ### Tips:
                - Ask specific questions for better results
                - The system retrieves the 5 most relevant documents
                - Questions work best when they match data in your database
                """
            )


if __name__ == "__main__":
    main()
