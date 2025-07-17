import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json

# Define the scope
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Load the service account credentials
try:
    with open("/home/ubuntu/service_account.json", "r") as f:
        creds_json = json.load(f)
    
    # Replace escaped newlines with actual newlines in the private_key
    creds_json["private_key"] = creds_json["private_key"].replace("\\n", "\n")

    creds = ServiceAccountCredentials.from_json_keyfile_dict(
        creds_json, scope
    )
    client = gspread.authorize(creds)
except Exception as e:
    print(f"Error loading credentials or authorizing gspread: {e}")
    exit()

# Google Sheet URL provided by the user
sheet_url = "https://docs.google.com/spreadsheets/d/1Dg6g0QFlETa4NdP6eR1qXGudldwe5syK8HbdZZu4h74/edit?gid=0#gid=0"

try:
    # Open the spreadsheet by URL
    spreadsheet = client.open_by_url(sheet_url)
    
    # Assuming the data is in the first sheet (index 0) or named 'Sheet1'
    # You can also open by name: worksheet = spreadsheet.worksheet("Sheet1")
    worksheet = spreadsheet.get_worksheet(0) # Get the first worksheet
    
    # Get all records as a list of dictionaries
    data = worksheet.get_all_records()
    
    if data:
        print("Successfully read data from Google Sheet.")
        print(f"Number of rows: {len(data)}")
        print("First 5 rows:")
        for i, row in enumerate(data[:5]):
            print(f"Row {i+1}: {row}")
        
        # Infer column headers
        if data:
            print("\nInferred Column Headers:")
            print(list(data[0].keys()))
    else:
        print("No data found in the Google Sheet.")

except gspread.exceptions.SpreadsheetNotFound:
    print(f"Error: Spreadsheet not found at URL: {sheet_url}. Please ensure the URL is correct and the service account has access.")
except gspread.exceptions.NoValidUrlKeyFound:
    print(f"Error: Invalid Google Sheet URL format: {sheet_url}. Please provide a valid Google Sheet URL.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")


