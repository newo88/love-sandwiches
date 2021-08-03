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
    while True:
        print("Please enter sales data from last market.")
        print("Data should be six numbers, seperated by a commas")
        print("Example 10,20,30,40,50,60\n")

        data_str = input("Enter your data here:\n ")

        sales_data = data_str.split(',')

        if validate_data(sales_data):
            print("Data is valid")
            break
    return sales_data


def validate_data(values):
    """
    Inside the try, converts all strings into integers.
    Raises ValueError is string cant be converted to int,
    or if there aint exactly six values.
    """
    print(values)
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values required you entered {len(values)}")

    except ValueError as e:
        print(f"Invalid data: {e} Please try again.\n")
        return False
    return True


def update_worksheet(data, worksheet):
    """
    Recieves a list of integers to be inserted into a worksheet
    Updated the relevant worksheet with the data provided
    """
    print(f'Updating {worksheet} worksheet.\n')
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} worksheet updated successfully.\n")


def calculate_surplace_data(sales_row):
    """
    Compare sales with stock and calculate the surplus for each item type.
    The surplus is defined as the sales figure subtracted from the stock:
    - Positive surplus indicates waste
    - Negative surplus indicates extra made when stock was sold out.
    """
    print("Calculating surplus data...\n")
    stock = SHEET.worksheet('stock').get_all_values()
    stock_row = stock[-1]
    surplace_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplace = int(stock) - sales
        surplace_data.append(surplace)
    return surplace_data


def get_last_5_entries_sales():
    """
    Collects collumns of data from sales worksheet
    """
    sales = SHEET.worksheet("sales")

    columns = []
    for ind in range(1, 7):
        column = sales.col_values(ind)
        columns.append(column[-5:])

    return columns 

def calculate_stock_data(data):
    """
    Calculate the average stock for each item type, adding 10%
    """
    print("Calculating stock data...\n")
    new_stock_data = []

    for column in data:
        int_column = [int(num) for num in column]
        average = sum(int_column) / len(int_column)
        stock_num = average * 1.1
        new_stock_data.append(round(stock_num))

    return new_stock_data




def main():
    """
    run all program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, "sales")
    new_surplace_data = calculate_surplace_data(sales_data)
    update_worksheet(new_surplace_data, "surplus")
    sales_columns = get_last_5_entries_sales()
    stock_data = calculate_stock_data(sales_columns)
    update_worksheet(sales_data, "stock")

print("Welcome to Love Sandwiches Data Automation")
main()