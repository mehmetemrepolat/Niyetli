import sqlite3

class LocalDatabase:
    def __init__(self):
        self.db = sqlite3.connect('Niyetli_Local.db')
        self.cursor = self.db.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS userpasswords(url, username, password, description)")
        self.db.commit()  # Commit table creation

    def insert_information_Password_Manager(self, url, username, password, description):
        query = "INSERT INTO userpasswords(url, username, password, description) VALUES (?, ?, ?, ?)"
        self.cursor.execute(query, (url, username, password, description))
        self.db.commit()  # Commit the changes after insertion

    def get_PasswordData(self):
        self.cursor.execute("SELECT * FROM userpasswords")
        result = self.cursor.fetchall()
        result = [(row[0], row[1], row[2], row[3]) for row in result]
        return result

# db = LocalDatabase()
# db.insert_information_Password_Manager("niyetli.com", "EmrePolat", "4568796", "Açıklama")
