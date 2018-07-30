from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from dbsetup import Category, Base, Item
 
engine = create_engine('sqlite:///item_catelog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()
 
# Insert a Category in the Category table
soccer = Category(name='Soccer')
session.add(soccer)
session.commit()
 
snowboarding = Category(name='Snowboarding')
session.add(snowboarding)
session.commit()

# Insert an item in the item table
cleats = Item(name='cleats', description='special shoes worn when playing soccer', category=soccer.name)
session.add(cleats)

ball = Item(name='ball', description='a ball specifically designed for playing a game of soccer', category=soccer.name)
session.add(ball)

shin_guards = Item(name='shinguards', description='guards to protect your shins when playing soccer', category=soccer.name)
session.add(shin_guards)

goggles = Item(name='goggles', description='protective glasses worn when snowboarding to keep your eyes safe', category=snowboarding.name)
session.add(goggles)

board = Item(name='snowboard', description='Most important piece of equipment for snowboarding; used to carving down mountains', category=snowboarding.name)
session.add(board)

session.commit()
