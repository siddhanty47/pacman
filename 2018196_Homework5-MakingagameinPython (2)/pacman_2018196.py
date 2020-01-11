import pygame
from pygame.locals import *
from numpy import loadtxt
import time
import random
import shelve


''' -----------------pacman----------------
in this the palyer (pacman) has to collect all the coins to reach next level.
there are 2 level in total.
also to stop you there are 6 monsters which move through the game which will kill you if you collide with them.
there are some big coins which deactivates monster for short period of time :D
controls:
up arrow--- move up
down arrow--- move down
right arrow--- move right
left arrow--- move left
no key pressed --- no motion
stick to one arrow key--- continuos movement in that direction
'''

#Constants for the game
WIDTH, HEIGHT = (32,32)
WALL_COLOR = pygame.Color(0, 0, 255, 255) # BLUE
PACMAN_COLOR = pygame.Color(69, 139, 0, 255) # GREEN
MONSTER_COLOR = pygame.Color(255, 0, 0, 255) #RED
COIN_COLOR = pygame.Color(255, 255, 0, 255) # RED
#directions
DOWN = (0,1)
RIGHT = (1,0)
TOP = (0,-1)
LEFT = (-1,0)
k1=k2=k3=k4=k5=k6=(0,-1)   #monster initial movement
num=50                      #monster deactivate time
score=100
flag=0
move_direction=s=(0,0)            #pacman initial movement
times=0                         #time spend
image=pygame.image.load('PacmanR.png')

#Draws a rectangle for the wall
def draw_wall(screen, pos):
        pixels = pixels_from_points(pos)
        image=pygame.image.load('wall.png')
        screen.blit(image,(pos[0]*WIDTH,pos[1]*HEIGHT))

#Draws player
def draw_pacman(screen, pos, image):
        pixels = pixels_from_points(pos)
        screen.blit(image,(pos[0]*WIDTH,pos[1]*HEIGHT))


#Draws a circle for the coin
def draw_coin(screen, pos):
        pixels = pixels_from_points(pos)
        pygame.draw.circle(screen, COIN_COLOR, (pixels[0]+15,pixels[1]+15), 4)

#draw bonus/big coin
def draw_big_coin(screen, pos):
        pixels = pixels_from_points(pos)
        pygame.draw.circle(screen, COIN_COLOR, (pixels[0]+15,pixels[1]+15), 9)

#draw monster
def draw_monster(screen, pos):
        pixels = pixels_from_points(pos)
        image=pygame.image.load('580b57fcd9996e24bc43c316.png')
        screen.blit(image,(pos[0]*WIDTH,pos[1]*HEIGHT))

#Uitlity functions
def add_to_pos(pos, pos2):
        return (pos[0]+pos2[0], pos[1]+pos2[1])

def pixels_from_points(pos):
        return (pos[0]*WIDTH, pos[1]*HEIGHT)


#Initializing pygame start image
pygame.init()
image3=pygame.image.load('images.jpg')
screen = pygame.display.set_mode((960,672), 0, 32)      #screen size
pygame.display.set_caption('PACMAN')                    #tab caption
background = pygame.surface.Surface((960,672)).convert()
font = pygame.font.Font(None, 50)
text = font.render("loading....", 1, (255,255,255))
textpos = text.get_rect()
background.blit(text, (750,600))
screen.blit(background,(0,0))
screen.blit(image3,(20,0))               #showing image
pygame.display.update()
time.sleep(2)


#Initializing pygame menu
pygame.init()
screen = pygame.display.set_mode((960,672), 0, 32)
background = pygame.surface.Surface((960,672)).convert()
image3=pygame.image.load('668412AA.jpg')
screen.blit(image3,(0,0))
image2=pygame.image.load('Pac-Man-Logo.png')
screen.blit(image2,(WIDTH*3,0))
pygame.display.update()




#Initializing variables
layout = loadtxt('layout.txt', dtype=str)       #layout of pacman
rows, cols = layout.shape                       #rows and cols of layout
pacman_position = (11,10)                       #initial pacman position
#moster positions
monster_position = []
for col in range(cols):
        for row in range(rows):
                value = layout[row][col]
                pos = (col, row)
                if value == 'm':
                        monster_position.append((col,row))


#check if wall is there or not
def in_wall(pacman_position):
        if layout[pacman_position[1]][pacman_position[0]]=='b' or layout[pacman_position[1]][pacman_position[0]]=='c' or layout[pacman_position[1]][pacman_position[0]]=='m' or layout[pacman_position[1]][pacman_position[0]]=='.':
                return True
        else:
                return False

#return monster next step 
def monster_movement(pos,k):
        u=add_to_pos(pos,(0,-1))
        d=add_to_pos(pos,(0,1))
        r=add_to_pos(pos,(1,0))
        l=add_to_pos(pos,(-1,0))
        z=0
        possible_move=[]
        if (0,-1)!=k and (layout[u[1]][u[0]]=='b' or layout[u[1]][u[0]]=='.' or layout[u[1]][u[0]]=='c' or layout[u[1]][u[0]]=='m'):
                z=z+1
                possible_move.append((0,-1))
        if (0,1)!=k and (layout[d[1]][d[0]]=='b' or layout[d[1]][d[0]]=='.' or layout[d[1]][d[0]]=='c' or layout[d[1]][d[0]]=='m'):
                z=z+1
                possible_move.append((0,1))
        if (1,0)!=k and (layout[r[1]][r[0]]=='b' or layout[r[1]][r[0]]=='.' or layout[r[1]][r[0]]=='c' or layout[r[1]][r[0]]=='m'):
                z=z+1
                possible_move.append((1,0))
        if (-1,0)!=k and (layout[l[1]][l[0]]=='b' or layout[l[1]][l[0]]=='.' or layout[l[1]][l[0]]=='c' or layout[l[1]][l[0]]=='m'):
                z=z+1
                possible_move.append((-1,0))
        if len(possible_move)>=2:
                return random.choice(possible_move)             #random points
        else:
                return k

t=True
#take initial input 'enter'
while t:
        for event in pygame.event.get():
                if event.type==pygame.KEYDOWN:
                        if event.key==pygame.K_RETURN:
                                t=False
                                running=True

#initialize game ground
pygame.init()
screen = pygame.display.set_mode((960,672), 0, 32)
pygame.display.set_caption('PACMAN')                            #tab caption
background = pygame.surface.Surface((960,672)).convert()




# Main game loop
running = True
x=0
while True:
        for event in pygame.event.get():
                if event.type == QUIT:
                        exit()

        screen.blit(background, (0,0))
        key=pygame.key.get_pressed()

        #Draw board from the 2d layout array.
          #In the board, '.' denote the empty space, 'w' are the walls, 'c' are the coins, 'b' are big coins, 'm' are monsters
        for col in range(cols):
                for row in range(rows):
                        value = layout[row][col]
                        pos = (col, row)
                        if value == 'w':
                                draw_wall(screen, pos)
                        elif value == 'c' or value == 'm':
                                draw_coin(screen, pos)
                        elif value == 'b':
                                draw_big_coin(screen, pos)


        #Update player position based on movement.
        draw_pacman(screen, pacman_position,image)
        
        times=times+0.25                #time spend during a game
        key=pygame.key.get_pressed()
        #update monster positions
        if num>=50:                      
                num=50
                if monster_position[0]==(15,0) or monster_position[0]==(15,20) or monster_position[0]==(0,10) or monster_position[0]==(29,10):
                        move1=(0,0)
                else:
                        move1=monster_movement(monster_position[0],k1)
                k1=move1
                monster_position[0]=add_to_pos(monster_position[0],move1)
                if monster_position[1]==(15,0) or monster_position[1]==(15,20) or monster_position[1]==(0,10) or monster_position[1]==(29,10):
                        move2=(0,0)
                else:
                        move2=monster_movement(monster_position[1],k2)
                k2=move2
                monster_position[1]=add_to_pos(monster_position[1],move2)
                if monster_position[2]==(15,0) or monster_position[2]==(15,20) or monster_position[2]==(0,10) or monster_position[2]==(29,10):
                        move3=(0,0)
                else:
                        move3=monster_movement(monster_position[2],k3)
                k3=move3
                monster_position[2]=add_to_pos(monster_position[2],move3)
                if monster_position[3]==(15,0) or monster_position[3]==(15,20) or monster_position[3]==(0,10) or monster_position[3]==(29,10):
                        move4=(0,0)
                else:
                        move4=monster_movement(monster_position[3],k4)
                k4=move4
                monster_position[3]=add_to_pos(monster_position[3],move4)
                if monster_position[4]==(15,0) or monster_position[4]==(15,20) or monster_position[4]==(0,10) or monster_position[4]==(29,10):
                        move5=(0,0)
                else:
                        move5=monster_movement(monster_position[4],k5)
                k5=move5
                monster_position[4]=add_to_pos(monster_position[4],move5)
                if monster_position[5]==(15,0) or monster_position[5]==(15,20) or monster_position[5]==(0,10) or monster_position[5]==(29,10):
                        move6=(0,0)
                else:
                        move6=monster_movement(monster_position[5],k6)
                k6=move6
                monster_position[5]=add_to_pos(monster_position[5],move6)

                #draw monsters at updated position
                draw_monster(screen, monster_position[0])
                draw_monster(screen, monster_position[1])
                draw_monster(screen, monster_position[2])
                draw_monster(screen, monster_position[3])
                draw_monster(screen, monster_position[5])
                draw_monster(screen, monster_position[4])
                for i in range(6):
                        if pacman_position==monster_position[i]:
                                score=score-int(times)*10
                                running = False
                        if monster_position[i]==(15,0):
                                monster_position[i]=(15,19)
                        elif monster_position[i]==(15,20):
                                monster_position[i]=(15,1)
                        elif monster_position[i]==(0,10):
                                monster_position[i]=(28,10)
                        elif monster_position[i]==(29,10):
                                monster_position[i]=(1,10)
                
                key=pygame.key.get_pressed()        
        #if big coin is eaten by pacman, this deactivates monsters for short period of time                        
        else:
                num=num+1
                if num%2==0 and num<40:
                        #draw monster blinking
                        draw_monster(screen, monster_position[0])
                        draw_monster(screen, monster_position[1])
                        draw_monster(screen, monster_position[2])
                        draw_monster(screen, monster_position[3])
                        draw_monster(screen, monster_position[5])
                        draw_monster(screen, monster_position[4])

                if num>40 and num<50:
                        draw_monster(screen, monster_position[0])
                        draw_monster(screen, monster_position[1])
                        draw_monster(screen, monster_position[2])
                        draw_monster(screen, monster_position[3])
                        draw_monster(screen, monster_position[5])
                        draw_monster(screen, monster_position[4])

        
        
        
        #Take input from the user and update pacman moving direction
        
        key=pygame.key.get_pressed()
        if pygame.key.get_focused()==True:
                s=(0,0)
                #check which key is pressed
                if key[K_LEFT]:
                        if in_wall(add_to_pos(pacman_position,LEFT))==True:
                                s=LEFT
                                image=pygame.image.load('PacmanL.png')
                        
                elif key[K_RIGHT]:
                        if in_wall(add_to_pos(pacman_position,RIGHT))==True:
                                s=RIGHT
                                image=pygame.image.load('PacmanR.png')
                        
                elif key[K_UP]:
                        if in_wall(add_to_pos(pacman_position,TOP))==True:
                                s=TOP
                                image=pygame.image.load('PacmanU.png')
                        
                elif key[K_DOWN]:
                        if in_wall(add_to_pos(pacman_position,DOWN))==True:
                                s=DOWN
                                image=pygame.image.load('PacmanD.png')
                        
                if in_wall(add_to_pos(pacman_position,s))==False:
                        s=(0,0)
                move_direction=s
                image1=image

                pacman_position = add_to_pos(pacman_position, move_direction)
                #teleport pacman at end points to put pacman back at the other end
                if pacman_position==(15,0):
                        pacman_position=(15,19)
                elif pacman_position==(15,20):
                        pacman_position=(15,1)
                elif pacman_position==(29,10):
                        pacman_position=(1,10)
                elif pacman_position==(0,10):
                        pacman_position=(28,10)
                if layout[pacman_position[1]][pacman_position[0]]=='b':
                        num=0
                
                if layout[pacman_position[1]][pacman_position[0]]=='c' or layout[pacman_position[1]][pacman_position[0]]=='m' or layout[pacman_position[1]][pacman_position[0]]=='b':
                        score=score+50                                          #updating score by 50 after every coin eaten
                        layout[pacman_position[1]][pacman_position[0]]='.'
                n=0
                for i in range(rows):
                        for j in range(col):
                                if layout[i][j] == 'c' or layout[i][j]=='m' or layout[i][j]=='b':
                                        n=n+1
                key=pygame.key.get_pressed()    
                
                #if all coins are eaten, move to next level
                if n==0:
                        time.sleep(0.5)
                        flag=1
                        if layout==loadtxt('layout2.txt', dtype=str):
                                flag=0
                        running = False
                        score=score+500
                        score=score-int(times)*10
                        score=str(score)

        #Update the display
        key=pygame.key.get_pressed()
        pygame.display.update()
        if running==False:
                score=str(score)
                pygame.init()
                time.sleep(1.1)
                screen = pygame.display.set_mode((640,640), 0, 32)
                background = pygame.surface.Surface((640,640)).convert()
                font = pygame.font.Font(None, 80)
                text1 = font.render(score, 1, (255,255,255))
                text = font.render("YOUR SCORE", 1, (255,255,255))
                textpos1 = text.get_rect()
                textpos = text.get_rect(centerx=background.get_width()/2)
                background.blit(text, textpos)
                background.blit(text1, [HEIGHT*7,WIDTH*3])
                screen.blit(background, (0,0))
                if flag==1:
                        image4=pygame.image.load('668412CC.jpg')
                else:
                        image4=pygame.image.load('668412BB.jpg')
                screen.blit(image4,(0,320))
                pygame.display.update()
                ti=True
                while ti:
                        for event in pygame.event.get():
                                if event.type==pygame.KEYDOWN:
                                        if event.key==pygame.K_q:
                                                ti=False
                                                exit()
                                        if event.key==pygame.K_RETURN:
                                                if flag==1:
                                                        layout = loadtxt('layout2.txt', dtype=str)      #level 2 layout
                                                else:
                                                        layout = loadtxt('layout.txt', dtype=str)       #level 1 layout
                                                        score=100
                                                rows, cols = layout.shape
                                                pacman_position = (10,10)
                                                monster_position = []
                                                running=True
                                                ti=False
                                                times=0
                                                for col in range(cols):
                                                        for row in range(rows):
                                                                value = layout[row][col]
                                                                pos = (col, row)
                                                                if value == 'm':
                                                                        monster_position.append((col,row))      #monster positions
                                                #initialising game groung
                                                pygame.init()
                                                screen = pygame.display.set_mode((960,672), 0, 32)
                                                pygame.display.set_caption('PACMAN')
                                                background = pygame.surface.Surface((960,672)).convert()
                                
        
        
        if x==0:
                x=x+2
                time.sleep(1.5)         #first time start wait

        key=pygame.key.get_pressed()
        #Wait for a while, computers are very fast.
        time.sleep(0.1)
