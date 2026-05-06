# RAG UI Setup and Running Instructions

## Running the RAG UI

### Prerequisites
1. Make sure Ollama is running with the `mistral` model available
2. Ensure your database credentials are set in `.env` file or environment variables
3. Install dependencies: `uv pip install streamlit`

### Start the UI

Run the following command from the project root:

```bash
streamlit run rag/ui/app.py
```

The UI will open in your default browser at `http://localhost:8501`

### Features

#### 1. **Index Management** (Sidebar)
- **Build Index**: Creates vector embeddings from your database
  - Extracts data from: `fact_sales`, `dim_product`, `dim_currency`
  - Stores embeddings in Chroma vector database
- **Refresh QA Chain**: Reloads the language model chain

#### 2. **Chat Settings** (Sidebar)
- Model selection (currently: Mistral via Ollama)
- Temperature adjustment for response creativity

#### 3. **Question Answering** (Main Area)
- Interactive chat interface
- Conversational history
- Real-time response generation
- Conversation clearing

### Workflow

1. Click **"Build Index"** in the sidebar (first time only, or when data changes)
2. Wait for the vector index to be created
3. Once ready, type your question in the input field
4. Click **"Ask"** or press Enter
5. View the AI-generated answer based on your data
6. Continue the conversation

### Example Questions

- "What were the total sales last month?"
- "Which products had the highest demand?"
- "How many currency rates are in the system?"
- "Show me sales trends by store"

### Troubleshooting

**Error: "Cannot connect to Ollama"**
- Make sure Ollama is running: `ollama serve`
- Verify Mistral model is available: `ollama list`

**Error: "Database connection failed"**
- Check your `.env` file has correct database credentials
- Ensure Azure SQL Server is accessible

**Index not building**
- Verify database queries are correct in `rag/ingestion/index_builder.py`
- Check database contains the required tables

### Architecture

```
rag/
├── ui/
│   ├── app.py           # Streamlit UI application
│   └── __init__.py
├── ingestion/
│   └── index_builder.py # Vector index creation
├── retriever/
│   └── retriever.py     # Vector search
├── chains/
│   └── qa_chain.py      # QA chain with LLM
└── main.py              # Original CLI interface
```

### Performance Notes

- First index build may take several minutes depending on data size
- Subsequent queries should be fast (< 5 seconds typically)
- Adjust temperature in settings to control response variations
