# AI Debate System

A multi-agent AI system for conducting structured debates with humans.
This is made by integrating LLMs, NLP, Information Retrieval, and security features.
Main Purpose: to provide support and practice sessions for debators on any topic they want.

## 🎯 Features

- **Multi-Agent Architecture**: 4 specialized agents working collaboratively
  - Keyword Extractor Agent
  - Argument Generator Agent
  - Counter-Argument Generator Agent
  - Evaluation Agent

- **Capabilities**:
  - Real-time debate with AI
  - Document upload and processing (PDF, DOCX, TXT)
  - Web scraping for topic research
  - Vector-based information retrieval
  - Argument evaluation and scoring
  - Model Context Protocol (MCP) for agent communication

- **Security & Responsible AI**:
  - JWT authentication
  - Rate limiting
  - Input validation and sanitization
  - Content filtering
  - CORS protection

## 🏗️ Architecture

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│   Frontend  │─────▶│   API Layer  │─────▶│   Agents    │
│   (React)   │      │   (FastAPI)  │      │  (Agentic)  │
└─────────────┘      └──────────────┘      └─────────────┘
                            │
                     ┌──────┴──────┐
                     │             │
              ┌──────▼────┐  ┌────▼──────┐
              │   Vector  │  │    LLM    │
              │   Store   │  │  Service  │
              └───────────┘  └───────────┘
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- Docker & Docker Compose (optional)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/Tanury/ai-debate-system.git
cd ai-debate-system
```

2. **Backend Setup**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Download NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys

# Run migrations (if using database)
alembic upgrade head

# Start backend
uvicorn app.main:app --reload
```

3. **Frontend Setup**
```bash
cd frontend
npm install
npm run dev
```

### Using Docker

```bash
# Copy environment file
cp backend/.env.example backend/.env
# Add your API keys to backend/.env

# Build and run
docker-compose up --build

# Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

## Instructions to use the system: 

### Starting a Debate

1. Enter a debate topic (e.g., "Renewable energy should be prioritized over fossil fuels")
2. Click "Start Debate"
3. Present your opening argument
4. The AI will analyze your argument and provide a counter-argument
5. Continue debating until someone admits defeat

### Uploading Documents

1. Click "Upload Docs"
2. Select PDF, DOCX, or TXT files
3. Documents are processed and added to the knowledge base
4. The AI will use this information in arguments

### Web Scraping

1. Click "Web Scrape"
2. The system scrapes relevant articles on the debate topic
3. Information is added to the knowledge base

## 🏢 Commercialization Strategy

### Pricing Model

#### Freemium Tier
- 10 debates per month
- Basic AI responses
- Limited document uploads (5 docs)
- Community support

**Price**: Free

#### Professional Tier
- Unlimited debates
- Advanced AI with GPT-4/Claude
- Unlimited document uploads
- Web scraping (50 pages/month)
- Priority support
- Export debate transcripts

**Price**: $29/month or $290/year (save 17%)

#### Enterprise Tier
- Everything in Professional
- Custom AI model fine-tuning
- API access
- White-label option
- Dedicated support
- SSO integration
- Custom integrations

**Price**: Custom (starting at $299/month)

### Target Markets

1. **Education**: Schools, universities, debate clubs
2. **Legal**: Law firms for case preparation
3. **Corporate**: Training and decision-making
4. **Research**: Academic research and analysis
5. **Content Creation**: Writers and journalists

### Revenue Projections

**Year 1**: 
- 1,000 free users
- 100 professional subscribers ($2,900/month)
- 5 enterprise clients ($1,495/month)
- **Monthly Recurring Revenue**: $4,395
- **Annual Revenue**: ~$53,000

**Year 2**:
- 5,000 free users
- 500 professional subscribers ($14,500/month)
- 20 enterprise clients ($5,980/month)
- **Monthly Recurring Revenue**: $20,480
- **Annual Revenue**: ~$246,000

**Year 3**:
- 20,000 free users
- 2,000 professional subscribers ($58,000/month)
- 50 enterprise clients ($14,950/month)
- **Monthly Recurring Revenue**: $72,950
- **Annual Revenue**: ~$875,000

## 🧪 Testing

```bash
cd backend
pytest tests/ -v --cov=app
```

## 📚 API Documentation

Access interactive API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🔒 Security Features

- **Authentication**: JWT-based auth system
- **Rate Limiting**: Token bucket algorithm
- **Input Validation**: XSS and injection prevention
- **Content Filtering**: Harmful content detection
- **HTTPS**: SSL/TLS encryption (production)
- **CORS**: Configurable origin whitelisting

## 🤝 Responsible AI Practices

- Content moderation for harmful content
- Transparent evaluation criteria
- User data privacy protection
- Bias mitigation in LLM responses
- Ethical use guidelines
- Accessibility features

## 📄 License

MIT License 

*/

