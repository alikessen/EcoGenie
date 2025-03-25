import mysql.connector
from flask_bcrypt import Bcrypt
import json


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

def get_user_by_id(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()
    return user


def save_user_input(user_id, diet_data, energy_data, transport_data,
                    diet_footprint, energy_footprint, transport_footprint):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO user_inputs 
            (user_id, diet_data, energy_data, transport_data, 
             diet_footprint, energy_footprint, transport_footprint)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (
                user_id,
                json.dumps(diet_data),
                json.dumps(energy_data),
                json.dumps(transport_data),
                diet_footprint,
                energy_footprint,
                transport_footprint
            )
        )
        conn.commit()
    finally:
        cursor.close()
        conn.close()


def get_user_history(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            """
            SELECT diet_footprint, energy_footprint, transport_footprint,
                   timestamp
            FROM user_inputs
            WHERE user_id = %s
            ORDER BY timestamp DESC
            """,
            (user_id,)
        )
        results = cursor.fetchall()
        return results
    finally:
        cursor.close()
        conn.close()
