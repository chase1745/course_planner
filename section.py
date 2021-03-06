from datetime import datetime, date, time, timedelta
from collections import OrderedDict
from course import Course
import re
import random


class Section(Course): 
    def __init__(self, department, courseNum, number, timeStart, timeFinish, days):
        super().__init__(department, courseNum)
        self.number = number
        self.name = department + " " + courseNum + " " + number
        self.courseName = department + courseNum
        
        self.days = OrderedDict()
        self.days['M'] = False
        self.days['T'] = False
        self.days['W'] = False
        self.days['R'] = False
        self.days['F'] = False
        for day in days:
            self.days[day] = True
        self.strDays = ""
        for day in days:
            if day:
                self.strDays += day

        hour = re.compile(r'\d\d?(?=:)')
        minute = re.compile(r'(?<=:)\d\d')
        am_or_pm = re.compile(r'am|pm|AM|PM')
        self.timeStart = time(int(hour.search(timeStart).group()), int(minute.search(timeStart).group()))
        self.timeFinish = time(int(hour.search(timeFinish).group()), int(minute.search(timeFinish).group()))
        if am_or_pm.search(timeStart).group() == "pm" or am_or_pm.search(timeStart).group() == "PM":
            self.AMorPM = "PM"
            self.morning = False
        else:
            self.AMorPM = "AM"
            self.morning = True

        self.secInfo = self.name + " - " + self.strDays + " " + self.timeStart.__str__() + "-" + self.timeFinish.__str__() + " " + self.AMorPM
        if not self.morning:
            outputTimeStart = datetime.combine(date.today(), self.timeStart) + timedelta(hours=12)
        else:
            outputTimeStart = datetime.combine(date.today(), self.timeStart)
        self.outputInfo = {
            'course': self.department + ' ' + self.courseNum,
            'section': self.number,
            'timeStart': timeStart,
            'timeFinish': timeFinish,
            'size': ((datetime.combine(date.today(), self.timeFinish) - datetime.combine(date.today(), self.timeStart)).total_seconds()) / 50 + 50,
            'topMargin': abs(((outputTimeStart - datetime.combine(date.today(), time(6,30))).total_seconds()) / 100),
            'color': random.choice(colors)
        }

    def __str__(self):
        return self.name

    def __lt__(self, other):
        if self.morning and not other.morning:
            return True
        elif other.morning and not other.morning:
            return False
        else:
            return self.timeFinish < other.timeStart

    def __gt__(self, other):
        if self.morning and not other.morning:
            return False
        elif other.morning and not self.morning:
            return True
        else:
            return self.timeStart > other.timeFinish

    def __xor__(self, other):
        return self.morning ^ other.morning

    def interfere(self, other):
        sameDay = False
        for day in self.days.keys():
            if self.days[day] and other.days[day]:
                sameDay = True

        if sameDay:
            if not self ^ other:  # Both in morning or afternoon
                if not self < other and not self > other:
                    # print(self.secInfo, '~', other.secInfo)
                    return True
                else:
                    # print(self.secInfo, '=', other.secInfo)
                    return False
            else:  # Cannot interfere because only one of them is in the morning
                # print(self.secInfo, '=', other.secInfo)
                return False
        else:
            # print(self.secInfo, '=', other.secInfo)
            return False

colors = ['#e74c3c', '#2ecc71', '#9b59b6', '#f39c12', '#3498db', '#34495e', '#F47983', '#7A942E', '#757D75', '#E29C45', '#006442']


