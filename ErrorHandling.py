 if __name__ == "__main__":
    calculate_square_root(25)
    
    calculate_square_root(-9)
    
    calculate_square_root("25")
    
    try:
        validate_positive(-5)
    except InvalidValueError as e:
        print(f"Custom error caught: {e}")
