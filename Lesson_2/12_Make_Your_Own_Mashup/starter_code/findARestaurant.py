from geocode import getGeocodeLocation
import json
import httplib2

# Ensure that non-ASCII characters also render properly in the code e.g. Chinese or Japanese, etc.
import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)

foursquare_client_id = "WQSO3VJHXZDVXJFB44Y1TDB0HJ4TL3QSIPSFGEYPZLSDHUHJ"
foursquare_client_secret = "QEVTEUWHWDHJWASH0UFL1T1W1RMIS1AJZJR5LKNZXFF2KHOM"


def findARestaurant(mealType, location):
	#1. Use getGeocodeLocation to get the latitude and longitude coordinates of the location string.
	google_latitude, google_longitude = getGeocodeLocation(location)
	foursquare_coordinate = (round(google_latitude, 2), round(google_longitude, 2))
	# For debugging, print coordinate to terminal
	# print foursquare_coordinate[0], foursquare_coordinate[1]

	#2.  Use foursquare API to find a nearby restaurant with the latitude, longitude, and mealType strings.
	#HINT: format for url will be something like https://api.foursquare.com/v2/venues/search?client_id=CLIENT_ID&client_secret=CLIENT_SECRET&v=20130815&ll=40.7,-74&query=sushi
	url = ('https://api.foursquare.com/v2/venues/search?client_id=%s&client_secret=%s&v=20180903&intent=browse&ll=%s,%s&radius=5000&query=%s' % (foursquare_client_id, foursquare_client_secret, foursquare_coordinate[0], foursquare_coordinate[1], mealType))
	h = httplib2.Http()
	# can print [0], but must jsonify [1], otherwise error!
	result = json.loads(h.request(url, 'GET')[1])
	# print result

	# To make sure at least one restaurant is found
	if result['response']['venues']:
		#3. Grab the first restaurant
		first_restaurant = result['response']['venues'][0]
		venue_id = first_restaurant['id']
		restaurant_name = first_restaurant['name']
		restaurant_address = first_restaurant['location']['formattedAddress']
		# Convert the current restaurant_address (a list) to a string
		updated_address = ""
		for partial_address in restaurant_address:
			updated_address += partial_address + ", "
		# Remove the last comma and space (", ") in the updated_address
		updated_address = updated_address[:-2]
		restaurant_address = updated_address

		#4. Get a  300x300 picture of the restaurant using the venue_id (you can change this by altering the 300x300 value in the URL or replacing it with 'orginal' to get the original picture
		photo_url = ('https://api.foursquare.com/v2/venues/%s/photos?client_id=%s&client_secret=%s&v=20180903' % (venue_id, foursquare_client_id, foursquare_client_secret))
		photo_result = json.loads(h.request(photo_url, 'GET')[1])

		#5. Grab the first image
		if photo_result['response']['photos']['items']:
			restaurant_first_picture = photo_result['response']['photos']['items'][0]
			prefix = restaurant_first_picture['prefix']
			suffix = restaurant_first_picture['suffix']
			restaurant_picture_url = prefix + "300x300" + suffix

		#6. If no image is available, insert default a image url
		else:
			restaurant_picture_url = 'https://upload.wikimedia.org/wikipedia/commons/6/6d/Good_Food_Display_-_NCI_Visuals_Online.jpg'

		#7. Return a dictionary containing the restaurant name, address, and image url
		restaurant_info = {'name': restaurant_name, 'address': restaurant_address, 'image': restaurant_picture_url}
		print "Restaurant Name: %s" % restaurant_info['name']
		print "Restaurant Address: %s" % restaurant_info['address']
		print "Restaurant Image: %s \n" % restaurant_info['image']
		return restaurant_info

	else:
		print "Sorry! No Restaurants found near %s" % location
		return "No Restaurants Found!"


if __name__ == '__main__':
	findARestaurant("Pizza", "Tokyo, Japan")
	findARestaurant("Tacos", "Jakarta, Indonesia")
	findARestaurant("Tapas", "Maputo, Mozambique")
	findARestaurant("Falafel", "Cairo, Egypt")
	findARestaurant("Spaghetti", "New Delhi, India")
	findARestaurant("Cappuccino", "Geneva, Switzerland")
	findARestaurant("Sushi", "Los Angeles, California")
	findARestaurant("Steak", "La Paz, Bolivia")
	findARestaurant("Gyros", "Sydney Australia")
