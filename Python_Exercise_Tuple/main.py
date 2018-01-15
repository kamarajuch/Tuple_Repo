from DBHandler import *
from utility import *
from Admin import admin_access
from User import user_access


def main():
    """
    This function executes the flow of sequence
    """
    while True:
        user_choice = check_login("User Login : 'ADMIN' or 'USER' : ")

        if user_choice == 'ADMIN': # Admin entry
            admin_access() # Accessing to Admin

        elif user_choice == 'USER': # User entry
            user_access() # USER access


def passengers_data():
    """
    This function reads passengers data from SQL table
    :return: dict : formated dictionary for ticketing table and ages table
    """
    global ticketing_table, ages
    data_of_passengers = get_data('passengers_data') # reads the raw data from database file
    # print('raw data :',data_of_passengers)
    ages = get_data('AgeLimits')

    if len(data_of_passengers)>0 and len(ages)>0:
        raw_data_of_passengers = [dict(tuple(map(convert,(k,v))) for k,v in val.items()) for val in data_of_passengers]
        ages = [dict(tuple(map(convert,(k,v))) for k,v in val.items())for val in ages]
        # Extracting the data of passengers in required format(dictionary)
        ticketing_table = {(raw_data_of_passengers[i]['Source'],raw_data_of_passengers[i]['Destination']):dict([item for item in list(raw_data_of_passengers[i].items())if (item[1]!='NULL' and item[1]!=None) and  item[0]!='Source' and item[0]!='Destination']) for i in range(len(raw_data_of_passengers))}
    return ticketing_table,ages


if __name__ == '__main__':
    global ticketing_table, ages
    ticketing_table, ages = [],[]
    ticketing_table,ages = passengers_data()
    if ticketing_table and ages:
        # print('main :',ticketing_table)
        global_modifier(ticketing_table,ages) # updating the global variables
        main() # calling main function
    else:
        print("wrong/empty/incorrect format database \nplease check and re run the program...")
