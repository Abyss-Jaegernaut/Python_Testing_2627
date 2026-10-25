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
