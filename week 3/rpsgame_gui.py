#Reference https://realpython.com/python-rock-paper-scissors/_https://github.com/siwei-yuan/180DA-WarmUp/blob/main/Week3/rps_gui.py
import paho.mqtt.client as mqtt
from paho.mqtt.subscribeoptions import SubscribeOptions
import pygame
import time
from pygame.locals import (
    K_r,
    K_p,
    K_s,
    KEYDOWN,
)
pygame.init()
font = pygame.font.Font('freesansbold.ttf', 32)


global OPPONENT_SELECTION
global player_id
OPPONENT_SELECTION = None
player_id = input("Please input your player_id (1/2): ")

def on_connect(client, userdata, flags, rc):
  print("Connection returned result: " + str(rc))
  options = SubscribeOptions(noLocal=True)
  global player_id
  if player_id == "1":
    topic = "ece180d/rps/2"
  elif player_id == "2":
    topic = "ece180d/rps/1"
  client.subscribe(topic, options=options)

def on_disconnect(client, userdata, rc):
  if rc != 0:
    print('Unexpected Disconnect')
  else:
    print('Expected Disconnect')

def on_message(client, userdata, message):
  global OPPONENT_SELECTION
  OPPONENT_SELECTION = str(message.payload)[2:-1]

client = mqtt.Client()
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message
client.connect('mqtt.eclipseprojects.io')
client.loop_start()

USER_SELECTION = None
RESULT = None
SELECTED = False

screen = pygame.display.set_mode([600, 500])
while True:

    screen.fill((0,0,128))
    img = pygame.image.load("gui.jpg")
    img = pygame.transform.scale(img, (600, 200))
    rect = img.get_rect()
    screen.blit(img, rect)

    text = font.render('ROCK', True, (0, 0, 255))
    textRect = text.get_rect()
    textRect.center = (100, 250)
    screen.blit(text, textRect)

    text = font.render('PAPER', True, (255, 0, 255))
    textRect = text.get_rect()
    textRect.center = (300, 250)
    screen.blit(text, textRect)

    text = font.render('SCISSORS', True, (0, 0, 255))
    textRect = text.get_rect()
    textRect.center = (500, 250)
    screen.blit(text, textRect)

    if not SELECTED:
        text = font.render('Press r/p/s to select', True, (255, 255, 255))
        textRect = text.get_rect()
        textRect.center = (300, 350)
        screen.blit(text, textRect)
    else :
        text = font.render('You selected: ' + USER_SELECTION , True,(255, 255, 255))
        textRect = text.get_rect()
        textRect.center = (300, 350)
        screen.blit(text, textRect)
    
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_r and not SELECTED:
                print("You selected rock")
                USER_SELECTION = "ROCK"
            if event.key == K_p and not SELECTED:
                print("You selected paper")
                USER_SELECTION = "PAPER"
            if event.key == K_s and not SELECTED:
                print("You selected paper")
                USER_SELECTION = "SCISSORS"

    if USER_SELECTION == "ROCK":
        pygame.draw.circle(screen, (255, 255, 255), (100, 300), 10)
    elif USER_SELECTION == "PAPER":
        pygame.draw.circle(screen, (255, 255, 255), (300, 300), 10)
    elif USER_SELECTION == "SCISSORS":
        pygame.draw.circle(screen, (255, 255, 255), (500, 300), 10)

    if USER_SELECTION and not SELECTED:
        client.publish("ece180d/rps/" + str(player_id), USER_SELECTION)
        SELECTED = True
        

    
    if OPPONENT_SELECTION and SELECTED:
        text = font.render('Opponent selected: ' + OPPONENT_SELECTION, True,(255, 255, 255))
        textRect = text.get_rect()
        textRect.center = (300, 380)
        screen.blit(text, textRect)

    if USER_SELECTION == OPPONENT_SELECTION and USER_SELECTION != None and OPPONENT_SELECTION != None:
        RESULT = "TIE"
    elif USER_SELECTION == "ROCK":
        if OPPONENT_SELECTION == "PAPER":
            RESULT = "LOSE"
        elif OPPONENT_SELECTION == "SCISSORS":
            RESULT = "WIN"
    elif USER_SELECTION == "PAPER":
        if OPPONENT_SELECTION == "SCISSORS":
            RESULT = "LOSE"
        elif OPPONENT_SELECTION == "ROCK":
            RESULT = "WIN"
    elif USER_SELECTION == "SCISSORS":
        if OPPONENT_SELECTION == "ROCK":
            RESULT = "LOSE"
        elif OPPONENT_SELECTION == "PAPER":
            RESULT = "WIN"

    if RESULT == "WIN":
        text = font.render('You win', True, (255, 0, 0))
    if RESULT == "LOSE":
        text = font.render('You lose', True, (255, 0, 0))
    if RESULT == "TIE":
        text = font.render('Tie', True, (255, 0, 0))


    pygame.display.update()