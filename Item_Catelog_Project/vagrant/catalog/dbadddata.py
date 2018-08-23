from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from dbsetup import Category, Base, Item
 
engine = create_engine('sqlite:///item_catelog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)

session = DBSession()
 
# Insert categories into the Category table
soccer = Category(name='Soccer')
session.add(soccer)
session.commit()

basketball = Category(name='Basketball')
session.add(basketball)
session.commit()

baseball = Category(name='Baseball')
session.add(baseball)
session.commit()

frisbee = Category(name='Frisbee')
session.add(frisbee)
session.commit()

snowboarding = Category(name='Snowboarding')
session.add(snowboarding)
session.commit()

rockclimbing = Category(name='Rock Climbing')
session.add(rockclimbing)
session.commit()

foosball = Category(name='Foosball')
session.add(foosball)
session.commit()

skating = Category(name='Skating')
session.add(skating)
session.commit()

hockey = Category(name='Hockey')
session.add(hockey)
session.commit()
 

# Insert a few starting items into the item table
cleats = Item(name='cleats', 
description='special shoes worn when playing soccer', category=soccer.name)
session.add(cleats)

ball = Item(name='ball',
 description='a ball specifically designed for playing a game of soccer', 
 category=soccer.name)
session.add(ball)

shinguards = Item(name='shinguards', 
description='guards to protect your shins when playing soccer', 
category=soccer.name)
session.add(shinguards)

goggles = Item(name='goggles', 
description='protective glasses worn when snowboarding to keep your eyes safe',
 category=snowboarding.name)
session.add(goggles)

snowboard = Item(name='snowboard',
 description='Most important piece of equipment for \
 snowboarding; used to carving down mountains', 
 category=snowboarding.name)
session.add(snowboard)

session.commit()
