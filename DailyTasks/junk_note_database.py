from Niyetli.database.db_connector import Database

db = Database()


note_title = 'Deneme Notu'
note = '.'
note_create_date = '2023-04-02'
note_category = 'Genel'
note_time = '10:00'

db.note_add(note_title, note, note_create_date, note_category, note_time)
