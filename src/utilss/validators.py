
#email validator 
import re 
def validate_email_format(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email)

#password validator 
def validate_password_strength(password):
    if len(password) < 8:
        return False    
    if not any(char.isdigit() for char in password):
        return False    
    if not any(char.isupper() for char in password):
        return False    
    return True


