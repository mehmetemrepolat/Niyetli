from Niyetli.database.db_connector import Database
from Niyetli.DailyTasks.AlarmCalendarReminderOP import DateOperations
from threading import Thread, Timer
from datetime import datetime, date, timedelta


class Reminder:
    db = Database()
    sb = DateOperations()

    # Bu metodun günde veya program her açıldığında bir kez çalışması gerekmekte ve buna göre hareket edilmesi gerekmekte

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



rm = Reminder()

print(rm.read_reminders(date.today()))

