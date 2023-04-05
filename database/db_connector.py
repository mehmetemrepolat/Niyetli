import mysql.connector

class Database:
    def __init__(self):
        self.config = {
            'user': 'root',
            'password': '****',
            'host': 'localhost',
            'database': 'niyetli'
        }
        self.db = mysql.connector.connect(**self.config)
        self.cursor = self.db.cursor()

    def note_add(self, note_title, note, note_create_date, note_category, note_time):
        while True:
            try:
                insert_query = "INSERT INTO notes (note_title, note, note_create_date, note_category, note_time) VALUES (%s, %s, %s, %s, %s)"
                values = (note_title, note, note_create_date, note_category, note_time)
                self.cursor.execute(insert_query, values)
                self.db.commit()
                break  # break out of the loop if no exception
            except mysql.connector.IntegrityError as e:
                if e.errno == 1062:  # Duplicate entry error code
                    # Burada Kullanıcıya "Bu not başlıklı bir not alınmış gözüküyor, Bu notu değiştirmek ister misiniz?"
                    # Tarzında soru yöneltilecek
                    note_title += " *"  # add suffix
                else:
                    raise e
        print(f"{self.cursor.rowcount} satır eklendi.")





    def update_note(self, note_id, note_title=None, note=None, note_create_date=None, note_category=None, note_time=None):
        update_query = "UPDATE notes SET "
        update_fields = []

        if note_title:
            update_fields.append(f"note_title = '{note_title}'")
        if note:
            update_fields.append(f"note = '{note}'")
        if note_create_date:
            update_fields.append(f"note_create_date = '{note_create_date}'")
        if note_category:
            update_fields.append(f"note_category = '{note_category}'")
        if note_time:
            update_fields.append(f"note_time = '{note_time}'")

        update_query += ", ".join(update_fields) + f" WHERE note_id = {note_id}"

        self.db_connector.cursor.execute(update_query)
        self.db_connector.db.commit()

        print(f"{self.db_connector.cursor.rowcount} satır güncellendi.")

    def delete_note(self, note_title):
        delete_query = f"DELETE FROM notes WHERE note_id = {note_title}"
        self.cursor.execute(delete_query)
        self.db.commit()

        print(f"{self.cursor.rowcount} satır silindi.")


