import json
from flask import Flask,render_template,request,redirect,flash,url_for
from datetime import datetime


def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()
booking_history = {} 

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary', methods=['POST'])
def showSummary():
    email = request.form.get('email', '').strip()
    club = next((c for c in clubs if c['email'] == email), None)
    if not club:
        flash("Adresse email non reconnue. Veuillez réessayer.")
        return redirect(url_for('index'))
    return render_template('welcome.html', club=club, competitions=competitions)

@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html',club=foundClub,competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])

    comp_date = datetime.strptime(competition['date'], "%Y-%m-%d %H:%M:%S")
    if comp_date < datetime.now():
        flash("Cette compétition est déjà passée, impossible de réserver des places.")
        return render_template('welcome.html', club=club, competitions=competitions)

    already_booked = booking_history.get((club['name'], competition['name']), 0)
    if already_booked + placesRequired > 12:
        places_restantes = 12 - already_booked
        flash(f"Vous ne pouvez pas réserver plus de 12 places au total pour cette compétition. Vous en avez déjà réservé {already_booked}.")
        return render_template('welcome.html', club=club, competitions=competitions)

    if placesRequired > int(competition['numberOfPlaces']):
        flash("Il n'y a pas assez de places disponibles dans cette compétition.")
        return render_template('welcome.html', club=club, competitions=competitions)

    if placesRequired > int(club['points']):
        flash("Votre solde de points est insuffisant pour effectuer cette réservation.")
        return render_template('welcome.html', club=club, competitions=competitions)

    competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesRequired
    club['points'] = int(club['points']) - placesRequired
    booking_history[(club['name'], competition['name'])] = already_booked + placesRequired

    flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions)



# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))