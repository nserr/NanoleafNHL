from nanoleaf import setup
from nanoleaf import Aurora
from time import sleep

IPaddress = '192.168.0.25'
token = setup.generate_auth_token(IPaddress)

myAurora = Aurora(IPaddress, token)
index = 0
while index < 4:
	myAurora.rgb = [255,0,0] #Red
	sleep(1) #5 seconds seemed like a good time for the red light to stay
	myAurora.rgb = [255,255,255] #White
	sleep(0.5)
	index = index + 1
myAurora.effect = "Flames"
#oogabooga