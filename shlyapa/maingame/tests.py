from django.test import TestCase
from django.test import Client
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from .models import Rooms
# Create your tests here.
from bs4 import BeautifulSoup
from .views import room
class RoomTestCase(TestCase) :

    def setUp(self) :
        from .models import UpdatedUserModel
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.room = Rooms.objects.create(name="room", password="password")
        self.updated_user = UpdatedUserModel.objects.create(user=self.user, room=self.room)


    def test_create(self) :
        c = Client()
        logged_in = c.login(username="testuser", password="12345")
        response = c.post(reverse("newroom"), {"name": "test"})
        test_room = Rooms.objects.get(name="test")
        self.assertEqual(test_room.name, "test")
        self.assertEqual(test_room.password, "password")


    def test_read(self) :
        c = Client()
        logged_in = c.login(username="testuser", password="12345")
        response = c.get(reverse("room", args=[self.room.id]), {"name": "test"})
        self.assertEqual(response.status_code, 200)


    def test_edit(self) :
        c = Client()
        logged_in = c.login(username="testuser", password="12345")
        test_room = Rooms.objects.get(name="room")
        test_room.password = "password2"
        test_room.save()
    

    def test_connect_to_room(self) :
        c = Client()
        logged_in = c.login(username="testuser", password="12345")
        room_url = reverse("room", args=[self.room.id])
        self.assertEquals(resolve(room_url).func, room)

        response = c.get(room_url)
        self.assertTemplateUsed(response, "room.html")
        soup = BeautifulSoup(response.content, "html.parser")
        
        user_name = soup.find("tr", {"class": "usernames"}).text
        self.assertEqual("testuser", user_name.strip())