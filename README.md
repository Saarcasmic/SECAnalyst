<p align="center">
  <img src="/logo.png" width="100" alt="Sovereign Logo"/>
</p>

<h1 align="center">SOVEREIGN</h1>

<p align="center">
  <em>AI-Powered SEC Financial Intelligence Platform</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/React-19.2.0-61DAFB?style=for-the-badge&logo=react&logoColor=white" alt="React"/>
  <img src="https://img.shields.io/badge/FastAPI-0.100+-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI"/>
  <img src="https://img.shields.io/badge/GPT--4o-Powered-412991?style=for-the-badge&logo=openai&logoColor=white" alt="OpenAI"/>
  <img src="https://img.shields.io/badge/Pinecone-Vector_DB-000000?style=for-the-badge&logo=pinecone&logoColor=white" alt="Pinecone"/>
  <img src="https://img.shields.io/badge/PostgreSQL-Ready-4169E1?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL"/>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/License-MIT-green.svg?style=flat-square" alt="License"/>
  <img src="https://img.shields.io/badge/PRs-Welcome-brightgreen.svg?style=flat-square" alt="PRs Welcome"/>
</p>

---

## 📺 Tutorial Video

<p align="center">
  <a href="#">
    <img src="https://placehold.co/800x450/1a1a2e/ffffff?text=Tutorial+Video+Coming+Soon" alt="Tutorial Video Placeholder" width="100%"/>
  </a>
</p>

<p align="center"><em>Click to watch the full walkthrough (coming soon)</em></p>

---

## 🏛️ Overview

**Sovereign** is an enterprise-grade financial intelligence platform that leverages cutting-edge AI to democratize access to SEC filings analysis. Built for analysts, researchers, and investors who demand precision, Sovereign transforms complex regulatory documents into actionable insights through natural language queries.

### The Problem

Analyzing SEC filings is traditionally:
- **Time-consuming**: 10-K reports can exceed 200 pages
- **Complex**: XBRL data requires specialized knowledge
- **Fragmented**: Data scattered across multiple sources
- **Expensive**: Professional terminals cost $20,000+/year

### The Solution

Sovereign provides:
- **Instant Answers**: Natural language queries against SEC data
- **Smart Metrics**: Automatic extraction of financial KPIs
- **Risk Analysis**: RAG-powered qualitative insights
- **Visual Analytics**: Interactive comparison charts
- **BYOK Security**: Your API keys, your control

---

## ✨ Features

### 🧠 Intelligent Query Processing

```
"What was Google's revenue in 2023?"
     ↓
┌─────────────────────────────────────────────────────────────────┐
│  1. Entity Resolution    │  Google → GOOGL (Alphabet Inc.)     │
│  2. Query Classification │  Type: metric, Year: 2023           │
│  3. Data Retrieval       │  SEC EDGAR API → XBRL Parsing       │
│  4. Response Generation  │  $307.394 Billion (10-K Filing)     │
└─────────────────────────────────────────────────────────────────┘
```

### 📊 Multi-Modal Response Types

| Query Type | Example | Response |
|------------|---------|----------|
| **Metric** | "Apple's net income 2023" | Precise numerical data with source |
| **RAG** | "What are Tesla's risk factors?" | AI-synthesized analysis from filings |
| **Comparison** | "Compare AAPL vs MSFT revenue" | Interactive multi-year charts |

### 🛡️ Enterprise Security

- **BYOK (Bring Your Own Key)**: OpenAI API keys never stored server-side
- **Input Guardrails**: LLM-powered content filtering
- **Hybrid Authentication**: User keys for AI, server keys for infrastructure

### 🎨 Premium User Experience

- **Holographic UI**: Glass-morphism design with WebGL backgrounds
- **Real-time Streaming**: Token-by-token response rendering
- **Thinking Visualization**: Transparent AI reasoning process
- **Responsive Design**: Seamless mobile-to-desktop experience

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              SOVEREIGN ARCHITECTURE                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐     │
│  │   React Frontend │────▶│   FastAPI Server │────▶│   SEC EDGAR API  │     │
│  │   (Vite + TW)    │     │   (Uvicorn)      │     │   (data.sec.gov) │     │
│  └──────────────────┘     └────────┬─────────┘     └──────────────────┘     │
│           │                        │                                         │
│           │                        ▼                                         │
│           │               ┌──────────────────┐                               │
│           │               │   Orchestrator   │                               │
│           │               │  ┌────────────┐  │                               │
│           │               │  │ Classifier │  │──────┐                        │
│           │               │  └────────────┘  │      │                        │
│           │               │  ┌────────────┐  │      ▼                        │
│           │               │  │ Guardrails │  │  ┌──────────┐                 │
│           │               │  └────────────┘  │  │  OpenAI  │                 │
│           │               │  ┌────────────┐  │  │  GPT-4o  │                 │
│           │               │  │ RAG Engine │  │──┴──────────┘                 │
│           │               │  └────────────┘  │                               │
│           │               └────────┬─────────┘                               │
│           │                        │                                         │
│           ▼                        ▼                                         │
│  ┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐     │
│  │  localStorage    │     │   PostgreSQL     │     │     Pinecone     │     │
│  │  (API Keys)      │     │   (Supabase)     │     │   (Vector DB)    │     │
│  └──────────────────┘     └──────────────────┘     └──────────────────┘     │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

### Backend
| Technology | Purpose |
|------------|---------|
| **FastAPI** | Async REST API with streaming support |
| **SQLAlchemy** | ORM with PostgreSQL/SQLite flexibility |
| **LangChain** | LLM orchestration and prompt management |
| **Pinecone** | Serverless vector search (1536-dim embeddings) |
| **OpenAI GPT-4o** | Query classification, RAG synthesis |
| **BeautifulSoup** | SEC filing HTML/XML parsing |

### Frontend
| Technology | Purpose |
|------------|---------|
| **React 19** | UI framework with latest features |
| **Vite** | Next-gen build tooling |
| **Tailwind CSS** | Utility-first styling |
| **Framer Motion** | Production-ready animations |
| **Three.js** | WebGL 3D background effects |
| **Recharts** | Financial data visualization |
| **React Markdown** | Rich text rendering |

### Infrastructure
| Technology | Purpose |
|------------|---------|
| **Supabase** | Managed PostgreSQL + Auth |
| **Pinecone** | Managed vector database |
| **Uvicorn** | ASGI server |

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- OpenAI API Key
- Pinecone API Key
- PostgreSQL (or use SQLite for development)

### 1️⃣ Clone Repository

```bash
git clone https://github.com/yourusername/sovereign.git
cd sovereign
```

### 2️⃣ Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your keys:
# - DATABASE_URL (PostgreSQL connection string)
# - PINECONE_API_KEY
# - USER_AGENT (for SEC API)

# Initialize database
python init_db.py

# Start server
python run_server.py
```

### 3️⃣ Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

### 4️⃣ Access Application

Open [http://localhost:5173](http://localhost:5173) in your browser.

> **Note**: On first query, you'll be prompted to enter your OpenAI API key. This is stored locally in your browser and never sent to our servers.

---

## 📁 Project Structure

```
sovereign/
├── backend/
│   ├── main.py              # FastAPI application entry
│   ├── orchestrator.py      # Central query routing engine
│   ├── agents.py            # QueryClassifier + AnalysisAgent
│   ├── guardrail.py         # LLM-based input filtering
│   ├── vector_store.py      # Pinecone integration
│   ├── repository.py        # Financial data repository
│   ├── retriever.py         # SEC EDGAR API client
│   ├── processor.py         # Filing text extraction
│   ├── database.py          # SQLAlchemy configuration
│   ├── models.py            # Company + FinancialMetric models
│   ├── init_db.py           # Database seeding script
│   └── requirements.txt     # Python dependencies
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── ChatInterface.jsx    # Main chat component
│   │   ├── FinancialChart.jsx   # Recharts wrapper
│   │   └── components/
│   │       ├── ApiKeyModal.jsx  # BYOK modal
│   │       ├── BackgroundWave.jsx
│   │       └── ui/              # Reusable UI primitives
│   ├── index.html
│   ├── tailwind.config.js
│   └── package.json
│
└── README.md
```

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the `backend/` directory:

```env
# Database (PostgreSQL recommended for production)
DATABASE_URL=postgresql://user:password@host:5432/dbname

# SEC EDGAR API (Required)
USER_AGENT=YourName contact@email.com

# Pinecone Vector Database
PINECONE_API_KEY=your_pinecone_key

# OpenAI (Optional - users provide via BYOK)
OPENAI_API_KEY=your_openai_key
```

### Supported Companies

Sovereign comes pre-configured with major tech companies:

| Ticker | Company | CIK |
|--------|---------|-----|
| AAPL | Apple Inc. | 0000320193 |
| MSFT | Microsoft Corp | 0000789019 |
| GOOGL | Alphabet Inc. | 0001652044 |
| AMZN | Amazon.com Inc. | 0001018724 |
| NVDA | NVIDIA Corp | 0001045810 |
| TSLA | Tesla Inc. | 0001318605 |
| META | Meta Platforms Inc. | 0001326801 |

---

## 📖 API Reference

### POST `/chat`

Stream financial intelligence responses.

**Headers:**
```
Authorization: Bearer <openai_api_key>
Content-Type: application/json
```

**Request Body:**
```json
{
  "query": "What was Apple's revenue in 2023?"
}
```

**Response (SSE Stream):**
```
{"type": "log", "message": "Analyzing query..."}
{"type": "log", "message": "Intent detected: metric"}
{"type": "log", "message": "Fetching from SEC EDGAR API..."}
{"type": "result", "data": "$383,285,000,000 (Fetched)"}
```

### GET `/health`

Health check endpoint.

**Response:**
```json
{
  "status": "healthy"
}
```

---

## 🧪 Example Queries

### Metric Queries
```
"What was Apple's revenue in 2023?"
"Show me Tesla's net income for 2022"
"Google's total assets last year"
```

### RAG Queries
```
"What are the main risk factors for NVIDIA?"
"Summarize Microsoft's business strategy"
"Explain Apple's supply chain risks"
```

### Comparison Queries
```
"Compare AAPL and MSFT revenue over the last 3 years"
"Chart Tesla vs NVIDIA performance"
```

---

## 🔒 Security

### BYOK (Bring Your Own Key)

Sovereign implements a **Hybrid Auth** model:

| Component | Key Source | Storage |
|-----------|------------|---------|
| OpenAI API | User-provided | Browser localStorage |
| Pinecone | Server-side | Environment variable |
| PostgreSQL | Server-side | Environment variable |

This ensures:
- ✅ Users control their AI costs
- ✅ No API key exposure to third parties
- ✅ Infrastructure keys remain secure

### Input Guardrails

All queries pass through an LLM-powered guardrail that filters:
- Off-topic requests (cooking, politics, etc.)
- Potentially harmful content
- Non-financial queries

---

## 🚢 Deployment

### Render / Railway

1. Create PostgreSQL database
2. Deploy backend with environment variables
3. Deploy frontend with `VITE_API_URL`

### Supabase + Vercel

1. Create Supabase project (PostgreSQL)
2. Deploy backend to Railway/Render
3. Deploy frontend to Vercel

### Docker (Coming Soon)

```bash
docker-compose up -d
```

---

## 🤝 Contributing

Contributions are welcome! Please read our contributing guidelines before submitting PRs.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [SEC EDGAR](https://www.sec.gov/edgar) for public financial data
- [OpenAI](https://openai.com) for GPT-4o
- [Pinecone](https://pinecone.io) for vector search
- [Supabase](https://supabase.com) for PostgreSQL hosting

---

<p align="center">
  <strong>Built with ❤️ for the financial community</strong>
</p>

<p align="center">
  <a href="#">Website</a> •
  <a href="#">Documentation</a> •
  <a href="#">Twitter</a> •
  <a href="#">Discord</a>
</p>
