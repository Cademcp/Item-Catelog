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
    temp = []
    for i in categories:
        temp.append(i.name)
    session.commit()
    return jsonify(temp)


@app.route('/catalog/<string:category>/items')
def showCategoryItmes(category):
    session = DBSession()

    items = session.query(Item).filter_by(category=category)

    temp = []
    for i in items:
        temp.append(i.name)
    session.commit()
    return jsonify(temp)


@app.route('/catalog/<string:category>/<string:item>')
def showItemInfo(category, item):
    session = DBSession()

    new_item = urllib.unquote(item)

    info = session.query(Item).filter_by(category=category, name=new_item)

    temp = []
    for i in info:
        temp.append(i.name)
        temp.append(i.description)
    session.commit()
    return jsonify(temp)


@app.route('/catalog/<string:item>/edit', methods=['GET', 'POST'])
def editItem(item):
    new_item = urllib.unquote(item)
    if request.method == 'GET':
        return render_template('editItem.html')


@app.route('/catalog/<string:item>/delete', methods=['GET'])
def deleteItem(item):
    new_item = urllib.unquote(item)

    return render_template('deleteItem.html', item=new_item)


@app.route('/deleteItem', methods=['POST'])
def delete():
    decision_maker = request.form['delete_value']
    session = DBSession()
    if decision_maker != 'no':
        info = session.query(Item).filter_by(name=decision_maker).first()
  
        session.delete(info)
        session.commit()

    return redirect('http://localhost:5000')


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
