from datetime import datetime, date, timedelta, time
from Niyetli.database.db_connector import Database
from Niyetli.DailyTasks.reminder import Reminder
class Note:
    db = Database()
    reminder = Reminder()

    @staticmethod
    def get_hour(self):
        time = datetime.now().strftime("%H:%M")
        return time
    # Şimdilik sadece not defterine kayıt tutacak veritabanı oluşturulması ve bağlantısından sonra
    # Veri tabanına tutacak şekilde güncellenecek
    # Tutulan notların düzenli bir şekilde kaydının gerçekleşmesi gerekiyor.
    # Not kategorisi şeklinde notlar sınıflandırılabilir.

    def return_similar_notes(self, note):
        similar_notes = self.db.get_results(f"SELECT note, note_id FROM notes where note LIKE '{note}%'")
        return similar_notes

    def get_result_similar(self, note):
        similar_list = self.return_similar_notes(note)
        if len(similar_list) > 1:
            which_list = self.reminder.which_one(similar_list)
            print(which_list)
            secim = input(f"'{note}' adında birden çok not mevcut, hangisini silmek istersiniz?")
            id_no = int(similar_list[int(secim)-1][1])
            msg = similar_list[int(secim)-1][0]
            sure = input(self.reminder.are_you_sure(msg, 'note'))
            if sure == '1':
                return self.reminder.delete_sql(id_no, 'note', 'notes')
            else:
                return None
        else:
            msg = similar_list[0][0]
            secim = input(self.reminder.are_you_sure(msg, 'note'))
            if secim == '1':
                return self.reminder.delete_sql(similar_list[0][1], 'note')
            else:
                return None

    def last_or_first_x_note(self, number=5, last_first="first"):
        query = "SELECT * FROM notes ORDER BY note_id "
        if last_first == "first":
            query += f"ASC LIMIT {number}"
        elif last_first == "last":
            query += f"DESC LIMIT {number}"
        mycursor = self.db.db.cursor()
        mycursor.execute(query)
        result = mycursor.fetchall()
        result = [(row[2]) for row in result]
        return result


class LocalNote:
    today = datetime.today()
    today = today.strftime("%A, %B %d, %Y")

    def take_note(self, note, note_title, file_path="root", note_category="yellow", note_remind_time=None):

        if file_path == "root":
            f = open(f"{note_title}", "w")
        else:
            f = open(f"{file_path}/{note_title}.txt", "w")
        f.write(f"{note}")
        if note_remind_time is None:
            tomorrow = datetime.today() + timedelta(+1)
            note_remind_time = tomorrow
            f.write(f"\n{note_remind_time}\t")
        else:
            f.write(f"\n{note_remind_time}\t")
        f.close()
        Contents = open("NoteContents.txt", "w")
        Contents.write(f"Bilgiler: noteId, {note_title}, {note}, {note_category}, {self.today}, {self.get_hour(self)}")
        Contents.close()


    def fast_note_local(self, note):
        if len(note) < 10:
            note_title = note
        else:
            note_title = " ".join(note.split()[:5])

        file_path = "root"






# notes = Note()
# print(notes.last_or_first_x_note())
# print(notes.get_result_similar(""))
# def edit_note(note_id, about_edit, edit)
# about_edit -> sil, düzenle, yeniden yaz, ekleme yap, çıkarma yap
# def read_note(note_id)
# take_note("some1", "some2")
# print(db.get_category("Deneme Notu4 *"))
# db.note_add(note_title, note, note_create_date, note_category, note_time)
# db.delete_note('Deneme Notu')
# db.fast_note("1. Not")

