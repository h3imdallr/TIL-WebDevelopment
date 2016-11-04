from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask import flash #give feedback to user, prompt message after action taken


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind= engine)
session = DBSession()


@app.route('/')
@app.route('/restaurant/<int:restaurant_id>/') # 인자값을 pass할 수 있음
def restaurantMenu(restaurant_id):# 인자값을 받아올 수 있
    # restaurant = session.query(Restaurant).first()
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id) # menu of first restaurant
    return render_template('menu.html', restaurant=restaurant, items = items) # HTML ESCAPING

"""JSONIFY"""
@app.route('/restaurant/<int:restaurant_id>/menu/JSON/')
def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
    return jsonify(MenuItems = [i.serialize for i in items] ) #refer to property in databse_setup.py

# ADD JSON API ENDPOINT HERE
"""JSONIFY"""
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON/')
def menuItemJSON(restaurant_id, menu_id):
    menuItem = session.query(MenuItem).filter_by(id=menu_id).one()
    return jsonify(MenuItem = menuItem.serialize)

@app.route('/restaurant/<int:restaurant_id>/new/', methods=['GET','POST'])
def newMenuItem(restaurant_id):
    if request.method =='POST':
        newItem = MenuItem(name = request.form['name'], restaurant_id = restaurant_id )
        session.add(newItem)
        session.commit()
        #flash message
        flash("new menu item created!")

        return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant_id = restaurant_id)

@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit/', methods = ['GET','POST'])
def editMenuItem(restaurant_id, menu_id):
    editedItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        session.add(editedItem)
        session.commit()

        #flash message
        flash("Menu Item has been edited")

        return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
    else:
        # USE THE RENDER_TEMPLATE FUNCTION BELOW TO SEE THE VARIABLES YOU
        # SHOULD USE IN YOUR EDITMENUITEM TEMPLATE
        return render_template('editmenuitem.html', restaurant_id= restaurant_id, menu_id=menu_id, item= editedItem)

@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete/', methods = ['GET','POST'])
def deleteMenuItem(restaurant_id, menu_id):
    itemToDelete = session.query(MenuItem).filter_by(id=menu_id).one()

    if request.method =='POST':
        session.delete(itemToDelete)
        session.commit()

        #flash message
        flash("Menu Item has been deleted")

        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('deleteconfirmation.html', item=itemToDelete)



if __name__ == '__main__':
    app.secret_key = 'super_secret_key' #  since flask.flash uses session
    app.debug = True
    app.run(host='0.0.0.0', port=5000)