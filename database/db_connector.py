import mysql.connector
from datetime import date, timedelta
import datetime

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

    def get_results(self, query):
        mycursor = self.db.cursor()
        mycursor.execute(query)
        result = mycursor.fetchall()
        return result


    def get_today_datas(self, category):
        pass
    def get_past_datas(self, category):
        pass

# >------------------------------------------------------------------------------------------------<
# >-----------------------------------------   COMMANDS   -----------------------------------------<
# >------------------------------------------------------------------------------------------------<

    def showCommands(self):
        query = "SELECT command, command_process FROM command_history ORDER BY command_id"
        mycursor = self.db.cursor()
        mycursor.execute(query)
        result = mycursor.fetchall()
        result = [(row[0], row[1]) for row in result]
        return result


# >------------------------------------------------------------------------------------------------<
# >-------------------------------------------   NOTES   ------------------------------------------<
# >------------------------------------------------------------------------------------------------<

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

    def note_add(self, note_title, note, note_create_date, note_time, note_category=None):
        if note_category is None:
            note_category = self.get_last_category('note')
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

        self.cursor.execute(update_query)
        self.db.commit()

        print(f"{self.cursor.rowcount} satır güncellendi.")


    def get_last_category(self, column):
        get_last_category_query = f"Select {column}_category FROM {column} ORDER BY {column}_id DESC LIMIT 1"
        mycursor = self.db.cursor()
        mycursor.execute(get_last_category_query)
        myresult = mycursor.fetchone()
        if myresult:
            category = myresult[0]
            return category
        else:
            print(f"Get last category error!")
            return None


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

    def get_sound_from_db(self, voice_note_title):
        query = f"SELECT voice_note_path FROM voice_notes WHERE voice_note_title='{voice_note_title}'"
        mycursor = self.db.cursor()
        mycursor.execute(query)
        myresult = mycursor.fetchone()
        if myresult:
            note_path = myresult[0]
            return note_path
        else:
            print(f"{voice_note_title} adlı sesli not bulunamadı.")
            return None


    def change_category(self, note_title, new_category):
        change_query = f"UPDATE notes SET note_category = '{new_category}' WHERE note_title = {note_title}"
        mycursor = self.db.cursor()
        mycursor.execute(change_query)
        result = mycursor.fetchall()
        return result

    def get_number_of_notes(self):
        query = "SELECT COUNT(*) FROM notes;"
        mycursor = self.db.cursor()
        mycursor.execute(query)
        myresult = mycursor.fetchall()
        return int(myresult[0][0])

    def show_onlyNotes(self):
        query = "SELECT note_title, note FROM notes ORDER BY note_id"
        mycursor = self.db.cursor()
        mycursor.execute(query)
        result = mycursor.fetchall()
        result = [(row[0]) for row in result]
        return result

    def showNotesDatas(self):
        query = "SELECT note_id, note_title, note, note_category, note_create_date FROM notes ORDER BY note_id"
        mycursor = self.db.cursor()
        mycursor.execute(query)
        result = mycursor.fetchall()
        result = [(row[0], row[1], row[2], row[3], datetime.datetime.strptime(str(row[4]), "%Y-%m-%d").date().strftime("%d-%m-%Y")) for row in result]
        return result

    def show_voiceNotes(self):
        query = "SELECT voice_note_title, voice_note_path, voice_note_categories From voice_notes"
        mycursor = self.db.cursor()
        mycursor.execute(query)
        result = mycursor.fetchall()
        result = [(row[0]) for row in result]
        return result



    def get_note_content(self, note):
        query = f"SELECT * FROM notes WHERE note_title = '{note}'"
        mycursor = self.db.cursor()
        mycursor.execute(query)
        result = mycursor.fetchall()
        return result

    def show_notes(self, desc, content="*", number=0):

        if content != "*":
            query = f"SELECT {content} FROM notes ORDER BY note_id"
        else:
            query = "SELECT * FROM notes ORDER BY note_id"
        if desc == 0:
            query += " ASC"
        else:
            query += " DESC"
        if number != 0:
            query += f" LIMIT {number};"

        mycursor = self.db.cursor()
        mycursor.execute(query)
        result = mycursor.fetchall()
        return result






    def delete_note(self, note_title):
        delete_query = f"DELETE FROM notes WHERE note_id = {note_title}"
        self.cursor.execute(delete_query)
        self.db.commit()

        print(f"{self.cursor.rowcount} satır silindi.")

# >------------------------------------------------------------------------------------------------<
# >------------------------------------------- REMINDER -------------------------------------------<
# >------------------------------------------------------------------------------------------------<

    def get_reminders(self):
        query = "SELECT  FROM notes ORDER BY note_id"
        mycursor = self.db.cursor()
        mycursor.execute(query)
        result = mycursor.fetchall()
        result = [(row[0], row[1]) for row in result]
        return result

    def reminder_add(self, reminder, reminder_date, reminder_time, reminder_category='1', attachment='', reminder_enabled='1'):
        if reminder_category == '1':
            reminder_category = self.get_last_category('reminder')
        while True:
            try:
                insert_query = "INSERT INTO reminder (reminder, attachment, reminder_category, reminder_create_date, reminder_create_time, reminder_date, reminder_time, reminder_enabled) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                values = (reminder, attachment, reminder_category, date.today().isoformat(), datetime.now().strftime("%H:%M:%S"), reminder_date, reminder_time, reminder_enabled)
                self.cursor.execute(insert_query, values)
                self.db.commit()
                break
            except mysql.connector.IntegrityError as e:
                if e.errno == 1062:  # Duplicate entry error code
                    # İleride burada Kullanıcıya "Bu not başlıklı bir not alınmış gözüküyor, Bu notu değiştirmek ister misiniz?"
                    # Tarzında soru yöneltilecek
                    reminder += " *"  # add suffix
                else:
                    raise e
        print(f"{self.cursor.rowcount} satır eklendi.")

    def fast_reminder(self, reminder):

        now = datetime.now()
        two_hours_later = now + timedelta(hours=2)
        reminder_time = two_hours_later.strftime("%H:%M")
        while True:
            try:
                cursor = self.db.cursor()
                fastReminderQuery = "INSERT INTO reminder (reminder, attachment, reminder_category, reminder_create_date, reminder_create_time, reminder_date, reminder_time, reminder_enabled)" \
                                    " VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                values = (reminder, '', 'Fast Reminder', date.today().isoformat(), datetime.now().strftime("%H:%M:%S"), date.today().isoformat(), reminder_time, '1')
                cursor.execute(fastReminderQuery, values)
                self.db.commit()
                cursor.close()
                print("Reminder added successfully.")
                break
            except:
                print("Hata")


    def get_today_reminders(self):
        today = date.today()
        today_str = today.strftime('%Y-%m-%d')
        get_reminders_query = f"Select reminder_id, reminder_time, reminder, reminder_category From reminder WHERE reminder_date='{today_str}'"
        mycursor = self.db.cursor()
        mycursor.execute(get_reminders_query)
        result = mycursor.fetchall()
        result = [(row[0], row[1], row[2], row[3]) for row in result]
        return result



# >------------------------------------------------------------------------------------------------<
# >------------------------------------------- TIMER ----------------------------------------------<
# >------------------------------------------------------------------------------------------------<


    def timer_db_control(self):
        today = date.today()
        today_str = today.strftime('%Y-%m-%d')
        get_timer_query = f"Select * From secreen_timer WHERE secreen_date='{today_str}'"
        mycursor = self.db.cursor()
        mycursor.execute(get_timer_query)
        result = mycursor.fetchall()
        return result


    def update_timer(self, program_id, secreen_time, day_counter):
        timer_update_query = f"Update secreen_timer SET secreen_time = secreen_time + {secreen_time}, day_counter = day_counter + {day_counter} where program_id = '{program_id}'"

        try:
            self.cursor.execute(timer_update_query)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            print("Timer güncellenirken bir hata oluştu:", str(e))



    def timer_into_database(self, program_id, program, is_program, time, date_counter=1):
        self.db.connect()

        data_today = self.timer_db_control()

        if any(item[1] == program_id for item in data_today):
            self.update_timer(program_id, time, date_counter)
            return
        else:
            cursor = self.db.cursor()
            data_insert_query = "INSERT INTO secreen_timer ( program_id, program_name, is_program, secreen_time, secreen_date, day_counter)" \
                                "VALUES(%s, %s, %s, %s, %s, %s)"
            values = (program_id, program, is_program, time, date.today(), date_counter)
            cursor.execute(data_insert_query, values)
            self.db.commit()
            cursor.close()
            print("Data added")
            return

    def get_timer_statics(self, number_of_stat=None, days_stat=-1):
        query = f"SELECT program_name, secreen_time, secreen_date, day_counter FROM secreen_timer"
        if number_of_stat is not None:
            query += f" LIMIT {number_of_stat}"

        mycursor = self.db.cursor()
        mycursor.execute(query)
        result = mycursor.fetchall()

        # Tarihi düz tarih formatına çevir
        result = [
            (row[0], row[1], datetime.datetime.strptime(str(row[2]), "%Y-%m-%d").date().strftime("%Y-%m-%d"), row[3])
            for row in result]

        return result

# >------------------------------------------------------------------------------------------------<
# >------------------------------------- ASSISTANT CHOICES-----------------------------------------<
# >------------------------------------------------------------------------------------------------<

    def get_search_engine_choices(self):
        query = "SELECT search_engine from user_preferences"
        mycursor = self.db.cursor()
        mycursor.execute(query)
        result = mycursor.fetchone()
        result = result[0]
        return result


deneme = Database()

