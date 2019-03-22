#!/usr/bin/env python3

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


# Constructor for game data.
class Game:
	def __init__(self, game_info):
		self.link  = game_info['link']
		self.date  = game_info['gameDate']
		self.away  = game_info['teams']['away']['team']['name']
		self.home  = game_info['teams']['home']['team']['name']


def main():
	##########################
	team = "Calgary Flames"
	teamEffect = "Flames"
	brightness = 65
	##########################
	game = get_games(team)
	live = get_live(game.link)
	myAurora.on = True
	myAurora.effect = teamEffect
	myAurora.brightness = brightness
	allPlays = 0

	while True:
		try:
			data = get_data(live)
			plays = data['liveData']['plays']['allPlays']

			if len(plays) > allPlays:
				allPlays = len(plays)
				print(plays[len(plays) - 1])
				print(datetime.datetime.now().time())
				currentPlay = plays[len(plays) - 1]

				if currentPlay['result']['event'] == "Goal" and currentPlay['team']['name'] == team:
					goal()
					reset(teamEffect, brightness)

			sleep(3)

		except KeyboardInterrupt:
			myAurora.off = True
			os._exit(0)


# Returns game data.
def get_games(team): 
	data = get_data("https://statsapi.web.nhl.com/api/v1/schedule")

	for game_info in data['dates'][0]['games']:
		game = Game(game_info)

		if team in game.away or team in game.home:
			return game


# Gets JSON response.
def get_data(url):
	response = (requests.get(url)).json()
	return response


# Creates link for current game's live feed.
def get_live(url):
	default = "https://statsapi.web.nhl.com"
	liveURL = default + url
	return liveURL
	

# Runs the goal light.
def goal():
	for x in range(0,4):
		myAurora.rgb = [255,0,0] 		# Red
		sleep(1) 						# Red delay
		myAurora.rgb = [255,255,255] 	# White
		sleep(1) 						# White delay


# Resets to previous colors and brightness.
def reset(teamEffect, brightness):
	myAurora.effect = teamEffect
	myAurora.brightness = brightness


if __name__ == "__main__":
	##########################
	ipAddress = '192.168.0.10'
	##########################
	token = setup.generate_auth_token(ipAddress)
	myAurora = Aurora(ipAddress, token)
	main()