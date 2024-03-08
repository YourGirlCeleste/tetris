import random
import time
import os
import sys
import keyboard
import threading

height = 20
width = 10

map = []
pictoralConversion = {0: "  ", 1: "🟥", 2:"🟩", 3:"🟦", 4:"🟧", 5:"🟨", 6:"🟪", 7:"⬜"}
pieceSpawns = [

    [(0,5),(0,4),(1,5),(1,6)], # green
    [(0,5),(0,6),(1,5),(1,4)], # red
    [(0,4),(1,4),(1,5),(1,6)], # blue
    [(0,6),(1,4),(1,5),(1,6)], # orange
    [(0,6),(0,5),(1,6),(1,5)], # yellow
    [(0,5),(1,4),(1,5),(1,6)], # purpur
    [(0,4),(0,5),(0,6),(0,7)]  # white
]

def setup():

    for x in range(height):

        map.append([])
        map[-1] = [y - y for y in range(width)]
    
    inputThread = threading.Thread(target=inputListen)
    inputThread.start()

def display():

    print('--'*(width+1))

    # Game Board
    for x in range(height):
        print('|', end="")
        for y in range(width):
            print(pictoralConversion[map[x][y]], end="")
        print('|')
    
    print('--'*(width+1))

def moveCurrentBlock(block, index):
    global map, moveDirection

    block.sort(reverse=True)

    if(moveDirection == 'right'):

        for y,x in enumerate(block):

            map[x[0]][x[1]+1] = index
            map[x[0]][x[1]] = 0
            block[y] = list(block[y])
            block[y][1] += 1
            block[y] = tuple(block[y])
    
    elif(moveDirection == 'left'):

        for y,x in enumerate(block):

            map[x[0]][x[1]-1] = index
            map[x[0]][x[1]] = 0
            block[y] = list(block[y])
            block[y][1] -= 1
            block[y] = tuple(block[y])
        
    # Reset Move Direction
    moveDirection = ""

    # Move Down
    for y,x in enumerate(block):

        map[x[0]+1][x[1]] = index
        map[x[0]][x[1]] = 0
        block[y] = list(block[y])
        block[y][0] += 1
        block[y] = tuple(block[y])

def isBlockGrounded(block):
    global map

    for x in block:

        if((x[0] == height-1) or (map[x[0]+1][x[1]] != 0 and ((x[0]+1,x[1]) not in block))):

            return True
        
    return False

def inputListen():
    global moveDirection

    while True:

        userInput = keyboard.read_key()
        
        if userInput == 'left' or userInput == 'right':
            moveDirection = userInput

setup()

currentBlock = None
pieceIndex = None
moveDirection = ""

while True:

    if(currentBlock):

        if(isBlockGrounded(currentBlock)):
            currentBlock = None

    if(currentBlock == None):
        pieceIndex = random.randint(1,len(pieceSpawns)-1)
        currentBlock = pieceSpawns[pieceIndex][:]
    print(moveDirection)

    moveCurrentBlock(currentBlock, pieceIndex)
    display()
    time.sleep(0.4)
    os.system('cls')

sys.exit()
