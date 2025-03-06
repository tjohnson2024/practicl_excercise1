import requests
import json

# Alma API Credentials
API_KEY = 'l8xx17c816b10f034a3da5cfd0e0424efd33'  # Replace with your actual Alma API key
BASE_URL = 'https://api-eu.hosted.exlibrisgroup.com/almaws/v1'


# Headers for API requests
headers = {
    'Authorization': 'apikey {API_KEY}',
    'Content-Type': 'application/json'
}

# Step 1: Fetch users from Alma API (read-only)
def get_users():
    url = "{BASE_URL}/users"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get('user', [])
    else:
        print("Error fetching users: {response.status_code}")
        return []

