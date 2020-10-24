from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import Venue, Show, Artist
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine('postgres://postgres:1234@localhost:5432/fyyur')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Venue.metadata.bind = engine

#Base.metadata.bind = engine
Base = declarative_base(bind=engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
#select * from "Venue";

venue1 = Venue(id=1,name= "The Musical Hop",city= "San Francisco",state= "CA",address= "1015 Folsom Street",phone= "123-123-1234",website= "https://www.themusicalhop.com", image_link= "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",facebook_link= "https://www.facebook.com/TheMusicalHop",genres = ["Jazz", "Reggae", "Swing", "Classical", "Folk"], seeking_talent= True,seeking_description= "We are on the lookout for a local artist to play every two weeks. Please call us.")
venue2 = Venue(id=2,name = "The Dueling Pianos Bar",genres =["Classical", "R&B", "Hip-Hop"],city = "New York",state = "NY",phone = "914-003-1132",facebook_link= "https://www.facebook.com/theduelingpianos",website="https://www.theduelingpianos.com", seeking_talent= False,image_link= "https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80")
venue3 = Venue(id=3, name = "Park Square Live Music & Coffee",genres= ["Rock n Roll", "Jazz", "Classical", "Folk"],address= "34 Whiskey Moore Ave",city="San Francisco",state= "CA", phone= "415-000-1234",website= "https://www.parksquarelivemusicandcoffee.com",facebook_link= "https://www.facebook.com/ParkSquareLiveMusicAndCoffee",seeking_talent= False,image_link= "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80")

artist1 = Artist(id=4,name= "Guns N Petals",genres=["Rock n Roll"],city= "San Francisco",state= "CA",phone= "326-123-5000",facebook_link= "https://www.facebook.com/GunsNPetals",seeking_venue= True,seeking_description= "Looking for shows to perform at in the San Francisco Bay Area!",image_link= "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80")
#artist1 ,website= "https://www.gunsnpetalsband.com"
artist2 = Artist(id=5,name= "Matt Quevedo",genres= ["Jazz"],city= "New York",state="NY",phone= "300-400-5000",facebook_link= "https://www.facebook.com/mattquevedo923251523",seeking_venue= False,image_link= "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80")
artist3 = Artist(id=6,name= "The Wild Sax Band",genres= ["Jazz", "Classical"],city= "San Francisco",state= "CA",phone= "432-325-5432",seeking_venue= False,image_link="https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80")


show1 = Show(id=1,venue_id=1,artist_id=4, start_time="2019-05-21T21:30:00.000Z")
show2 = Show(id=2,venue_id=3,artist_id=5, start_time="2019-06-15T23:00:00.000Z")
show3 = Show(id=3,venue_id=3,artist_id=6, start_time="2035-04-01T20:00:00.000Z")
show4 = Show(id=4,venue_id=3,artist_id=6, start_time="2035-04-08T20:00:00.000Z")
show5 = Show(id=5,venue_id=3,artist_id=6, start_time="2035-04-15T20:00:00.000Z")

session.add(venue3)
session.commit()
session.add(venue1)
session.commit()
session.add(venue2)
session.commit()
session.add(artist1)
session.commit()
session.add(artist2)
session.commit()
session.add(artist3)
session.commit()
session.add(show1)
session.commit()
session.add(show2)
session.commit()
session.add(show3)
session.commit()
session.add(show4)
session.commit()
session.add(show5)
session.commit()