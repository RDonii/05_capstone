# Menu API Backend

## About

This is the simple "Menu" API project. Everyone can get information about todays menu of restaurans which sorted by their located city. Only owners of restaurans can add restaurant to the list after login their account. Deleting and updating is require permission which given only to manager.

## API

In order to use the API users don't need to be authentificated, but for adding new restaurant - it is indeed crucial. Users can either have a guest, chief and manager status. An overview of the API can be found below as well as in the provided postman collection.

### Retreiving data

**GET** `/cities`

Retrieves list of all cities and number of them.

```
curl -X GET \
  https://tmenu.herokuapp.com/cities'
```

Sample response:
```
{
    "cities": ["Tashkent", "Kokand", "Bukhara"],
    "count": 3
}
```

**GET** `/restaurants`

Retrieves list of all restaurants and number of them

```
curl -X GET \
  https://tmenu.herokuapp.com/restaurants
```

Sample response:
```
{
    "restaurants": ["La Piola", "Piramida", "Ipak Yuli", "Uch baqaloq"],
    "count": 4
}
```

**GET** `/cities/<int:id>/restaurants`

Retrieves list and number of restaurants of specific city

```
curl -X GET \
  https://tmenu.herokuapp.com/cities/2/restaurants
```

Sample response:
```
{
    "restaurants": ["Piramida", "Uch baqaloq"]
    "count": 2
}
```

### Managing data

**POST** `/restaurants` (Supports both manager and chief role)

Add a new restaurant

```
curl -X POST \
  https://tmenu.herokuapp.com/restaurants \
  -H 'Authorization: Bearer <VALID_TOKEN>' \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "Choyxona",
    "description": "Cooks the best plov",
    "menu": {"meal1": "plov",
              "meal2": "samsa",
              "meal3": "lagman",
              "meal4": "manti",
              "meal5": "vaju"},
    "city": "Kokand"
}'
```
Sample response:
```
{'restaurant': [{
    "name": "Choyxona",
    "description": "Cooks the best plov",
    "menu": [{"meal1": "plov",
              "meal2": "samsa",
              "meal3": "lagman",
              "meal4": "manti",
              "meal5": "vaju"}],
    "city": "Kokand"
}]}
```

**PATCH** `/restaurants/<int:id>` (manager role only)

Update restaurant's data

```
curl -X PATCH \
  https://tmenu.herokuapp.com/restaurants/5 \
  -H 'Authorization: Bearer <VALID_TOKEN>' \
  -H 'Content-Type: application/json' \
  -d '{
    "menu": {"meal1": "mastava",
             "meal2": "borj",
             "meal3": "kabab",
             "meal4": "tabaka",
             "meal5": "dimlama"}
}'
```
Sample response:
```
{'restaurant': [{
    "name": "Choyxona",
    "description": "Cooks the best plov",
    "menu": [{"meal1": "mastava",
             "meal2": "borj",
             "meal3": "kabab",
             "meal4": "tabaka",
             "meal5": "dimlama"}],
    "city": "Kokand"
}]}
```


**DELETE** `/restaurants/<int:id>` (manager role only)

Delete a given restaurant

```
curl -X DELETE \
  https://tmenu.herokuapp.com/restaurants/4 \
  -H 'Authorization: Bearer <VALID_TOKEN> ' \

```
Sample response:
```
{
  'deleted': 4
}
```

## Installation

The following section explains how to set up and run the project locally.

### Installing Dependencies

The project requires Python 3.9.5 Using a virtual environment such as `pipenv` is recommended. Set up the project as follows:

```

pipenv shell
pipenv install

```
### Database Setup


With Postgres running, create a database and import data using the blog_api.psql file provided. In terminal run:
```

sudo -u postgres createdb meal
psql meal < tmenu.psql
```

### Running the server

To run the server, first set the environment variables, then execute:

```bash
python manage.py runserver
```

## Testing

To test the API, first create a test database in postgres and then execute the tests as follows:

```
sudo -u postgres createdb meal_test
psql meal_test < tmenu.psql
python test_app.py
```
