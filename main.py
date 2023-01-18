import threading
import time

requests = []
current_floor = 5
direction = None


def up_movement(up, up_temp):
    global current_floor
    for i in range(len(up)):
        time.sleep(5)
        current_floor = up[i]
        requests.remove(up[i])
        up_temp.remove(up[i])
        print(f'we are at floor {current_floor}')


def down_movement(down, down_temp):
    global current_floor
    for i in range(len(down) - 1, -1, -1):
        time.sleep(5)
        current_floor = down[i]
        requests.remove(down[i])
        down_temp.remove(down[i])
        print(f'we are at floor {current_floor}')


def handle_request(requests):
    down = []
    up = []

    global current_floor
    global direction

    for req in requests:
        if req > current_floor:
            up.append(req)
        elif req < current_floor:
            down.append(req)

    up.sort()
    down.sort()

    up_temp = up.copy()
    down_temp = down.copy()

    if up and down:
        for i in range(2):
            if direction == 'down':
                down_movement(down, down_temp)
                if up_temp:
                    direction = "up"

            elif direction == "up":
                up_movement(up, up_temp)
                if down_temp:
                    direction = "down"

    elif up:
        direction = 'up'
        up_movement(up, up_temp)

    elif down:
        direction = 'down'
        down_movement(down, down_temp)


def get_input():
    while True:
        request = int(input())
        requests.append(request)


threading.Thread(target=get_input).start()

while True:
    if requests:
        handle_request(requests)

