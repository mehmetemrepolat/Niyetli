from db_connector import Database
from datetime import date
db = Database()
print(db.get_number_of_notes())

print(db.show_notes(0, 2))

