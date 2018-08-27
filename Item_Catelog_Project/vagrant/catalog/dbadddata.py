from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from dbsetup import Category, Base, Item, User
 
engine = create_engine('sqlite:///item_catelog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)

session = DBSession()

User1 = User(name="Cade McPartlin", email="cademcp@gmail.com")
session.add(User1)
session.commit()
 
# Insert categories into the Category table
soccer = Category(user_id=1, name='Soccer')
session.add(soccer)
session.commit()

basketball = Category(user_id=1, name='Basketball')
session.add(basketball)
session.commit()

baseball = Category(user_id=1, name='Baseball')
session.add(baseball)
session.commit()

frisbee = Category(user_id=1, name='Frisbee')
session.add(frisbee)
session.commit()

snowboarding = Category(user_id=1, name='Snowboarding')
session.add(snowboarding)
session.commit()

rockclimbing = Category(user_id=1, name='Rock Climbing')
session.add(rockclimbing)
session.commit()

foosball = Category(user_id=1, name='Foosball')
session.add(foosball)
session.commit()

skating = Category(user_id=1, name='Skating')
session.add(skating)
session.commit()

hockey = Category(user_id=1, name='Hockey')
session.add(hockey)
session.commit()
 

# Insert a few starting items into the item table
cleats = Item(user_id=1, name='cleats', 
description='special shoes worn when playing soccer', category=soccer.name)
session.add(cleats)

ball = Item(user_id=1, name='ball',
 description='a ball specifically designed for playing a game of soccer', 
 category=soccer.name)
session.add(ball)

shinguards = Item(user_id=1, name='shinguards', 
description='guards to protect your shins when playing soccer', 
category=soccer.name)
session.add(shinguards)

goggles = Item(user_id=1, name='goggles', 
description='protective glasses worn when snowboarding to keep your eyes safe',
 category=snowboarding.name)
session.add(goggles)

snowboard = Item(user_id=1, name='snowboard',
 description='Most important piece of equipment for \
 snowboarding; used to carving down mountains', 
 category=snowboarding.name)
session.add(snowboard)

bat = Item(user_id=1, name='bat',
 description='Used for hitting baseballs out of the park', 
 category=baseball.name)
session.add(bat)

disc = Item(user_id=1, name='disc',
 description='Frisbee disc used to score points in frisbee golf', 
 category=frisbee.name)
session.add(disc)

boots = Item(user_id=1, name='boots',
 description='Hiking boots are an important piece of equipment when rock \
 climbing', 
 category=rockclimbing.name)
session.add(boots)

table = Item(user_id=1, name='Foosball Table',
 description='This is where the game of foosball is played', 
 category=foosball.name)
session.add(table)


rollerskates = Item(user_id=1, name='rollerskates',
 description='Roller skates are shoes that have four wheels, two of which \
 are in the front and two in the back of the shoe horizontal to each other', 
 category=skating.name)
session.add(rollerskates)

stick = Item(user_id=1, name='Hockey Stick',
 description='The piece of equipment used to hit the hockey puck into the net', 
 category=hockey.name)
session.add(stick)

session.commit()
