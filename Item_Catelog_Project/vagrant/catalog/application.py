from flask import Flask, render_template, request, redirect, jsonify, url_for, flash, request, make_response
from flask import session as login_session

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
 
from dbsetup import Category, Base, Item

app = Flask(__name__)

engine = create_engine('sqlite:///item_catelog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)


@app.route('/')
@app.route('/catalog')
def showCategories():
    session = DBSession()
    categories = session.query(Category).all()
    temp = []
    for i in categories:
        temp.append(i.name)
    session.commit()
    return jsonify(temp)


@app.route('/catalog/<string:category>/items')
def showCategoryItmes(category):
    session = DBSession()

    items = session.query(Item).filter_by(category = category)

    temp = []
    for i in items:
        temp.append(i.name)
    session.commit()
    return jsonify(temp)


@app.route('/catalog/<string:category>/<string:item>')
def showItemInfo(category, item):
    session = DBSession()

    info = session.query(Item).filter_by(category = category, name = item)
    
    temp = []
    for i in info:
        temp.append(i.name)
        temp.append(i.description)
    session.commit()
    return jsonify(temp)


@app.route('/catalog/<string:category>/<string:item>/edit', methods=['GET', 'POST'])
def editItem(category, item):
    if request.method == 'GET':
        return render_template('editItem.html')


if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port=5000)
