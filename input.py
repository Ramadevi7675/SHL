import re

# Function to clean user input
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    return text

# Function to get cleaned user query
def get_user_query():
    user_input = input("Enter job description or query: ")
    cleaned_input = clean_text(user_input)
    print("Cleaned input:", cleaned_input)
    return cleaned_input
