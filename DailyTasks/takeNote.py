import os
from datetime import datetime, date, timedelta


# Şimdilik sadece not defterine kayıt tutacak veritabanı oluşturulması ve bağlantısından sonra
# Veri tabanına tutacak şekilde güncellenecek
def take_note(note, note_title, file_path="root", note_subject="something", note_remind_time=None):

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




take_note("some", "some", "root", "aa", "2023-03-23 20:35:13.055375")
