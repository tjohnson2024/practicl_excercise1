import requests
import json

# Alma API Credentials
API_KEY = 'l8xx17c816b10f034a3da5cfd0e0424efd33'  # Replace with your actual Alma API key
BASE_URL = 'https://api-eu.hosted.exlibrisgroup.com/almaws/v1'


headers = {
    'Authorization': 'apikey {}'.format(API_KEY),  # Using .format() for compatibility with Python 2.7
    'Content-Type': 'application/json'
}


def get_users():
    url = "{}/users".format(BASE_URL)  # Ensure the correct URL is being used
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get('user', [])
    else:
        print("Error fetching users: {}".format(response.status_code))  # .format() used
        return []


def get_loans(user_id):
    url = "{}/users/{}/loans".format(BASE_URL, user_id)  # Correct URL with v1
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get('loan', [])
    else:
        print("Error fetching loans for user {}: {}".format(user_id, response.status_code))  # .format() used
        return []


def get_fines(user_id):
    url = "{}/users/{}/fees".format(BASE_URL, user_id)  # Correct URL with v1
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get('fee', [])  # Correct key for fees/fines
    else:
        print("Error fetching fines for user {}: {}".format(user_id, response.status_code))  # .format() used
        return []


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


    with open("user_fines_and_loans.html", "w") as file:
        file.write(html_content)
    print("HTML file has been generated: user_fines_and_loans.html")


def main():
    users = get_users()  # Step 1: Fetch users
    users_data = []

    # Loop through each user to fetch loans and fines
    for user in users:
        user_id = user['user_id']
        loans = get_loans(user_id)  # Step 2: Get loans
        fines = get_fines(user_id)  # Step 3: Get fines

        # Calculate total fines and loan count
        total_fines = sum(float(fine['amount']) for fine in fines) if fines else 0
        loan_count = len(loans)

        # Store user data for sorting and display
        users_data.append({
            'name': "{} {}".format(user['first_name'], user['last_name']),  # .format() used for compatibility
            'total_fines': total_fines,
            'loan_count': loan_count
        })

    # Sort users by total fines in descending order
    users_data.sort(key=lambda x: x['total_fines'], reverse=True)

    # Step 4: Generate HTML output
    generate_html(users_data)

# Run the main function
if __name__ == "__main__":
    main()
