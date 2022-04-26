from hashlib import new

from cv2 import cartToPolar
from sklearn.ensemble import RandomTreesEmbedding
from Track import *
from Car import *
from CarAI import *
from Monaco import setupMonaco
from Traces import clearTraces, saveTraces
from render import Render
from tqdm import tqdm
from multiprocessing import Process, Manager
import random
from copy import deepcopy
from ShowNet import NetRender
from Track import Track
import os
import time






points = [[143,112],[150,104],[159,94],[167,86],[176,78],[185,71],[196,64],[206,56],[217,49],[228,44],[238,37],[246,28],[255,22],[266,16],[277,15],[289,18],[300,25],[309,30],[318,36],[329,43],[339,49],[350,54],[360,59],[372,64],[383,68],[395,73],[405,77],[418,81],[428,86],[439,91],[450,97],[460,103],[471,108],[481,113],[494,116],[506,117],[519,117],[531,115],[542,113],[552,108],[561,101],[571,94],[580,85],[588,77],[595,68],[602,59],[610,50],[620,43],[631,37],[643,33],[654,31],[666,29],[679,28],[692,26],[703,25],[716,25],[727,27],[738,35],[739,46],[734,58],[726,67],[715,74],[703,79],[693,83],[682,87],[671,92],[659,99],[652,108],[653,119],[663,127],[674,128],[685,124],[697,120],[708,114],[718,107],[727,100],[738,94],[750,91],[760,98],[765,108],[765,120],[759,130],[751,138],[741,146],[730,152],[720,158],[710,165],[699,171],[690,177],[678,183],[668,188],[657,192],[646,196],[634,199],[621,201],[609,203],[597,204],[584,205],[572,206],[559,206],[547,206],[536,204],[523,202],[510,200],[499,196],[488,190],[476,183],[455,171],[440,167],[429,172],[418,168],[408,162],[398,156],[395,142],[375,131],[366,124],[356,120],[347,114],[335,109],[325,103],[315,99],[302,96],[291,93],[278,92],[266,92],[254,95],[241,99],[230,104],[220,108],[208,114],[198,120],[189,127],[182,138],[185,147],[194,158],[190,167],[182,176],[175,185],[168,194],[160,201],[149,206],[138,207],[125,208],[116,215],[107,221],[100,231],[93,241],[88,252],[86,263],[84,272],[75,278],[63,280],[51,279],[42,274],[33,268],[28,257],[28,246],[32,235],[42,227],[52,221],[60,217],[69,208],[77,199],[83,188],[90,175],[97,164],[103,155],[111,145],[119,138]]
width = 22

track = Track(points, width)
render = Render(track, 1000, 500)
netrender = NetRender(1000, 500)


def step(car, ren=False):
    if car.gameOver:
        pass
    else:
        car.control()
        car.move()
        car.updateScore()
        if car.checkCollision():
            car.gameOver = True
    if ren:
        render.render()
        render.renderCar(int(car.x), int(car.y), int(car.rot))
        render.show()

def render_net(car):
    net = car.nn
    netrender.drawNet(net)
    netrender.show()

name = 'moin'
car = CarAI(track)

if os.path.isfile(name + '.txt'):
    car.nn.load(name)
render_net(car)


steps = 0
while True:
    step(car, True)
    steps += 1
    if car.gameOver:
        print(f'steps: {steps} score: {car.score} score per step: {car.score/steps}')
        time.sleep(1)
        car.reset()
        steps = 0