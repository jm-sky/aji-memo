# Project Structure

## Recommended FastAPI Project Layout

```
aji-memo/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app initialization
│   ├── config.py               # Configuration settings
│   ├── dependencies.py         # Common dependencies (auth, etc.)
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── router.py       # Main v1 router
│   │   │   └── endpoints/
│   │   │       ├── __init__.py
│   │   │       └── auth.py         # Authentication endpoints
│   │   │
│   │   └── middleware/
│   │       ├── __init__.py
│   │       ├── rate_limit.py   # Rate limiting middleware
│   │       └── auth.py         # JWT authentication middleware
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── security.py         # JWT handling, password hashing
│   │   ├── rate_limiter.py     # Rate limiting logic
│   │   └── exceptions.py       # Custom exceptions
│   │
│   ├── db/
│   │   ├── __init__.py
│   │   ├── database.py         # Database connection
│   │   ├── models.py           # SQLAlchemy models
│   │   └── migrations/         # Alembic migrations
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── cache_service.py    # Cache management
│   │   └── auth_service.py     # Authentication logic
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── auth.py             # Authentication schemas
│   │
│   └── utils/
│       ├── __init__.py
│       └── helpers.py          # Common utilities
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py            # Test configuration
│   ├── test_api/
│   └── test_services/
│
├── docs/                      # Current documentation
├── requirements.txt           # Python dependencies
├── .env.example              # Environment variables example
├── docker-compose.yml        # Docker setup
├── Dockerfile               # Container definition
└── README.md               # Project README
```

## Key Components

### 1. API Layer (`app/api/`)
- Versioned endpoints (`/api/v1/`)
- Request/response handling
- Input validation
- Middleware integration

### 2. Core Logic (`app/core/`)
- Security utilities (JWT, rate limiting)
- Custom exceptions
- Cross-cutting concerns

### 3. Data Layer (`app/db/`)
- Database models
- Connection management
- Migration scripts

### 5. Business Services (`app/services/`)
- Main application logic
- Data aggregation
- Cache management
- Webhook processing

### 6. Data Models (`app/schemas/`)
- Pydantic models for API
- Request/response validation
- Type safety


## Dependencies

```txt
fastapi>=0.104.0
uvicorn>=0.24.0
sqlalchemy>=2.0.0
alembic>=1.13.0
psycopg2-binary>=2.9.0
redis>=5.0.0
pydantic>=2.5.0
python-jose[cryptography]>=3.3.0
passlib[bcrypt]>=1.7.4
httpx>=0.25.0
python-multipart>=0.0.6
```

This structure provides:
- Clear separation of concerns
- Scalable architecture
- Easy testing
- Professional FastAPI patterns
