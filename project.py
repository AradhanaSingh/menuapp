'''
this file starts webserver
'''
# importing Flask class
from flask import Flask , render_template, request, redirect, url_for, flash, jsonify

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
    # looks for html page in template directory
    return render_template('menu.html', restaurant = restaurant, items = items)

# by default app.route takes get method
# using methods we can add it for GET and POST request
@app.route('/restaurants/<int:restaurant_id>/new/', methods = ['GET','POST'])
def newMenuItem(restaurant_id):
        if request.method == 'POST':
            newItem = request.form['name']
            description = request.form['description']
            price = request.form['price']
            course = request.form['course']
            newItemObj = MenuItem(name = newItem, restaurant_id = restaurant_id, description = description, price = price , course = course)
            session.add(newItemObj)
            session.commit()
            flash("new menu item created")
            # after adding menu item redirect to url home page
            return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id ))
        return render_template('newmenuitem.html', restaurant_id = restaurant_id)

@app.route('/restaurants/<int:restaurant_id>/edit/<int:menu_id>', methods= ['GET','POST'])
def editMenuItem(restaurant_id, menu_id):
    editedItem = session.query(MenuItem).filter_by(id = menu_id).one()
    if request.method == 'POST':
        editedItem.name = request.form['name']
        session.add(editedItem)
        session.commit()
        flash("Menu Item has been edited")
        return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
    else:
        return render_template('editmenuitem.html', restaurant_id = restaurant_id, editedItem = editedItem)


@app.route('/restaurants/<int:restaurant_id>/delete/<int:menu_id>', methods=['GET','POST'])
def deleteMenuItem(restaurant_id, menu_id):
    deletedItem = session.query(MenuItem).filter_by(id = menu_id).one()
    if request.method=="POST":
        session.delete(deletedItem)
        session.commit()
        flash('Menu item has been deleted')
        return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
    return render_template('deletemenuitem.html', deletedItem = deletedItem )


# Making an api endpoint for get request
@app.route('/restaurantsjson/<int:restaurant_id>')
def getRestaurantsjson(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    # serializing so that flask can read it
    return jsonify(Restaurant = restaurant.serialize)

# python interpretor gets the __name__ set to  __main__
# if statement makes sures that webserver is run only when script is executed directly from the python interpretor
if __name__ == '__main__':
    # session is way a server can store information across multiple web pages to create more personalized user experience
    app.secret_key = 'super_secret_key'
    # latest code would be deployed on webser without restarting it manually
    app.debug = True
    # runs the local server
    # '0.0.0.0' tells the server to lok on all public ip address
    app.run(host = '0.0.0.0', port = 5000)
