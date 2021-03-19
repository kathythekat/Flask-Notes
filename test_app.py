from unittest import TestCase

from app import app
from models import db, connect_db, User, Note

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///notes_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

db.drop_all()
db.create_all()

USER_DATA = {
    "username": "testuser",
    "password": "password",
    "email": "user@gmail.com",
    "first_name": "test",
    "last_name": "test"
}

class UserTest(TestCase):
    """Tests for users."""

    def setUp(self):
        """Make demo data."""
        User.query.delete()

        # "**" means "pass this dictionary as individual named params"
        user = User(**USER_DATA)
        db.session.add(user)
        db.session.commit()

        self.user = user

    def tearDown(self):
        """Clean up fouled transactions."""

        db.session.rollback()

    def test_invalid_username_url(self):
        with app.test_client() as client:
            url = "/users/invalid_username"

            response = client.get(url)

            self.assertEqual(response.status_code, 404)
  
    def test_invalid_url(self):
        with app.test_client() as client:
            url = "/user"

            response = client.get(url)

            self.assertEqual(response.status_code, 404)

    def test_register_page(self):
      """Make sure register page shows up correctly."""
      with app.test_client() as client:
        response = client.get('/register')
        html = response.get_data(as_text=True)
        self.assertIn('<button type="submit">Register</button>', html)
    
    def test_show_user_info(self):
        with app.test_client() as client:
            url = f"users/{self.user.username}"
            resp = client.get(url)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)

            data = USER_DATA

            self.assertEqual(data, {
                "username": "testuser",
                "password": "password",
                "email": "user@gmail.com",
                "first_name": "test",
                "last_name": "test"     
            })
            self.assertIn('<p>Username: testuser</p>', html)

    