if __name__ == "__main__":
    
    print(validate_username("alice_123")) 
    print(validate_username("al"))        
    
    print(validate_email("alice@example.com"))  
    print(validate_email("alice@.com"))         
    
    print(validate_age(25))   
    print(validate_age(150))  
