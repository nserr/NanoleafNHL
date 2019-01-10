from nanoleaf import setup
from nanoleaf import Aurora
from time import sleep

IPaddress = '192.168.0.25'
token = setup.generate_auth_token(IPaddress)

myAurora = Aurora(IPaddress, token)
index = 0
while index < 4:
	myAurora.rgb = [255,0,0] # Red
	sleep(2) # Red delay
	myAurora.rgb = [255,255,255] # White
	sleep(0.5) # White delay
	index = index + 1
myAurora.effect = "Flames"