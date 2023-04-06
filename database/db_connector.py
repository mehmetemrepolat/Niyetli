import mysql.connector
from datetime import datetime, date, timedelta, time

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

    def fast_note(self, note):
        today = datetime.today()
        while True:
            try:
                fastNoteQuery = "INSERT INTO notes (note_title, note, note_create_date, note_category, note_time) VALUES (%s, %s, %s, %s, %s)"
                note_title = " ".join(note.split()[:5])
                values = (note_title, note, date.today().isoformat(), 'Fast Note', datetime.now().strftime("%H:%M:%S"))
                self.cursor.execute(fastNoteQuery, values)
                self.db.commit()
                break  # break out of the loop if no exception

            except mysql.connector.IntegrityError as e:
                if e.errno == 1062:  # Duplicate entry error code
                    note_title += " *"
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




"""
note_add(self, note_title, note, note_create_date, note_category, note_time): Bu metot, veritabanına yeni bir not
    eklemek için kullanılır. note_title, note, note_create_date, note_category, ve note_time parametreleri ile 
    notun başlık, içerik, oluşturma tarihi, kategori ve saat bilgileri alınır. Veritabanına INSERT SQL sorgusu
    ile yeni bir kayıt eklenir. Eğer aynı başlığa sahip bir not zaten varsa, kullanıcıya "Bu not başlıklı bir
    not alınmış gözüküyor, Bu notu değiştirmek ister misiniz?" şeklinde bir soru yöneltir ve başlığın sonuna * 
    ekleyerek benzersizleştirme yapar.
    
fast_note(self, note): Bu metot, hızlı bir şekilde not eklemek için kullanılır. note parametresi ile not içeriği
    alınır. Not başlığı, ilk 5 kelime kullanılarak oluşturulur ve note_create_date ve note_time bilgileri şu anki
    tarih ve saat olarak atanır. Veritabanına INSERT SQL sorgusu ile yeni bir kayıt eklenir. Eğer aynı başlığa
    sahip bir not zaten varsa, başlığın sonuna * ekleyerek benzersizleştirme yapar.

update_note(self, note_id, note_title=None, note=None, note_create_date=None, note_category=None, note_time=None):
    Bu metot, mevcut bir notu güncellemek için kullanılır. note_id parametresi ile güncellenecek notun ID'si alınır.
    note_title, note, note_create_date, note_category, ve note_time parametreleri ile güncellenecek notun yeni başlık,
    içerik, oluşturma tarihi, kategori ve saat bilgileri alınır. Veritabanına UPDATE SQL sorgusu ile güncelleme yapılır.

delete_note(self, note_title): Bu metot, bir notu silmek için kullanılır. note_title parametresi ile silinecek notun
    başlık bilgisi alınır. Veritabanından DELETE SQL sorgusu ile not silinir.

"""