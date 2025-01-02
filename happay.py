import os
import pandas as pd
import requests
import uuid
import json

# Function to generate requestId and userId
def generate_ids():
    request_id = str(uuid.uuid4())
    user_id = f"usr_{uuid.uuid4().hex}"
    return request_id, user_id

# Function to determine title based on gender
def get_title(gender):
    return "Mr." if gender.lower() == "male" else "Ms."

# Function to construct email if missing
def construct_email(first_name, last_name):
    return f"{first_name.lower()}.{last_name.lower()}@happay.in"

# Read the input file (Excel/CSV)
def read_file(file_path):
    if file_path.endswith(".csv"):
        return pd.read_csv(file_path)
    elif file_path.endswith(".xlsx"):
        return pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported file format. Use .csv or .xlsx.")

# API call to provision users
def provision_user(payload, token):
    url = 'https://api-v2.happay.in/auth/v1/cards/add_user/'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        return response.json().get("userId", "Unknown")
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

# Main function to process the file and make API calls
def main(file_path):
    # Check if file_path is empty or file is in the same directory as the script
    if not file_path:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, "sample_file.csv")  # Replace with your file name
        print(f"Defaulting to file in the same directory: {file_path}")

    # Validate file existence
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    token = "iiKZR5dXUwwku5xjUMg0D46zQ"  # Bearer token

    # Read user data from the file
    try:
        user_data = read_file(file_path)
    except Exception as e:
        print(f"Failed to read file: {e}")
        return

    for _, row in user_data.iterrows():
        # Extract user details from the row
        first_name = str(row.get("First Name", "Unknown"))
        last_name = str(row.get("Last Name", "Unknown") or '')
        email = row.get("Email", construct_email(first_name, last_name))
        mobile_no = str(row.get("Mobile", ""))
        mobile_extension = str(row.get("mobile_extension", "+91"))
        dob = row.get("Date of Birth", "")
        gender = row.get("Gender", "Male")
        cost_centre = row.get("Cost Centre", "")
        cost_category = row.get("Cost Category", "")
        designation = row.get("Designation", "")
        department = row.get("Department", "")

        # Generate unique IDs
        request_id, user_id = generate_ids()

        # Construct payload
        payload = {
            "requestId": request_id,
            "userId": user_id,
            "firstName": first_name,
            "lastName": last_name,
            "emailId": email,
            "mobileNo": mobile_no,
            "mobile_extension": mobile_extension,
            "dob": dob,
            "title": get_title(gender),
            "gender": gender,
            "extra_fields": {
                "cost_centre": cost_centre,
                "cost_category": cost_category,
                "designation": designation,
                "department": department
            }
        }

        # Make the API call
        print(f"Provisioning user: {first_name} {last_name} ({email})")
        happay_user_id = provision_user(payload, token)
        if happay_user_id:
            print(f"User provisioned successfully. Happay User ID: {happay_user_id}")
        else:
            print("Failed to provision user.")

if __name__ == "__main__":
    main('')
