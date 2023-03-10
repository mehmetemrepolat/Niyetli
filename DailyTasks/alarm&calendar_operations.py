from datetime import datetime, date, timedelta


def get_date(today = date.today()):
    if today != date.today():
        return date.today() + timedelta(today)
    else:
        return today


def get_date_w_string(date):
    # date = date.strftime()
    return date.strftime("%B %d, %Y")


def get_date_only_number(date):
    return date.split()[1].replace(",", "")


today = date.today()
tomorrow = today + timedelta(1)






print(datetime.now().strftime("%H:%M"))

print(today.strftime("%B %d, %Y"))

print("Yarın:", tomorrow.strftime("%B %d, %Y"))

print(get_date())

print(get_date(-19))

print(get_date_w_string(get_date(2)))

print(get_date_only_number(get_date_w_string(get_date(3))))

