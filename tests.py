from unittest import TestCase
from server import app
from model import connect_to_db, db
from flask import session


class FlaskTestsBasic(TestCase):
    """Flask tests."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

        # connect_to_db(app)
        # db.create_all()


    def test_homepage_route(self):
        """ Test homepage """

        result = self.client.get("/")
        self.assertIn(b"Let Nature Be Nature", result.data)
    

    def test_plan_trip_route(self):
        """ Test plan-trip page/ route """

        result = self.client.get("/plan-trip")
        self.assertIn(b"Plan a trip!", result.data)

    
    def test_log_in_route(self):
        """ Test log in route """
    
        result = self.client.get("/login")
        self.assertIn(b"Log In", result.data)
    


class FlaskTestsLoggedIn(TestCase):
    """ Flask tests with user logged in to session."""

    def setUp(self):
        """Stuff to do before every test."""

        app.config['TESTING'] = True
        # app.config['SECRET_KEY'] = 'key'
        self.client = app.test_client()

        # connect_to_db(app)

        # Start each test with a user ID stored in the session.
        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_email'] = "user1@test.com"
        
        

    def test_user_profile_page(self):
        """Test user profile page """

        result = self.client.get("/users/1")
        self.assertIn(b"Favorites", result.data)
    


if __name__ == "__main__":
    import unittest

    connect_to_db(app)
    unittest.main()