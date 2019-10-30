import time
import mysql.connector
from mysql.connector import Error
from datetime import date
th="BYC19 >>"
print(th+"Welcome to bayesian Classifier 2019")
hostname=input(th+"Enter Hostname:")
db=input(th+"Enter Database name:")
username=input(th+"Enter Username:")
password=input(th+"Enter Password:")
datatable=input(th+"Enter tablename:")


try:
    connection = mysql.connector.connect( host=hostname,
  user=username,
  passwd=password,
  database=db)
    if connection.is_connected():
       db_Info = connection.get_server_info()
       print(th+"Connected to Server successfuly with version on ",db_Info)
       cursor = connection.cursor()
       print(th)
       print(th+"Press Y for yes and N for No or Quit")
       while(input(th+"Are You want to continue:").lower()=='y'):
           sql = "SELECT * FROM " + datatable
           cursor.execute(sql)
           myresult = cursor.fetchall()
           rc = cursor.rowcount
           n = len(myresult[0])
           num_fields = len(cursor.description)
           field_names = cursor.column_names
           dataset = list()
           newdata = list()
           print(th + "Data successfuly fetched")
           print(th)
           print(th + "Enter unknown Sample X:")
           for i in range(n - 1):
               newdata.append(input(th + str(field_names[i]) + ":"))
           print(th)
           if myresult:
               for j in range(n):
                   ls = list()
                   for i in range(rc):
                       ls.append(str(myresult[i][j]))
                   dataset.append(ls)

           py = dataset[n - 1].count('yes')
           pn = dataset[n - 1].count('no')
           pyc = py
           pnc = pn
           py = py / rc
           pn = pn / rc
           print(th + "P(" + field_names[n - 1] + "=yes)=" + str(py))
           print(th + "P(" + field_names[n - 1] + "=no)=" + str(pn))
           pyl = list()
           pnl = list()
           for i in range(n - 1):
               pyl.append(0)
               pnl.append(0)

           for i in range(n - 1):
               for j in range(rc):
                   if str(dataset[i][j]) == str(newdata[i]) and str(dataset[n - 1][j]) == 'yes':
                       pyl[i] = pyl[i] + 1
                   if str(dataset[i][j]) == str(newdata[i]) and str(dataset[n - 1][j]) == 'no':
                       pnl[i] = pnl[i] + 1
           pycn = 1
           pncn = 1
           for i in range(n - 1):
               pyl[i] = pyl[i] / pyc
               pnl[i] = pnl[i] / pnc
               print(th + "P("+field_names[i]+"="+ newdata[i] + "," + field_names[n-1] + "=yes)=" + str(pyl[i]))
               print(th + "P("+field_names[i]+"="+newdata[i]+","+ field_names[n-1] + "=no)=" + str(pnl[i]))
               pycn = pycn * pyl[i]
               pncn = pncn * pnl[i]
           print(th + "P(X,yes)=" + str(pycn * py))
           print(th + "P(X,no)=" + str(pncn * pn))
           new_class=''
           if pncn * pn > pycn * pn:
               print(th + "Sample classify as No")
               new_class='no'
               print(th)
               if input(th+"You wanna enter this sample to dataset,Press Y for yes and N for No:").lower()=='y':
                   sql = "INSERT INTO "+datatable
                   mid=" ("
                   vls=" VALUES ("
                   sel= "SELECT * FROM "+datatable+" WHERE "
                   for i in range(n):
                       if i<n-1:
                            mid=mid+field_names[i]+", "

                            vls=vls+"'"+newdata[i]+"', "
                            sel=sel+field_names[i]+"='"+newdata[i]+"' AND "

                       else:
                           mid = mid + field_names[i]

                           vls = vls +"'"+new_class+"'"
                           sel = sel + field_names[i] + "='" + new_class+"'"
                   mid=mid+")"
                   vls=vls+")"
                   sql=sql+mid+vls

                   cursor.execute(sel)
                   res=cursor.fetchall()
                   n=cursor.rowcount
                   if n>0:
                       print(th+"Sample allready available")
                   else:

                       cursor.execute(sql)

                       connection.commit()
                       print(th+"Sample added")

           else:
               sql = "INSERT INTO " + datatable
               mid = " ("
               vls = " VALUES ("
               sel = "SELECT * FROM " + datatable + " WHERE "
               for i in range(n):
                   if i < n - 1:
                       mid = mid + field_names[i] + ", "

                       vls = vls + "'" + newdata[i] + "', "
                       sel = sel + field_names[i] + "='" + newdata[i] + "' AND "

                   else:
                       mid = mid + field_names[i]

                       vls = vls + "'" + new_class + "'"
                       sel = sel + field_names[i] + "='" + new_class + "'"
               mid = mid + ")"
               vls = vls + ")"
               sql = sql + mid + vls

               cursor.execute(sel)
               res = cursor.fetchall()
               n = cursor.rowcount
               if n > 0:
                   print(th+"Sample allready available")
               else:

                   cursor.execute(sql)

                   connection.commit()
                   print(th+"Sample added")





except Error as e :
    print (th+"Error while connecting to server", e)
finally:
    #closing database connection.
    if(connection.is_connected()):
        cursor.close()
        connection.close()
        print(th+"Server closing....")
time.sleep(2)