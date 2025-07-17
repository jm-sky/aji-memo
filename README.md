# 🧠 Aji-Memo – External AI Memory via REST API (GET)

**Aji-Memo** is an external contextual memory system that can be used by language models (e.g., ChatGPT) through simple HTTP `GET` requests. This allows LLMs to save and retrieve information in an external system without needing complex integrations (e.g., plugins or function calling).

---

## 🎯 Project Goals & Purpose

### Why Aji-Memo?
- **Simplicity First**: AI models can access memory using simple GET requests - no complex APIs or authentication flows
- **Persistent Context**: Store and retrieve contextual information across conversations and sessions
- **Scalable Architecture**: Support multiple AI users, namespaces, and organizations
- **Full-text Search**: Advanced search capabilities with PostgreSQL's powerful FTS engine
- **Tag-based Organization**: Categorize and filter memories using flexible tagging system

### Key Benefits
- **No Plugin Dependencies**: Works with any AI model capable of making HTTP requests
- **Instant Integration**: Start using with just a token and namespace registration
- **Flexible Data Structure**: Store any text-based information with optional metadata
- **Multi-tenant Support**: Isolated memory spaces per user/organization via namespaces
- **Production Ready**: Built with FastAPI, PostgreSQL, and industry-standard security

---

## 🤖 AI Integration Prompt

Use this example prompt to enable ChatGPT or other AI models to use Aji-Memo:

````
You now have access to an external memory system called Aji-Memo. This allows you to save and retrieve information across our conversations.

**Memory System Instructions:**
- API Base URL: https://api.aji-memo.saasbase.ovh/api/v1/ai
- Your Token: [INSERT_YOUR_TOKEN_HERE]
- Your UID: [INSERT_YOUR_UID_HERE]
- Your Namespace: [INSERT_YOUR_NAMESPACE_HERE]

**Available Commands:**

1. **Save Memory**: When you want to remember something important
   ```
   GET https://api.aji-memo.saasbase.ovh/api/v1/ai/memory/save?uid=[YOUR_UID]&token=[YOUR_TOKEN]&text=[URL_ENCODED_TEXT]&tags=[OPTIONAL_TAGS]
   ```

2. **Query Memory**: When you need to recall information
   ```
   GET https://api.aji-memo.saasbase.ovh/api/v1/ai/memory/query?uid=[YOUR_UID]&token=[YOUR_TOKEN]&query=[SEARCH_TERMS]&tags=[OPTIONAL_TAGS]
   ```

**Usage Guidelines:**
- Save important user preferences, decisions, or context
- Use descriptive tags like "preferences", "project", "settings", "user_info"
- Query memory before answering questions to provide personalized responses
- URL-encode text content (replace spaces with + or %20)

**Example Usage:**
- Save: "User prefers concise explanations" with tags "preferences,communication"
- Query: Search for "preferences" to recall user communication style
- Save: "Working on React project called MyApp" with tags "project,react"
- Query: Search for "project" to recall current work context

Always use this memory system to provide more personalized and context-aware responses.
````

**Setup Instructions:**
1. Register for a token: `GET https://api.aji-memo.saasbase.ovh/api/v1/ai/register?namespace=mycompany&uid=my-ai-assistant`
2. Replace `[INSERT_YOUR_TOKEN_HERE]`, `[INSERT_YOUR_UID_HERE]`, and `[INSERT_YOUR_NAMESPACE_HERE]` with your actual values
3. Send the customized prompt to your AI model

**Production URLs:**
- **Frontend**: https://aji-memo.saasbase.ovh
- **API**: https://api.aji-memo.saasbase.ovh
- **API Documentation**: https://api.aji-memo.saasbase.ovh/docs

---

## 🧩 Technology Stack

- **Backend:** [FastAPI](https://fastapi.tiangolo.com/) with Python 3.12+
- **Frontend:** [Next.js](https://nextjs.org/) with TypeScript
- **Database:** PostgreSQL with JSONB, arrays, and full-text search
- **Cache:** Redis for session management and caching
- **Search:** PostgreSQL TSVECTOR with GIN indexes for full-text search
- **Authentication:** JWT tokens for web, API tokens for AI integration
- **Containerization:** Docker with docker-compose for development

---

## 🚀 API Endpoints

### AI Integration Endpoints (GET)
Simple GET endpoints designed for AI/LLM integration:

#### 1. Register AI User
```
GET /api/v1/ai/register
```
**Parameters:**
- `namespace` (required): Organization/company identifier
- `uid` (required): User/session identifier
- `token` (optional): API token (generated if not provided)

**Response:**
```json
{
  "success": true,
  "data": {
    "uid": "ai-assistant",
    "namespace": "mycompany",
    "email": "ai-assistant@mycompany.ai",
    "token": "abc123xyz...",
    "message": "Registration successful"
  }
}
```

#### 2. Save Memory
```
GET /api/v1/ai/memory/save
```
**Parameters:**
- `uid` (required): User/session identifier
- `token` (required): API authentication token
- `text` (required): Memory content to save
- `namespace` (optional): Memory namespace (defaults to uid)
- `tags` (optional): Comma-separated tags (e.g., "preferences,ui")

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 123,
    "uid": "ai-assistant",
    "namespace": "mycompany",
    "text": "User prefers dark mode",
    "tags": ["preferences", "ui"],
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  }
}
```

#### 3. Query Memory
```
GET /api/v1/ai/memory/query
```
**Parameters:**
- `uid` (required): User/session identifier
- `token` (required): API authentication token
- `namespace` (optional): Memory namespace filter
- `tags` (optional): Comma-separated tags to filter by
- `query` (optional): Full-text search query
- `limit` (optional): Max results (1-100, default: 10)
- `offset` (optional): Pagination offset (default: 0)

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 123,
      "uid": "ai-assistant",
      "namespace": "mycompany",
      "text": "User prefers dark mode",
      "tags": ["preferences", "ui"],
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

#### 4. Validate Token
```
GET /api/v1/ai/token/validate
```
**Parameters:**
- `token` (required): API token to validate

**Response:**
```json
{
  "success": true,
  "data": {
    "token_name": "AI Token for ai-assistant",
    "user_id": 1,
    "permissions": {"memory": ["read", "write"]},
    "rate_limit_per_hour": 1000,
    "expires_at": "2025-01-15T10:30:00Z",
    "is_active": true
  }
}
```

### Web Interface Endpoints (POST)
Standard REST API endpoints for web applications:

- `POST /api/v1/auth/login` - User authentication
- `POST /api/v1/auth/register` - User registration
- `GET /api/v1/auth/me` - Get current user info
- `POST /api/v1/memory/save` - Save memory (authenticated)
- `POST /api/v1/memory/query` - Query memories (authenticated)

### Core Parameters

| Parameter    | Required | Default Value | Description |
|-------------|----------|---------------|-------------|
| `token`     | ✅ Yes   | —             | API authentication token |
| `uid`       | ✅ Yes   | —             | User or session identifier |
| `namespace` | ⛔ Optional | `uid`       | Memory namespace (for organization) |
| `tags`      | ⛔ Optional | `[]`        | Comma-separated tags |
| `query`     | ⛔ Optional | —           | Full-text search query |
| `limit`     | ⛔ Optional | `10`        | Results limit (1-100) |
| `offset`    | ⛔ Optional | `0`         | Pagination offset |

---

## 🛠️ Development Environment

### Prerequisites
- **Docker & Docker Compose** - For containerized development
- **Node.js 18+** - For frontend development
- **Python 3.12+** - For backend development (if running locally)

### Quick Start
1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd aji-memo
   ```

2. **Set up environment**
   ```bash
   # Run the setup script
   ./scripts/dev-setup.sh

   # Or manually:
   cp .env.example .env
   docker-compose up -d
   ```

3. **Run database migrations**
   ```bash
   ./scripts/db-migrate.sh

   # Or manually:
   docker-compose exec app alembic upgrade head
   ```

4. **Access the services**
   - **API**: http://localhost:8000
   - **API Documentation**: http://localhost:8000/docs
   - **Frontend**: http://localhost:3000
   - **Database Admin**: http://localhost:8080 (Adminer)
   - **Redis Admin**: http://localhost:8081 (Redis Commander)

### Development Commands

#### Backend
```bash
# View API logs
docker-compose logs -f app

# Run migrations
docker-compose exec app alembic upgrade head

# Create new migration
docker-compose exec app alembic revision --autogenerate -m "description"

# Access Python shell
docker-compose exec app python

# Run database seed
docker-compose exec app python app/db/seed.py
```

#### Frontend
```bash
cd frontend

# Start development server
npm run dev

# Build for production
npm run build

# Run linter
npm run lint
```

#### Database
```bash
# Connect to PostgreSQL
docker-compose exec db psql -U ajimemo -d ajimemo

# Backup database
docker-compose exec db pg_dump -U ajimemo ajimemo > backup.sql

# Restore database
docker-compose exec -T db psql -U ajimemo -d ajimemo < backup.sql
```

### Environment Variables
Create a `.env` file based on `.env.example`:

```bash
# Database
DATABASE_URL=postgresql://ajimemo:password@localhost:5432/ajimemo

# Redis
REDIS_URL=redis://localhost:6379

# Security
SECRET_KEY=your-secret-key-change-this
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Admin User
ADMIN_EMAIL=admin@ajimemo.com
ADMIN_PASSWORD=admin123

# Ports
APP_PORT=8000
DB_PORT=5432
REDIS_PORT=6379
ADMINER_PORT=8080
REDIS_COMMANDER_PORT=8081
```

### Testing
```bash
# Run backend tests
docker-compose exec app pytest

# Run frontend tests
cd frontend && npm test

# Run specific test
docker-compose exec app pytest tests/test_memory.py::test_save_memory
```

---

## 📖 Usage Examples

### AI Integration Flow
1. **Register AI user and get token**
   ```
   GET /api/v1/ai/register?namespace=mycompany&uid=ai-assistant
   ```

2. **Save user preference**
   ```
   GET /api/v1/ai/memory/save?uid=ai-assistant&token=abc123&text=User+prefers+dark+mode&tags=preferences,ui
   ```

3. **Query preferences later**
   ```
   GET /api/v1/ai/memory/query?uid=ai-assistant&token=abc123&tags=preferences
   ```

### Search Capabilities
- **Tag-based**: `tags=preferences,ui`
- **Full-text**: `query=dark+mode`
- **Combined**: `tags=preferences&query=dark+mode`
- **Pagination**: `limit=20&offset=40`

---

## 🔒 Security Considerations

- **Tokens in URLs**: May leak to logs or browser history - use dedicated domains
- **GET vs POST**: GET endpoints are for AI convenience - use POST for human interfaces
- **Token Security**: API tokens are hashed with bcrypt, include expiration and rate limits
- **Rate Limiting**: Configurable per token (AI tokens get higher limits)
- **CORS**: Configured for specific origins in production
- **Input Validation**: All inputs are validated using Pydantic schemas

---
