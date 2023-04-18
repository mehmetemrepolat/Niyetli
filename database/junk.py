from db_connector import Database
from datetime import date
db = Database()

today = date.today()
today_str = today.strftime('%Y-%m-%d')
print(today_str)

sonuc = db.timer_db_control()


print(sonuc)

print(sonuc[1][0])

print(sonuc[1][3])


print(len(sonuc))
print("----")

if '3fb1' in sonuc[2]:
    print("var")

