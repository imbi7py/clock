import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from bs4 import BeautifulSoup
from urllib.request import urlopen
from PyQt5.QtGui import *
from pygame import mixer


class MyWidget(QMainWindow):

    def __init__(self):
        global alarm_minute, alarm_hour
        super().__init__()
        uic.loadUi('design.ui', self)
        LIST_OF_TIME_ZONES = ['(UTC−12)',
                              'Ниуэ (UTC−11)',
                              'США(Гавайи) (UTC−10)',
                              'США(Аляска) (UTC−9)',
                              'североамериканское тихоокеанское время\
                              (UTC-8)',
                              'горное время (UTC-7)',
                              'центральноамериканское время (UTC-6)',
                              'североамериканское восточное время\
                              (UTC-5)',
                              'атлантическое время (UTC-4)',
                              'Канада (Ньюфаундленд) (UTC−3:30)',
                              'южноамериканское восточное время (UTC-3)',
                              'среднеатлантическое время (UTC-2)',
                              'Азорские острова (UTC−1)',
                              'западноафриканское время (UTC+0)',
                              'центральноевропейское время (UTC+1)',
                              'восточноевропейское время (UTC+2)',
                              'московское время (UTC+3)',
                              'Иран (UTC+3:30)',
                              'самарское время (UTC+4)',
                              'Афганистан (UTC+4:30)',
                              'екатеринбургское время (UTC+5)',
                              'Индия (UTC+5:30)',
                              'Непал (UTC+5:45)',
                              'омское время (UTC+6)',
                              'Мьянма (UTC+6:30)',
                              'красноярское время (UTC+7)',
                              'иркутское время (UTC+8)',
                              'Австралия (UTC+8:45)',
                              'якутское время (UTC+9)',
                              'Австралия (UTC+9:30)',
                              'владивостокское время (UTC+10)',
                              'Австралия (UTC+10:30)',
                              'магаданское время (UTC+11)',
                              'камчатское время (UTC+12)',
                              'Новая Зеландия (UTC+12:45)',
                              'Тонга (UTC+13)',
                              'Кирибати (UTC+14)',
                              ]
        alarm_minute, alarm_hour = '', ''
        self.time_zone1 = '(UTC−12)'
        self.time_zone2 = '(UTC−12)'
        self.time_zone3 = '(UTC−12)'
        self.time_edit_1.move(30, 180)
        self.time_edit_1.resize(190, 20)
        self.time_edit_2.move(280, 180)
        self.time_edit_2.resize(190, 20)
        self.time_edit_3.move(510, 180)
        self.time_edit_3.resize(190, 20)
        self.time_edit_1.addItems(LIST_OF_TIME_ZONES)
        self.time_edit_2.addItems(LIST_OF_TIME_ZONES)
        self.time_edit_3.addItems(LIST_OF_TIME_ZONES)

        self.time_edit_1.activated.connect(self.handleActivated_1)
        self.time_edit_2.activated.connect(self.handleActivated_2)
        self.time_edit_3.activated.connect(self.handleActivated_3)

        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)

        self.showTime()

    def set_alarm(self):
        try:
            self.alarm_window = AlarmWindow(self)
            self.alarm_window.show()
        except Exception as e:
            print(str(e))

    def showTime(self):
        global alarm_minute, alarm_hour
        text = self.now_time()

        self.Time_1.display(self.check_time_zone(text, self.time_zone1))
        self.Time_2.display(self.check_time_zone(text, self.time_zone2))
        self.Time_3.display(self.check_time_zone(text, self.time_zone3))

        self.alarm = QPushButton(self)
        self.alarm.setText('Будильник')
        self.alarm.move(30, 400)

        self.alarm.clicked.connect(self.set_alarm)

        if str(alarm_minute) == QTime.currentTime().toString('mm').lstrip('0') and\
                str(alarm_hour) == QTime.currentTime().toString('hh').lstrip('0'):
            alarm_minute, alarm_hour = '', ''
            try:
                self.reset_alarm_window = StopAlarmWindow(self)
                self.reset_alarm_window.show()
            except Exception as e:
                print(str(e))

    def handleActivated_1(self, index):
        self.time_zone1 = (self.time_edit_1.itemText(index))

    def handleActivated_2(self, index):
        self.time_zone2 = (self.time_edit_2.itemText(index))

    def handleActivated_3(self, index):
        self.time_zone3 = (self.time_edit_3.itemText(index))

    def now_time(self):
        try:
            text = self.parse_time()
        except Exception:                           # В случае отсутствия
            time = QTime.currentTime()              # интернет соединения
            text = time.toString('hh:mm')           # берутся данные системы
            if time.second() % 2 == 0:
                text = text[:2] + ' ' + text[3:]
        return text

    def parse_time():
        """Функция для парсинга времени в интернете"""
        html_doc = urlopen(
            'https://www.timeserver.ru/cities/ru/moscow').read()
        soup = BeautifulSoup(html_doc, "html.parser")

        time = soup.find('div', 'timeview-data')
        parse_list = time.find_all('span', {})

        hours = parse_list[0].text
        minutes = parse_list[2].text
        seconds = parse_list[4].text
        text = hours + ':' + minutes
        if seconds % 2 == 0:
            text = text[:2] + ' ' + text[3:]
        return text

    def check_time_zone(self, text, time_zone):
        if time_zone == '(UTC−12)':
            text = str(int(text[:2]) + 9) + text[2:]

        elif time_zone == 'Ниуэ (UTC−11)':
            text = str(int(text[:2]) + 10) + text[2:]

        elif time_zone == 'США(Гавайи) (UTC−10)':
            text = str(int(text[:2]) + 11) + text[2:]

        elif time_zone == 'США(Аляска) (UTC−9)':
            text = str(int(text[:2]) + 12) + text[2:]

        elif time_zone == 'североамериканское тихоокеанское время\
                              (UTC-8)':
            text = str(int(text[:2]) + 13) + text[2:]

        elif time_zone == 'горное время (UTC-7)':
            text = str(int(text[:2]) + 14) + text[2:]

        elif time_zone == 'центральноамериканское время (UTC-6)':
            text = str(int(text[:2]) + 15) + text[2:]

        elif time_zone == 'североамериканское восточное время\
                              (UTC-5)':
            text = str(int(text[:2]) + 16) + text[2:]

        elif time_zone == 'атлантическое время (UTC-4)':
            text = str(int(text[:2]) + 17) + text[2:]

        elif time_zone == 'Канада (Ньюфаундленд) (UTC−3:30)':
            text = str(int(text[:2]) + 17) + text[2] + str(int(text[3:]) + 30)

        elif time_zone == 'южноамериканское восточное время (UTC-3)':
            text = str(int(text[:2]) + 18) + text[2:]

        elif time_zone == 'среднеатлантическое время (UTC-2)':
            text = str(int(text[:2]) + 19) + text[2:]

        elif time_zone == 'Азорские острова (UTC−1)':
            text = str(int(text[:2]) + 20) + text[2:]

        elif time_zone == 'западноафриканское время (UTC+0)':
            text = str(int(text[:2]) + 21) + text[2:]

        elif time_zone == 'центральноевропейское время (UTC+1)':
            text = str(int(text[:2]) + 22) + text[2:]

        elif time_zone == 'восточноевропейское время (UTC+2)':
            text = str(int(text[:2]) + 23) + text[2:]

        elif time_zone == 'московское время (UTC+3)':
            text = text

        elif time_zone == 'Иран (UTC+3:30)':
            text = text[:3] + str(int(text[3:]) + 30)

        elif time_zone == 'самарское время (UTC+4)':
            text = str(int(text[:2]) + 1) + text[2:]

        elif time_zone == 'Афганистан (UTC+4:30)':
            text = str(int(text[:2]) + 1) + text[2] + str(int(text[3:]) + 30)

        elif time_zone == 'екатеринбургское время (UTC+5)':
            text = str(int(text[:2]) + 2) + text[2:]

        elif time_zone == 'Индия (UTC+5:30)':
            text = str(int(text[:2]) + 2) + text[2] + str(int(text[3:]) + 30)

        elif time_zone == 'Непал (UTC+5:45)':
            text = str(int(text[:2]) + 2) + text[2] + str(int(text[3:]) + 45)

        elif time_zone == 'омское время (UTC+6)':
            text = str(int(text[:2]) + 3) + text[2:]

        elif time_zone == 'Мьянма (UTC+6:30)':
            text = str(int(text[:2]) + 3) + text[2] + str(int(text[3:]) + 30)

        elif time_zone == 'красноярское время (UTC+7)':
            text = str(int(text[:2]) + 4) + text[2:]

        elif time_zone == 'иркутское время (UTC+8)':
            text = str(int(text[:2]) + 5) + text[2:]

        elif time_zone == 'Австралия (UTC+8:45)':
            text = str(int(text[:2]) + 5) + text[2] + str(int(text[3:]) + 45)

        elif time_zone == 'якутское время (UTC+9)':
            text = str(int(text[:2]) + 6) + text[2:]

        elif time_zone == 'Австралия (UTC+9:30)':
            text = str(int(text[:2]) + 6) + text[2] + str(int(text[3:]) + 30)

        elif time_zone == 'владивостокское время (UTC+10)':
            text = str(int(text[:2]) + 7) + text[2:]

        elif time_zone == 'Австралия (UTC+10:30)':
            text = str(int(text[:2]) + 7) + text[2] + str(int(text[3:]) + 30)

        elif time_zone == 'магаданское время (UTC+11)':
            text = str(int(text[:2]) + 8) + text[2:]

        elif time_zone == 'камчатское время (UTC+12)':
            text = str(int(text[:2]) + 9) + text[2:]

        elif time_zone == 'Новая Зеландия (UTC+12:45)':
            text = str(int(text[:2]) + 9) + text[2] + str(int(text[3:]) + 45)

        elif time_zone == 'Тонга (UTC+13)':
            text = str(int(text[:2]) + 10) + text[2:]

        elif time_zone == 'Кирибати (UTC+14)':
            text = str(int(text[:2]) + 11) + text[2:]

        if (QTime.currentTime().second() % 2) == 0:
            separator = ' '
        else:
            separator = ':'

        try:
            int(text[2])
            text = '0' + text
        except Exception:
            pass

        if int(text[:2]) > 23:
            if int(text[:2]) - 24 < 10:
                text = '0' + str(int(text[:2]) - 24) + separator + \
                    text[3:]
            else:
                text = str(int(text[:2]) - 24) + separator + text[3:]

        if int(text[3:]) > 59:
            if int(text[3:]) - 60 < 10:
                text = str(int(text[:2]) + 1) + \
                    '0' + str(int(text[3:]) - 60)
            else:
                text = str(int(text[:2]) + 1) + \
                    separator + str(int(text[3:]) - 60)

        return text


class AlarmWindow(QWidget):
    def __init__(self, other):
        super().__init__()
        self.setGeometry(300, 300, 150, 100)
        self.setWindowTitle('Будильник')

        self.alarm_edit = QTimeEdit(self)
        self.alarm_edit.move(30, 10)

        self.alarm_set_button = QPushButton(self)
        self.alarm_set_button.setText("Поставить")
        self.alarm_set_button.resize(self.alarm_set_button.sizeHint())
        self.alarm_set_button.move(28, 40)
        self.alarm_set_button.clicked.connect(self.set_alarm)

    def set_alarm(self):
        global alarm_hour, alarm_minute
        alarm_hour = self.alarm_edit.dateTime().time().hour()
        alarm_minute = self.alarm_edit.dateTime().time().minute()
        self.close()


class StopAlarmWindow(QWidget):
    def __init__(self, other):
        super().__init__()
        self.setGeometry(300, 300, 150, 100)

        mixer.init()
        mixer.music.load('music.mp3')
        mixer.music.play()

        self.alarm_reset_button = QPushButton(self)
        self.alarm_reset_button.setText("Выключить")
        self.alarm_reset_button.resize(self.alarm_reset_button.sizeHint())
        self.alarm_reset_button.move(28, 10)
        self.alarm_reset_button.clicked.connect(self.reset_alarm)

        self.alarm_add_five_minute_button = QPushButton(self)
        self.alarm_add_five_minute_button.setText("Добавить 5 минут")
        self.alarm_add_five_minute_button.resize(
            self.alarm_add_five_minute_button.sizeHint())
        self.alarm_add_five_minute_button.move(28, 40)
        self.alarm_add_five_minute_button.clicked.connect(self.add_five_minute)

    def reset_alarm(self):
        mixer.music.stop()
        self.close()

    def add_five_minute(self):
        global alarm_hour, alarm_minute
        mixer.music.stop()
        alarm_hour = int(QTime.currentTime().toString('hh').lstrip('0'))
        alarm_minute = int(QTime.currentTime().toString('mm').lstrip('0')) + 5
        if alarm_minute > 59:
            alarm_minute = 60 - alarm_minute
            alarm_hour += 1
        self.close()


app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.exit(app.exec_())
