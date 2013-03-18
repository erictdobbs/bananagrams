
from pygame import *
import random
import math
from pygame.locals import *
import mmap
from time import sleep


#####################################################################
# blankcoord()
# Returns a pair (x,y) of a blank cell on the board. 
def blankcoord():
    blanks = []
    for ii in range(COLS):
        for jj in range(ROWS):
            if array[ii][jj] == ' ': blanks.append((ii,jj))
    return random.choice(blanks)
#####################################################################


#####################################################################
# checkdictionary(string)
# Returns TRUE if string is in the dictionary file, or FALSE if not. 
def checkdictionary(string):
    if (string + "\n") in (open('C:\Python27\dictionary.txt').read()).upper():
        return True
    else: return False
#####################################################################

 
##################################################################### 
# checkwords()
# Returns TRUE if the board is in a valid configuration. This requires that: 
#    1) The cursor is not currently holding a tile
#    2) All sets of tiles are at least 3 tiles long
#    3) Each set of tiles forms an English word 
# Returns FALSE if any of the above conditions are not met. 
def checkwords():
    global wrongfade
    wrongfade = 0
    #for cell in invalid: invalid.remove(cell)
    if grabbed != ' ': return False
    valid = True
    
    # This section checks that all cells are part of one contiguous region
    unchecked = []
    neighbors = []
    done = []
    for ii in range(COLS):
        for jj in range(ROWS):
            if array[ii][jj] != ' ' and array[ii][jj] != '_': unchecked.append((ii,jj))
    cell = unchecked.pop(0)
    if unchecked.count((cell[0]+1,cell[1])) != 0: 
        neighbors.append((cell[0]+1,cell[1]))
        unchecked.remove((cell[0]+1,cell[1]))
    if unchecked.count((cell[0]-1,cell[1])) != 0: 
        neighbors.append((cell[0]-1,cell[1]))
        unchecked.remove((cell[0]-1,cell[1]))   
    if unchecked.count((cell[0],cell[1]+1)) != 0: 
        neighbors.append((cell[0],cell[1]+1))
        unchecked.remove((cell[0],cell[1]+1))  
    if unchecked.count((cell[0],cell[1]-1)) != 0: 
        neighbors.append((cell[0],cell[1]-1))
        unchecked.remove((cell[0],cell[1]-1))
    done.append(cell)
    while len(neighbors) != 0:
        cell = neighbors.pop(0)
        if unchecked.count((cell[0]+1,cell[1])) != 0: 
            neighbors.append((cell[0]+1,cell[1]))
            unchecked.remove((cell[0]+1,cell[1]))
        if unchecked.count((cell[0]-1,cell[1])) != 0: 
            neighbors.append((cell[0]-1,cell[1]))
            unchecked.remove((cell[0]-1,cell[1]))   
        if unchecked.count((cell[0],cell[1]+1)) != 0: 
            neighbors.append((cell[0],cell[1]+1))
            unchecked.remove((cell[0],cell[1]+1))  
        if unchecked.count((cell[0],cell[1]-1)) != 0: 
            neighbors.append((cell[0],cell[1]-1))
            unchecked.remove((cell[0],cell[1]-1))
        done.append(cell)
        

    if len(unchecked) > 0: 
        valid = False
    
    # This section makes sure all formed words are in the dictionary
    for ii in range(COLS):
        for jj in range(ROWS):
            string = ""
            if not array[ii][jj] in [' ','_']:
                if jj == 0 or array[ii][jj-1] in [' ','_']:
                    kk = jj
                    while kk != ROWS and not array[ii][kk] in [' ','_']:
                        string += array[ii][kk] 
                        kk += 1
            if len(string) > 1: 
                if checkdictionary(string) == False or len(string) < 3:
                    kk -= 1
                    valid = False
                    while kk >= jj: 
                        invalid.append((ii,kk))
                        kk -= 1
            string = ""
            if not array[ii][jj] in [' ','_']:
                if ii == 0 or array[ii-1][jj] in [' ','_']:
                    kk = ii
                    while kk != COLS and not array[kk][jj] in [' ','_']:
                        string += array[kk][jj] 
                        kk += 1
            if len(string) > 1: 
                if checkdictionary(string) == False or len(string) < 3:
                    valid = False
                    kk -= 1
                    while kk >= ii: 
                        invalid.append((kk,jj))
                        kk -= 1
                 
    if valid == False: 
        wrongfade = 195
        return False
    else: return True
#####################################################################

 
#####################################################################
# tilecolor(char)
# Returns a list [R,G,B] based on the character given. This function
# is deterministic, so any given character will always get the same
# result.
def tilecolor(char):
    if char == ' ': return [200,200,100]
    if char == '_': return [ 60, 60, 30 ]
    value = ord(char) - 65 # range 0 to 25
    return [ int( 60 * (math.sin(value) + 3)) , int( 60 * (math.sin(3*value) + 3)), int( 60 * (math.sin(5*value) + 3))]
#####################################################################


#####################################################################
# drawtile(ii,jj)
# Draws the cell at (ii,jj) to the screen. Draws the colored tile, 
# the character, and an outline.
def drawtile(ii, jj):
    char = array[ii][jj].upper()
    draw.rect(screen, tilecolor(char), (framehor + ii*SIZE, framever + jj*SIZE, SIZE, SIZE))
    if not char in [' ','_']: 
        myfont = font.SysFont("Times New Roman", SIZE - 3)
        label = myfont.render(char, 1, [0,0,0])
        screen.blit(label, (framehor + ii*SIZE - ((myfont.size(char))[0] - SIZE)/2, framever + jj*SIZE + 1))
    draw.rect(screen, [60,60,60], (framehor + ii*SIZE, framever + jj*SIZE, SIZE, SIZE), 2)
#####################################################################


#####################################################################
# drawconsole()
# Draws the portion of the screen below the gameboard, including the 
# game clock.  
def drawconsole():
    screen.fill([200,200,100])
    draw.rect(screen, [60,60,60], (framehor-3, framever-3 + SIZE*(ROWS+1), SIZE*COLS+7, SIZE*2+7), 3)
    draw.rect(screen, [60,60,60], (framehor, framever + SIZE*(ROWS+1), SIZE*COLS, SIZE*2), 2)
    myfont = font.SysFont("Courier", 2*SIZE - 3)
    label = myfont.render(str(round(gametime,1)), 1, [0,0,0])
    screen.blit(label,(framehor + 5, framever + SIZE*(ROWS+1) + 2))
#####################################################################


#####################################################################
# drawgameboard()
# Draws the gameboard, both the cells in the board and any tile 
# currently held. Colors borders on cells that form an incorrect 
# word. 
def drawgameboard():
    global wrongfade
    draw.rect(screen, [60,60,60], (framehor-3, framever-3, SIZE*COLS+7, SIZE*ROWS+7), 3)
    for ii in range(COLS):
        for jj in range(ROWS):
            drawtile(ii,jj)
    if len(invalid) > 0:
        wrongfade -= 1
        if wrongfade < 0: wrongfade = 0
        for cell in invalid:
            draw.rect(screen, [60 + wrongfade,60,60], (framehor + cell[0]*SIZE, framever + cell[1]*SIZE, SIZE, SIZE), 2)
            if wrongfade == 0: invalid.remove(cell)
    if grabbed != ' ':
        draw.rect(screen, [60,60,60], (framehor + mousex + 1 - offsetx, framever + mousey + 1 - offsety, SIZE, SIZE), 1)
        draw.rect(screen, [60,60,60], (framehor + mousex + 2 - offsetx, framever + mousey + 2 - offsety, SIZE, SIZE), 1)
        draw.rect(screen, tilecolor(grabbed), (framehor + mousex - offsetx, framever + mousey - offsety, SIZE, SIZE))
        myfont = font.SysFont("Times New Roman", SIZE - 3)
        label = myfont.render(grabbed, 1, [0,0,0])
        screen.blit(label, (framehor + mousex - offsetx - ((myfont.size(grabbed))[0] - SIZE)/2, framever + mousey + 1 - offsety))
        draw.rect(screen, [60,60,60], (framehor + mousex - offsetx, framever + mousey - offsety, SIZE, SIZE), 2)
#####################################################################



init()
mixer.init()
#soundpop = mixer.Sound("C:\Windows\Media\Windows Pop-up Blocked.wav")
ROWS = 15
COLS = 13
SIZE = 40
array = [[' ']*ROWS for x in xrange(COLS)] # format is array[column][row]
invalid = []

screenwidth = int(SIZE * COLS)
screenheight = int(SIZE * ROWS)
framehor = SIZE
framever = SIZE

screen=display.set_mode([screenwidth + framehor*2,screenheight + framever*5])
display.set_caption("BANANAGRAMS!")
screen.fill([200,200,100])

done = False
grabbed = ' '
offsetx = 0
offsety = 0
waitmouse = 0
wrongfade = 0    
clock = time.Clock()
gametime = 0.0
letterfreq = [13,3,3,6,18,3,4,3,12,2,2,5,3,8,11,3,2,9,6,9,6,3,3,2,3,2]
letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
letterbag = ""
for ii in range(len(letters)): letterbag += letterfreq[ii] * letters[ii]


def peelletter():
    global letterbag, grabbed
    grabbed = random.choice(letterbag)
    newletterbag = letterbag.replace(grabbed, "", 1)
    letterbag = newletterbag
    
def freshletters(numletters):
    for ii in range(COLS): 
        for jj in range(ROWS): 
            array[ii][jj] = ' '
    for ii in range(4):
        (randx, randy) = blankcoord()
        array[randx][randy] = '_'
    letterbag = ""
    for ii in range(len(letters)): letterbag += letterfreq[ii] * letters[ii]
    skipanimation = False
    for ii in range(numletters): 
        character = random.choice(letterbag)
        newletterbag = letterbag.replace(character, "", 1)
        letterbag = newletterbag
        (randx, randy) = blankcoord()
        array[randx][randy] = character
        drawconsole()
        drawgameboard()
        display.flip()
        if skipanimation == False: 
            sleep(0.15)
            #soundpop.play()
        for myevent in event.get():
            if myevent.type == MOUSEBUTTONDOWN or myevent.type == KEYDOWN: skipanimation = True

freshletters(21)
while done==False:
    if gametime == 0: 
        clock.tick()
        gametime += 0.001
    else: gametime += clock.tick()/1000.0
    drawconsole()
    drawgameboard()
    for myevent in event.get(): # User did something
        try:
            if myevent.type == QUIT: # If user clicked close
                done=True # Flag that we are done so we exit this loop
            if myevent.type == MOUSEBUTTONDOWN and grabbed == ' ' and waitmouse == 0:
                invalid = []
                waitmouse = 1
                mousex = myevent.pos[0] - framehor
                mousey = myevent.pos[1] - framever
                if mousex < 0 or mousex > screenwidth: continue
                if mousey < 0 or mousey > screenheight: continue
                if not array[mousex/SIZE][mousey/SIZE] in [' ','_']:
                    # PICKING UP A TILE
                    grabbed = array[mousex/SIZE][mousey/SIZE]
                    array[mousex/SIZE][mousey/SIZE] = ' '
                    offsetx = mousex % SIZE
                    offsety = mousey % SIZE
            if myevent.type == MOUSEBUTTONDOWN and grabbed != ' ' and waitmouse == 0:
                invalid = []
                waitmouse = 1
                mousex = myevent.pos[0] - framehor
                mousey = myevent.pos[1] - framever
                if mousex + SIZE/2 - offsetx < 0 or mousex + SIZE/2 - offsetx > screenwidth: continue
                if mousey + SIZE/2 - offsety < 0 or mousey + SIZE/2 - offsety > screenheight: continue
                if array[(mousex + SIZE/2 - offsetx)/SIZE][(mousey + SIZE/2 - offsety)/SIZE] == ' ':
                    array[(mousex + SIZE/2 - offsetx)/SIZE][(mousey + SIZE/2 - offsety)/SIZE] = grabbed
                    grabbed = ' '
                elif array[(mousex + SIZE/2 - offsetx)/SIZE][(mousey + SIZE/2 - offsety)/SIZE] != '_':
                    temp = grabbed
                    grabbed = array[(mousex + SIZE/2 - offsetx)/SIZE][(mousey + SIZE/2 - offsety)/SIZE]
                    array[(mousex + SIZE/2 - offsetx)/SIZE][(mousey + SIZE/2 - offsety)/SIZE] = temp
            if myevent.type == MOUSEMOTION and grabbed != ' ':
                mousex = myevent.pos[0] - framehor
                mousey = myevent.pos[1] - framever
            if myevent.type == MOUSEBUTTONUP:
                waitmouse = 0
            if myevent.type == KEYDOWN:
                invalid = []
                if myevent.key == K_SPACE: 
                    # PEEL!
                    # First check that the board is valid 
                    if checkwords() == True: peelletter()
                if myevent.key == K_BACKSPACE: 
                    grabbed = ' '
                if myevent.key == K_r: 
                    freshletters(21)
                if myevent.key == K_LEFT: 
                    temp = array[0]
                    for ii in range(COLS - 1): array[ii] = array[ii + 1]
                    array[COLS - 1] = temp
                if myevent.key == K_RIGHT: 
                    temp = array[COLS - 1]
                    for ii in range(COLS - 1): array[COLS - ii - 1] = array[COLS - ii - 2]
                    array[0] = temp
                if myevent.key == K_UP:
                    temp = [0]*COLS
                    for ii in range(COLS): temp[ii] = array[ii][0]
                    for ii in range(COLS): 
                        for jj in range(ROWS - 1): 
                            array[ii][jj] = array[ii][jj+1]
                    for ii in range(COLS): array[ii][ROWS-1] = temp[ii]
                if myevent.key == K_DOWN:
                    temp = [0]*COLS
                    for ii in range(COLS): temp[ii] = array[ii][ROWS-1]
                    for ii in range(COLS): 
                        for jj in range(ROWS - 1): 
                            array[ii][ROWS - 1 - jj] = array[ii][ROWS - 2 - jj]
                    for ii in range(COLS): array[ii][0] = temp[ii]
        except IndexError:
            continue
    display.flip()
    
    
quit()