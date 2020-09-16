import datetime as dt
import mysql.connector as mcon
from libs.ColorPython import Color
def insert_into_database(temp):
    try:
        cnx=mcon.connect(user='root',password='swapn',host='127.0.0.1',database='smarty')
        curA=cnx.cursor()
        insert_data = (
        "INSERT INTO searches (search_list,s_date,s_time) "
        "VALUES (%s, %s, %s)"
        )
        data=(temp,dt.datetime.now(),dt.datetime.now())
        curA.execute(insert_data,data)
        cnx.commit()
        cnx.close()
    except:
        pass
def show_history():
    try:
        cnx=mcon.connect(user='root',password='swapn',host='127.0.0.1',database='smarty')
        curA=cnx.cursor()
        curA.execute("SELECT * FROM searches")
        #temp=pd.DataFrame(curA,columns=['s_id','search','s_date','s_time'])
        #print(temp)
        #cnx.close()
        temp=curA.fetchall()
        t=1
        for i in temp:
            if t%2==0:
                print(t,Color.bold['cyan'] + ".........."+ i[1] + Color.reset )
            else:
                print(t,Color.bold['purple'] + ".........."+ i[1] + Color.reset )
            t+=1
        cnx.close()
    except:
        pass
db={'HISTORY':show_history}
