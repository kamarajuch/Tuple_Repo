import pymysql

hostName = 'localhost'
userName = 'root'
password = 'root'
database = 'Reservation_NF'


def databaseHandler():
    """
    This function opens SQL DB handler and creates cursor Object
    :param database: str :Name of the database
    :return: void : nothing returns
    """
    global curObj,dbObj
    dbObj = pymysql.connect(host=hostName, user=userName, passwd=password, db=database, cursorclass=pymysql.cursors.DictCursor)
    curObj = dbObj.cursor()
    execute('use ' + database)


def get_data(tableName):
    """
    This function fetches the data from given table in SQL DB
    :param tableName: str : name of the table
    :return: dict : returns data of given table
    """
    databaseHandler()
    data= []
    if tableName == 'passengers_data':
        # print(data)
        execute("select passengers_data.id,passengers_data.Source,passengers_data.Destination,ticket_fare.passenger, ticket_fare.fare,discounts.discount_type,discounts.discount,discounts.number,discounts.flag  from passengers_data INNER JOIN ticket_fare ON ticket_fare.id = passengers_data.id LEFT JOIN discounts ON discounts.id = passengers_data.id;")
        final = curObj.fetchall()
        print("Final",final)
        for a in final:
            for k,v in a.items():
                if k =='discount_type':
                    if a['discount_type'] == 'TripDiscount':
                        d={}
                        d.update({a['discount_type']:a['discount'],a['passenger']:a['fare'],'TripDiscountFlag':a['flag'],'PassengerCount':a['number']})
                    elif a['discount_type']== 'PassengerDiscount':
                        d={}
                        d.update({a['discount_type']:a['discount'],a['passenger']:a['fare'],'PassengerDiscountFlag':a['flag'],'PassengerTripCount':a['number']})
                    elif a['discount_type']== None:
                        d={}
                        d.update({a['passenger']:a['fare']})
            del (a['discount_type'],a['passenger'],a['discount'],a['fare'],a['flag'],a['number'])
            a.update(d)
            data.append(a)
        index = [id+1 for id in range(len(data)-1) if data[id]['id']==data[id+1]['id']]
        dat = [data[id].update(data[id+1]) for id in range(len(data)-1) if data[id]['id']==data[id+1]['id']]
        removed_data = [data.remove(data[i]) for i in sorted(index,reverse=True)]
    else:
        execute('select * from '+tableName)
        data = curObj.fetchall()
    closeHandler()
    return data


def execute(cmd):
    """
    This function executes SQL command
    :param cmd: str : command to be executed
    :return: command output
    """
    return curObj.execute(cmd)


def set_data(tableName,ipDict) :
    databaseHandler()
    print("ip : ",ipDict)
    if tableName != 'passengers_data':
        execute('delete from '+tableName+';')
        for eachvalue in ipDict:
            print('eachvalue ==>',eachvalue)
            eachvalue = list(zip(*eachvalue.items()))
            print('After zipping ==>',eachvalue)
            columns = ','.join(['%s' for i in range(len(eachvalue[0]))]) if not isinstance(eachvalue,str) else '%s'
            print('columns==>',columns)
            print("Insert "+tableName+" ("+columns%(eachvalue[0])+") "+"values"+str(eachvalue[1]))
            execute("Insert "+tableName+" ("+columns%(eachvalue[0])+") "+"values"+str(eachvalue[1]))
    else:
        [execute('delete from '+tableName+';') for tableName in ('ticket_fare','discounts')]
        for v in ipDict:
            if "PassengerDiscount" in v.keys():
                execute("insert into discounts values('%s','%s','%s','%s','%s');"%(str(v['id']),"PassengerDiscount",str(v["PassengerDiscount"]),str(v["PassengerTripCount"]),str(v["PassengerDiscountFlag"])))
            if "TripDiscount" in v.keys():
                execute("insert into discounts values('%s','%s','%s','%s','%s');" % (str(v['id']), "TripDiscount", str(v["TripDiscount"]), str(v["PassengerCount"]), str(v["TripDiscountFlag"])))
            if "Adult" in v.keys():
                execute("insert into ticket_fare values('%s','%s','%s');"%(str(v['id']),"Adult",str(v["Adult"])))
            if "Child" in v.keys():
                execute("insert into ticket_fare values('%s','%s','%s');" % (str(v['id']), "Child", str(v["Child"])))
    dbObj.commit()
    closeHandler()


def closeHandler():
    """
    closes database handler
    :return: void :  nothing returns
    """
    dbObj.close()

# da=get_data('passengers_data')
# print('da',da)
# set_data('passengers_data',da)
