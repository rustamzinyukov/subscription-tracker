#!/usr/bin/env python3
"""
Migration script for adding advanced subscription fields
"""
import os
import sys
from alembic.config import Config
from alembic import command

def run_migration():
    """Run the migration to add advanced subscription fields"""
    print("🚀 Starting database migration...")
    
    # Get the path to alembic.ini
    alembic_cfg = Config("alembic.ini")
    
    try:
        # Run the migration
        command.upgrade(alembic_cfg, "head")
        print("✅ Migration completed successfully!")
        return True
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return False

if __name__ == "__main__":
    success = run_migration()
    sys.exit(0 if success else 1)
