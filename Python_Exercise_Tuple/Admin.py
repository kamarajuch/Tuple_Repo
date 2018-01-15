from utility import *
from DBHandler import *


def ticket_fare_modifier():
    """
    This function modifies the data of ticketing table
    :return: dict : returns ticketing_table
    """
    global ticketing_table
    start_bus_stop,end_bus_stop = stopsValidation()
    while True:
        passenger_fare_choice = check("Enter New Passenger Fare for\n1.Adult\n2.Child\n3.exit",3)

        if passenger_fare_choice == '1':
            passenger_new_fare = check("Enter new fare for Adult : ",0)
            ticketing_table[(start_bus_stop,end_bus_stop)]['Adult'] = passenger_new_fare

        elif passenger_fare_choice == '2':
            child_flag = check("Do You want to add or remove child fare\n1.ADD child\n2.Remove child\n3.Exit \nYour choice is : ",3)
            if child_flag == '1':
                passenger_new_fare = check("Enter new fare for Child : ",0)
                ticketing_table[(start_bus_stop,end_bus_stop)]['Child'] = passenger_new_fare

            elif child_flag == '2':
                if 'Child' in ticketing_table[(start_bus_stop,end_bus_stop)].keys():
                    del(ticketing_table[(start_bus_stop,end_bus_stop)]['Child'])
                else:
                    print('-------No child at given stops--------')
            elif child_flag == '3':
                break
            else:
                print('Entered choice is wrong \nRe-Enter correct choice - 1 or 2 ')
        elif passenger_fare_choice == '3':
            break
        else:
            print('Entered choice is wrong \nRe-Enter correct choice - 1 or 2 or 3 ')
    # print('tkt modify : ',ticketing_table)
    return ticketing_table


def passenger_age_modifier():
    """
    This function modifies age limit of Adults & Children
    :return: dict : returns modified age limit of adults & Children
    """
    global ages
    while True:
        print('AgeLimit Conditions : adult maximum age not be >100,Diffrence b/w Adult_mininmum and child_maximum should be equals to one')
        adult_max_age = check('Enter maximum age of adult : ',2)
        adult_min_age = check('Enter minimum age of adult : ',2)
        child_max_age = check('Enter maximum age of child : ',2)
        child_min_age = check('Enter minimum age of child : ',2)
        if (adult_max_age<=100) and ((adult_min_age-child_max_age) == 1)and(adult_min_age<adult_max_age) and (child_min_age<child_max_age):
            ages[0]['Adult_min_age'], ages[0]['Adult_max_age'], ages[0]['child_min_age'], ages[0]['child_max_age'] = adult_min_age, adult_max_age, child_min_age, child_max_age
            print("Age limit of passengers are modified. ")
            break
        else:
            print("-----Invalid AgeLimit Conditions-----\nRe-enter Valid AgeLimit conditions")

    return ages


def trip_discount_modifier():
    """
    This function modifies the data of trip discounts
    :return: dict : returns trip discounts modified data
    """
    global ticketing_table,start_stops,end_stops
    start_bus_stop,end_bus_stop = stopsValidation()
    while True:

        choice = check("Enter the choice for \n1.Add/Modify TripDiscount(1%-100%)\n2.Add/Modify DiscountFlag\n3.PassengerCount\n4.Exit ",4)
        if choice == '1':
            passenger_trip_disc = check("Enter the discount rate for passenger : ",2)
            ticketing_table[(start_bus_stop,end_bus_stop)]['TripDiscount'] = passenger_trip_disc
            print('----Trip Discount is added/modified---')
        elif choice == '2':
            discount_flag = check("Enter DiscountFlag \n1.CHILD\n2.ADULT\n3.TOTAL",3)
            discount_flag_dict = {'1':'CHILD','2':'ADULT','3':'TOTAL'}
            if discount_flag in discount_flag_dict.keys():
                ticketing_table[(start_bus_stop,end_bus_stop)]['TripDiscountFlag'] = discount_flag_dict[discount_flag]
                print("----Trip Discount Flag ->'%s' is added/modified---"%(discount_flag_dict[discount_flag]))
            else:
                print("--------Invalid Discount Flag---------\nRe-enter the correct input 1 or 2 or 3")
        elif choice == '3':
            passenger_trip_count = check("Enter the passenger trip count : ",0)
            if passenger_trip_count!=0:
                ticketing_table[(start_bus_stop,end_bus_stop)]['PassengerCount'] = passenger_trip_count
                print('----Passenger count is added/modified---')
            else:
                print('----InValid PassengerCount---\nRe-enter option 3 again')
        elif choice == '4':
            break
    return ticketing_table

def passenger_discount_modifier():
    global ticketing_table,start_stops,end_stops
    start_bus_stop,end_bus_stop = stopsValidation()
    while True:
        choice = check("Enter the choice for \n1.Add/Modify PassengerDiscount(1%-100%)\n2.Add/Modify PassengerDiscountFlag\n3.PassengerTripCount\n4.Exit ",4)
        if choice == '1':
            passenger_trip_disc = check("Enter the discount rate for passenger : ",2)
            ticketing_table[(start_bus_stop,end_bus_stop)]['PassengerDiscount'] = passenger_trip_disc
            print('----Passenger Discount is added/modified---')
        elif choice == '2':
            discount_flag = check("Enter PassengerDiscountFlag \n1.CHILD\n2.ADULT\n3.TOTAL",3)
            discount_flag_dict = {'1':'CHILD','2':'ADULT','3':'TOTAL'}
            if discount_flag in discount_flag_dict.keys():
                ticketing_table[(start_bus_stop,end_bus_stop)]['PassengerDiscountFlag'] = discount_flag_dict[discount_flag]
                print("----Passenger Discount Flag ->'%s' is added/modified---"%(discount_flag_dict[discount_flag]))
            else:
                print("--------Invalid PassengerDiscount Flag---------\nRe-enter the correct input 1 or 2 or 3")
        elif choice == '3':
            passenger_trip_count = check("Enter the passenger trip count : ",0)
            if passenger_trip_count!=0:
                ticketing_table[(start_bus_stop,end_bus_stop)]['PassengerTripCount'] = passenger_trip_count
                print('----Passenger Trip count is added/modified---')
            else:
                print('----InValid Passenger TripCount---\nRe-enter option 3 again')
        elif choice == '4':
            break
    return ticketing_table

def write_admin(ticketing_table,ages):
    # Formatting the passengers data to required written format to file
    print(ticketing_table)
    global_modifier(ticketing_table,ages) # updating the global variables
    final_data = []
    for eachkey in ticketing_table.keys():
        data_table = list(zip(['Source','Destination'],[ v for v in eachkey]))
        sub_items = [v for v in list(ticketing_table[eachkey].items())]
        [data_table.append(i) for i in sub_items]
        final_data.append(dict(data_table))
        data_table = []             # making list as empty end of iteration.
    # writing to file
    # print(final_data)
    set_data('passengers_data',final_data)
    set_data('AgeLimits',ages)


def admin_access():
    """
    This function executes the sequence of Admin
    :return: list of list/list : returns modified data
    """
    global ticketing_table,ages,start_stops,end_stops
    # Reading global variables
    ticketing_table,ages = read_global_vars()
    while True:
        choice = check("Do you want to modify \n1.TicketFare table\n2.Age limit of Passenger\n3.Trip Discounts\n4.PassengerDiscount\n5.Exit Admin access\nPress respective input - 1 or 2 or 3 or 4 or 5 ==>",1)
        if choice == '1':
            ticketing_table = ticket_fare_modifier() # Access to Ticket fare modification
        elif choice == '2':
            ages = passenger_age_modifier()         # Access to Age limit modification
        elif choice == '3':
            ticketing_table = trip_discount_modifier()  # Access to Trip discounts Modification
        elif choice == '4':
            ticketing_table = passenger_discount_modifier()
        elif choice == '5':
            break
        else:
            print('Entered choice is wrong \nRe-Enter correct choice - 1 or 2 ')
    write_admin(ticketing_table,ages)

