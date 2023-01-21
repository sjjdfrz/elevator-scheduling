from threading import Thread
import time

class Elevator(Thread):

    def __init__(self, name, current_floor):
        Thread.__init__(self)
        self.name = name
        self.current_floor = current_floor
        self.direction = 'up' or 'down'
        self.requests = []

    def up_movement(self, up, up_temp):
        for i in range(len(up)):
            time.sleep((up[i] - self.current_floor) * 2)
            self.current_floor = up[i]
            self.requests.remove(up[i])
            up_temp.remove(up[i])
            print(f'We are at elevator {self.name} and at floor {self.current_floor}')

    def down_movement(self, down, down_temp):
        for i in range(len(down) - 1, -1, -1):
            time.sleep((self.current_floor - down[i]) * 2)
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

    def run(self):
        while True:
            if self.requests:
                self.handle_request()

def get_input():
    global requests
    while True:
        request = input()
        request = request.split(' ')
        request[1] = int(request[1])
        if len(request) == 3:
            request[2] = int(request[2])
        requests.append(request)

requests = []
Thread(target=get_input).start()
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

                if one.current_floor == req[1]:
                    print(f'We are at elevator {one.name} and at floor {one.current_floor}')
                elif two.current_floor == req[1]:
                    print(f'We are at elevator {two.name} and at floor {two.current_floor}')
                elif three.current_floor == req[1]:
                    print(f'We are at elevator {three.name} and at floor {three.current_floor}')
                else:
                    Elevator.choose_elevator(one, two, three, req[1]).requests.append(req[1])

            else:

                if req[1] == 1:
                    if one.current_floor != req[2]:
                        one.requests.append(req[2])
                    else:
                        print(f'We are at elevator {one.name} and at floor {one.current_floor}')

                elif req[1] == 2:
                    if two.current_floor != req[2]:
                        two.requests.append(req[2])
                    else:
                        print(f'We are at elevator {two.name} and at floor {two.current_floor}')

                else:
                    if three.current_floor != req[2]:
                        three.requests.append(req[2])
                    else:
                        print(f'We are at elevator {three.name} and at floor {three.current_floor}')

