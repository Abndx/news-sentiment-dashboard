
 # 📰 AWS Serverless Real-Time News Sentiment Pipeline & Dashboard

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg?style=flat-square&logo=python)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-FF4B4B.svg?style=flat-square&logo=streamlit)](https://streamlit.io/)
[![AWS](https://img.shields.io/badge/Cloud-AWS-232F3E.svg?style=flat-square&logo=amazon-aws)](https://aws.amazon.com/)
[![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-4169E1.svg?style=flat-square&logo=postgresql)](https://www.postgresql.org/)

An end-to-end serverless data engineering pipeline that automatically streams live news feeds, performs real-time Natural Language Processing (NLP) sentiment scoring, stores transactional records in a cloud data warehouse, and hosts an interactive web visualization platform.

---

## 🏗️ Architecture Overview

The pipeline leverages a modern decoupled architecture where backend data ingestion, text processing, database storage, and frontend presentation function independently.             
              

               
              ┌──────────────────────────────┐
              │   AWS EventBridge (Cron)     │
              └──────────────┬───────────────┘
                             │ Triggers
                             ▼
              ┌──────────────────────────────┐
              │    AWS Lambda (Ingestion)     │ ◄── [ get_layer.py ]
              └──────────────┬───────────────┘
                             │ Extracts, Computes Sentiment (NLTK)
                             ▼
              ┌──────────────────────────────┐
              │    AWS RDS (PostgreSQL)      │ ◄── [ maintenance scripts ]
              └──────────────┬───────────────┘
                             │ Real-time Queries
                             ▼
              ┌──────────────────────────────┐
              │   Streamlit Community Cloud  │
              └──────────────────────────────┘



### 🛰️ Data Lifecycle & Tech Stack
1. **Ingestion Scheduling:** **AWS EventBridge** triggers a serverless handler function at pre-set cron intervals.
2. **Compute & NLP Extraction:** **AWS Lambda** fetches target RSS feeds, isolates headlines/summaries, and computes polarity scores utilizing the **NLTK (VADER)** engine.
3. **Relational Storage:** Processed JSON objects are structured and committed to a highly available **AWS RDS PostgreSQL** instance.
4. **Presentation Layer:** A live **Streamlit Community Cloud** dashboard connects directly to the RDS layer to render key operational metrics, moving averages, and data tables.

---

## 📂 Project Structure & Developer Toolkit

This workspace is cleanly split into frontend application code and a dedicated backend maintenance suite.

### 🎛️ Core Application
* **`app.py`** – The application entrance point. Manages secure database connection pools, fetches transactional real-time data, and builds the visual interface blocks.
* **`requirements.txt`** – The cloud-native manifest declaring every Python package dependency required to construct the runtime container.

### 🛠️ Custom Maintenance Suite
Managing cloud-based databases and serverless architectures requires automated workflows. This repository includes specialized developer scripts to control the complete ecosystem layout:

> 🧼 **`wipe_old_data.py` — The Lifecycle Cleaner**
> Automatically handles data pruning on AWS RDS by clearing out items past a specific expiration window. This controls table indexing sizes, avoids storage optimization blockages, and enforces predictable cost ceilings.

> 🩺 **`fix_db.py` — The Schema Migration Tool**
> Modifies operational live tables gracefully using targeted DDL executions. Allows you to inject columns, alter constraint keys, or change column types without destroying your historic production data.

> 🚨 **`nuclear_reset.py` — The System Purge Switch**
> Drops the primary production schema completely and rebuilds clean, normalized relational tables from scratch. Crucial during development phases to eliminate corrupted records or test schema rewrites instantly.

> 📦 **`get_layer.py` — The Cloud Lambda Packer**
> AWS Lambda has strict deployment package limits. This script auto-compiles heavy dependencies (such as `nltk`) and builds a cleanly structured `.zip` archive to be uploaded as an AWS Lambda Layer.

### 🔒 Security Guards
* **`.gitignore`** – Prevents local testing footprints (`__pycache__/`, `venv/`) and local vault credentials from slipping into public source control history.

---

## 🔐 Advanced Credential Strategy

The repository follows production-grade security patterns to protect cloud resources across multiple runtime environments.

### Local Development Flow (`.env`)
When executed locally, `app.py` sources your database host, port, and security keys using a standalone `.env` file that stays hidden on your machine.

### Cloud Deployment Flow (`Streamlit Secrets`)
In production, your `.env` file is left out entirely. Instead, the application taps into an encrypted cloud secrets manager via `st.secrets`. 

The codebase automatically manages this switchover under the hood:
```python
DB_HOST = st.secrets.get("DB_HOST", os.environ.get("DB_HOST"))
