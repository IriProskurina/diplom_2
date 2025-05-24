import string
import random

def generate_random_email():
    domain = "@example.com"
    username_length = random.randint(5, 10)
    letters = string.ascii_lowercase
    username = ''.join(random.choice(letters) for _ in range(username_length))
    return username + domain

def generate_random_string(length=10):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(length))