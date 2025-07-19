#!/bin/bash

# Database Migration Script

set -e

echo "🗃️ Running database migrations..."

# Determine which docker-compose file to use
COMPOSE_FILE=""
if [ -f "docker-compose.prod.yml" ] && docker compose -f docker-compose.prod.yml ps app 2>/dev/null | grep -q "Up"; then
    COMPOSE_FILE="-f docker-compose.prod.yml"
    echo "📦 Using production docker-compose configuration"
elif docker compose ps app 2>/dev/null | grep -q "Up"; then
    COMPOSE_FILE=""
    echo "📦 Using development docker-compose configuration"
else
    echo "❌ App container is not running. Please start it first with 'docker compose up -d' or 'docker compose -f docker-compose.prod.yml up -d'"
    exit 1
fi

# Run migrations
echo "📋 Running Alembic migrations..."
docker compose $COMPOSE_FILE exec app alembic upgrade head

echo "✅ Database migrations completed successfully!"

# Optionally seed with test data
read -p "Would you like to seed the database with test data? (y/N): " -r
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🌱 Seeding database with test data..."
    docker compose $COMPOSE_FILE exec app python app/db/seed.py
fi

echo ""
echo "🎉 Database setup completed!"
echo ""
echo "📍 Database access:"
echo "  • Admin UI:     http://localhost:${PGADMIN_PORT:-5050}"
echo "  • Connection:   postgresql://${POSTGRES_USER:-ajimemo}:${POSTGRES_PASSWORD:-password}@localhost:${DB_PORT:-5433}/${POSTGRES_DB:-ajimemo}"
echo ""
