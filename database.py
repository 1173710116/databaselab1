import pymysql
import datetime
'''
connection = pymysql.connect(host='localhost', port=3306, user='root',
                             password='000000', db='database_lab1', charset='utf8')
cursor = connection.cursor()
name = "riko@hotmail.com"
cursor.execute("DELETE FROM blogs WHERE auther = '" + name + "'")
# row_1 = cursor.fetchall()
connection.commit()

row_1 = cursor.fetchone()
connection.commit()
cursor.close()
connection.close()
print('123456' == row_1[0])
'''
print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
