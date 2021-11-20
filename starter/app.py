import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy.sql.base import NO_ARG
from sqlalchemy.sql.functions import count
from .database.models import create_db, City, Rest

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  create_db(app)
  CORS(app)

  @app.route('/')
  def home_page():
    return 'not implemented'

  @app.route('/cities', methods = 'GET')
  def get_all_city():
    all_city_query = City.query.all()
    city_formated = [city.format for city in all_city_query]
    count = len(city_formated)

    return jsonify({
      'cities': city_formated,
      'count': count
    })

  @app.route('/restaurants')
  def get_all_restaurants():
    all_restaurants_query = Rest.query.all()
    restaurant_formated = [rest.format for rest in all_restaurants_query]
    count = len(restaurant_formated)

    return jsonify({
      'restaurants': restaurant_formated,
      'count': count
    })

  @app.route('/restaurants/<int:id>', methods = 'DELETE')
  def delete_restaurant(id):
    restaurant = Rest.query.filter(Rest.id==id).one_or_none()
    if restaurant in None:
      abort(404)
    
    restaurant.delete()
  
  @app.route('/restaurants/', methods = 'POST')
  def post_new_restaurant():
    data = request.get_json()

    n_name = data.get('name', None)
    n_description = data.get('description', None)
    n_city = data.get('city', None)
    
    new_city = City.query.filter((City.name).lower==n_city.lower).one_or_none()
    if new_city==None:
      new_city = City(name=n_city)
      new_city.insert()

    new_restaurant = Rest(name=n_name, description=n_description, city_id=new_city.id)
    new_restaurant.insert()

    new_restaurant_formated = new_restaurant.format()

    return jsonify({
      'restaurant': new_restaurant_formated
    })
  
  @app.route('/restaurants/<int:id>', methods = "PATCH")
  def update_restaurant(id):
    rest = Rest.query.filter(Rest.id==id).one_or_none()
    if rest==None:
      abort(404)
    
    data = request.get_json()
    n_name = data.get('name', None)
    n_description = data.get('description', None)
    n_city = data.get('city', None)

    if n_name!=None:
      rest.name = n_name
    if n_description!=None:
      rest.description = n_description
    if n_city!= None:
      new_city = City.query.filter((City.name).lower==n_city.lower).one_or_none()
      if new_city==None:
        new_city = City(name=n_city)
        new_city.insert()
      
      rest.city_id = new_city.id
    
    rest.update()

    restaurant_formated = rest.format()

    return jsonify({
      'restaurant': restaurant_formated
    })

  @app.route('/cities/<int:id>/restaurants')
  def restaurants_by_city(id):
    restaurants_query = Rest.query.filter(Rest.id==id)
    restaurants_formated = [rest.format for rest in restaurants_query]
    count = len(restaurants_formated)

    return jsonify({
      'restaurants': restaurants_formated,
      'count': count
    })

  return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)