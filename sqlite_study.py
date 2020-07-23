import sqlite3

con = sqlite3.connect("/Users/soom/OneDrive/Documents/python/kospi.db")
cursor = con.cursor()

cursor.execute("SELECT * FROM kakao")

# print(cursor.fetchone())
# print(cursor.fetchone())
# print(cursor.fetchone())

kakao = cursor.fetchall()
print(kakao[0][0])
print(kakao[0][1])
print(kakao[0][2])
