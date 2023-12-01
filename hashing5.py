import hashlib
import secrets


# Function to generate a random salt
def generate_salt():
    return secrets.token_hex(16)  # 16 bytes of randomness


# Function to calculate the hash of a given string with a provided salt
def calculate_hash_with_salt(input_string, salt):
    # Concatenate the salt with the input string and calculate the hash
    salted_string = salt + input_string
    return hashlib.sha256(salted_string.encode()).hexdigest()


# Example string to hash
password = "SecretPassword"

# Generate a random salt
salt = generate_salt()

# Calculate hash with the generated salt
hashed_password = calculate_hash_with_salt(password, salt)
print(hashed_password)

# Store both the hashed password and the salt in your database or wherever you save credentials
stored_password_hash = hashed_password
stored_salt = salt

# Later during verification (e.g., during a login attempt)

# Retrieve the salt associated with the user
# In a real-world scenario, you would typically retrieve this from your data storage
retrieved_salt = stored_salt

# Get the password provided during the login attempt
login_password = "SecretPassword"

# Calculate the hash of the login attempt using the retrieved salt
hashed_login_attempt = calculate_hash_with_salt(login_password, retrieved_salt)
print(hashed_login_attempt)

# Compare the calculated hash with the stored hash
if hashed_login_attempt == stored_password_hash:
    print("Password is correct.")
else:
    print("Password is incorrect.")
