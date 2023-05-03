from Niyetli.database.db_connector import Database
from Niyetli.DailyTasks.AlarmCalendarReminderOP import DateOperations
from threading import Thread, Timer
from datetime import datetime, date, timedelta


db = Database()
sb = DateOperations()
reminders2 = db.get_today_reminders()


# Bu metodun günde veya program her açıldığında bir kez çalışması gerekmekte ve buna göre hareket edilmesi gerekmekte
def set_reminder():
    now = datetime.now()
    today = now.date()
    reminders = db.get_today_reminders()
    for x in range(0, len(reminders)):
        reminder_time = datetime.strptime(reminders[x][1], '%H:%M').time()  # String to Time
        reminder_datetime = datetime.combine(today, reminder_time)
        delta = (reminder_datetime - now).total_seconds()
        if delta < 0:
            pass

        else:
            timer = Timer(delta, sb.show_balloon, args=[reminders[x][3], reminders[x][2]])
            timer.start()



def read_reminders(day):
    reminders_list = db.get_results(f"SELECT reminder, reminder_category, reminder_time FROM reminder WHERE reminder_date='{day}'")
    return reminders_list





print(read_reminders(date.today()))

