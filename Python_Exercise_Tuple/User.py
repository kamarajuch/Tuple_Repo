from utility import *
from DBHandler import *

def fare_calculator(stop1, stop2, age_list, passenger_count):
    """
    This function calculates the fare of given passengers as per conditions
    :param stop1: int : Starting source of bus stop
    :param stop2: int : Bus stop destination
    :param age_list: list : Age of passengers
    :param passenger_count: Number of passengers
    :return: int/float : Total fare of Passengers(total,adult,child)
    """
    global ticketing_table, stops, ages

    fare_of_passenger = None
    fare = ticketing_table[(stop1,stop2)]
    total_fare = 0; child_fare = 0; adult_fare = 0
    if ('Adult' in list(ticketing_table[(stop1,stop2)].keys())):
        # print("Inside loop")
        # calculates the total fare of passengers
        for age in age_list:
            if age < ages[0]['Adult_min_age']:
                if (age >= ages[0]['child_min_age']) and (age <= ages[0]['child_max_age']):  # allows if age of person between child min age and child max age
                    fare_of_passenger = fare['Child'] if 'Child' in list(fare.keys()) else fare['Adult'] * 0.5
                    child_fare += fare_of_passenger
                else:  # allows age of person below child min age
                    fare_of_passenger = 0
            elif age <= ages[0]['Adult_max_age']:  # allows age of person between adult min age and adult max age
                fare_of_passenger = fare['Adult']
                adult_fare += fare_of_passenger
            else:  # allows age of person more than adult max age
                fare_of_passenger = fare['Adult'] * 0.5
                adult_fare += fare_of_passenger  # check if want to add senior or not

            print('fare of passenger at the age %s : %s' % (str(age), fare_of_passenger))
            total_fare += fare_of_passenger

        total_fare_tdisc, child_fare_tdisc, adult_fare_tdisc = total_fare, child_fare, adult_fare
        if 'PassengerCount' in ticketing_table[(stop1,stop2)]  and passenger_count > ticketing_table[(stop1,stop2)]['PassengerCount']:
            total_fare_tdisc, child_fare_tdisc, adult_fare_tdisc = discount_on_trip(stop1, stop2, total_fare, child_fare, adult_fare)
            # print('tdisc',total_fare_tdisc, child_fare_tdisc, adult_fare_tdisc)

        total_fare_pdisc, child_fare_pdisc, adult_fare_pdisc= discount_on_user(stop1, stop2, total_fare, child_fare, adult_fare)

        total_fare, child_fare, adult_fare  = min(total_fare_pdisc,total_fare_tdisc), min(child_fare_pdisc,child_fare_tdisc),min(adult_fare_pdisc,adult_fare_tdisc)
        # print('pdisc ',total_fare_pdisc, child_fare_pdisc, adult_fare_pdisc)
        return total_fare, child_fare, adult_fare
    else:
        return  None,None,None


def discount_on_trip(stop1, stop2, total_fare, child_fare, adult_fare):
    """
    This function calculates the trip discount on given routes
    :param stop1: int :Starting source of bus stop
    :param stop2: int : Bus stop destination
    :param total_fare: int/float : Total fare of Passengers
    :param child_fare: int/float : Total fare for only child
    :param adult_fare: int/float : Total fare for only adults
    :return: int/float: After discount on total_fare, child_fare, adult_fare
    """
    global stops,ticketing_table

    child_flag = 'CHILD'; adult_flag = "ADULT"; total_flag = "TOTAL"
    # stops = list(zip(*stops))
    keys = list(ticketing_table[(stop1, stop2)].keys())
    if ('TripDiscount' in keys) and ('TripDiscountFlag' in keys):
        disc_trip = float((ticketing_table[(stop1,stop2)]['TripDiscount'])/100)
        flag = ticketing_table[(stop1,stop2)]['TripDiscountFlag']
        if child_flag == flag.upper():
            child_fare = child_fare - (child_fare * disc_trip)
        elif adult_flag == flag.upper():
            adult_fare = adult_fare - (adult_fare * disc_trip)
        elif total_flag == flag.upper():
            total_fare = total_fare - (total_fare * disc_trip)
        else:
            print('Trip Discount Flag is wrong --- Hence No discount applied for given stops')
    else:
        print("Trip Discounts : No discount for given stops ")

    return total_fare, child_fare, adult_fare


def discount_on_user(stop1, stop2, total_fare, child_fare, adult_fare):
    """
    This function calculates fare on passenger discount
    :param stop1: int: source of bus-stop
    :param stop2: int: destination of bus-stop
    :param total_fare: float: fare of the total passengers
    :param child_fare: float: fare of the child passengers
    :param adult_fare: float: fare of the adult passengers
    :return: float: return fare of total, adult, child passengers
    """
    global user_disc_dict, stops, user_name,user_dict, passenger_discounts
    keys = list(ticketing_table[(stop1, stop2)].keys())
    # print('k==>',keys)
    if ("PassengerDiscount" in keys) and ("PassengerTripCount" in keys) and ("PassengerDiscountFlag" in keys):
        disc_trip = float((ticketing_table[(stop1,stop2)]['PassengerDiscount'])/100)

        flag = ticketing_table[(stop1,stop2)]['PassengerDiscountFlag']
        child_flag = 'CHILD'; adult_flag = "ADULT"; total_flag = "TOTAL"

        user_disc_dict = {(user_name,stop1,stop2):ticketing_table[(stop1,stop2)]['PassengerTripCount']}
        if (user_dict[(user_name,stop1,stop2)]%user_disc_dict[(user_name,stop1,stop2)]) == 0:
            if child_flag == flag.upper():
                child_fare = child_fare - (child_fare * disc_trip)
            elif adult_flag == flag.upper():
                adult_fare = adult_fare - (adult_fare * disc_trip)
            elif total_flag == flag.upper():
                total_fare = total_fare - (total_fare * disc_trip)
            else:
                print("Passenger Discount/Passenger discount Flag is wrong --- Hence No discount applied for given stops")
        else:
            print("Passenger Discounts : No discount for given stops ")
    else:
        print("Passenger Discounts : No discount for given stops ")

    return total_fare, child_fare, adult_fare


def user_id(userDict):
    """
    This function handles the user log in
    :param userDict: dict : dict :data user records
    :return: dict/str : returns source,destination,user dictionary
    """
    global passenger_discounts,stops,user_name

    source_stop , destination_stop = stopsValidation()
    if (user_name,source_stop,destination_stop) in list(userDict.keys()):
        userDict[(user_name,source_stop,destination_stop)]+=1
    else:
        userDict.update({(user_name,source_stop,destination_stop):1})
    executeUser(source_stop , destination_stop)

    return userDict


def executeUser(source_stop,destination_stop):
    # Reading global variables
    global ticketing_table, ages,stops
    ticketing_table, ages= read_global_vars()
    # print('user tkts : ',ticketing_table)
    stops = list(ticketing_table.keys())
    stops = list(zip(*stops))
    # Entry to fare calculation
    no_of_passenger = check("Enter number of passengers travelling : ",0)
    age_of_passenger = [check("Enter age of passenger : ",2) for passenger in range(int(no_of_passenger))]

    #calculates fare of passengers
    fare_total, fare_child, fare_adult = fare_calculator(int(source_stop), int(destination_stop), age_of_passenger,int(no_of_passenger))
    if fare_total != None and fare_child != None and fare_adult != None:
        print('TotalFare : %s\nChildFare : %s\nAdultFare:%s\n' % (fare_total, fare_child, fare_adult))
    else:
        print("---Adult/Child fare is not available for given stops---Please check database and re run program")


def write_user(user_dict):

    data_table =[] ; user_data = []
    #Formatting data to written format to file
    for eachkey in user_dict.keys():
        data_table = list(zip(['username','source','destination'],[v for v in eachkey]))
        data_table.append(('Tripcount',user_dict[eachkey]))
        user_data.append(dict(data_table))
        data_table = []
    # writing modified user data to file
    set_data('userdata',user_data)


def user_access():
    """
    This function executes the sequence of USER
    :return: void : Nothing returns
    """
    global user_name,user_dict
    # Reading user records from database file(txt)
    user_records = get_data('userdata')
    user_records = [dict(tuple(map(convert,(k,v))) for k,v in val.items())for val in user_records]
    user_dict = {}
    if user_records :
        for i in range(len(user_records)):
            user_dict.update({(user_records[i]['username'],user_records[i]['source'],user_records[i]['destination']):user_records[i]['Tripcount']})
    while True:
        log_in_option = check("User log in :\n1.Sign in\n2.Sign up\n3.Exit ",3)
        if log_in_option != '1' and log_in_option != '2' and log_in_option != '3':
            print("----InValid login----\n Re-enter valid log in")
        elif log_in_option == '3': break
        else:
            flag = False
            user_name = input("Enter user name :")
            keys = [key[0] for key in list(user_dict.keys())]
            if (log_in_option == '1') and (user_name not in keys):
                print('Invalid User Name. Please login with correct user name')
            elif (log_in_option == '2') and (user_name in keys):
                print("User name already exists.Try other username")
            else:
                user_dict = user_id(user_dict) # Tracking user data if new user entry/updating values of old users
                flag = True
                print("====================USER Trip Completed================================")
                # print('outer loop :',user_dict)
        while flag:
            choice = input("Do you want to make one more trip?(Y/N) ==>")
            if choice.upper() == 'Y':
                user_dict = user_id(user_dict)
                flag = True
            elif choice.upper() == 'N': break
            else: print("---InValid input---\nRe-enter valid input 'Y'or 'N' ")
            print("====================USER Trip Completed================================")
            # print('inner loop :',user_dict)
        write_user(user_dict)




