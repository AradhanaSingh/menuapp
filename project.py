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
# decorator wraps the function that flask has already created
# so if either of these routes gets sent from the browser, then the method provided get called
# when a webserver gets a request that matches the path, following method would be executed
# both the below urls take to the same page, "/" calls "/hello"
@app.route('/')
@app.route('/hello')
def HelloWorld():
    restaurant = session.query(Restaurant).first()
    items = session.query(MenuItem).filter_by( restaurant_id = restaurant.id)
    output = ''
    for i in items:
        output += i.name
        output += '<br>'
    return output

# python interpretor gets the __name__ set to  __main__
# if statement makes sures that webserver is run only when script is executed directly from the python interpretor
if __name__ == '__main__':
    # latest code would be deployed on webser without restarting it manually
    app.debug = True
    # runs the local server
    # '0.0.0.0' tells the server to lok on all public ip address
    app.run(host = '0.0.0.0', port = 5000)
