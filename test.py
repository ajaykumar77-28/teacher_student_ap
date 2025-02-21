import gspread
from google.oauth2.service_account import Credentials

# Define the correct scopes
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# Load credentials with updated scopes
creds = Credentials.from_service_account_file("tasa-451512-264c90afc971.json", scopes=SCOPES)
client = gspread.authorize(creds)

# Open Google Sheet
sheet = client.open_by_key("1fJwfK4CJWRB_4fVSk8zlNu1nZMMH_cu9koifz2KFQfw").sheet1

# Read data
data = sheet.get_all_records()
print(data)

for sheet in client.openall():
    print(sheet.title)

