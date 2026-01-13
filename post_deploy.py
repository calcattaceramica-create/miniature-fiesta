#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Post-deployment script for Render
This script runs automatically after deployment to initialize the database
"""

import os
import sys
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def check_database_connection():
    """Check if database is accessible"""
    try:
        from app import db
        db.engine.connect()
        logger.info("✅ Database connection successful")
        return True
    except Exception as e:
        logger.error(f"❌ Database connection failed: {e}")
        return False

def initialize_database():
    """Initialize database tables"""
    try:
        from app import db, app
        
        with app.app_context():
            # Check if tables already exist
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            existing_tables = inspector.get_table_names()
            
            if existing_tables:
                logger.info(f"ℹ️ Database already has {len(existing_tables)} tables")
                return True
            
            # Create all tables
            logger.info("🔨 Creating database tables...")
            db.create_all()
            logger.info("✅ Database tables created successfully")
            return True
            
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")
        return False

def seed_initial_data():
    """Add initial data if database is empty"""
    try:
        from app import db, app
        from models import User, Role
        
        with app.app_context():
            # Check if admin user exists
            admin = User.query.filter_by(username='admin').first()
            
            if admin:
                logger.info("ℹ️ Admin user already exists")
                return True
            
            # Create admin role
            logger.info("👤 Creating admin role...")
            admin_role = Role(
                name='admin',
                name_ar='مدير النظام',
                description='Full system access'
            )
            db.session.add(admin_role)
            
            # Create admin user
            logger.info("👤 Creating admin user...")
            admin_user = User(
                username='admin',
                email='admin@ded-erp.com',
                full_name='System Administrator',
                full_name_ar='مدير النظام',
                is_active=True,
                must_change_password=True
            )
            admin_user.set_password('admin123')
            admin_user.roles.append(admin_role)
            
            db.session.add(admin_user)
            db.session.commit()
            
            logger.info("✅ Initial data seeded successfully")
            logger.warning("⚠️ Default password is 'admin123' - CHANGE IT IMMEDIATELY!")
            return True
            
    except Exception as e:
        logger.error(f"❌ Data seeding failed: {e}")
        db.session.rollback()
        return False

def main():
    """Main post-deployment function"""
    logger.info("🚀 Starting post-deployment setup...")
    
    # Check if we're in production
    if os.getenv('FLASK_ENV') != 'production':
        logger.warning("⚠️ Not in production environment, skipping...")
        return 0
    
    # Check database connection
    if not check_database_connection():
        logger.error("❌ Cannot proceed without database connection")
        return 1
    
    # Initialize database
    if not initialize_database():
        logger.error("❌ Database initialization failed")
        return 1
    
    # Seed initial data
    if not seed_initial_data():
        logger.error("❌ Data seeding failed")
        return 1
    
    logger.info("🎉 Post-deployment setup completed successfully!")
    logger.info("📝 Next steps:")
    logger.info("   1. Access your application")
    logger.info("   2. Login with username: admin, password: admin123")
    logger.info("   3. CHANGE THE PASSWORD IMMEDIATELY!")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())

