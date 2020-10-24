#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
from flask_migrate import Migrate
import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#
# TODO: connect to a local postgresql database
app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

migrate = Migrate(app , db)#flask db init , flask db migrate

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#
    
class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    website= db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String(120)))
    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String())
    showsR = db.relationship('Show', backref="venues", lazy=True)
     # TODO: implement any missing fields, as a database migration using Flask-Migrate


class Artist(db.Model):
  __tablename__ = 'Artist'

  id = db.Column(db.Integer, primary_key=True)
  name = name = db.Column(db.String)
  city = db.Column(db.String(120))
  state = db.Column(db.String(120))
  phone = db.Column(db.String(120))
  genres = db.Column(db.String(120))
  image_link = db.Column(db.String(500))
  facebook_link = db.Column(db.String(120))
  seeking_venue = db.Column(db.Boolean, default=False)
  seeking_description = db.Column(db.String(120))
  showsR = db.relationship('Show', backref='artist', lazy=True)
   # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
class Show(db.Model):
    __tablename__ = 'shows'
    id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'))
    start_time = db.Column(db.DateTime)


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)
app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@ app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.

    CityAndState = db.session.query(Venue).filter_by(city=Venue.city, state=Venue.state).distinct(Venue.city, Venue.state)
    DataP = []
    venues = []
    for CityState in CityAndState:
        venuesL = db.session.query(Venue).filter_by(city=CityState.city, state=CityState.state).all()
        for ven in venuesL:
            venues.append({"id": ven.id,"name": ven.name })
        DataP.append({"city": CityState.city,'state': CityState.state,'venues': venuesL})

    return render_template('pages/venues.html', areas=DataP)


@ app.route('/venues/search', methods=['POST'])  
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
   searchTerm = request.form.get('search_term', '')
   results = db.session.query(Venue).filter(Venue.name.ilike("%" + searchTerm + "%")).all()  
   venues = []
   for Result in results:
        shows = db.session.query(Show.start_time).filter_by(artist_id=Result.id)
        numUpcomingShows = []
        for show in shows:
            if show.start_time > datetime.now():#comaparing date to get upcoming showes
                numUpcomingShows.append(show)
        venues.append({'id': Result.id,'name': Result.name,'num_upcoming_shows': len(numUpcomingShows)})

   response = {
        "count": len(venues),
        "data": venues
    }
   return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    ven = db.session.query(Venue).get(venue_id)
    show_query = db.session.query(Show).join(Venue).filter(venue_id == Show.venue_id)#join
    upcoming_shows = []
    past_shows = []

    for show in show_query: 
        showDate = show.start_time
        if showDate > datetime.now():
            upcoming_shows.append({'artist_id': show.artist_id,'artist_name': db.session.query(Artist).get(show.artist_id).name,'artist_image_link': db.session.query(Artist).get(show.artist_id).image_link,'start_time': str(show.start_time)})
        else:
            past_shows.append({'artist_id': show.artist_id,'artist_name': db.session.query(Artist).get(show.artist_id).name,'artist_image_link': db.session.query(Artist).get(show.artist_id).image_link,'start_time': str(show.start_time)})

    DataV = {'id': ven.id,'name': ven.name,'genres': ven.genres,'address': ven.address,'city': ven.city,'state': ven.state,'phone': ven.phone,'facebook_link': ven.facebook_link,'seeking_talent': ven.seeking_talent,'seeking_description': ven.seeking_description,'image_link': ven.image_link,
        'past_shows': past_shows,
        'upcoming_shows': upcoming_shows,
        'past_shows_count': len(past_shows),
        'upcoming_shows_count': len(upcoming_shows)} 
    return render_template('pages/show_venue.html', venue=DataV)

# Create Venue
 #----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
    name = request.form['name']
    city = request.form['city']
    state = request.form['state']
    address = request.form['state']
    phone = request.form['phone']
    image_link = request.form['image_link']
    genres = request.form.getlist('genres')
    facebook_link = request.form['facebook_link']
    try:
       db.session.add(Venue(name=name, city=city, state=state, address=address, phone=phone, image_link=image_link,genres=genres, facebook_link=facebook_link, seeking_talent=False, seeking_description=""))
       db.session.commit()
       flash('Venue ' + request.form['name'] + ' was successfully listed!')

    except:
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
        flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
        db.session.rollback()

    return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  try:
    Venue.query.filter_by(id=venue_id).delete()
    db.session.commit()
    flash("Venue successfully deleted!")
  except:
    db.session.rollback() 
    flash("An error occurred could not be deleted, please try again")
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  artists = Artist.query.all()
  data = []
  for artist in artists:
    data.append({'id':artist.id,'name':artist.name})
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  search_term = request.form.get('search_term', '')
  search_query = db.session.query(Artist).filter(Artist.name.ilike("%"+ search_term +"%")).all()
  data = []
  for artist in search_query:
    show_query = db.session.query(Show.start_time).filter_by(artist_id=artist.id)
    num_upcoming_shows=[]
    for show in show_query:
      if show.start_time > datetime.now():
        num_upcoming_shows.append(show)
        data.append({'id':artist.id,'name':artist.name,'num_upcoming_shows':len(num_upcoming_shows)})
  response = {"num":len(search_query),"data":data}
        
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
 # data = list(filter(lambda d: d['id'] == artist_id, [data1, data2, data3]))[0]
    artist = db.session.query(Artist).get(artist_id)
    shows = db.session.query(Show).join(Artist).filter(artist_id == Show.artist_id)
    past_shows = []
    upcoming_shows = []
    for sh in shows:
        if sh.start_time > datetime.now():
            upcoming_shows.append({'venue_id': sh.venue_id,'venue_name': db.session.query(Venue).get(sh.venue_id).name,'venue_image_link': db.session.query(Venue).get(sh.venue_id).image_link,'start_time': str(sh.start_time)})
        else:
            past_shows.append({'venue_id': sh.venue_id,'venue_name': db.session.query(Venue).get(sh.venue_id).name,'venue_image_link': db.session.query(Venue).get(sh.venue_id).image_link,'start_time': str(sh.start_time)})

    DataA ={"id": artist.id,"name": artist.name,"genres": artist.genres,"city": artist.city,"state": artist.state,"phone": artist.phone,"seeking_venue": artist.seeking_venue,"seeking_description": artist.seeking_description,"image_link": artist.image_link,'past_shows': past_shows,'upcoming_shows': upcoming_shows,'past_shows_count': len(past_shows),'upcoming_shows_count': len(upcoming_shows)}
    return render_template('pages/show_artist.html', artist=DataA)#error

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()
    name = form.name.data = db.session.query(Artist.name).filter_by(id=artist_id).scalar()
    city = form.city.data = db.session.query(Artist.city).filter_by(id=artist_id).scalar()
    state = form.state.data = db.session.query(Artist.state).filter_by(id=artist_id).scalar()
    genres = form.genres.data = db.session.query(Artist.genres).filter_by(id=artist_id).all()
    facebook_link = form.facebook_link.data = db.session.query(Artist.facebook_link).filter_by(id=artist_id).scalar()
    image_link = form.image_link.data = db.session.query(Artist.image_link).filter_by(id=artist_id).scalar()
    phone = form.phone.data = db.session.query(Artist.phone).filter_by(id=artist_id).scalar()
    artist = {"id": artist_id,"name": name,"genres": genres,"city": city,"state": state,"phone": phone,"facebook_link": facebook_link,"image_link": image_link,"website": "https://www.gunsnpetalsband.com","seeking_venue": False,"seeking_description": ""}
  # TODO: populate form with fields from artist with ID <artist_id>
    return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
    try:
        artistObj = Artist(id=db.session.query(Artist).get(artist_id),name=request.form['name'],city = request.form['city'],state = request.form['state'],phone = request.form['phone'],genres = request.form.getlist('genres'),facebook_link = request.form['facebook_link'],image_link = request.form['image_link'])
        db.session.commit()
        flash("Artist successfully edited!")
    except:
        flash("An error occurred could not be edited, please try again")
    return redirect(url_for('show_artist', artist_id=artist_id))
  #return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    name = form.name.data = db.session.query(Venue.name).filter_by(id=venue_id).scalar()
    city = form.city.data = db.session.query(Venue.city).filter_by(id=venue_id).scalar()
    state = form.state.data = db.session.query(Venue.state).filter_by(id=venue_id).scalar()
    genres = form.genres.data = db.session.query(Venue.genres).filter_by(id=venue_id).all()
    facebook_link = form.facebook_link.data = db.session.query(Venue.facebook_link).filter_by(id=venue_id).scalar()
    image_link = form.image_link.data = db.session.query(Venue.image_link).filter_by(id=venue_id).scalar()
    phone = form.phone.data = db.session.query(Venue.phone).filter_by(id=venue_id).scalar()
    address = form.address.data = db.session.query(Venue.address).filter_by(id=venue_id).scalar()

    venue = {"id": venue_id,"name": name,"genres": genres,"address": address,"city": city,"state": state,"phone": phone,"website": "","facebook_link": facebook_link,"image_link": image_link,"seeking_talent": False,"seeking_description": ""}
  # TODO: populate form with values from venue with ID <venue_id>
    return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
    name = request.form['name']
    city = request.form['city']
    state = request.form['state']
    phone = request.form['phone']
    genres = request.form.getlist('genres')
    image_link = request.form['image_link']
    facebook_link = request.form['facebook_link']
    try:
        db.session.add(Artist(name=name, city=city, state=state, phone=phone, genres=genres, image_link=image_link, facebook_link=facebook_link, seeking_venue=False, seeking_description=""))
        db.session.commit()
        flash('Artist ' + request.form['name'] + ' was successfully listed!')
    except:
        flash('Artist ' + request.form['name'] + ' was unsuccessfully listed.')
        db.session.rollback()

    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.


    show_query = db.session.query(Show).join(Artist).filter(Artist.id == Show.artist_id).all()#join shows and artist by id 
    DataSh = []
    for show in show_query:
        artist = db.session.query(Artist).get(show.artist_id)#get artisist
        venue = db.session.query(Venue).get(show.venue_id)#get venue 
        DataSh.append({'venue_id': venue.id,'venue_name': venue.name,'artist_id': artist.id,'artist_name': artist.name,'artist_image_link': artist.image_link,'start_time': str(show.start_time)})

    return render_template('pages/shows.html', shows=DataSh)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead

    artistID = request.form['artist_id']
    venueID = request.form['venue_id']
    startTime = request.form['start_time']

    if (len(db.session.query(Artist).filter_by(id=request.form['artist_id']).all()) or len(db.session.query(Venue).filter_by(id=request.form['venue_id']).all())) == 1:
          try:
            db.session.add(Show(venue_id=request.form['venue_id'], artist_id=request.form['artist_id'], start_time=request.form['start_time']))
            db.session.commit()
            flash('Show successfully added!')  # on successful db insert, flash success
              # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
          except expression as identifier:
            db.session.rollback()
            flash('An error occurred. Show could not be listed.')
    else:
      flash(' Artist or Venue don not exist , please rty again')
      

    return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
      return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

'''


