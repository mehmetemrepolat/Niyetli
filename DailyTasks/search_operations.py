# Burada arama motoru ile arama yapabilme yer alacak.
# Arama motorundan(bazı spesifik aramalar için) bilgiler çekilip kullanıcıya okunması sağlanacak.
import time
import webbrowser
import pyperclip as pc

from Niyetli.database.db_connector import Database


def get_engine():
    db = Database()
    print("Adana")
    engine_preference = db.get_results("Select search_engine FROM user_preferences")
    print(engine_preference[0][0])
    return engine_preference[0][0]
# duckduckgo.com/?q=deneme
# www.bing.com/search?q=deneme
# www.google.com/search?q={search}
def search(search):
    url = f"www.google.com/search?q={search}"
    webbrowser.get().open_new_tab(url)

def copy_to_search():
    coppied_text = pc.paste()
    search_url = f"www.google.com/search?q={coppied_text}"
    return webbrowser.get().open_new_tab(search_url)


print(copy_to_search())
#search("Anan")
