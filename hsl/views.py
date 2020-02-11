from django.shortcuts import render, redirect
import requests
import json
from datetime import datetime

def Info(request):
	url = "https://api.digitransit.fi/routing/v1/routers/hsl/index/graphql"
	headers = {'content-type': 'application/json'}
	query = """{
	  plan(
		from: {lat: 60.184112, lon: 24.829139}
		to: {lat: 60.169402, lon: 24.926114}
		numItineraries: 20
	  ) {
		itineraries {
		  legs {
			startTime
			endTime
			mode
			duration
			distance
			from {
				name
			},
			to {
			  name
			},
			}
		}
	  }
	}"""
	r = requests.post(url, headers = headers, json={'query': query})
	json_data = json.loads(r.text)
	itineraries = json_data['data']['plan']['itineraries']
	count = 1
	for itinerary in itineraries[-5:]:
		print(count)
		itinerary['count'] = count
		count += 1
		routes = dict()
		for route in itinerary['legs']:
			ts = int(str(route['endTime'])[:-3])
			route['endTime'] = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
			ts = int(str(route['startTime'])[:-3])
			route['startTime'] = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
			route['duration'] = str(int(route['duration']//60)) + ':' + str(int(route['duration']%60))
			route['distance'] = str(int(route['distance']))
		print("option:", itinerary)
	return render(request, 'home.html',{'itineraries':itineraries[-5:]})