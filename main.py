from threading import Thread
import random
import time

class Elevator(Thread):

    def __init__(self, name, current_floor):
        Thread.__init__(self)
        self.name = name
        self.current_floor = current_floor
        self.direction = None
        self.requests = []

    def up_movement(self, up, up_temp):
        for i in range(len(up)):
            time.sleep(5)
            self.current_floor = up[i]
            self.requests.remove(up[i])
            up_temp.remove(up[i])
            print(f'We are at elevator {self.name} and at floor {self.current_floor}')

    def down_movement(self, down, down_temp):
        for i in range(len(down) - 1, -1, -1):
            time.sleep(5)
            self.current_floor = down[i]
            self.requests.remove(down[i])
            down_temp.remove(down[i])
            print(f'We are at elevator {self.name} and at floor {self.current_floor}')

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
                        self.direction = "up"

                elif self.direction == "up":
                    self.up_movement(up, up_temp)
                    if down_temp:
                        self.direction = "down"

        elif up:
            self.direction = 'up'
            self.up_movement(up, up_temp)

        elif down:
            self.direction = 'down'
            self.down_movement(down, down_temp)

    def run(self):
        while True:
            if self.requests:
                self.handle_request()

requests = []

def get_input():
    global requests
    while True:
        request = input()
        request = request.split(' ')
        request[1] = int(request[1])
        if len(request) == 3:
            request[2] = int(request[2])
        requests.append(request)

Thread(target = get_input).start()

one = Elevator('1', 5)
two = Elevator('2', 3)
three = Elevator('3', 2)
one.start()
two.start()
three.start()

while True:
    if requests:

        reauests_temp = requests.copy()

        for req in reauests_temp:
            requests.remove(req)

            if req[0] == 'e':
                x = random.randint(1, 3)
                if x == 1:
                    one.requests.append(req[1])
                elif x == 2:
                    two.requests.append(req[1])
                else:
                    three.requests.append(req[1])

            else:
                if req[1] == 1:
                    one.requests.append(req[2])
                elif req[1] == 2:
                    two.requests.append(req[2])
                else:
                    three.requests.append(req[2])



