# Tests d'authentification et de session


def test_index_page(client):
    """Vérifie que la page d'accueil se charge correctement."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome to the GUDLFT Registration Portal!" in response.data


def test_login_successful(client):
    """Vérifie la connexion réussie avec un email existant."""
    response = client.post(
        '/showSummary', data={'email': 'john@simplylift.co'}
    )
    assert response.status_code == 200
    assert b"Welcome, john@simplylift.co" in response.data


def test_login_unknown_email(client):
    """Vérifie qu'un email inconnu redirige avec un message d'erreur."""
    response = client.post(
        '/showSummary',
        data={'email': 'test@gmail.com'},
        follow_redirects=True
    )
    assert response.status_code == 200
    assert b"Welcome to the GUDLFT Registration Portal!" in response.data
    assert (
        b"D&#39;adresse email non reconnue" in response.data
        or b"non reconnue" in response.data
        or b"not found" in response.data.lower()
    )


def test_login_empty_email(client):
    """Vérifie qu'une tentative avec un champ vide est rejetée."""
    response = client.post(
        '/showSummary', data={'email': ''}, follow_redirects=True
    )
    assert response.status_code == 200
    assert b"Welcome to the GUDLFT Registration Portal!" in response.data


def test_login_and_logout_session(client):
    """Vérifie la gestion sécurisée de la session utilisateur."""
    client.post('/showSummary', data={'email': 'john@simplylift.co'})
    with client.session_transaction() as session:
        assert session.get('user') == 'john@simplylift.co'

    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200

    with client.session_transaction() as session:
        assert 'user' not in session
