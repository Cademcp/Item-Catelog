from flask import Flask, render_template, request, redirect, jsonify, url_for, flash, request, make_response
from flask import session as login_session

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker

from dbsetup import Category, Base, Item

import urllib

app = Flask(__name__)

engine = create_engine('sqlite:///item_catelog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)


@app.route('/')
@app.route('/catalog')
def showCategories():
    session = DBSession()
    categories = session.query(Category).all()
    session.commit()
    return render_template('home.html', item=categories)


@app.route('/catalog/JSON')
def showCategoriesJSON():
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


@app.route('/catalog/<string:category>/items')
def showCategoryItems(category):
    session = DBSession()

    items = session.query(Item).filter_by(category=category)
    session.commit()
    return render_template('showItems.html', category=category, item=items)


@app.route('/catalog/<string:category>/<string:item>')
def showItemInfo(category, item):
    session = DBSession()
    new_category = urllib.unquote(category)
    new_item = urllib.unquote(item)

    info = session.query(Item).filter_by(category=new_category, name=new_item)
    session.commit()

    return render_template('showItemInfo.html', category=new_category, item=info)


@app.route('/catalog/<string:category>/<string:item>/edit', methods=['GET'])
def editItem(category, item):
    new_category = urllib.unquote(category)
    new_item = urllib.unquote(item)

    session = DBSession()
    category_info = session.query(Category).all()
    item_info = session.query(Item).filter_by(
        category=new_category, name=new_item)
    session.commit()

    return render_template('editItem.html', category=new_category, item=new_item, category_info=category_info, item_info=item_info)


@app.route('/editItem', methods=['POST'])
def edit():
    decision_maker = request.form
    session = DBSession()

    session.query(Item).filter_by(id=decision_maker['itemID']).update(
        {"name": decision_maker['itemName'], "description": decision_maker['itemDescription'], 'category': decision_maker['itemCategory']})

    session.commit()

    return redirect('http://localhost:5000')


@app.route('/catalog/<string:category>/<string:item>/delete', methods=['GET'])
def deleteItem(category, item):
    new_category = urllib.unquote(category)
    new_item = urllib.unquote(item)

    return render_template('deleteItem.html', category=new_category, item=new_item)


@app.route('/deleteItem', methods=['POST'])
def delete():
    decision_maker = request.form['delete_value']
    session = DBSession()
    if decision_maker != 'no':
        info = session.query(Item).filter_by(name=decision_maker).first()

        session.delete(info)
        session.commit()

    return redirect('http://localhost:5000')


@app.route('/catalog/<string:category>/items/add', methods=['GET'])
def addItem(category):
    new_category = urllib.unquote(category)

    session = DBSession()
    info = session.query(Category).all()
    session.commit()

    return render_template('addItem.html', info=info, category=new_category)


@app.route('/addItem', methods=['POST'])
def add():
    decision_maker = request.form
    session = DBSession()

    new_item = Item(name=decision_maker['itemName'],
                    description=decision_maker['itemDescription'], category=decision_maker['category'])
    session.add(new_item)
    session.commit()

    return redirect('http://localhost:5000')


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
