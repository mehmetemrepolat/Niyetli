import mysql.connector
from datetime import datetime, date, timedelta, time

class Database:
    def __init__(self):
        self.config = {
            'user': 'root',
            'password': '*****',
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
        if len(note) < 5:
            note_title = note
        else:
            note_title = " ".join(note.split()[:5])

        while True:
            try:
                cursor = self.db.cursor()
                fastNoteQuery = "INSERT INTO notes (note_title, note, note_category, note_create_date, note_time) VALUES (%s, %s, %s, %s, %s)"
                values = (note_title, note, 'Fast Note', date.today().isoformat(), datetime.now().strftime("%H:%M:%S"))
                cursor.execute(fastNoteQuery, values)
                self.db.commit()
                cursor.close()
                print("Note added successfully.")
                break
            except:
                note_title += "*"




    def get_category(self, note_title):
        get_category_query = f"SELECT note_category FROM notes WHERE note_title = '{note_title}'"
        mycursor = self.db.cursor()

        mycursor.execute(get_category_query)

        myresult = mycursor.fetchone()

        if myresult:
            category = myresult[0]
            return category
        else:
            print(f"{note_title} adlı nota ait kategori bulunamadı.")
            return None

    def change_category(self, note_title, new_category):
        change_query = f"UPDATE notes SET note_category = '{new_category}' WHERE note_title = {note_title}"

    def delete_note(self, note_title):
        delete_query = f"DELETE FROM notes WHERE note_id = {note_title}"
        self.cursor.execute(delete_query)
        self.db.commit()

        print(f"{self.cursor.rowcount} satır silindi.")

    def timer_db_control(self):
        today = date.today()
        today_str = today.strftime('%Y-%m-%d')
        get_timer_query = f"Select * From secreen_timer where secreen_date='{today_str}'"
        mycursor = self.db.cursor()
        mycursor.execute(get_timer_query)
        result = mycursor.fetchall()

        return result


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

    def update_timer(self, program_id, secreen_time, day_counter):
        today = date.today()
        today_str = today.strftime('%Y-%m-%d')
        timer_update_query = f"Update secreen_timer SET secreen_time = secreen_time + {secreen_time}, day_counter = day_counter + {day_counter} where program_id = '{program_id}'"

        try:
            self.cursor.execute(timer_update_query)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            print("Timer güncellenirken bir hata oluştu:", str(e))



    def timer_into_database(self, program_id, Program, is_program, time, date_counter=1):
        self.db.connect()

        data_today = self.timer_db_control()

        if any(item[1] == program_id for item in data_today):
            self.update_timer(program_id, time, date_counter)
            return
        else:
            cursor = self.db.cursor()
            data_insert_query = "INSERT INTO secreen_timer ( program_id, program_name, is_program, secreen_time, secreen_date, day_counter)" \
                                "VALUES(%s, %s, %s, %s, %s, %s)"
            values = (program_id, Program, is_program, time, date.today(), date_counter)
            cursor.execute(data_insert_query, values)
            self.db.commit()
            cursor.close()
            print("Data added")
            return
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