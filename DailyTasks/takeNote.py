import os
from datetime import datetime, date, timedelta, time
from Niyetli.database.db_connector import Database
db = Database()


def get_hour():
    time = datetime.now().strftime("%H:%M")
    return time
# Şimdilik sadece not defterine kayıt tutacak veritabanı oluşturulması ve bağlantısından sonra
# Veri tabanına tutacak şekilde güncellenecek
# Tutulan notların düzenli bir şekilde kaydının gerçekleşmesi gerekiyor.
# Not kategorisi şeklinde notlar sınıflandırılabilir.



def take_note(note, note_title, file_path="root", note_category="yellow", note_remind_time=None):
    today = datetime.today()
    today = today.strftime("%A, %B %d, %Y")


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
    Contents = open("NoteContents", "w")
    Contents.write(f"Bilgiler: noteId, {note_title}, {note}, {note_category}, {today}, {get_hour()}")
    Contents.close()


def fast_note(note):
    today = datetime.today()
    # Kullanıcının hızlıca not almasını sağlayacak,
    # Bu durumda not kategorisini değiştirmek gerekiyor
    # note_category = 'fast'
    # Kullanıcı hızlı notları bu kategori üzerinden kontrol edebilecek


# def edit_note(note_id, about_edit, edit)
# about_edit -> sil, düzenle, yeniden yaz, ekleme yap, çıkarma yap

# def read_note(note_id)


# take_note("some1", "some2")

note_title = 'Deneme Notu4'
note = '.'
note_create_date = '2023-04-02'
note_category = 'Genel'
note_time = '10:00'


db.note_add(note_title, note, note_create_date, note_category, note_time)

# db.delete_note('Deneme Notu')

