from threading import Thread
import time
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QIcon
import sys


def start_req():
    while True:
        if Window.requests:

            requests_temp = Window.requests.copy()

            for req in requests_temp:
                Window.requests.remove(req)

                if req[0] == 'e':

                    if elevator1.current_floor == req[1]:
                        print(f'We are at elevator {elevator1.name} and at floor {elevator1.current_floor}')
                    elif elevator2.current_floor == req[1]:
                        print(f'We are at elevator {elevator2.name} and at floor {elevator2.current_floor}')
                    elif elevator3.current_floor == req[1]:
                        print(f'We are at elevator {elevator3.name} and at floor {elevator3.current_floor}')
                    else:
                        Elevator.choose_elevator(elevator1, elevator2, elevator3, req[1]).requests.append(req[1])

                else:

                    if req[1] == 1:
                        if elevator1.current_floor != req[2]:
                            elevator1.requests.append(req[2])
                        else:
                            print(f'We are at elevator {elevator1.name} and at floor {elevator1.current_floor}')

                    elif req[1] == 2:
                        if elevator2.current_floor != req[2]:
                            elevator2.requests.append(req[2])
                        else:
                            print(f'We are at elevator {elevator2.name} and at floor {elevator2.current_floor}')

                    else:
                        if elevator3.current_floor != req[2]:
                            elevator3.requests.append(req[2])
                        else:
                            print(f'We are at elevator {elevator3.name} and at floor {elevator3.current_floor}')


class Elevator(Thread):

    def __init__(self, name, current_floor):

        Thread.__init__(self)
        self.name = name
        self.current_floor = current_floor
        self.direction = 'up' or 'down'
        self.requests = []

    def up_movement(self, up, up_temp):
        for i in range(len(up)):
            self.current_floor = up[i]
            self.requests.remove(up[i])
            up_temp.remove(up[i])
            print(f'We are at elevator {self.name} and at floor {self.current_floor}')
            window.move_elevator(int(self.name), self.current_floor)

    def down_movement(self, down, down_temp):
        for i in range(len(down) - 1, -1, -1):
            self.current_floor = down[i]
            self.requests.remove(down[i])
            down_temp.remove(down[i])
            print(f'We are at elevator {self.name} and at floor {self.current_floor}')
            window.move_elevator(int(self.name), self.current_floor)

    def handle_request(self):
        down = []
        up = []

        for req in self.requests:
            if req > self.current_floor:
                up.append(req)
            elif req < self.current_floor:
                down.append(req)

        up.sort()
        down.sort()
        up_temp = up.copy()
        down_temp = down.copy()

        if up and down:

            for i in range(2):

                if self.direction == 'down':
                    self.down_movement(down, down_temp)
                    if up_temp:
                        self.direction = 'up'

                elif self.direction == 'up':
                    self.up_movement(up, up_temp)
                    if down_temp:
                        self.direction = 'down'

        elif up:
            self.direction = 'up'
            self.up_movement(up, up_temp)

        elif down:
            self.direction = 'down'
            self.down_movement(down, down_temp)

    @staticmethod
    def choose_elevator(a, b, c, floor):
        elevator = [a, b, c]
        result = {
            elevator[0]: 0,
            elevator[1]: 0,
            elevator[2]: 0
        }

        for e in elevator:

            # اگر آسانسور در طبقه ای، زیر طبقه درخواست باشد و به بالا حرکت کند
            if e.current_floor < floor and e.direction == "up":
                result[e] = (floor - e.current_floor) * 2
                for n in e.requests:
                    if e.current_floor < n < floor:
                        result[e] += 2

            # اگر آسانسور در طبقه ای، زیر طبقه درخواست باشد و به پایین حرکت کند
            elif e.current_floor < floor and e.direction == "down":

                if e.requests and min(e.requests) < e.current_floor:
                    result[e] = ((e.current_floor - min(e.requests)) + (floor - min(e.requests))) * 2
                else:
                    result[e] = (floor - e.current_floor) * 2

                for n in e.requests:
                    if n < floor:
                        result[e] += 2

            # اگر آسانسور در طبقه ای، بالای طبقه درخواست باشد و به بالا حرکت کند
            elif e.current_floor > floor and e.direction == "up":

                if e.requests and max(e.requests) > e.current_floor:
                    result[e] = ((max(e.requests) - e.current_floor) + (max(e.requests) - floor)) * 2
                else:
                    result[e] = (e.current_floor - floor) * 2

                for n in e.requests:
                    if n > floor:
                        result[e] += 2

            # اگر آسانسور در طبقه ای، بالای طبقه درخواست باشد و به پایین حرکت کند
            else:
                result[e] = (e.current_floor - floor) * 2
                for n in e.requests:
                    if floor < n < e.current_floor:
                        result[e] += 2

        x = min(result.get(elevator[0]), result.get(elevator[1]), result.get(elevator[2]))
        for e in elevator:
            if result.get(e) == x:
                return e

    @pyqtSlot()
    def run(self):
        while True:
            if self.requests:
                self.handle_request()


class Window(QMainWindow):
    requests = []

    def __init__(self):
        super().__init__()

        self.acceptDrops()
        self.setWindowTitle("Elevator")
        self.setWindowIcon(QIcon('images/icon.png'))
        self.setFixedSize(1300, 640)
        # self.setFixedSize(2600, 1280)
        self.setStyleSheet("background-image: url(images/back.png);")
        self.label3 = QLabel(self)
        self.label0 = QLabel(self)
        self.label1 = QLabel(self)
        self.label2 = QLabel(self)

        self.pixmap0 = QPixmap('images/0.png')
        self.pixmap1 = QPixmap('images/1.png')
        self.pixmap2 = QPixmap('images/2.png')
        self.pixmap3 = QPixmap('images/3.png')

        self.label0.setPixmap(self.pixmap0)
        self.label1.setPixmap(self.pixmap1)
        self.label2.setPixmap(self.pixmap2)
        self.label3.setPixmap(self.pixmap3)

        self.label0.setGeometry(672, 600, self.pixmap0.width(), self.pixmap0.height())
        self.label1.setGeometry(702, 600, self.pixmap1.width(), self.pixmap1.height())
        self.label2.setGeometry(733, 600, self.pixmap2.width(), self.pixmap2.height())
        self.label3.setGeometry(640, 0, self.pixmap3.width(), self.pixmap3.height())
        # self.label0.setGeometry(1344, 1200, self.pixmap0.width(), self.pixmap0.height())
        # self.label1.setGeometry(1404, 1200, self.pixmap1.width(), self.pixmap1.height())
        # self.label2.setGeometry(1466, 1200, self.pixmap2.width(), self.pixmap2.height())
        # self.label3.setGeometry(1280, 0, self.pixmap3.width(), self.pixmap3.height())

        self.label4 = QLabel(self)
        self.label4.setText(' Internal 1:')
        self.label4.setGeometry(20, 20, 120, 40)
        # self.label4.setGeometry(40, 40, 240, 80)
        self.label4.setStyleSheet(open('stylesheet/labelSheet.css').read())

        self.label5 = QLabel(self)
        self.label5.setText(' Internal 2:')
        self.label5.setGeometry(20, 80, 120, 40)
        # self.label5.setGeometry(40, 160, 240, 80)
        self.label5.setStyleSheet(open('stylesheet/labelSheet.css').read())

        self.label6 = QLabel(self)
        self.label6.setText(' Internal 3:')
        self.label6.setGeometry(20, 140, 120, 40)
        # self.label6.setGeometry(40, 280, 240, 80)
        self.label6.setStyleSheet(open('stylesheet/labelSheet.css').read())

        self.label7 = QLabel(self)
        self.label7.setText(' External:')
        self.label7.setGeometry(20, 200, 100, 40)
        # self.label7.setGeometry(40, 400, 200, 80)
        self.label7.setStyleSheet(open('stylesheet/labelSheet.css').read())

        self.line1 = QLineEdit(self)
        self.line1.move(140, 20)
        self.line1.resize(50, 40)
        # self.line1.move(280, 40)
        # self.line1.resize(100, 80)
        self.line1.setStyleSheet(open('stylesheet/textboxSheet.css').read())

        self.line2 = QLineEdit(self)
        self.line2.move(140, 80)
        self.line2.resize(50, 40)
        # self.line2.move(280, 160)
        # self.line2.resize(100, 80)
        self.line2.setStyleSheet(open('stylesheet/textboxSheet.css').read())

        self.line3 = QLineEdit(self)
        self.line3.move(140, 140)
        self.line3.resize(50, 40)
        # self.line3.move(280, 280)
        # self.line3.resize(100, 80)
        self.line3.setStyleSheet(open('stylesheet/textboxSheet.css').read())

        self.line4 = QLineEdit(self)
        self.line4.move(120, 200)
        self.line4.resize(70, 40)
        # self.line4.move(240, 400)
        # self.line4.resize(140, 80)
        self.line4.setStyleSheet(open('stylesheet/textboxSheet.css').read())

        pybutton1 = QPushButton('GO', self)
        pybutton1.clicked.connect(self.internal1_req)
        pybutton1.resize(50, 40)
        pybutton1.move(200, 20)
        # pybutton1.resize(100, 80)
        # pybutton1.move(400, 40)
        pybutton1.setStyleSheet(open('stylesheet/buttonSheet.css').read())

        pybutton2 = QPushButton('GO', self)
        pybutton2.clicked.connect(self.internal2_req)
        pybutton2.resize(50, 40)
        pybutton2.move(200, 80)
        # pybutton2.resize(100, 80)
        # pybutton2.move(400, 160)
        pybutton2.setStyleSheet(open('stylesheet/buttonSheet.css').read())

        pybutton3 = QPushButton('GO', self)
        pybutton3.clicked.connect(self.internal3_req)
        pybutton3.resize(50, 40)
        pybutton3.move(200, 140)
        # pybutton3.resize(100, 80)
        # pybutton3.move(400, 280)
        pybutton3.setStyleSheet(open('stylesheet/buttonSheet.css').read())

        pybutton4 = QPushButton('GO', self)
        pybutton4.clicked.connect(self.external_req)
        pybutton4.resize(50, 40)
        pybutton4.move(200, 200)
        # pybutton4.resize(100, 80)
        # pybutton4.move(400, 400)
        pybutton4.setStyleSheet(open('stylesheet/buttonSheet.css').read())

        self.show()

    def internal1_req(self):
        Window.requests.append(['i', 1, int(self.line1.text())])
        self.line1.clear()

    def internal2_req(self):
        Window.requests.append(['i', 2, int(self.line2.text())])
        self.line1.clear()

    def internal3_req(self):
        Window.requests.append(['i', 3, int(self.line3.text())])
        self.line1.clear()

    def external_req(self):
        Window.requests.append(['e', int(self.line4.text())])
        self.line1.clear()

    def move_elevator(self, elevator, floor):
        y = ((15 - floor) * 40)
        # y = ((15 - floor) * 80)
        elevator_label = None
        x = None

        if elevator == 1:
            elevator_label = window.label0
            x = 672
            # x = 1344
        elif elevator == 2:
            elevator_label = window.label1
            x = 702
            # x = 1404
        elif elevator == 3:
            elevator_label = window.label2
            x = 733
            # x = 1466

        while elevator_label.y() != y:
            if elevator_label.y() < y:
                elevator_label.move(x, elevator_label.y() + 5)
                # elevator_label.move(x, elevator_label.y() + 10)
            else:
                elevator_label.move(x, elevator_label.y() - 5)
                # elevator_label.move(x, elevator_label.y() - 10)
            time.sleep(0.0001)

        time.sleep(1)


App = QApplication(sys.argv)
window = Window()
elevator1 = Elevator('1', 0)
elevator2 = Elevator('2', 0)
elevator3 = Elevator('3', 0)
elevator1.start()
elevator2.start()
elevator3.start()
Thread(target=start_req).start()
sys.exit(App.exec())
