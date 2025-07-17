# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Aji-Memo** is an external AI memory system designed for LLM integration via simple GET requests. The system allows AI models (like ChatGPT) to save and retrieve contextual information through HTTP GET endpoints, eliminating the need for complex integrations or function calling.

### Core Purpose
- **AI-first design**: Primary interface is GET requests for AI/LLM ease of use
- **Memory storage**: Store and retrieve contextual information with tags and namespaces
- **Full-text search**: PostgreSQL-based search with TSVECTOR and GIN indexes
- **Dual interface**: GET endpoints for AI, POST endpoints for web/human use

## Technology Stack

- **Backend**: FastAPI with PostgreSQL, Redis, SQLAlchemy, Alembic
- **Frontend**: Next.js with TypeScript, Tailwind CSS, React Query
- **Database**: PostgreSQL with JSONB, arrays, and full-text search
- **Containerization**: Docker with docker-compose

## Development Commands

### Backend Development
```bash
# Setup development environment
./scripts/dev-setup.sh

# Run database migrations
./scripts/db-migrate.sh

# Start services
docker-compose up -d

# View logs
docker-compose logs -f app

# Run migrations manually
docker-compose exec app alembic upgrade head

# Create new migration
docker-compose exec app alembic revision --autogenerate -m "description"

# Access database
docker-compose exec app python -c "from app.db.database import SessionLocal; print('DB connected')"
```

### Frontend Development
```bash
cd frontend
npm run dev          # Start development server
npm run build        # Build for production
npm run lint         # Run ESLint
```

### Service URLs
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Database Admin**: http://localhost:8080 (Adminer)
- **Redis Admin**: http://localhost:8081 (Redis Commander)
- **Frontend**: http://localhost:3000

## Architecture

### API Route Structure
The API has two distinct interfaces:

**AI/LLM Interface (GET only)**:
- `/api/v1/ai/register` - Register AI user and get token
- `/api/v1/ai/memory/save` - Save memory entry
- `/api/v1/ai/memory/query` - Query memories
- `/api/v1/ai/token/validate` - Validate API token

**Human/Web Interface (POST)**:
- `/api/v1/auth/login` - User authentication
- `/api/v1/auth/register` - User registration
- `/api/v1/memory/save` - Save memory (POST)
- `/api/v1/memory/query` - Query memories (POST)

### Database Architecture

**Core Models**:
- `User` - User accounts with email, password, plan
- `ApiToken` - API tokens with permissions, rate limits, expiry
- `Memory` - Memory entries with uid, namespace, text, tags, search_vector

**Key Features**:
- **Full-text search**: Uses PostgreSQL TSVECTOR with GIN indexes
- **Tag filtering**: PostgreSQL array overlap operator (`&&`)
- **Namespace isolation**: Group memories by namespace (defaults to uid)
- **Search relevance**: Uses `ts_rank` for relevance scoring

### Memory Model Structure
```python
class Memory(Base):
    id: int
    user_id: int (optional, links to User)
    uid: str (required, AI session identifier)
    namespace: str (required, defaults to uid)
    text: str (required, memory content)
    tags: List[str] (optional, for categorization)
    created_by: str (optional, audit trail)
    search_vector: TSVECTOR (auto-updated for FTS)
    created_at: datetime
    updated_at: datetime
```

### Token Authentication
- **API Tokens**: Hashed with bcrypt, stored in `api_tokens` table
- **JWT Tokens**: For web interface authentication
- **Rate Limiting**: Configurable per token (AI tokens get higher limits)
- **Permissions**: JSON field defining allowed operations

## AI Integration Usage

### 1. Register AI User
```
GET /api/v1/ai/register?namespace=company&uid=ai-assistant&token=optional
```

### 2. Save Memory
```
GET /api/v1/ai/memory/save?uid=ai-assistant&token=abc123&text=User+prefers+dark+mode&tags=preferences,ui
```

### 3. Query Memory
```
GET /api/v1/ai/memory/query?uid=ai-assistant&token=abc123&query=dark+mode&tags=preferences&limit=10
```

## Important Implementation Details

### Database Migration Requirements
- Always run migrations when models change: `alembic upgrade head`
- Search vectors are updated via raw SQL after memory creation/update
- Use `.is_(True)` not `== True` for SQLAlchemy boolean comparisons

### Memory Search Implementation
- **Tag filtering**: Uses PostgreSQL array overlap (`tags.op('&&')`)
- **Full-text search**: Uses `plainto_tsquery` with `search_vector.op('@@')`
- **Relevance ranking**: Orders by `ts_rank` for text search, `created_at` otherwise
- **Search vector updates**: Automatically combines text and tags for indexing

### API Token Security
- Tokens are hashed with bcrypt before storage
- Include rate limiting and expiration
- AI tokens get 1-year expiry and higher rate limits
- Validate permissions using JSON structure in database

### Configuration
- Environment variables are managed through `app.config.Settings`
- Database URL, Redis URL, and secrets are configurable
- CORS settings support multiple origins for development

## Code Quality Standards

### SQLAlchemy Patterns
- Use `SqlAlchemy.is_(True)` for boolean comparisons, not `== True`
- Add `# type: ignore` for complex SQLAlchemy column access
- Use proper typing with `Optional[Type]` for nullable fields

### API Patterns
- Separate GET (AI) and POST (web) endpoints
- Use dependency injection for database sessions and authentication
- Return structured responses with `success: bool` and `data: object`
- Include proper error handling with specific HTTP status codes

### Database Best Practices
- Use transactions for multi-step operations
- Update search vectors after text/tag changes
- Use proper indexes for performance (GIN for arrays and full-text search)
- Implement proper foreign key relationships with cascade deletes