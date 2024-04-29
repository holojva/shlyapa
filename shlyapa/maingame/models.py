from django.db import models
from django.contrib.auth.models import User
import random
from datetime import datetime
# Create your models here.
from django.urls import reverse

class Rooms(models.Model) :
    name = models.CharField(max_length=30)
    password = models.CharField(max_length=40)
    users = models.ManyToManyField(User)
    guessed_words_by_user = models.IntegerField(default=0, null=True)
    user_playing = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_playing", unique=False, null=True)
    started = models.BooleanField(default=False)
    admin_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_admin", unique=False, null=True)
    room_started_time = models.TimeField(null=True)
    play_sequence = models.CharField(null=True, max_length=200)
    def start_room(self) :
        self.started=True
    def end_room(self) :
        self.started=False
    def get_absolute_url(self):
        return reverse("room", kwargs={"pk": self.pk})
    def prepare_room(self) :
        self.start_room()
        users_playing = self.users.all()
        user_list = []
        for user in users_playing :
            user_list.append(user.username)
        random.shuffle(user_list)
        user_string = ",".join(user_list)
        print(users_playing)
        self.play_sequence = user_string
        self.room_started_time = datetime.now()
        self.user_playing = User.objects.get(username=user_list[0])
        self.save()

class Words(models.Model) :
    word = models.CharField(max_length=30)
    room = models.ForeignKey(Rooms, on_delete=models.CASCADE)
    guessed_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="created_by")
    used = models.BooleanField(default=False)
    def guessed_word(self) :
        self.used = True
class UpdatedUserModel(models.Model) :
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Rooms, null=True, on_delete=models.CASCADE)





