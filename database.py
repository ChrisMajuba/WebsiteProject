import mysql.connector
from mysql.connector import Error
import os

HOST=os.getenv("host")
USERNAME=os.getenv("user_name")
PASSWORD=os.getenv("password")
DATABASE=os.getenv("database")

#Function to get info from the database
def get_experts():
  trainers_list = []
  try:
      connection = mysql.connector.connect(host=HOST,
                                           database=DATABASE,
                                           user=USERNAME,
                                           password=PASSWORD)
      if connection.is_connected():
          db_Info = connection.get_server_info()
          print("Connected to MySQL Server version ", db_Info)
          cursor = connection.cursor()
          cursor.execute("select * from trainers;")
          record = cursor.fetchall()
          index  = cursor.column_names
          for row in record:
            info = zip(index,row)
            trainers_list.append(dict(info))
  
  except Error as e:
      print("Error while connecting to MySQL", e)
  finally:
      if connection.is_connected():
          cursor.close()
          connection.close()
  return trainers_list

#Function to add applicants into database
def add_applicant_db(applicant_dict,string):
  try:
    connection = mysql.connector.connect(host=HOST,
                                             database=DATABASE,
                                             user=USERNAME,
                                             password=PASSWORD)
    mycursor = connection.cursor()
    if connection.is_connected:
      if string == "session":
        insert_string = """insert into applicants(_name,_age,_email,_tickets) values(%s,%s,%s,%s);"""
        record =(applicant_dict["_name"],applicant_dict["_age"],applicant_dict["_email"],applicant_dict["_tickets"])
        mycursor.execute(insert_string,record)
      connection.commit()
      if string == "membership":
        insert_string = """insert into membership(_name,_age,_email,_pass) values(%s,%s,%s,%s);"""
        record = (applicant_dict["_name"],applicant_dict["_age"],applicant_dict["_email"],applicant_dict["_pass"])
        mycursor.execute(insert_string,record)
        connection.commit()
        print(applicant_dict)
  except Error as e:
    print("Error! could not send info", e)
  finally:
    if connection.is_connected:
      mycursor.close()
      connection.close()
      print("Applicant successfully sent")

#Function to check if the member is registered
def check_member(info):
  _email,_pass = info["_email"],info["_pass"]
  connection   = None
  member_exist = None
  try:
    #connecting variable
    connection = mysql.connector.connect(host=HOST,
                                             database=DATABASE,
                                             user=USERNAME,
                                             password=PASSWORD)
    if connection.is_connected:
      #Check if we connected to the correct database
      db_Info = connection.get_server_info()
      print("Connected to MySQL Server version ", db_Info)
      mycursor = connection.cursor()
      #The Query to select the user infomation
      string = "SELECT DISTINCT _name,_age,_email,_pass FROM membership WHERE _email='{}' AND _pass='{}';".format(_email,_pass)
      mycursor.execute(string)
      member = mycursor.fetchone() #fecth the returned output
      index  = mycursor.column_names # fecth the names of the columns
      member_exist = dict(zip(index,member)) #create a pair of tuples using the cloumn-names and returned info
  except Error:
    print("error could not connect",Error)
  finally:
    if connection.is_connected:
      #close the connections
      connection.close()
      mycursor.close()
      return member_exist
