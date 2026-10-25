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
