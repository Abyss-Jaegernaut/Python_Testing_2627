from locust import HttpUser, task, between


class SecretaryUser(HttpUser):
    wait_time = between(1, 2)

    def on_start(self):
        """Initialisation : connexion au début de session."""
        self.client.post("/showSummary", data={"email": "john@simplylift.co"})

    @task(3)
    def view_index(self):
        """Chargement de la page d'accueil."""
        self.client.get("/")

    @task(3)
    def view_points_display(self):
        """Consultation publique du tableau des points des clubs."""
        self.client.get("/pointsDisplay")

    @task(2)
    def view_booking_page(self):
        """Accès au formulaire de réservation d'une compétition."""
        self.client.get("/book/Spring Festival/Simply Lift")

    @task(1)
    def purchase_places(self):
        """Mise à jour : réservation de places (doit être < 2s)."""
        self.client.post("/purchasePlaces", data={
            "club": "Simply Lift",
            "competition": "Spring Festival",
            "places": "1"
        })

    @task(1)
    def login_and_logout(self):
        """Cycle complet de connexion et déconnexion."""
        self.client.get("/logout")
        self.client.post("/showSummary", data={"email": "admin@irontemple.com"})
