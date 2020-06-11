#!/usr/bin/env python

import os
import NaiveBayes as nb
import json
import requests
import random
import re
from flask import Flask, make_response, request, jsonify

cuisine = ["albanian", "argentine", "andhra", "anglo-indian", "arab", "armenian", "assyrian", "awadhi", "azerbaijani", 
			"balochi", "belarusian", "bangladeshi", "bengali", "berber", "brazilian", "cajun", "cantonese", "carribean",
			"chechen", "chinese", "circassian", "crimean tatar", "cypriot", "danish", "english", "estonian", "french",
			"filipino", "georgian", "german", "goan", "greek", "gujarati", "hyderabad", "indian", "indonesian", "inuit",
			"irish", "italian", "jamaican", "japanese", "jewish", "karnataka", "kazakh", "korean", "keralite", "kurdish",
			"laotian", "lebanese", "latvian", "lithuanian", "mangalorean", "malay", "malaysian", "mediterranean", "mexican",
			"mordoian", "mughal", "nepalese", "odia", "parsi", "pashtun", "polish", "pakistani", "persian", "peruvian",
			"portuguese", "punjabi", "romanian", "russian", "sami", "serbian", "slovak", "slovenian", "somali", "spanish",
			"sri lankan", "taiwanese", "tatar", "thai", "turkish", "tamil", "udupi", "ukrainian", "vietnamese", "yamal", 
			"zambian", "zanziban"]

randomRecipe = ["i want something random", "i want a random recipe", "give me something random", "give me a random recipe", "surprise me", "i'm feeling frisky", "i'm feeling lucky"]
# initialize the flask app
classifier = nb.NaiveBayes()
app = Flask(__name__)

# default route
@app.route('/')
def index():
	return 'Hello World!'


def find_cuisine(cuisine):
	url = "https://api.spoonacular.com/recipes/search?apiKey=5817a68eb4fe467ca250842a0dbe0c9d"

	parameters = {
		'number': 10,
		'query': ' ',
		'cuisine': cuisine
	}

	headers = {
		"Accept": "application/json"
	}

	return requests.get(url, params=parameters, headers=headers).json()

def random_recipe():
	url = "https://api.spoonacular.com/recipes/random?apiKey=5817a68eb4fe467ca250842a0dbe0c9d"

	parameters = {
		'limitLicense': False,
		'number': 1
	}

	headers = {
		"Accept": "application/json"
	}

	return requests.get(url, params=parameters, headers=headers).json()


# function for responses
def results():
	req = request.get_json(force=True)# fetch action from json

	#action = req.get('queryResult').get('action')# return a fulfillment response

	userInput = req['queryResult']['queryText'] #User input in text form. Use for parsing.
	data = ""
	isCuisine = False

	if userInput in randomRecipe:
		#offer random recipe here
		temp_data = random_recipe()
		data = temp_data['recipes'][0]['title'] + ": " + temp_data['recipes'][0]['sourceUrl']
	else:
		inputArray = userInput.split()
		cuisineInput = ""
		for x in inputArray:
			if x in cuisine:
				cuisineInput = x
				isCuisine = True
				break

		if isCuisine:
			#return recipes by cuisine here
			temp_data = find_cuisine(cuisineInput)
			rand = random.randint(0,9)
			returnString = "1. " + temp_data['results'][rand]['title'] + ": " + temp_data['results'][rand]['sourceUrl']
			data = returnString

		else:
			#return recipes by ingredients here
			ingredients = [userInput]
			print("Input:", ingredients)
			output = classifier.nb_classify(ingredients)
			print("Output:", output)
			out_formatted = "The recipe is most likely "
			for i in range(len(output)):
				out_formatted += output[i][0] + " with a score of " + str(output[i][1])
				if i is not (len(output) - 1):
					out_formatted += ", followed by "
				else:
					out_formatted += "."
			print(out_formatted)
			data = out_formatted


	return {'fulfillmentText': data}# response route for webhook. Response must be in a proper JSON format. 

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
	return make_response(jsonify(results()))

# run the app
if __name__ == '__main__':
	classifier.load_pickle()
	app.run()

