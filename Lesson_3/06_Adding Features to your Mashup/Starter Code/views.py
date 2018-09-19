from findARestaurant import findARestaurant
from models import Base, Restaurant
from flask import Flask, jsonify, request
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)


#foursquare_client_id = ''

#foursquare_client_secret = ''

#google_api_key = ''

engine = create_engine('sqlite:///restaruants.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)

@app.route('/restaurants', methods = ['GET', 'POST'])
def all_restaurants_handler():
  #YOUR CODE HERE
  if request.method == 'GET':
    # Return all restaurants in database
    restaurants = session.query(Restaurant).all()
    return jsonify(restaurants = [restaurant.serialize for restaurant in restaurants])
  
  elif request.method == 'POST':
    # Make a new restaurant and store it in database
    location = request.args.get('location') # or ('location', '')
    mealType = request.args.get('mealType')
    restaurantInfo = findARestaurant(mealType, location)
    if restaurantInfo != "No Restaurants Found":
      restaurant = Restaurant(restaurant_name = unicode(restaurantInfo['name']), restaurant_address = unicode(restaurantInfo['address']), restaurant_image = unicode(restaurantInfo['image']))
      session.add(restaurant)
      session.commit()
      return jsonify(restaurant = restaurant.serialize)
    else:
      return jsonify({'Error':'No Restaurant Found for %s around %s'} % (mealType, location))


@app.route('/restaurants/<int:id>', methods = ['GET','PUT', 'DELETE'])
def restaurant_handler(id):
  #YOUR CODE HERE
  restaurant = session.query(Restaurant).filter_by(id = id).one()

  if request.method == 'GET':
    # Return a specific restaurant
    return jsonify(restaurant = restaurant.serialize)

  elif request.method == 'PUT':
    # Update a specific restaurant
    updated_name = request.args.get('name', '')
    updated_address = request.args.get('address', '')
    updated_image = request.args.get('image', '')
    if updated_name:
      restaurant.restaurant_name = updated_name
    if updated_address:
      restaurant.restaurant_address = updated_address
    if updated_image:
      restaurant.restaurant_image = updated_image
    session.commit()
    return jsonify(restaurant = restaurant.serialize)

  elif request.method == 'DELETE':
    # Delete a specific restaurant
    session.delete(restaurant)
    session.commit()
    return jsonify({'Success':'Restaurant Deleted'})


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
