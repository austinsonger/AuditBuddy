import requests
import os
import csv
import base64
from datetime import datetime


API_KEY = os.getenv('TRINET_API_KEY')
API_SECRET = os.getenv('TRINET_API_SECRET')
COMPANY_ID = "CJ6"
TOKEN_URL = "https://api.trinet.com/oauth/accesstoken?grant_type=client_credentials"
EMPLOYEE_LIST_URL_TEMPLATE = "https://api.trinet.com/v1/company/{companyId}/employees"
BASE_DIR = "evidence-artifacts/personnel"  # Base directory for storing the employee list


# Helper function to get access token
def get_access_token(api_key, api_secret):
    client_credentials = f"{api_key}:{api_secret}"
    encoded_credentials = base64.b64encode(client_credentials.encode('utf-8')).decode('utf-8')
    headers = {
        'Authorization': f'Basic {encoded_credentials}'
    }
    response = requests.get(TOKEN_URL, headers=headers)
    if response.status_code == 200:
        token_data = response.json()
        return token_data['access_token']
    else:
        raise Exception(f"Error getting access token: {response.text}")

# Helper function to fetch employee list
def get_employee_list(access_token, company_id=COMPANY_ID, limit=100, offset=None):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
        'grant_type': 'client_credentials'
    }
    url = EMPLOYEE_LIST_URL_TEMPLATE.format(companyId=company_id)
    params = {"limit": limit}
    if offset is not None:
        params["offset"] = offset
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error fetching employee list: {response.status_code} - {response.text}")

# Helper function to extract relevant fields from employee data
def extract_employee_data(employee):
    # Exclude terminated employees
    employment_status = employee.get('employmentInfo', {}).get('employmentStatus', '')
    if employment_status == 'T':  # Assuming 'T' represents terminated employees
        return None

    # Extract primary name from the names array
    names = employee.get('names', [])
    first_name, last_name = "", ""
    if names:
        primary_name = names[0]  # Assuming the first entry is the primary name
        first_name = primary_name.get('firstName', '')
        last_name = primary_name.get('lastName', '')

    # Extract job title and department info
    business_title = employee.get('employmentInfo', {}).get('businessTitle', 'Unknown')
    employee_type = employee.get('employmentInfo', {}).get('employeeType', 'Unknown')

    # Extract department details
    department_info = employee.get('departmentSplit', [])
    department_id = department_name = "Unknown"
    if department_info:
        department_id = department_info[0].get('deptId', 'Unknown')
        department_name = department_info[0].get('departmentName', 'Unknown')
    
    # Extract other relevant fields
    employee_id = employee.get('employeeId', '')
    supervisor_id = employee.get('supervisorId', '')
    citizenship_status = employee.get('workEligibility', {}).get('citizenshipStatus', '')
    birthdate = employee.get('bioInfo', {}).get('birthdate', '')
    gender = employee.get('bioInfo', {}).get('gender', '')

    return {
        'employeeId': employee_id,
        'firstName': first_name,
        'lastName': last_name,
        'businessTitle': business_title,  # Adding job title
        'employeeType': employee_type,    # Adding employee type
        'supervisorId': supervisor_id,
        'citizenshipStatus': citizenship_status,
        'birthdate': birthdate,
        'gender': gender,
        'departmentId': department_id,    # Adding department ID
        'departmentName': department_name  # Adding department name
    }

# Function to save employee data to a CSV file
def save_employee_list_to_csv(employee_data):
    # Get current year and month
    current_year = datetime.now().year
    current_month = datetime.now().month

    # Create directory if it doesn't exist
    output_dir = os.path.join(BASE_DIR, str(current_year), str(current_month))
    os.makedirs(output_dir, exist_ok=True)

    # Path for the CSV file
    output_csv_path = os.path.join(output_dir, 'employee_list.csv')

    # Extract and flatten relevant employee data, excluding terminated employees
    flattened_data = [extract_employee_data(employee) for employee in employee_data if extract_employee_data(employee)]

    # Define the CSV columns
    fieldnames = ['employeeId', 'firstName', 'lastName', 'businessTitle', 'employeeType', 'supervisorId',
                  'citizenshipStatus', 'birthdate', 'gender', 'departmentId', 'departmentName']

    # Write to the CSV file
    with open(output_csv_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(flattened_data)

    print(f"Employee list saved to {output_csv_path}")

# Main function to fetch data and generate CSV
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
            response_data = get_employee_list(token, company_id=COMPANY_ID, offset=offset)
            employee_data = response_data.get('data', {}).get('employeeData', [])
            all_employees.extend(employee_data)
            
            # Check if there are more employees to fetch
            has_more = response_data.get('data', {}).get('hasMore', False)
            
            # Set offset for the next request only if there are more employees
            if has_more:
                offset = offset + 100 if offset is not None else 101  # Start at 101 for second request
        
        # Once we have all the employees, generate the CSV
        save_employee_list_to_csv(all_employees)

    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
