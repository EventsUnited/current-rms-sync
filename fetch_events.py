import requests
import datetime
import gspread
from google.oauth2.service_account import Credentials

# CONFIGURATION
subdomain = "eventsunited"
api_token = "6fz77CKrkmGez-aFmBQz"
sheet_id = "1vtrgixjjL8BoVCkoJhqTSh24Wlc2ORWjHEFRVnj1BQU"
sheet_tab_name = "APR 2025"
service_account_file = "/Users/tim/API Scheduler/events-united-sheets-api-7f6a70b8c083.json"

# Setup Google Sheets API
creds = Credentials.from_service_account_file(
    service_account_file,
    scopes=["https://www.googleapis.com/auth/spreadsheets"]
)
gc = gspread.authorize(creds)
sh = gc.open_by_key(sheet_id)

# Ensure worksheet exists
try:
    sheet = sh.worksheet(sheet_tab_name)
except gspread.exceptions.WorksheetNotFound:
    sheet = sh.add_worksheet(title=sheet_tab_name, rows="100", cols="100")

# Clear the sheet
sheet.clear()

# Start calendar generation
start_date = datetime.date(2025, 4, 1) - datetime.timedelta(days=5)
end_date = datetime.date(2025, 4, 30)
date_range = [start_date + datetime.timedelta(days=i) for i in range((end_date - start_date).days + 6)]

# Starting column index (F = column 6)
start_col = 6
start_row = 9

# Format day names
day_row = [""] * (start_col - 1) + [d.strftime("%a") for d in date_range]
sheet.update(f"A{start_row}", [day_row])

# Format dates (e.g., 4/1/25)
date_row = [""] * (start_col - 1) + [d.strftime("%-m/%-d/%y") for d in date_range]
sheet.update(f"A{start_row + 1}", [date_row])

# Placeholder for 7 rows of event detail lines (rows 1–7)
for row_idx in range(1, 8):
    sheet.update(f"A{row_idx}", [[""] * len(day_row)])

print("✅ 'APR 2025' tab initialized and formatted.")
