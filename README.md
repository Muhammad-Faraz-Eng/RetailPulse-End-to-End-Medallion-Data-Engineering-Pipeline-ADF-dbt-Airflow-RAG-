# 🚀 RetailPulse — End-to-End Data Engineering Project

## 📌 Overview
RetailPulse is a complete, hands-on Data Engineering project designed to simulate a modern data platform. It covers the full lifecycle of data — from ingestion to analytics and AI-powered querying.

This project follows a **Medallion Architecture (Bronze → Silver → Gold)** and integrates orchestration, cloud storage, transformation tools, BI dashboards, and a Retrieval-Augmented Generation (RAG) system.

---

## 🏗️ Architecture

### High-Level Flow
```
Landing (CSV/API)
   ↓
Bronze Layer (Validation + Parquet + ADLS)
   ↓
Silver Layer (Cleaned Data - Python)
   ↓
Gold Layer (Star Schema - dbt)
   ↓
Azure SQL (Warehouse)
   ↓
Metabase (Dashboards)
   ↓
RAG (LangChain + Ollama)
```

---

## 🧱 Tech Stack

| Layer | Tools |
|------|------|
| Ingestion | Python, Config-driven YAML |
| Storage | Azure Data Lake Storage Gen2 |
| Processing | Pandas, PyArrow |
| Transformation | Python (Silver), dbt (Gold) |
| Orchestration | Apache Airflow |
| Database | Azure SQL |
| BI | Metabase |
| AI | LangChain, Ollama, ChromaDB |
| Infra | Docker |

---

## 📂 Project Structure
```
retailpulse/
├── configs/                # YAML pipeline configs
├── validation/
│   ├── bronze/             # Bronze validation + ingestion
│   ├── silver/             # Silver transformations
├── dbt/                    # dbt models (Gold layer)
├── airflow/                # DAGs
├── rag/                    # RAG pipeline
├── docker/                 # Docker setup
├── logs/                   # Logs
└── main.py
```

---

## 🥉 Bronze Layer — Raw Data Processing

### Objective
- Ingest raw data
- Validate schema
- Enforce data types
- Store clean data in Parquet

### Features
- Config-driven ingestion (YAML)
- Schema validation
- Type casting
- Quarantine for invalid data
- Partitioned storage in ADLS

### Output Structure
```
bronze/
 ├── sales/
 ├── products/
 ├── currency/
 └── quarantine/
```

---

## 🥈 Silver Layer — Data Cleaning & Transformation

### Objective
Transform raw data into structured datasets.

### Transformations
- Deduplication
- Type standardization
- Derived columns (e.g., total_amount)
- Flattening nested JSON (currency rates)

### Output
Stored in:
- Azure SQL (tables)

---

## 🥇 Gold Layer — Data Warehouse (dbt)

### Objective
Build analytics-ready models using star schema.

### Models
- `fact_sales`
- `dim_product`
- `dim_currency`
- `dim_date`

### Concepts Implemented
- Star schema
- Fact & dimension modeling
- dbt transformations

---

## 🔄 Orchestration (Airflow)

### DAG Flow
```
bronze_engine → silver_engine → dbt run
```

### Features
- Task dependency management
- Retry mechanism
- Manual trigger (learning mode)

---

## 📊 BI Layer — Metabase Dashboards

### Dashboards Built

#### 1. Sales Overview
- Total Revenue
- Total Orders
- Average Order Value
- Revenue Trend

#### 2. Product Analytics
- Revenue by category

#### 3. Store Performance
- Store-wise revenue

#### 4. Currency Insights
- Currency distribution

---

## 🤖 RAG Layer — AI Query System

### Objective
Enable natural language querying on data.

### Components
- Embeddings: Ollama
- Vector DB: ChromaDB
- LLM: Mistral
- Framework: LangChain

### Features
- Build index from data
- Ask natural language questions
- Retrieve context + generate answers

---

## ⚙️ Configuration-Driven Design

All pipelines are controlled via:
```
configs/pipeline.yaml
```

### Benefits
- No hardcoding
- Easy extensibility
- Add new data sources without code changes

---

## 🧪 How to Run

### 1. Setup Environment
```
uv venv
pip install -r requirements.txt
```

### 2. Start Docker
```
docker compose up -d
```

### 3. Run Bronze Layer
```
python -m validation.bronze.bronze_engine
```

### 4. Run Silver Layer
```
python -m validation.silver.silver_engine
```

### 5. Run dbt
```
cd dbt/retailpulse
 dbt run
```

### 6. Airflow
- Open: http://localhost:8080
- Trigger DAG: `bronze_layer_pipeline`

### 7. RAG
```
python -m rag.main
```

---

## 🧠 Key Learnings

- Medallion Architecture implementation
- Config-driven pipeline design
- Data validation & quality handling
- dbt transformations
- Airflow orchestration
- Cloud storage (ADLS)
- BI dashboarding
- RAG system integration

---

## 📈 Future Improvements

- Incremental processing
- Streaming ingestion (Kafka)
- Production-grade logging
- CI/CD pipelines
- SQL-based RAG agent

---

## 👤 Author

**Muhammad Faraz**  
Data Engineering Enthusiast

---

## ⭐ Conclusion

RetailPulse demonstrates a complete data engineering workflow combining modern tools and architectures. It serves as a strong portfolio project showcasing practical, end-to-end implementation skills.

