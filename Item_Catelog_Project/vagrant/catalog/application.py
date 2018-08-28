from flask import Flask, render_template, request, redirect, jsonify, \
    url_for, flash, request, make_response
from flask import session as login_session

import random
import string
import urllib
import httplib2
import json
import requests

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker

from dbsetup import Category, Base, Item, User


app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']

engine = create_engine('sqlite:///item_catelog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)


@app.route('/login')
def showLogin():
    """Shows login screen when user tries to access information that they must
    be authenticated for"""
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already \
        connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: \
    150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps(
            'Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % \
        login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return redirect('/catalog')
    else:
        response = make_response(json.dumps(
            'Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/')
@app.route('/catalog')
def showCategories():
    """Gets a list of all categories in the db and displays them
    in a template"""
    session = DBSession()
    categories = session.query(Category).all()
    session.commit()

    if 'username' not in login_session:
        return render_template('publichome.html', item=categories)
    else:
        return render_template('home.html', item=categories)


@app.route('/JSON')
def showAllJSON():
    """JSON endpoint to show all information held in the catalog"""
    session = DBSession()
    db_category = session.query(Category).all()
    categories = list()
    for category in db_category:
        db_items = session.query(Item).filter_by(category=category.name)
        items = list()
        for item in db_items:
            items.append(item.serialize)
        categories.append({'id': category.id,
                           'name': category.name,
                           'Item': items})

    return jsonify(Category=categories)


@app.route('/catalog/JSON')
def showCategoriesJSON():
    """JSON endpoint to show all categories and information about them"""
    session = DBSession()
    db_category = session.query(Category).all()
    categories = list()
    for category in db_category:
        categories.append({'id': category.id, 'name': category.name})
    session.commit()
    return jsonify(Category=categories)


@app.route('/catalog/<string:category>/items')
def showCategoryItems(category):
    """Gets items specific to selected category"""
    session = DBSession()

    temp_category = session.query(Category).filter_by(name=category).one()
    items = session.query(Item).filter_by(category=category)

    session.commit()

    creator = getUserInfo(temp_category.user_id)
    if 'username' not in login_session or creator.id!=login_session['user_id']:
        return render_template('publicshowitems.html', category=category,
                               item=items)
    else:
        return render_template('showItems.html', category=category, item=items)


@app.route('/catalog/<string:category>/items/JSON')
def showItemJSON(category):
    """JSON endpoint to show items specific to a category"""
    session = DBSession()

    items = session.query(Item).filter_by(category=category)

    temp = list()
    for item in items:
        temp.append({'id': item.id, 'name': item.name})
    session.commit()

    return jsonify(Items=temp)


@app.route('/catalog/<string:category>/<string:item>')
def showItemInfo(category, item):
    """Shows information based on item selected"""
    if 'username' not in login_session:
        return redirect('/login')
    session = DBSession()
    new_category = urllib.unquote(category)
    new_item = urllib.unquote(item)

    info = session.query(Item).filter_by(category=new_category, name=new_item)
    session.commit()

    return render_template('showItemInfo.html', category=new_category,
                           item=info)


@app.route('/catalog/<string:category>/<string:item>/edit', methods=['GET'])
def editItem(category, item):
    """Allows authenticated user to edit items within a category"""
    session = DBSession()

    temp_category = session.query(Category).filter_by(name=category).one()
    creator = getUserInfo(temp_category.user_id)

    if 'username' not in login_session or creator.id!=login_session['user_id']:
        return render_template('accessDenied.html')

    new_category = urllib.unquote(category)
    new_item = urllib.unquote(item)

    category_info = session.query(Category).all()
    item_info = session.query(Item).filter_by(
        category=new_category, name=new_item)
    session.commit()

    return render_template('editItem.html', category=new_category,
                           item=new_item, category_info=category_info,
                           item_info=item_info)


@app.route('/editItem', methods=['POST'])
def edit():
    """Helper route for editing items"""
    decision_maker = request.form
    session = DBSession()

    session.query(Item).filter_by(id=decision_maker['itemID']).update(
        {"name": decision_maker['itemName'],
         "description": decision_maker['itemDescription'],
         'category': decision_maker['itemCategory']})

    session.commit()

    return redirect('http://localhost:5000')


@app.route('/catalog/<string:category>/<string:item>/delete', methods=['GET'])
def deleteItem(category, item):
    """Allows authenticated user to delete items within a category"""
    session = DBSession()

    temp_category = session.query(Category).filter_by(name=category).one()
    creator = getUserInfo(temp_category.user_id)

    if 'username' not in login_session or creator.id!=login_session['user_id']:
        return render_template('accessDenied.html')

    new_category = urllib.unquote(category)
    new_item = urllib.unquote(item)

    return render_template('deleteItem.html', category=new_category,
                           item=new_item)


@app.route('/deleteItem', methods=['POST'])
def delete():
    """Helper route for deleting items"""
    decision_maker = request.form['delete_value']
    session = DBSession()
    if decision_maker != 'no':
        info = session.query(Item).filter_by(name=decision_maker).first()

        session.delete(info)
        session.commit()

    return redirect('http://localhost:5000')


@app.route('/catalog/<string:category>/items/add', methods=['GET'])
def addItem(category):
    """Allows authenticated user to add items within a category"""

    if 'username' not in login_session:
        return redirect('/login')

    new_category = urllib.unquote(category)

    session = DBSession()
    info = session.query(Category).all()
    session.commit()

    return render_template('addItem.html', info=info, category=new_category)


@app.route('/addItem', methods=['POST'])
def add():
    """Helper route for adding items"""
    decision_maker = request.form
    session = DBSession()

    new_item = Item(name=decision_maker['itemName'],
                    description=decision_maker['itemDescription'],
                    category=decision_maker['category'],
                    user_id=login_session['user_id'])
    session.add(new_item)
    session.commit()

    return redirect('http://localhost:5000')


@app.route('/catalog/add', methods=['GET'])
def addCategory():
    """Allows authenticated user to add new Categories to catalog"""
    return render_template('addCategory.html')
        

@app.route('/catalog/addCategory', methods=['POST'])
def addCategoryPOST():
    decision_maker = request.form
    session = DBSession()

    new_item = Category(name=decision_maker['categoryName'],
                        user_id=login_session['user_id'])
    session.add(new_item)
    session.commit()

    return redirect('http://localhost:5000')


def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session = DBSession()
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    session = DBSession()
    user = session.query(User).filter_by(id=user_id).one()
    session.commit()
    return user


def getUserID(email):
    try:
        session = DBSession()
        user = session.query(User).filter_by(email=email).one()
        session.commit()
        return user.id
    except:
        return None


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
