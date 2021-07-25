import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPE_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPE_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')

def get_sales_data():
    """
    Gets Sales figure data from user
    """

    print("Please enter sales data from last market.")
    print("Data should be six numbers, seperated by a commas")
    print("Example 10,20,30,40,50,60\n")

    data_str = input("Enter your data here: ")
    print(f"The data you entered was {data_str}")

get_sales_data()
