# from SQL_DBhandler import *
db = 'TicketReservation'


def global_modifier(ticket, ages_of_passengers):
    """
    This function modifies global variables
    :param ticket: list : Ticket fares
    :param ages_of_passengers: list of list: age of passengers
    :return: ticketing_table, ages
    """
    global ticketing_table, ages

    ticketing_table, ages = ticket, ages_of_passengers
    return ticketing_table, ages

def read_global_vars():
    """
    This function returns all global variables
    :return: ticketing_table,ages
    """
    return ticketing_table, ages


def check_login(login):
    """
    This function validates the given login is user or admin.
    :param login: str : Accepts user login
    :return: str : returns user type
    """
    while True:
        val = None
        val = input(login)
        if val.upper() != 'ADMIN' and val.upper() != 'USER':
            print('----Entered invalid Login-----\nRe-enter valid login input - ADMIN or USER')
        else:
            break
    return val.upper()

def check(input_msg,flag):
    """
    This function validates the given input
    :param input_msg: str : Displays the given message on console
    :return: int : returns an integer value given by user
    """
    while True:
        value=input(input_msg)
        if(value.isnumeric() and int(value) !=0):
            if(flag == 1):
                if(int(value) <=5):
                    return (value)
            elif(flag == 2):
                if(int(value) > 0 and int(value) < 101):
                    return (int(value))
            elif(flag == 0):
                return(int(value))
            elif(flag == 3):
                if(int(value) <= 3):
                    return (value)
            elif(flag == 4):
                if(int(value) <=4):
                    return (value)

        print("---InValid input-----\nRe-Enter valid input")

def convert(param):
    """
    This function converts the type of data to integer if it is numeric
    :param param: list : data contains string type
    :return: int/str : returns the converted data
    """
    if str(param).isnumeric():
        param = int(param)
    elif param == 'None':
        param = None
    else:
        param = param
    return param


def stopsValidation():
    global ticketing_table
    ticketing_table, ages= read_global_vars()
    stops = list(ticketing_table.keys())
    stops = list(zip(*stops))
    # start_stops,end_stops = max(stops[0]),max(stops[1])
    # bus_stops = list(zip(*stops))
    while True:
        source_stop = check("Enter starting stop number: ",0)
        destination_stop = check("Enter ending stop number: ",0)
        if (source_stop == destination_stop) or (source_stop not in stops[0] or destination_stop not in stops[1]):
            print('-------Invalid stops-------\n-----Re-Enter Valid stops')
        elif (source_stop,destination_stop) not in list(ticketing_table.keys()):
            print("--Given stops was not found in database--Please check and re enter correct stops")
        else: break
    return source_stop,destination_stop
