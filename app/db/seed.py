#!/usr/bin/env python3
"""Database seeding script for AjiMemo."""

import sys
import os
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

# Add the app directory to the path so we can import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from app.db.database import SessionLocal  # noqa: E402
from app.db.models import User, ApiToken  # noqa: E402
from app.utils.security import hash_password  # noqa: E402
from app.config import settings  # noqa: E402


def seed_admin_user(db: Session) -> None:
    """Seed the database with an admin user."""

    # Check if admin user already exists
    admin_user = db.query(User).filter(User.email == settings.admin_email).first()
    if admin_user:
        print("✅ Admin user already exists!")
        return

    # Create admin user
    admin_user = User(
        email=settings.admin_email,
        name=settings.admin_name,
        password_hash=hash_password(settings.admin_password),
        plan="enterprise",
        is_active=True,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )

    try:
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        print("✅ Admin user created successfully!")
        print(f"   Name: {settings.admin_name}")
        print(f"   Email: {settings.admin_email}")
        print(f"   Password: {settings.admin_password}")
        print("   Plan: enterprise")

        # Create an admin API token
        admin_token = ApiToken(
            user_id=admin_user.id,
            token_name="Admin Token",
            token_hash=hash_password("admin-token-123"),
            permissions={"all": True},
            rate_limit_per_hour=10000,
            is_active=True,
            created_at=datetime.now(timezone.utc)
        )

        db.add(admin_token)
        db.commit()
        print("✅ Admin API token created!")

    except IntegrityError as e:
        db.rollback()
        print(f"❌ Error creating admin user: {e}")


def seed_test_user(db: Session) -> None:
    """Seed the database with a test user."""

    # Check if test user already exists
    test_user = db.query(User).filter(User.email == "test@ajimemo.com").first()
    if test_user:
        print("✅ Test user already exists!")
        return

    # Create test user
    test_user = User(
        email="test@ajimemo.com",
        name="Test User",
        password_hash=hash_password("test123"),
        plan="free",
        is_active=True,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )

    try:
        db.add(test_user)
        db.commit()
        print("✅ Test user created successfully!")
        print("   Email: test@ajimemo.com")
        print("   Password: test123")
        print("   Plan: free")

    except IntegrityError as e:
        db.rollback()
        print(f"❌ Error creating test user: {e}")


def main():
    """Main seeding function."""
    print("🌱 Starting database seeding...")

    # Create database session
    db = SessionLocal()

    try:
        # Seed admin user
        print("\n📝 Seeding admin user...")
        seed_admin_user(db)

        # Seed test user
        print("\n📝 Seeding test user...")
        seed_test_user(db)

        print("\n🎉 Database seeding completed successfully!")

    except Exception as e:
        print(f"\n❌ Error during seeding: {e}")
        db.rollback()
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    main()
