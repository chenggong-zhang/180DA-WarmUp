#Reference https://realpython.com/python-rock-paper-scissors/
#
import paho.mqtt.client as mqtt

ReceiveDataA = False
ReceiveDataB = False
Ainput = None
Binput = None
def on_connect(client, userdata, flags, rc):
  print("Connection returned result: " + str(rc))
  client.subscribe("rpsgame/player1", qos=1)
  client.subscribe("rpsgame/player2", qos=2)


def on_disconnect(client, userdata, rc):
  if rc != 0:
    print('Unexpected Disconnect')
  else:
    print('Expected Disconnect')
def on_message(client, userdata, message):

    global ReceiveDataA
    global ReceiveDataB
    global Ainput
    global Binput

    if message.topic == 'rpsgame/player1': 
        Ainput =  message.payload
        ReceiveDataA = True
    elif message.topic == 'rpsgame/player2': 
        Binput = message.payload
        ReceiveDataB = True
    # if str(message.payload) in ['rock', 'paper', 'scissors']: 
    print('Received another player choice: ' + 'on topic "' + message.topic + '" with QoS ' + str(message.qos))



client = mqtt.Client()
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message
client.connect_async('mqtt.eclipseprojects.io')
client.loop_start()


# ask player id.

player_id = input('Enter player number [A/B]: ')


###the Subscriber
while True:
    
    print("Enter your choice")
    if player_id == 'A':
        client.publish("rpsgame/player1", input(), qos=1)
    if player_id == 'B':  
        client.publish("rpsgame/player2", input(), qos=1)
    
    while(ReceiveDataA != True or ReceiveDataB != True):
        pass


    if (Ainput is not None and Binput is not None):
        user_action = Ainput.decode() #input("Enter a choice (rock, paper, scissors): ")
        # client.publish("rpsgame", input(), qos=1)
        computer_action = Binput.decode()
        print(f"\n playerA chose {user_action}, playerB chose {computer_action}.\n")

        if user_action == computer_action:
            print(f"Both players selected {user_action}. It's a tie!")
        elif user_action == "rock":
            if computer_action == "scissors":
                print("Rock smashes scissors!")
            else:
                print("Paper covers rock!")
        elif user_action == "paper":
            if computer_action == "rock":
                print("Paper covers rock!")
            else:
                print("Scissors cuts paper!")
        elif user_action == "scissors":
            if computer_action == "paper":
                print("Scissors cuts paper!")
            else:
                print("Rock smashes scissors!")
        Ainput = None
        Binput = None
        ReceiveDataA = False
        ReceiveDataB = False


 