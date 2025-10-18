/**
# System Architecture

## Overview

The AI Debate System follows a microservices architecture with clear separation of concerns.

## Components

### 1. Frontend Layer
- **Technology**: React 18, Vite, TailwindCSS
- **Responsibilities**:
  - User interface and interactions
  - Real-time WebSocket connections
  - State management
  - API communication

### 2. API Layer
- **Technology**: FastAPI, Python 3.11
- **Responsibilities**:
  - HTTP REST endpoints
  - WebSocket management
  - Request validation
  - Authentication/Authorization
  - Rate limiting

### 3. Agent Layer
- **Technology**: Custom Python agents
- **Agents**:
  1. **Keyword Extractor**: NLP-based keyword extraction
  2. **Argument Generator**: LLM-powered argument creation
  3. **Counter-Argument Generator**: Strategic rebuttal generation
  4. **Evaluation Agent**: Multi-criteria argument assessment

- **Communication Protocol**: Model Context Protocol (MCP)
  - Asynchronous message passing
  - Correlation IDs for tracking
  - State management per agent

### 4. Service Layer
- **LLM Service**: OpenAI/Anthropic integration
- **Information Retrieval**: Vector-based search (ChromaDB)
- **Web Scraper**: BeautifulSoup, httpx
- **Document Processor**: PDF, DOCX parsing

### 5. Data Layer
- **PostgreSQL**: Persistent storage
- **Redis**: Caching and sessions
- **ChromaDB**: Vector embeddings

## Data Flow

1. User submits argument → Frontend
2. Frontend → API Gateway → Input Validation
3. API → Agent Coordinator
4. Coordinator → Keyword Extractor Agent
5. Extractor → Counter-Argument Agent
6. Counter-Argument Agent → LLM Service → IR Service
7. All results → Evaluation Agent
8. Evaluation → API → Frontend
9. Frontend renders response

## Security Architecture

- **Authentication**: JWT tokens
- **Authorization**: Role-based access control
- **Rate Limiting**: Token bucket per user/IP
- **Input Sanitization**: XSS prevention
- **Content Filtering**: Harmful content detection
- **HTTPS**: TLS 1.3 in production

## Scalability Considerations

- Horizontal scaling via containerization
- Load balancing with Nginx
- Caching layer with Redis
- Async processing with Celery
- Database connection pooling
- Vector store sharding

## Monitoring & Logging

- **Logging**: Structured JSON logs
- **Metrics**: Prometheus + Grafana
- **Tracing**: OpenTelemetry
- **Alerting**: PagerDuty integration
*/