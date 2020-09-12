import asyncio
import websockets
from time import sleep
from tracker import Tracker
from calculator import Calculator
from config import Config

connected = False

async def handler(socket, path):
    global connected
    if connected:
        await socket.close()
        return
    connected = True
    print(f'Connected from {socket.remote_address}')

    tracker = Tracker()
    calc = Calculator(tracker.width)
    while True:
        try:
            if tracker.update():
                calc.update(tracker.points)
                await socket.send(f'AngleX {calc.angle_x()}')
                await socket.send(f'AngleY {calc.angle_y()}')
                await socket.send(f'AngleZ {calc.angle_z()}')
                await socket.send(f'EyeLOpen {calc.eye_l_open()}')
                await socket.send(f'EyeROpen {calc.eye_r_open()}')
                await socket.send(f'EyeBallX {calc.eye_ball_x()}')
                await socket.send(f'EyeBallY {calc.eye_ball_y()}')
                await socket.send(f'MouthOpenY {calc.mouth_open_y()}')
                await socket.send(f'BodyAngleZ {calc.body_angle_z()}')
                sleep(Config['DELAY'] / 1000)
        except websockets.exceptions.ConnectionClosedError:
            connected = False
            print('Disconnect')
            break
        except Exception as e:
            print(e)


server = websockets.serve(handler, 'localhost', Config['PORT'])
asyncio.get_event_loop().run_until_complete(server)
asyncio.get_event_loop().run_forever()

