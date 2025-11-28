"""
Script to create an admin user in the database
Run this with: poetry run python create_admin.py (from backend directory)

Usage:
    python create_admin.py
    # Will prompt for email, password, first_name, last_name

Or set environment variables:
    ADMIN_EMAIL=admin@example.com
    ADMIN_PASSWORD=securepassword123
    ADMIN_FIRST_NAME=Admin
    ADMIN_LAST_NAME=User
    python create_admin.py
"""
import os
import sys
from app.database_config import SessionLocal
from app.crud import user as user_crud
from app.schemas import UserCreate

def create_admin_user(
    email: str,
    password: str,
    first_name: str = "Admin",
    last_name: str = "User"
):
    """Create an admin user in the database"""
    db = SessionLocal()
    try:
        # Check if user already exists
        existing_user = user_crud.get_user_by_email(db, email)
        if existing_user:
            print(f"[ERROR] User with email {email} already exists!")
            response = input("Do you want to make this user an admin? (y/n): ")
            if response.lower() == 'y':
                # Update existing user to admin
                update_user_to_admin(db, existing_user.id, email)
                return
            else:
                print("[CANCELLED] Exiting without changes.")
                return
        
        # Create new admin user
        user_data = UserCreate(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        
        # user_crud.create_user creates a regular user. We need to make them admin.
        # Or we can manually create admin.
        # But simpler to create user then update to admin.
        user = user_crud.create_user(db, user_data)
        
        # Update to admin
        user = user_crud.update_user_admin_status(db, user.id, True)
        
        print(f"[SUCCESS] Admin user created successfully!")
        print(f"  Email: {email}")
        print(f"  Name: {first_name} {last_name}")
        print(f"  User ID: {user.id}")
        print(f"  Admin: {user.is_admin}")
        
    except Exception as e:
        print(f"[ERROR] Failed to create admin user: {str(e)}")
        sys.exit(1)
    finally:
        db.close()


def update_user_to_admin(db, user_id: int, email: str):
    """Update an existing user to admin status"""
    try:
        user = user_crud.update_user_admin_status(db, user_id, is_admin=True)
        if user:
            print(f"[SUCCESS] User {email} has been promoted to admin!")
            print(f"  User ID: {user.id}")
            print(f"  Admin: {user.is_admin}")
        else:
             print(f"[ERROR] User not found")
    except Exception as e:
        print(f"[ERROR] Failed to update user: {str(e)}")


def main():
    """Main function to create admin user"""
    print("=" * 50)
    print("Create Admin User")
    print("=" * 50)
    
    # Get credentials from environment variables or prompt
    email = os.getenv("ADMIN_EMAIL")
    password = os.getenv("ADMIN_PASSWORD")
    first_name = os.getenv("ADMIN_FIRST_NAME", "Admin")
    last_name = os.getenv("ADMIN_LAST_NAME", "User")
    
    if not email:
        email = input("Enter admin email: ").strip()
        if not email:
            print("[ERROR] Email is required!")
            sys.exit(1)
    
    if not password:
        password = input("Enter admin password (min 8 characters): ").strip()
        if not password:
            print("[ERROR] Password is required!")
            sys.exit(1)
        if len(password) < 8:
            print("[ERROR] Password must be at least 8 characters!")
            sys.exit(1)
        
        # Confirm password
        password_confirm = input("Confirm password: ").strip()
        if password != password_confirm:
            print("[ERROR] Passwords do not match!")
            sys.exit(1)
    
    if not os.getenv("ADMIN_FIRST_NAME"):
        first_name_input = input(f"Enter first name (default: {first_name}): ").strip()
        if first_name_input:
            first_name = first_name_input
    
    if not os.getenv("ADMIN_LAST_NAME"):
        last_name_input = input(f"Enter last name (default: {last_name}): ").strip()
        if last_name_input:
            last_name = last_name_input
    
    print("\nCreating admin user...")
    create_admin_user(email, password, first_name, last_name)


if __name__ == "__main__":
    main()
