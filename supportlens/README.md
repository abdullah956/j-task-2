# SupportLens

SupportLens is a real-time support conversation analytics platform that automatically classifies customer support interactions and provides insights through an interactive dashboard.

## Architecture

The application consists of three main components:

### 1. **Backend (FastAPI + PostgreSQL)**
- RESTful API built with FastAPI
- Async SQLAlchemy for database operations
- Groq LLM integration for:
  - AI-powered chatbot responses
  - Automatic conversation classification into 5 categories (Billing, Refund, Account Access, Cancellation, General Inquiry)
- Provides analytics endpoints for dashboard insights

### 2. **Frontend (React + Vite + Tailwind)**
- Interactive chatbot interface for testing support conversations
- Real-time analytics dashboard with:
  - Key metrics cards (total conversations, avg response time, top category)
  - Category distribution chart using Recharts
  - Filterable conversation table
  - Detailed conversation modal view
- Auto-polling every 5 seconds for live updates

### 3. **Database (PostgreSQL)**
- Stores all conversation traces with timestamps, categories, and response times
- Seeded with 20 realistic support conversations on startup

## Prerequisites

- Docker and Docker Compose installed
- A Groq API key (get one free at https://console.groq.com/)

## Setup

1. **Clone the repository:**
   ```bash
   cd supportlens
   ```

2. **Configure environment variables:**
   ```bash
   cp .env.example .env
   ```

3. **Add your Groq API key to `.env`:**
   ```
   DATABASE_URL=postgresql+asyncpg://postgres:postgres@postgres:5432/supportlens
   GROQ_API_KEY=your_actual_groq_api_key_here
   ```

4. **Run the application:**
   ```bash
   docker-compose up --build
   ```

   This single command will:
   - Start PostgreSQL database
   - Build and run the FastAPI backend
   - Build and run the React frontend
   - Auto-seed the database with sample conversations

## Access Points

Once running, access the application at:

- **Frontend (Chat + Dashboard):** http://localhost:5173
- **Backend API:** http://localhost:8000
- **API Documentation (Swagger):** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health

## Usage

1. **Test the Chatbot:**
   - Open http://localhost:5173
   - Use the left panel to chat with the AI support agent
   - Ask questions about billing, refunds, account access, etc.
   - Each conversation is automatically classified and saved

2. **View Analytics:**
   - The right panel shows real-time analytics
   - Filter conversations by category
   - Click on any conversation to view full details
   - Watch metrics update automatically as you chat

## Features

- ✅ AI-powered chatbot using Groq LLM (Llama 3.1)
- ✅ Automatic conversation classification (5 categories)
- ✅ Real-time analytics dashboard
- ✅ Response time tracking
- ✅ Category-based filtering
- ✅ Auto-polling for live updates
- ✅ Conversation history with detailed view
- ✅ Pre-seeded with realistic sample data

## Technology Stack

**Backend:**
- FastAPI
- SQLAlchemy (async)
- PostgreSQL
- Groq Python SDK
- Pydantic

**Frontend:**
- React 18
- Vite
- Tailwind CSS
- Recharts
- Axios

**Infrastructure:**
- Docker
- Docker Compose

## API Endpoints

- `POST /api/chat` - Chat with the support bot
- `POST /api/traces` - Save conversation trace
- `GET /api/traces` - Get all traces (optional category filter)
- `GET /api/analytics` - Get analytics summary
- `GET /health` - Health check

## Development

To run locally without Docker:

**Backend:**
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

Make sure PostgreSQL is running and `.env` is configured correctly.

## License

MIT
