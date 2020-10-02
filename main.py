import csv
import os
import sys
import time
from tabulate import tabulate
from api_handler import ApiHandler

def clear():
    '''
    Clears the screen based on the OS type
    '''
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

clear()

# Printing Application Banner
print('*' * 40)
print(f"{'Welcome to Fuel Checker':*^40}")
print('*' * 40)
print("\n")

def postcode_exists(code):
    '''
    Input postal code 
    Returns:
        True if code is a valid NSW postcode
        False otherwise
    '''
    # Working out the current path
    abs_path = os.path.abspath(__file__)
    main_dir = os.path.dirname(abs_path)
    suburbs_csv = f"{main_dir}/suburbs.csv"
    with open(suburbs_csv, 'r') as f:
        lines = csv.reader(f)
        for line in lines:
            if str(code).startswith('2') and len(str(code)) == 4 and code == line[0]:
                return True
    return False

def ask_region():
    '''
    User Input:
        Either NSW Suburb name or Postcode (Delivery Area)
    Returns:
        Postal Code of NSW Delivery Area
    Example: 2000, 2170
    '''
    # Create ApiHandler Class instance
    # This class handles all API calls and data collections
    api = ApiHandler()
    print("This app will find petrol stations around you")
    print("based on the 'suburb' or 'postcode' provided.\n")
    print("press 'q' to quit.\n")

    user_input = input('Please Enter your Postcode or Suburb: (q to exit)\n')
    while True:
        clear()
        if user_input.lower() == 'q':
            print('Thanks for using this app, Bye!')
            sys.exit()
        if user_input.isnumeric():
            if postcode_exists(user_input):
                return user_input
            else:
                print('Entered Postcode is not valid NSW Delivery Area Postal Code')
                print('Please make sure the postcode is a valid postcode (e.g.: starts with 2 and 4 digit long)')
        else:
            postcode = api.get_postcode(user_input)
            if postcode:
                return postcode
            else:
                print("The system cannot match the entered suburb to a valid NSW postal code.")
                print("Please enter valided or nearby adjacent suburbs...")
        user_input = input('Please Enter Postcode or Suburb: \n')

def stations_by_postcode():
    '''
    User need to provide Location (NSW Only):
     - Postcode (Delivery Area)
     - Suburb
    '''
    # Initiate API Handling Class
    api = ApiHandler()
    # Obtain User  input (location info)
    region = ask_region() 
    # calling API stage
    # API call uses free account, hence the limit of API call per minute
    # if quoata is exceeded, Error will be thrown, catching it here
    try:
        ps = api.stations_with_fuel_types(region)
    except Exception as e:
        # Trying to wait for one more minute to see if the quoata limit is lifted.
        print(e)
        print("There has been an network issue, trying in a minute again...")
        print("Please be patient...")
        for i in range(1, 7):
            time.sleep(10)
            print(f'{i * 10} seconds elapsed...')
        try:
            # calling API again
            ps = api.stations_with_fuel_types(region)
        except Exception as e2:
            print(e2)
            print("An unknow Network error occurred. The Data(API) privder is being now contacted for further troubleshoot.")
            print("Sorry for any inconvenience, please try this app later again. Thanks!!!")
            sys.exit()
    return ps

def print_table(stns):
    '''
    Receives a list of stations
    Uses 'tabulate' module to print the stations and prices of the fuels in a tabular format
    '''
    # Table Headers to be used by 'tabulate' class
    fuel_headers = ['Station', 'E10', 'U91', 'P95', 'P98', 'LPG', 'DL',]
    # Table actual data to be used by 'tabulate' class
    T = []
    # Station Listing number
    # will be used by later for user selection.
    station_counter = 1
    for stn in stns:
        # price table data holder, empty
        template = ['X' for _ in range(7)]
        # update the table with price
        template[0] = f"{station_counter}) {stn.name}"
        for f in stn.fuel_types:
            if f.fuel_type.upper() == 'E10':
                template[1] = f.price
            if f.fuel_type.upper() == 'U91':
                template[2] = f.price
            if f.fuel_type.upper() == 'P95': 
                template[3] = f.price
            if f.fuel_type.upper() == 'P98': 
                template[4] = f.price
            if f.fuel_type.upper() == 'LPG': 
                template[5] = f.price
            if f.fuel_type.upper() == 'DL': 
                template[6] = f.price
        T.append(template)
        station_counter += 1
    print(tabulate(T, headers=fuel_headers))

def select_station(stns):
    '''
    Receives list of stations
    User selects a station by number
    Returns the selected station number
    '''
    if len(stns) == 0:
        return 0
    stn = input("Please select station from the table (Number only):\n")
    while True:
        if stn.lower() == 'q':
            break
        if stn.isnumeric() and int(stn) in range(1, len(stns) + 1):
            return int(stn)
        clear()
        print_table(stns)
        print()
        print(f"The provided input [{stn}] is not valid")
        print(f"Please use one of the below selection:")
        print(f"{tuple(range(1, len(stns)+1))}\n")
        stn = input("Enter Station number: ")

def station_details(num, stns):
    '''
    Receives selected station number and list of stations
    Prints out selected station details:
     - name
     - brand
     - address 
     - fueltypes
    '''
    if num == 0:
        print('No details found!, Returning to Main Menu.')
        time.sleep(2)
        return 0
    stn = stns[num - 1]
    print(f'Station Brand: {stn.brand}')
    print(f'Station Name: {stn.name}')
    print(f'Station Address: {stn.address}')
    print(f'Offers:')
    for fuel in stn.fuel_types:
        if fuel.fuel_type in ('E10', 'U91', 'P95', 'P98', 'LPG', 'DL'):
            print(f" - {fuel.fuel_name:<12}: {fuel.price:>3} cents")


def main():
    print('You can search fuel prices by location')
    print('Or, search for particular interested Fuel Type: (e.g. E10 or P98)')
    print('You can quit any time by pressing "q".\n')

    try:
        option = input("What would you like to do? \n 1)Search By location\n 2)Search for Fuel Type\n")
        while True:
            if option.lower() == 'q':
                print('Thank you for using this App, Bye!')
                sys.exit()
            if option == '1':
                ps = stations_by_postcode()
                if ps:
                    print_table(ps)
                    option2 = input('Load Prices for different location? (yes/no)')
                    while True:
                        if option2.lower() in ('yes', 'y', 'yeah', 'ok'):
                            ps = stations_by_postcode()
                            print_table(ps)
                        if option2.lower() in ('no', 'nope', 'n', 'nah', 'negative'):
                            break
                        option2 = input('Load Prices for different location? (yes/no)')
                    print()
                    station_num = select_station(ps)
                    print()
                    station_details(station_num, ps)
                    input('Press any key to continue...')
                else:
                    print('No stations found for the given location. Return to main menu...')
                    time.sleep(3)
            if option == '2':
                pass
            clear()
            option = input("What would you like to do? \n 1)Search By location\n 2)Search for Fuel Type\n")
    except KeyboardInterrupt:
        print('Ctrl+C butten is pressed, exiting the programm, Bye!')
        sys.exit()

if __name__ == '__main__':
    main()







