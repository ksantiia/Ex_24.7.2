import os

from dotenv import load_dotenv

load_dotenv()

valid_email = os.getenv('valid_email')
valid_password = os.getenv('valid_password')
invalid_password = os.getenv('invalid_password')
invalid_email = os.getenv('invalid_email')
password_space = ''
email_space = ''
