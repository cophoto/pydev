from django.test import TestCase
from sign.models import Event, Guest
from django.contrib.auth.models import User

# Create your tests here.
class ModelTest(TestCase):
    def setUp(self):
        Event.objects.create(id=1, name="one plus event", status=True,
                             limit=1000, address="shenzhen", start_time="2018-1-1 09:00:00")
        Guest.objects.create(id=1, event_id=1, realname="alen", phone="18888888888", email="aaa@aaa.com", sign=False)

    def test_event_model(self):
        result = Event.objects.get(name="one plus event")
        self.assertEqual(result.address, "beijing")
        self.assertTrue(result.status)

    def test_guest_model(self):
        result = Guest.objects.get(phone="18888888888")
        self.assertEqual(result.realname, "alen")
        self.assertFalse(result.sign)

class IndexPageTest(TestCase):
    def test_index_page_render_index_template(self):
        response = self.client.get("/index/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")

class LoginActionTest(TestCase):
    def setUp(self):
        User.objects.create_user("admin", "admin@mail.com", "admin123")

    def test_add_admin(self):
        user = User.objects.get(username="admin")
        self.assertEqual(user.username, "admin")
        self.assertEqual(user.email, "admin@mail.com")

    def test_login_action_username_password_null(self):
        test_data = {"username":"", "password":""}
        response = self.client.post("/login_action/", data =test_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"username or password error!", response.content)

    def test_login_action_username_password_error(self):
        test_data = {"username": "aaa", "password": "bbb"}
        response = self.client.post("/login_action/", data=test_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"username or password error!", response.content)

    def test_login_action_success(self):
        test_data = {"username": "admin", "password": "admin123"}
        response = self.client.post("/login_action/", data=test_data)
        self.assertEqual(response.status_code, 302)
        self.assertIn(b"username or password error!", response.content)
