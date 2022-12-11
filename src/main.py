from random import random
from tree import RGBXmasTree
from colorzero import Color
from time import sleep
import random
import signal

tree = RGBXmasTree()
colors = [Color('red'), Color('yellow'), Color('blue'), Color('green'), Color('orange'), Color('pink')]

def handle_exit(*args):
    print("signal")
    tree.close()

def random_colours(tree, iterations):
    iteration=0
    try:
        while iterations<=0 or iteration<iterations:
            if iterations>0:
                iteration+=1

            for color in colors:
                pixels=list(range(0,25))
                random.shuffle(pixels);
                for pixel in pixels:
                    tree[pixel].color=color

    except Exception as e:
        print(e)

def one_at_a_time(delay, colour):
    tree.color=(0,0,0)
    for pixel in range(0, 25):
        tree[pixel].color=colour
        if delay>0:
            sleep(delay)

def line(ix, colour):
    lines=[[0,6,7,12,13,18,21,22],[1,5,8,11,14,17,20,23],[16],[2,4,9,10,15,19,24],[3]]
    for pixel in lines[ix]:
        tree[pixel].color=colour

signal.signal(signal.SIGTERM, handle_exit)
signal.signal(signal.SIGINT, handle_exit)
signal.signal(signal.SIGILL, handle_exit)


tree.brightness=0.05
while True:
    random_colours(tree, 15)
    sleep(1)
    for colour in colors:
        one_at_a_time(1/20, colour)
    for colour in colors:
        tree.color=colour
        sleep(0.3)
        tree.color=Color('black')
        sleep(0.3)
    for colour in colors:
        for lx in range(0,5):
            line(lx, colour)
            sleep(1)
