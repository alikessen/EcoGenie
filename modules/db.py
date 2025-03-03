import mysql.connector
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",  
        password="",
        database="EcoGenieDB"
    )

def register_user(username, email, password):
    """Registers a new user with a hashed password."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Hash the password before storing
    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

    try:
        cursor.execute(
            "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)",
            (username, email, hashed_password)
        )
        conn.commit()
        return True
    except mysql.connector.IntegrityError:
        return False  # Username or email already exists
    finally:
        cursor.close()
        conn.close()

def get_user_by_username(username):
    """Fetch user details by username."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()
    return user