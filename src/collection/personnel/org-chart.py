import requests
import os
from graphviz import Digraph
from datetime import datetime
import base64

# Set your TriNet API credentials
API_KEY = os.getenv('TRINET_API_KEY')
API_SECRET = os.getenv('TRINET_API_SECRET')

# Set your Company ID
COMPANY_ID = "CJ6"

# API endpoints
TOKEN_URL = "https://api.trinet.com/oauth/accesstoken?grant_type=client_credentials"
EMPLOYEE_LIST_URL_TEMPLATE = "https://api.trinet.com/v1/company/{companyId}/employees"
BASE_DIR = "evidence-artifacts/personnel"  # Base directory for storing the employee list

def get_access_token(api_key, api_secret):
    # Create the Basic Authentication header for client credentials
    client_credentials = f"{api_key}:{api_secret}"
    encoded_credentials = base64.b64encode(client_credentials.encode('utf-8')).decode('utf-8')
    headers = {
        'Authorization': f'Basic {encoded_credentials}'
    }

    # Request access token using the client credentials
    response = requests.get(TOKEN_URL, headers=headers)
    
    print(f"Token Response: {response.status_code}, {response.text}")  # Debugging
    
    if response.status_code == 200:
        token_data = response.json()
        return token_data['access_token']
    else:
        raise Exception(f"Error getting access token: {response.text}")

def get_employee_list(access_token, company_id=COMPANY_ID, employment_status="A", view_type="All", limit=100, offset=None):
    # Get employee data
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
        'grant_type': 'client_credentials'
    }
    
    # Build the API URL with the company ID and query parameters
    url = EMPLOYEE_LIST_URL_TEMPLATE.format(companyId=company_id)
    params = {
        "viewType": view_type,
        "limit": limit,
        "employmentStatus": employment_status  # Filter by employment status
    }
    
    # Only add offset if it's not None
    if offset is not None:
        params["offset"] = offset
    
    response = requests.get(url, headers=headers, params=params)
    
    print(f"Employee List Status Code: {response.status_code}")
    print(f"Employee List Response: {response.text}")  # Debugging response text
    
    if response.status_code == 200:
        try:
            return response.json()
        except ValueError:
            raise Exception("Invalid JSON response received")
    else:
        raise Exception(f"Error fetching employee list: {response.status_code} - {response.text}")

def generate_org_chart(employee_data):
    dot = Digraph(comment='Organization Chart')

    # Add nodes (employees) and edges (supervisor relationships)
    for employee in employee_data:
        emp_id = employee.get('employeeId')
        supervisor_id = employee.get('supervisorId')

        # Handle None values for names (if fields are missing or None, use an empty string)
        first_name = employee.get('firstName', '') or ''
        last_name = employee.get('lastName', '') or ''
        name = f"{first_name} {last_name}".strip()  # Make sure there's no extra space

        # Add employee node with their name
        dot.node(emp_id, name if name else "Unknown")  # Use "Unknown" if no name is available

        # Only add an edge if supervisor_id is not None
        if supervisor_id:
            dot.edge(supervisor_id, emp_id)

    # Create directory based on year/month
    current_year = datetime.now().year
    current_month = datetime.now().month
    output_dir = os.path.join(BASE_DIR, str(current_year), str(current_month))

    os.makedirs(output_dir, exist_ok=True)
    
    # Save the org chart as a PNG image
    output_path = os.path.join(output_dir, 'organization_chart')
    dot.render(output_path, format='png')
    print(f"Organization chart saved to {output_path}.png")

def main():
    try:
        # Use environment variables or input API key and secret directly
        api_key = API_KEY or input("Enter your API Key: ")
        api_secret = API_SECRET or input("Enter your API Secret: ")

        token = get_access_token(api_key, api_secret)

        # Paginate through the employee list
        offset = None  # Start with no offset
        has_more = True
        all_employees = []

        while has_more:
            response_data = get_employee_list(token, offset=offset)
            employee_data = response_data.get('data', {}).get('employeeData', [])
            all_employees.extend(employee_data)
            
            # Check if there are more employees to fetch
            has_more = response_data.get('data', {}).get('hasMore', False)
            
            # Set offset for the next request only if there are more employees
            if has_more:
                offset = offset + 100 if offset is not None else 101  # Start at 101 for second request
        
        # Once we have all the employees, generate the organizational chart
        generate_org_chart(all_employees)

    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()