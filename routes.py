from fastapi import FastAPI, HTTPException
import gspread
from google.oauth2.service_account import Credentials

# Load credentials & initialize Google Sheets API
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file("tasa-451512-264c90afc971.json", scopes=SCOPES)
client = gspread.authorize(creds)

# Open the Google Sheet
SPREADSHEET_NAME = "teacher_and_student_app"
try:
    sheet = client.open_by_key("1fJwfK4CJWRB_4fVSk8zlNu1nZMMH_cu9koifz2KFQfw").sheet1  # First sheet
except Exception as e:
    raise HTTPException(status_code=500, detail=f"Error opening sheet: {e}")

# FastAPI app instance
app = FastAPI()

@app.get("/")
def home():
    return {"message": "Teacher & Student Management API is running!"}

@app.get("/students")
def get_students():
    try:
        data = sheet.get_all_records()
        return {"students": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching student data: {e}")

@app.post("/update_student")
def update_student(student_name: str, marks: int):
    try:
        records = sheet.get_all_records()
        for i, record in enumerate(records, start=2):  # Row index starts from 2 (after headers)
            if record["Name"] == student_name:
                sheet.update_cell(i, 5, marks)  # Assuming marks are in column 5
                return {"message": f"Updated {student_name}'s marks to {marks}"}
        return {"error": "Student not found"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating student data: {e}")
