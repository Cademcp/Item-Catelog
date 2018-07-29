from flask import Flask, render_template, request, redirect, jsonify, url_for, flash


from flask import session as login_session
import random
import string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
 
from dbsetup import Category, Base, Item

app = Flask(__name__)


if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port=5000)

# TODO DB CRUD code for later
# engine = create_engine('sqlite:///item_catelog.db')
# Base.metadata.bind = engine

# DBSession = sessionmaker(bind=engine)

# session = DBSession()

# category = session.query(Category.name).all()

# for i in category:
#     print i.name

# category = session.query(Item.name).all()

# for i in category:
#     print i.name