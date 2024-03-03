import unittest
from flask_testing import TestCase
from flask import url_for
from website import create_app, db
from website.models import User


class TestAuth(TestCase):

    def create_app(self):
        app = create_app()
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        return app

    def setUp(self):
        db.create_all()
        user = User(email="test@example.com", first_name="Test", password="testpassword")
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_login(self):
        response = self.client.post(url_for('auth.login'),
                                    data=dict(email='test@example.com', password='testpassword'),
                                    follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        self.client.post(url_for('auth.login'),
                         data=dict(email='test@example.com', password='testpassword'),
                         follow_redirects=True)
        response = self.client.get(
            url_for('auth.logout'),
            follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_sign_up(self):
        response = self.client.post(url_for('auth.sign_up'),
                                    data=dict(email='newuser@example.com',
                                    firstName='New',
                                    password1='newpassword',
                                    password2='newpassword'),
                                    follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    if __name__ == '__main__':
        unittest.main()
