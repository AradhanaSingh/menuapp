'''
this file starts webserver
'''
# importing Flask class
from flask import Flask

# anytime python applicatin is run, special variable __name__ gets declared
# createa an object using the
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///menuapp.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()


# following are decorator in python, starts with @
# decorators are used to find function with url
# decorator wraps the function that flask has already created
# so if either of these routes gets sent from the browser, then the method provided get called
# when a webserver gets a request that matches the path, following method would be executed
# both the below urls take to the same page, "/" calls "/hello"
@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by( id = restaurant_id).one()
    items = session.query(MenuItem).filter_by( restaurant_id = restaurant.id)
    output = ''
    for i in items:
        output += i.name
        output += '<br>'
        output += i.price
        output += '<br>'
        output += i.description
        output += '<br><br>'
    return output


@app.route('/restaurants/<int:restaurant_id>/newmenuitem')
def newMenuItem(restaurant_id):
        return "page to create a new menu item."

@app.route('/restaurants/<int:restaurant_id>/editmenuitem/<int:menu_id>')
def editMenuItem(restaurant_id, menu_id):
    return "page to edit menu item"

@app.route('/restaurants/<int:restaurant_id>/deletemenuitem/<int:menu_id>')
def deleteMenuItem(restaurant_id, menu_id):
    return "page to delete a menu item"

# python interpretor gets the __name__ set to  __main__
# if statement makes sures that webserver is run only when script is executed directly from the python interpretor
if __name__ == '__main__':
    # latest code would be deployed on webser without restarting it manually
    app.debug = True
    # runs the local server
    # '0.0.0.0' tells the server to lok on all public ip address
    app.run(host = '0.0.0.0', port = 5000)
