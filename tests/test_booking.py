from server import clubs, competitions

def test_deduction_points_club(client):
    
    club = [c for c in clubs if c['name'] == 'Simply Lift'][0]
    initial_points = int(club['points'])
    places_to_buy = 3

    response = client.post('/purchasePlaces', data={
        'club': 'Simply Lift',
        'competition': 'Spring Festival',
        'places': str(places_to_buy)
    })

    assert response.status_code == 200
    assert int(club['points']) == initial_points - places_to_buy
    expected_display = f"Points available: {initial_points - places_to_buy}".encode()
    assert expected_display in response.data

# Vérifie qu'on ne peut pas réserver plus de places qu'il n'en reste dans la compétition

def test_surreservation_competition(client):
    
    competition = [c for c in competitions if c['name'] == 'Fall Classic'][0]
    club = [c for c in clubs if c['name'] == 'Simply Lift'][0]

    competition['numberOfPlaces'] = 4
    initial_club_points = int(club['points'])

    response = client.post('/purchasePlaces', data={
        'club': club['name'],
        'competition': competition['name'],
        'places': '6'
    })

    assert response.status_code == 200

    assert int(competition['numberOfPlaces']) == 4
    assert int(club['points']) == initial_club_points
    assert b"pas assez de places" in response.data.lower() or b"disponibles" in response.data.lower()

# Vérifie qu'un club ne peut pas acheter plus de places que son solde de points le permet

def test_purchase_more_places_than_club_points(client):

    club = [c for c in clubs if c['name'] == 'Iron Temple'][0]
    competition = [c for c in competitions if c['name'] == 'Spring Festival'][0]

    initial_points = int(club['points'])
    initial_competition_places = int(competition['numberOfPlaces'])

    response = client.post('/purchasePlaces', data={
        'club': club['name'],
        'competition': competition['name'],
        'places': '6'
    })

    assert response.status_code == 200

    assert int(club['points']) == initial_points
    assert int(competition['numberOfPlaces']) == initial_competition_places
    assert b"pas assez de points" in response.data.lower() or b"insuffisant" in response.data.lower()

#Vérifie qu'un club ne peut pas réserver plus de 12 places pour une compétition

def test_purchase_more_than_12_places(client):

    club = [c for c in clubs if c['name'] == 'Simply Lift'][0]
    competition = [c for c in competitions if c['name'] == 'Spring Festival'][0]

    initial_points = int(club['points'])
    initial_competition_places = int(competition['numberOfPlaces'])

    response = client.post('/purchasePlaces', data={
        'club': club['name'],
        'competition': competition['name'],
        'places': '13'
    })

    assert response.status_code == 200

    assert int(club['points']) == initial_points
    assert int(competition['numberOfPlaces']) == initial_competition_places
    assert b"12 places" in response.data

# Vérifie qu'un club ne peut pas dépasser 12 places en faisant plusieurs réservations successives

def test_cumulative_booking_limit_12_places(client):

    club = [c for c in clubs if c['name'] == 'Simply Lift'][0]
    competition = [c for c in competitions if c['name'] == 'Spring Festival'][0]

    club['points'] = 25
    competition['numberOfPlaces'] = 25

    response1 = client.post('/purchasePlaces', data={
        'club': club['name'],
        'competition': competition['name'],
        'places': '8'
    })
    assert response1.status_code == 200
    assert int(club['points']) == 17

    response2 = client.post('/purchasePlaces', data={
        'club': club['name'],
        'competition': competition['name'],
        'places': '5'
    })
    assert response2.status_code == 200

    assert int(club['points']) == 17
    assert b"12 places" in response2.data or b"deja reserves" in response2.data or b"quota" in response2.data.lower()

# Vérifie qu'on ne peut pas réserver de places pour une compétition passée

def test_cannot_book_past_competition(client):

    club = [c for c in clubs if c['name'] == 'Simply Lift'][0]
    competition = [c for c in competitions if c['name'] == 'Fall Classic'][0]

    competition['date'] = "2026-07-04 10:01:24"
    initial_points = int(club['points'])
    initial_places = int(competition['numberOfPlaces'])

    response = client.post('/purchasePlaces', data={
        'club': club['name'],
        'competition': competition['name'],
        'places': '2'
    })

    assert response.status_code == 200

    assert int(club['points']) == initial_points
    assert int(competition['numberOfPlaces']) == initial_places
    assert "passée" in response.data.decode() or "terminée" in response.data.decode()

# Vérifie que la saisie d'un nombre négatif, nul ou de texte est rejetée

def test_invalid_places_input(client):
    club = [c for c in clubs if c['name'] == 'Simply Lift'][0]
    competition = [c for c in competitions if c['name'] == 'Spring Festival'][0]

    initial_points = int(club['points'])
    initial_places = int(competition['numberOfPlaces'])

    response_neg = client.post('/purchasePlaces', data={
        'club': club['name'],
        'competition': competition['name'],
        'places': '-3'
    })
    assert response_neg.status_code == 200

    assert int(club['points']) == initial_points
    assert "positif" in response_neg.data.decode().lower() or "invalide" in response_neg.data.decode().lower()

    response_zero = client.post('/purchasePlaces', data={
        'club': club['name'],
        'competition': competition['name'],
        'places': '0'
    })
    assert response_zero.status_code == 200

    assert int(club['points']) == initial_points

    response_text = client.post('/purchasePlaces', data={
        'club': club['name'],
        'competition': competition['name'],
        'places': 'abc'
    })
    assert response_text.status_code == 200
    
    assert int(club['points']) == initial_points

# Vérifie que la route gère proprement les noms inconnus

def test_book_unknown_club_or_competition(client):

    response_club = client.get('/book/Spring Festival/RealMadrid', follow_redirects=True)
    assert response_club.status_code == 200

    assert "introuvable" in response_club.data.decode().lower() or "wrong" in response_club.data.decode().lower() or "welcome" in response_club.data.decode().lower()

    response_comp = client.get('/book/LaLiga/Simply Lift', follow_redirects=True)
    assert response_comp.status_code == 200
    
    assert "introuvable" in response_comp.data.decode().lower() or "wrong" in response_comp.data.decode().lower() or "welcome" in response_comp.data.decode().lower()

# Vérifie que la réservation réussie applique le pattern PRG (redirection 302 pour éviter la double soumission de rafraichissement)

def test_purchase_places_redirects_after_post(client):
    client.post('/showSummary', data={'email': 'john@simplylift.co'})

    response = client.post('/purchasePlaces', data={
        'club': 'Simply Lift',
        'competition': 'Spring Festival',
        'places': '1'
    })

    assert response.status_code == 302
