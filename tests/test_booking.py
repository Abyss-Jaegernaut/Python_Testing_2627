from server import clubs, competitions


def test_deduction_points_club(client):
    """Vérifie la déduction effective des points après réservation."""
    club = [c for c in clubs if c['name'] == 'Simply Lift'][0]
    initial_points = int(club['points'])
    places_to_buy = 3

    client.post('/showSummary', data={'email': 'john@simplylift.co'})

    response = client.post('/purchasePlaces', data={
        'club': 'Simply Lift',
        'competition': 'Spring Festival',
        'places': str(places_to_buy)
    }, follow_redirects=True)

    assert response.status_code == 200
    assert int(club['points']) == initial_points - places_to_buy
    expected = f"Points available: {initial_points - places_to_buy}".encode()
    assert expected in response.data


def test_surreservation_competition(client):
    """Vérifie le blocage si la demande dépasse les places disponibles."""
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
    assert (
        b"pas assez de places" in response.data.lower()
        or b"disponibles" in response.data.lower()
    )


def test_purchase_more_places_than_club_points(client):
    """Vérifie le blocage si le club n'a pas assez de points."""
    club = [c for c in clubs if c['name'] == 'Iron Temple'][0]
    competition = [
        c for c in competitions if c['name'] == 'Spring Festival'
    ][0]

    initial_points = int(club['points'])
    initial_places = int(competition['numberOfPlaces'])

    response = client.post('/purchasePlaces', data={
        'club': club['name'],
        'competition': competition['name'],
        'places': '6'
    })

    assert response.status_code == 200
    assert int(club['points']) == initial_points
    assert int(competition['numberOfPlaces']) == initial_places
    assert (
        b"pas assez de points" in response.data.lower()
        or b"insuffisant" in response.data.lower()
    )


def test_purchase_more_than_12_places(client):
    """Vérifie qu'un club ne peut pas réserver plus de 12 places d'un coup."""
    club = [c for c in clubs if c['name'] == 'Simply Lift'][0]
    competition = [
        c for c in competitions if c['name'] == 'Spring Festival'
    ][0]

    initial_points = int(club['points'])
    initial_places = int(competition['numberOfPlaces'])

    response = client.post('/purchasePlaces', data={
        'club': club['name'],
        'competition': competition['name'],
        'places': '13'
    })

    assert response.status_code == 200
    assert int(club['points']) == initial_points
    assert int(competition['numberOfPlaces']) == initial_places
    assert b"12 places" in response.data


def test_cumulative_booking_limit_12_places(client):
    """Vérifie qu'un club ne peut pas dépasser 12 places en cumulé."""
    club = [c for c in clubs if c['name'] == 'Simply Lift'][0]
    competition = [
        c for c in competitions if c['name'] == 'Spring Festival'
    ][0]

    club['points'] = 25
    competition['numberOfPlaces'] = 25

    response1 = client.post('/purchasePlaces', data={
        'club': club['name'],
        'competition': competition['name'],
        'places': '8'
    }, follow_redirects=True)

    assert response1.status_code == 200
    assert int(club['points']) == 17

    response2 = client.post('/purchasePlaces', data={
        'club': club['name'],
        'competition': competition['name'],
        'places': '5'
    })
    assert response2.status_code == 200
    assert int(club['points']) == 17
    assert (
        b"12 places" in response2.data
        or b"deja reserves" in response2.data
        or b"quota" in response2.data.lower()
    )


def test_cannot_book_past_competition(client):
    """Vérifie l'interdiction de réserver sur une compétition passée."""
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
    assert (
        "passée" in response.data.decode()
        or "terminée" in response.data.decode()
    )


def test_invalid_places_input(client):
    """Vérifie le rejet des saisies de places négatives, nulles ou texte."""
    club = [c for c in clubs if c['name'] == 'Simply Lift'][0]
    competition = [
        c for c in competitions if c['name'] == 'Spring Festival'
    ][0]

    initial_points = int(club['points'])

    response_neg = client.post('/purchasePlaces', data={
        'club': club['name'],
        'competition': competition['name'],
        'places': '-3'
    })
    assert response_neg.status_code == 200
    assert int(club['points']) == initial_points
    assert (
        "positif" in response_neg.data.decode().lower()
        or "invalide" in response_neg.data.decode().lower()
    )

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


def test_book_unknown_club_or_competition(client):
    """Vérifie la gestion d'URLs de réservation invalides ou forgées."""
    response_club = client.get(
        '/book/Spring Festival/RealMadrid', follow_redirects=True
    )
    assert response_club.status_code == 200
    assert (
        "introuvable" in response_club.data.decode().lower()
        or "wrong" in response_club.data.decode().lower()
        or "welcome" in response_club.data.decode().lower()
    )

    response_comp = client.get(
        '/book/LaLiga/Simply Lift', follow_redirects=True
    )
    assert response_comp.status_code == 200
    assert (
        "introuvable" in response_comp.data.decode().lower()
        or "wrong" in response_comp.data.decode().lower()
        or "welcome" in response_comp.data.decode().lower()
    )


def test_purchase_places_redirects_after_post(client):
    """Vérifie l'application du pattern PRG (redirection 302)."""
    client.post('/showSummary', data={'email': 'john@simplylift.co'})

    response = client.post('/purchasePlaces', data={
        'club': 'Simply Lift',
        'competition': 'Spring Festival',
        'places': '1'
    })

    assert response.status_code == 302


def test_welcome_separates_upcoming_and_past_competitions(client):
    """Vérifie la séparation visuelle entre compétitions à venir et passées."""
    response = client.post(
        '/showSummary', data={'email': 'john@simplylift.co'}
    )
    assert response.status_code == 200
    data = response.data.decode()

    assert (
        ("Compétitions à venir" in data) or ("Upcoming Competitions" in data)
    )
    assert ("Compétitions passées" in data) or ("Past Competitions" in data)
    assert ("Terminée" in data) or ("closed" in data)


def test_booking_form_html5_validation_and_cancel_link(client):
    """Vérifie les contraintes min, max, required et le lien d'annulation."""
    response = client.get('/book/Spring Festival/Simply Lift')
    assert response.status_code == 200
    data = response.data.decode()

    assert 'min="1"' in data
    assert 'max="12"' in data
    assert 'required' in data
    assert 'showSummary' in data or 'Annuler' in data or 'Cancel' in data
