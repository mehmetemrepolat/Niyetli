from Niyetli.database.db_connector import Database

db = Database()

# db.fast_reminder("Deneme anımsatıcı")
db.reminder_add("Deneme anımsatıcı-", "2023-04-21", "23:38")

# Show Ballon eklenecek.
