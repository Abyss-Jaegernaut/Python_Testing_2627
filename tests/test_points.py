from server import clubs


def test_public_points_display_status_code(client):
    response = client.get('/pointsDisplay')
    assert response.status_code == 200


def test_public_points_display_content(client):
    response = client.get('/pointsDisplay')
    data = response.data.decode()
    for club in clubs:
        assert club['name'] in data
        assert str(club['points']) in data
