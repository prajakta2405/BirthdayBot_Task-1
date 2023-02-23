import mysql.connector
import env_config
#Can import any library but with a comment of imported eg.
import xyz #imported /*Remove this library when modifying*/
import datetime


#Declaring database cursor /*Do Not Modify*/
mydb = mysql.connector.connect(
            host=env_config.dbHost,
            user=env_config.dbUser,
            password=env_config.dbPass,
            database=env_config.dbName
        )
query = mydb.cursor() #Use this to execute db queries eg query.execute(db_query_here)


def toggleNotify(userId,changeNotify):
    print("Change the value of a column attribute for a particular user.")
    #userId is the id of the user and is primary key in db
    #changeNotify is the variable which gives the value to change i.e On or Off
    #return 0 when option is changed to Off and 1 when On
    #Check both cases i.e if same value present in both just return , if different then change and return
    query.execute("select notify_satus from User where userid=%s",[userId])
    x=query.fetchall()
    if changeNotify in x:
        return
    if changeNotify not in x:
      y="update User set notify_satus=%s where userid=%s"
      query.execute(y(changeNotify,userId))
      mydb.commit()
      return




def insertData(name,date,month,year,userid):
    print("Function for inserting data into the db")
    #check if user exists {try fetching userid and matching with the argument}
    #if exists return 1 , if not then insert the data and return 0
    query.execute("select userid from User where userid=%s",[userid])
    if query.fetchall():
        return 1
    else:
        query.execute("insert into Dates(Name,date,month,year,userid)values(?,?,?,?,?)",(name,date,month,year,userid))
        mydb.commit()
        return 0


def removeData(name,date,month,year,userid):
    print("Function for deleting data from the db")
    #check if user exists {try fetching userid and matching with the argument}
    #if exists then delete it and return 0 , if not then return 0
    query.execute("select userid from User where userid=%s",[userid])
    query.fetchall()
    if query.rowcount !=0:
        a="delet from dates where Name=%s,date=%s,month=%s,year=%s ,userid=%s"
        query.execute(a(name,date,month,year,userid))
        mydb.commit()
        return 0
    else:
        return 0

        
    

def retrieveData(userId,parameter,paramId):
    print("Function to return data from db using either userid and (name or date)")
    #paramId{1 or 2} represents the parameter{name or date(01/12)} i.e 1 = userId+name, 2 = userId+date, and 0 or other represents just userId
    #then return all the dates that are fetched but the query
    
    


    if paramId==1:
        query.execute("select date,month from dates where userId=%s and Name=%s",[userId,parameter])
        
    elif paramId==2:
        dt= datetime.datetime.strptime(parameter,'%d/%m')
        x=dt.day +1
        y=dt.month
        query.execute("select date,month from dates where userId=%s and date=%s and month=%s",[userId,x,y])
        
    else:
        query.execute("select date,month from dates where userId=%s",[userId])
        result=query.fetchall()
        for i in result:
            print(i[0]+"/"+i[1])


def getDate(day,month,year):
    print("Function to return birthdate i.e. 1 day post the date of notification")
    #input is date, month and year
    #also consider the month change when date is 1 and also check for leap year when feb month
    #return in string format 01/12

    if((year%400==0 or year%4==0) and month==2):
        next_day=day+1
        next_month=month
        next_year=year
        
    elif(month==2 and day==28):
        next_day=1
        next_month=month+1
        next_year=year
        
    elif(month==12 and day==31):
        next_day=1
        next_month=1
        next_year=year+1
    elif(day==31 ):
        next_day=1
        next_month=month+1
        next_year=year
    elif((day==30) and (month==4 or month==6 or month==9 or month==11)):
        next_day=1
        next_month=month+1
        next_year=year
    else:
        next_day=day+1
        next_month=month
        next_year=year
    
    
    print(next_day +"/"+next_month+"/"+next_year)







