"""
Vercel serverless function entry point for Flask application
"""
import sys
import os

# Set Vercel environment flag
os.environ['VERCEL'] = '1'

# Add the parent directory to the path so we can import app
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Import the Flask app
from app import app, db, create_admin_user

# Initialize database tables and create admin user if they don't exist
# Note: In serverless, /tmp is ephemeral, so data won't persist between deployments
# For production, consider using Vercel Postgres or another database service
def initialize_database():
    """Initialize database and create admin user"""
    try:
        # Create all database tables
        db.create_all()
        # Create admin user (username: admin, password: admin123)
        create_admin_user()
        print("Database and admin user initialized successfully")
        return True
    except Exception as e:
        print(f"Database initialization error: {e}")
        import traceback
        traceback.print_exc()
        return False

# Initialize on module load
with app.app_context():
    initialize_database()

# Export the app for Vercel
# Vercel Python runtime automatically handles WSGI applications
