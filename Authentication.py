if __name__ == "__main__":
    register_user("alice", "SecurePass123!")
    authenticate_user("alice", "WrongPass")  # Fails
    authenticate_user("alice", "SecurePass123!")  # Succeeds
