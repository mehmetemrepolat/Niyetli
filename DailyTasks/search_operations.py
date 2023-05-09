# Burada arama motoru ile arama yapabilme yer alacak.
# Arama motorundan(bazı spesifik aramalar için) bilgiler çekilip kullanıcıya okunması sağlanacak.
from Niyetli.database.db_connector import Database

db = Database()
engine_preference = db.get_results("Select search_engine FROM user_preferences")
print(engine_preference[0][0])