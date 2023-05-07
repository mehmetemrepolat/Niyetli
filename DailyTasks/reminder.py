from Niyetli.database.db_connector import Database
from Niyetli.DailyTasks.AlarmCalendarReminderOP import DateOperations
from threading import Thread, Timer
from datetime import datetime, date, timedelta


class Reminder:
    db = Database()
    sb = DateOperations()

    # Bu metodun günde veya program her açıldığında bir kez çalışması gerekmekte ve buna göre hareket edilmesi gerekmekte
    def are_you_sure(self, msg, column):
        question = ""
        if column == "note":
            question = f"{msg}, notu silinecek emin misin?"
        elif column == 'reminder':
            question = f"{msg}, anımsatıcısı silinecek emin misin?"
        return question

    def set_reminder(self):
        now = datetime.now()
        today = now.date()
        reminders = self.db.get_today_reminders()
        for x in range(0, len(reminders)):
            reminder_time = datetime.strptime(reminders[x][1], '%H:%M').time()  # String to Time
            reminder_datetime = datetime.combine(today, reminder_time)
            delta = (reminder_datetime - now).total_seconds()
            if delta < 0:
                pass
            else:
                timer = Timer(delta, self.sb.show_balloon, args=[reminders[x][3], reminders[x][2]])
                timer.start()

    def read_reminders(self, day):
        reminders_list = self.db.get_results(f"SELECT reminder, reminder_category, reminder_time FROM reminder WHERE reminder_date='{day}'")
        return reminders_list


    def which_one(self, similarreminders):  # read_reminders ta da bu özelliği kullanabilirim.
        set_list = []
        for x in range(0, len(similarreminders)):
            set_list.append(f"{x+1} - {similarreminders[x][0]}")
        return set_list

    def return_similar_reminders(self, reminder):
        similar_reminders = self.db.get_results(f"SELECT reminder, reminder_id FROM reminder where reminder LIKE '{reminder}%'")
        list_reminders = []
        #return self.which_one(similar_reminders)
        return similar_reminders

    def get_result_similar(self, reminder):
        similar_list = self.return_similar_reminders(reminder)
        if len(similar_list) > 1:
            which_list = self.which_one(similar_list)
            print(which_list)
            secim = input(f"Birden çok '{reminder}' anımsatıcısı mevcut, hangisini silmek istersiniz?")
            # print(similar_list[int(secim)-1][1])
            id_no = int(similar_list[int(secim)-1][1])
            msg = similar_list[int(secim)-1][0]
            sure = input(self.are_you_sure(msg, 'reminder'))
            if sure == '1':
                self.delete_sql(id_no, 'reminder')
            else:
                return None
        else:
            msg = similar_list[0][0]
            # Burda direkt "... Anımsatıcısı silinecek emin misiniz? diye soracak"
            secim = input(self.are_you_sure(msg, 'reminder'))
            if secim == '1':
                return self.delete_sql(similar_list[0][1], 'reminder')
            else:
                return None



    def delete_sql(self, id, column_name, table_name='reminder'):
        delete_query = f"DELETE FROM {table_name} WHERE {column_name}_id = '{id}'"
        self.db.cursor.execute(delete_query)
        self.db.db.commit()
        message = f"{self.db.cursor.rowcount} satır silindi."
        return message



# rm = Reminder()
# print(rm.read_reminders(date.today()))
# print(rm.get_result_similar("msg"))
# rm.delete_sql(119, "reminder")

