import hashlib
import uuid

# Simulate a user database (stores hashed passwords and salt)
user_database = {}

def hash_password(password: str, salt: str = None) -> tuple[str, str]:
    """Hash a password with a random salt for security."""
    if not salt:
        salt = uuid.uuid4().hex  # Generate unique salt
    hashed = hashlib.sha256((password + salt).encode()).hexdigest()
    return hashed, salt

def register_user(username: str, password: str) -> bool:
    """Register a new user with a hashed password."""
    if username in user_database:
        print("Username already exists!")
        return False
    hashed_pw, salt = hash_password(password)
    user_database[username] = {"hashed_password": hashed_pw, "salt": salt}
    print("User registered successfully!")
    return True

def authenticate_user(username: str, password: str) -> bool:
    """Authenticate a user by verifying password hash."""
    user = user_database.get(username)
    if not user:
        print("Username not found!")
        return False
    # Re-hash input password with stored salt
    input_hashed, _ = hash_password(password, user["salt"])
    if input_hashed == user["hashed_password"]:
        print("Authentication successful!")
        return True
    print("Incorrect password!")
    return False

# Example usage
if __name__ == "__main__":
    register_user("alice", "SecurePass123!")
    authenticate_user("alice", "WrongPass")  # Fails
    authenticate_user("alice", "SecurePass123!")  # Succeeds
