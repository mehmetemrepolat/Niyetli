import webbrowser
import pyperclip
from Niyetli.database.db_connector import Database


class SearchOperations:
    db = Database()

    def search_in_new_tab(self):
        if pyperclip.paste is not None:
            text = pyperclip.paste()
            searchEngine = self.db.get_search_engine_choices()
            webbrowser.open_new_tab(f"https://www.{searchEngine}.com/search?q={text}")
        else:
            return None



SO = SearchOperations()

SO.search_in_new_window()
