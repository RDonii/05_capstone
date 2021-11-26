import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy.sql.base import NO_ARG
from sqlalchemy.sql.functions import count
from database.models import create_db, City, Rest
from sqlalchemy import func, or_
from auth.auth import AuthError, requires_auth
import json


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  create_db(app)
  CORS(app)

  @app.route('/')
  def home_page():
    return 'not implemented'

  @app.route('/cities', methods = ['GET'])
  def get_all_city():
    all_city_query = City.query.all()
    city_formated = [city.format() for city in all_city_query]
    count = len(city_formated)

    return jsonify({
      'cities': city_formated,
      'count': count
    })

  @app.route('/restaurants', methods = ["GET"])
  def get_all_restaurants():
    all_restaurants_query = Rest.query.all()
    restaurant_formated = [rest.format() for rest in all_restaurants_query]
    count = len(restaurant_formated)

    return jsonify({
      'restaurants': restaurant_formated,
      'count': count
    })

  @app.route('/restaurants/<int:id>', methods = ['DELETE'])
  @requires_auth('delete:restaurants')
  def delete_restaurant(payload, id):
    restaurant = Rest.query.filter(Rest.id==id).one_or_none()
    if restaurant==None:
      abort(404)
    try:
      
      restaurant.delete()

      return jsonify({
        'deleted': restaurant.id
      })

    except:
      abort(422)
  
  @app.route('/restaurants', methods = ['POST'])
  @requires_auth('post:restaurants')
  def post_new_restaurant(payload):
    data = request.get_json()

    n_name = data.get('name', None)
    n_description = data.get('description', None)
    n_menu = data.get('menu', None)
    n_city = data.get('city', None)

    try:
      new_city = City.query.filter(func.lower(City.name)==func.lower(n_city)).one_or_none()
      if new_city==None:
        new_city = City(name=n_city)
        new_city.insert()

      n_menu = "["+json.dumps(n_menu)+"]"
      new_restaurant = Rest(name=n_name, description=n_description, menu=n_menu, city_id=new_city.id)
      new_restaurant.insert()

      new_restaurant_formated = [new_restaurant.format()]

      return jsonify({
        'restaurant': new_restaurant_formated
      })
    
    except:
      abort(422)
  
  @app.route('/restaurants/<int:id>', methods = ["PATCH"])
  @requires_auth('patch:restaurants')
  def update_restaurant(payload, id):
    rest = Rest.query.filter(Rest.id==id).one_or_none()
    if rest==None:
      abort(404)
    try:      
      data = request.get_json()
      n_name = data.get('name', None)
      n_description = data.get('description', None)
      n_menu = data.get('menu', None)
      n_city = data.get('city', None)

      if n_name!=None:
        rest.name = n_name
      if n_description!=None:
        rest.description = n_description
      if n_menu!=None:
        n_menu = "["+json.dumps(n_menu)+"]"
        rest.menu = n_menu
      if n_city!= None:
        new_city = City.query.filter(func.lower(City.name)==func.lower(n_city)).one_or_none()
        if new_city==None:
          new_city = City(name=n_city)
          new_city.insert()
        
        rest.city_id = new_city.id
      
      rest.update()

      restaurant_formated = [rest.format()]

      return jsonify({
        'restaurant': restaurant_formated
      })
    
    except:
      abort(422)

  @app.route('/cities/<int:id>/restaurants', methods = ["GET"])
  def restaurants_by_city(id):
    restaurants_query = Rest.query.filter(Rest.id==id)
    restaurants_formated = [rest.format() for rest in restaurants_query]
    count = len(restaurants_formated)
    if count==0:
      abort(404)

    return jsonify({
      'restaurants': restaurants_formated,
      'count': count
    })

  @app.errorhandler(404)
  def not_found(error):
    return (jsonify({
      'error': 404,
      'message': 'not found'
    }), 404)
  
  @app.errorhandler(422)
  def unprocessable(error):
    return (jsonify({
      'error': 422,
      'message': 'unprocessable'
    }), 422)
  
  @app.errorhandler(AuthError)
  def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response

  return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)