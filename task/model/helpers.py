from datetime import date
from datetime import timedelta


class DateHelper:
    @staticmethod
    def get_formated_workday(date: date):
        dayofweek = date.weekday() + 1
        if (dayofweek == 6) or (dayofweek == 7):
            return (date + timedelta(7 - dayofweek + 1)).strftime("%Y.%m.%d")
        return date.strftime("%Y.%m.%d")

    @staticmethod
    def _is_leap(year):
        "year -> true if leap year, else false."
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

    @staticmethod
    def get_next_birthday(birthday: date, fromdate: date):
        if (
            DateHelper._is_leap(birthday.year)
            and not DateHelper._is_leap(fromdate.year)
            and (birthday.day == 29)
            and (birthday.month == 2)
        ):
            birthday_this_year = date(fromdate.year, 3, 1)
        else:
            birthday_this_year = date(fromdate.year, birthday.month, birthday.day)
        if birthday_this_year < fromdate:
            return DateHelper.get_next_birthday(birthday, date(fromdate.year + 1, 1, 1))
        return birthday_this_year
