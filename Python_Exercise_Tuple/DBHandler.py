from utility import *


def get_data(filename):
    """
    This function reads the data from the given file
    :param filename: str :Path of the file to be read
    :return: list of dict : returns whole data of file
    """
    data = list() ; data_input = [];heading = []
    with open(filename+'.txt') as file_map:
        for row in file_map:
            if not row.startswith('#'):
                row = row.rstrip().rstrip(',').split(',')
                # print(row)
                if len(row) == len(heading):
                    a = dict([(heading[i],row[i])for i in range(len(heading))])
                    # print([tuple(map(convert,(heading[i],row[i])))for i in range(len(heading)) if row[i]!='N'])
                    data.append(a)
                else:
                    print("Input File is Empty or Incorrect format \nplease check and re run the program....")
                    data=[]
                    break
            else:
                heading = row.rstrip().rstrip(',').split(',')[1:]
                data_input.append(data)
        # print('data=====>',data)
    return data


def set_data(filename,*sequence_of_data):
    """
    This function writes the data to file
    :param filename: str :Path of the file to be written
    :param sequence_of_data: list of list : data to be written
    :return: void : Nothing returns
    """
    with open(filename+'.txt','w') as wfile:
        data_keys = {'passengers_data':[['Source','Destination','Adult','Child','PassengerCount','TripDiscount','TripDiscountFlag','PassengerDiscount','PassengerTripCount','PassengerDiscountFlag']],
                      'AgeLimits':[['Adult_min_age','Adult_max_age','child_min_age','child_max_age']],
                      'userdata':[['username','source','destination','Tripcount']]
                     }
        for id,each_sequence in enumerate(sequence_of_data):
            wfile.write('#,')
            [wfile.write(v+',') for v in data_keys[filename][id]]
            wfile.write('\n')
            for each_dict in each_sequence:
                for eachkey in data_keys[filename][id]:
                    if eachkey in each_dict.keys():
                        if (isinstance(each_dict[eachkey],int)) or (type(each_dict[eachkey]) == float):
                            wfile.write(str(each_dict[eachkey])+',')
                        else:
                            wfile.write(each_dict[eachkey]+',')
                    else:
                        each_dict[eachkey] = 'NULL'
                        wfile.write(each_dict[eachkey]+',')
                wfile.write('\n')

# if __name__ == '__main__':
#     d=[['Source','Destination','Adult','Child','TripDiscount','TripDiscountFlag','PassengerDiscount','PassengerTripCount','PassengerDiscountFlag']]
#     final_data= get_data('passengers_data')
#     print(final_data)
#     data1 = get_data('AgeLimits')
#     set_data('passengers_data1',d,final_data)
#     print(final_data)
#     print(data1)
