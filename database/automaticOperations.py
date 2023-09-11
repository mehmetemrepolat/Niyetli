import mysql.connector

class Database:
    def __init__(self):
        self.config = {
            'user': 'root',
            'password': '413508',
            'host': 'localhost',
            'database': 'niyetli'
        }
        self.db = mysql.connector.connect(**self.config)
        self.cursor = self.db.cursor()

    def save_command(self, command, task):
        while True:
            try:
                query = f"INSERT INTO command_history(command, command_process) VALUES (%s, %s)"
                values = (command, task)
                self.cursor.execute(query, values)
                self.db.commit()
                break
            except mysql.connector.IntegrityError as e:
                return e


