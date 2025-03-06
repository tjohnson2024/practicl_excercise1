import requests
import json

# Alma API Credentials
API_KEY = 'l8xx17c816b10f034a3da5cfd0e0424efd33'  # Replace with your actual Alma API key
BASE_URL = 'https://api-eu.hosted.exlibrisgroup.com/almaws/v1'

# Headers for API requests
headers = {
    'Authorization': 'apikey {}'.format(API_KEY),  # Using .format() for compatibility with Python 2.7
    'Content-Type': 'application/json'
}

# Step 1: Fetch users from Alma API (read-only)
def get_users():
    url = "{}/users".format(BASE_URL)  # Using .format() to create the URL
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get('user', [])
    else:
        print("Error fetching users: {}".format(response.status_code))  # .format() used
        return []

# Step 2: Fetch loans for a user (read-only)
def get_loans(user_id):
    url = "{}/users/{}/loans".format(BASE_URL, user_id)  # Using .format() to create the URL
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get('loan', [])
    else:
        print("Error fetching loans for user {}: {}".format(user_id, response.status_code))  # .format() used
        return []

# Step 3: Fetch fines for a user (read-only)
def get_fines(user_id):
    url = "{}/users/{}/fines".format(BASE_URL, user_id)  # Using .format() to create the URL
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get('fine', [])
    else:
        print("Error fetching fines for user {}: {}".format(user_id, response.status_code))  # .format() used
        return []

# Step 4: Generate HTML output
def generate_html(users_data):
    html_content = """
    <html>
    <head><title>User Fines and Loans</title></head>
    <body>
        <h1>Users with Overdue Loans and Fines</h1>
        <table border="1">
            <thead>
                <tr><th>User Name</th><th>Total Fines ($)</th><th>Loans Count</th></tr>
            </thead>
            <tbody>
    """

    # Add user data to the table
    for user in users_data:
        html_content += """
            <tr>
                <td>{}</td>
                <td>{}</td>
                <td>{}</td>
            </tr>
        """.format(user['name'], user['total_fines'], user['loan_count'])  # Using .format() to insert data

    html_content += """
            </tbody>
        </table>
    </body>
    </html>
    """

    # Save the HTML content to a file
    with open("user_fines_and_loans.html", "w") as file:
        file.write(html_content)
    print("HTML file has been generated: user_fines_and_loans.html")

