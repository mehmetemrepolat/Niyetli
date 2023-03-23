import os
from datetime import datetime, date, timedelta, time


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

# def edit_note(note_id, about_edit, edit)
# about_edit -> sil, düzenle, yeniden yaz, ekleme yap, çıkarma yap

# def read_note(note_id)


take_note("some1", "some2")





