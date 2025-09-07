from django.test import TestCase

# Create your tests here.
import os

file_path = "alx_travel_app/requirements.txt"

if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
    print(f"'{file_path}' exists and is not empty")
else:
    print(f"'{file_path}' does not exist or is empty")
