from dis import code_info
from os import stat
from random import random
from tree import RGBXmasTree
from colorzero import Color
from time import sleep
from flask import Flask
from concurrent.futures import ThreadPoolExecutor
import random
import signal


app = Flask(__name__)

tree = RGBXmasTree()
state={}
state["value"]="stop"

executor = ThreadPoolExecutor(1)

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

def random_columns(tree, iterations):
    iteration=0
    try:
        while iterations<=0 or iteration<iterations:
            if iterations>0:
                iteration+=1

            for color in colors:
                columns=list(range(0,8))
                random.shuffle(columns);
                for cx in columns:
                    column(cx, color)

    except Exception as e:
        print(e)

def random_lines(tree, iterations):
    iteration=0
    try:
        while iterations<=0 or iteration<iterations:
            if iterations>0:
                iteration+=1

            for color in colors:
                lines=list(range(0,5))
                random.shuffle(lines);
                for lx in lines:
                    line(lx, color)

    except Exception as e:
        print(e)

def one_at_a_time(delay, colour):
    tree.color=(0,0,0)
    for pixel in range(0, 25):
        tree[pixel].color=colour
        if delay>0:
            sleep(delay)

def line(ix, colour):
    lines=[[0,6,7,12,15,19,16,24],[1,5,8,11,14,17,20,23],[13,18,22],[2,4,9,10, 21],[3]]
    for pixel in lines[ix]:
        tree[pixel].color=colour

def column(ix, colour):
    columns=[[0,1,2,3],[7,8,9],[19,20,21],[24,23,22],[12,11,10],[6,5,4,3],[16,17,18],[15,14,13]]
    for pixel in columns[ix]:
        tree[pixel].color=colour

def play():
    while True:
        if state["value"]=="stop":
            tree.brightness=0.05
            tree.color=Color('black')
            tree[3].color=Color('white')
            sleep(1)
            tree[3].color=Color('black')
            sleep(5)
            continue

        tree.brightness=0.05
        random_colours(tree, 15)
        if state["value"]=="stop":
            continue
        random_columns(tree, 15)
        if state["value"]=="stop":
            continue
        random_lines(tree, 15)
        if state["value"]=="stop":
            continue

        sleep(1)
        for colour in colors:
            one_at_a_time(1/50, colour)
        if state["value"]=="stop":
            continue
        for colour in colors:
            tree.color=colour
            sleep(0.3)
            tree.color=Color('black')
            sleep(0.3)
        if state["value"]=="stop":
            continue
        for colour in colors:
            for lx in range(0,5):
                line(lx, colour)
                sleep(1/50)
        if state["value"]=="stop":
            continue
        for colour in colors:
            for lx in reversed(range(0,5)):
                line(lx, colour)
                sleep(1/50)
        if state["value"]=="stop":
            continue
        prevColor=Color("white")
        for colour in colors:
            for cx in range(0,4):
                column(cx, colour)
                column(cx+4, colour)
                sleep(1/2)
                tree.color=prevColor
            prevColor=colour

signal.signal(signal.SIGTERM, handle_exit)
signal.signal(signal.SIGINT, handle_exit)
signal.signal(signal.SIGILL, handle_exit)

@app.route('/play')
def set_play():
    state["value"]='play'
    return 'play'

@app.route('/stop')
def set_stop():
    state["value"]='stop'
    return 'stop'

@app.route('/health')
def health():
    return state["value"]

if __name__ == '__main__':
    executor.submit(play)
    app.run(host="192.168.1.171", port=8080)