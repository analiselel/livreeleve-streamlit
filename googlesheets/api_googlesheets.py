import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import openpyxl

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = "1UrHlSlGhGGx6NZa1YqrT7gqMkCbvqcmRVcACy2JYopo"
SAMPLE_RANGE_NAME = "Backup!A1:D"


def main():
    creds = None
    
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("sheets", "v4", credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME).execute()
        valores = result['values']
        
        # Create a new Excel workbook
        wb = openpyxl.Workbook()
        ws = wb.active
        
        # Write the values to the Excel workbook
        for row in valores:
            ws.append(row)
        
        # Save the Excel workbook
        wb.save("movimentacao_estoque.xlsx")
        
        print("Planilha do Excel gerada com sucesso.")

    except HttpError as err:
        print(err)


if __name__ == "__main__":
    main()
