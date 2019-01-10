#!/usr/bin/env python3

# Author: u/sriuba, Noah Serr

import json
from time import sleep
import sys
import requests
import datetime
import os
import itertools
from nanoleaf import setup
from nanoleaf import Aurora
import argparse


# Returns data from nanoleaf.
def info():
	ipAddress = '192.168.0.25'
	token = setup.generate_auth_token(ipAddress)
	return ipAddress, token


# Constructor for game data.
class Game:
	def __init__(self, game_info):
		self.link  = game_info['link']
		self.date  = game_info['gameDate']
		self.away  = game_info['teams']['away']['team']['name']
		self.home  = game_info['teams']['home']['team']['name']


# Gets JSON response.
def get_data(url):
	response = requests.get(url)
	response = response.json()
	return response


# Returns game data.
def get_games(team):
	url = "https://statsapi.web.nhl.com/api/v1/schedule" 
	data = get_data(url)

	for game_info in data['dates'][0]['games']:
		game = Game(game_info)

		if team in game.away or team in game.home:
			return game

	
def main():
	team = "Calgary Flames"
	teamEffect = "Flames"
	game = get_games(team)
	live = get_live(game.link)
	myAurora.on = True
	myAurora.effect = teamEffect
	brightness = 65
	myAurora.brightness = brightness
	allPlays = 0

	while True:
		try:
			data = get_data(live)
			plays = data['liveData']['plays']['allPlays']

			if len(plays) > allPlays:
				allPlays = len(plays)
				print(plays[len(plays)-1])
				print(datetime.datetime.now().time())
				currentPlay = plays[len(plays) - 1]

				if currentPlay['result']['event'] == "Goal" and currentPlay['team']['name'] == team:
					sleep(1)
					goal()
					reset(teamEffect, brightness)

			sleep(5)

		except KeyboardInterrupt:
			myAurora.off = True
			os._exit(0)
	

# Runs the goal light
def goal():
	index = 0
	while index < 5:
		myAurora.rgb = [255,0,0] # Red
		sleep(2) # Red delay (sec)
		myAurora.rgb = [255,255,255] # White
		sleep(0.5) # White delay (sec)
		index = index + 1


# Resets to previous colors and brightness.
def reset(teamEffect, brightness):
	myAurora.effect = teamEffect
	myAurora.brightness = brightness


# Creates link for current game's live feed
def get_live(url):
	default = "https://statsapi.web.nhl.com"
	liveURL = default + url
	return liveURL


if __name__ == "__main__":
	ipAddress, token = info()
	myAurora = Aurora(ipAddress, token)
	main()
