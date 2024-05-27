from django.db import models
from django.contrib.auth.models import User
import random
from datetime import datetime
from django.utils import timezone

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
    room_started_time = models.DateTimeField(null=True)
    play_sequence = models.CharField(null=True, max_length=200)
    minutes_for_player = models.CharField(default="1:00", max_length=5)

    def __str__(self) :
        return self.name
    

    def time_convert(self) :
        split_list = self.minutes_for_player.split(":")
        whole_sec = int(split_list[0])*60+int(split_list[1])
        return whole_sec
    

    def start_room(self) :
        self.started=True


    def end_room(self) :
        self.started=False


    def get_absolute_url(self):
        return reverse("room", kwargs={"pk": self.pk})
    

    def prepare_room(self) :
        self.start_room()
        users_playing = [objekt.user for objekt in UpdatedUserModel.objects.filter(room=self)]
        user_list = []
        for user in users_playing :
            user_list.append(user.username)
        random.shuffle(user_list)
        user_string = ",".join(user_list)
        self.play_sequence = user_string
        self.room_started_time = timezone.now()
        self.user_playing = User.objects.get(username=user_list[0])
        self.save()


    def get_sequence(self) :
        user_list = self.play_sequence.split(",")
        return user_list
    

    def get_time_from_start(self) :
        time_started = self.room_started_time
        time_now = timezone.now()
        time_from_start = time_now - time_started
        return time_from_start
    

    def get_seconds_from_start(self) :
        time_from_start = self.get_time_from_start()
        whole_sec = time_from_start.total_seconds()
        return whole_sec
    

    def get_player_index(self) :
        time_from_start = self.get_seconds_from_start()
        time_seconds = self.time_convert()
        player_index = (time_from_start - (time_from_start % time_seconds)) / time_seconds
        print(player_index)
        return int(player_index)
    

    def update_player(self) :
        player_index = self.get_player_index()
        player_sequence = self.get_sequence()
        current_player_name = player_sequence[player_index % len(UpdatedUserModel.objects.filter(room=self))]
        current_player = User.objects.get(username=current_player_name)
        if self.user_playing != current_player :
            for word in Words.objects.filter(wasted=True) :
                word.wasted = False
                word.save()
        self.user_playing = current_player


    def get_time_left(self) :
        time_from_round_start = self.get_seconds_from_start() % self.time_convert()
        time_left = self.time_convert() - time_from_round_start
        return int(time_left)
    

class Words(models.Model) :
    word = models.CharField(max_length=30)
    room = models.ForeignKey(Rooms, on_delete=models.CASCADE)
    guessed_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="created_by")
    used = models.BooleanField(default=False)
    wasted = models.BooleanField(default=False)
    def guessed_word(self, user) :
        self.used = True
        self.guessed_by = user
    def wasted_word(self) :
        self.wasted = True
        self.guessed_by = None
    def restart(self) :
        self.used = False
        self.wasted = False
        self.guessed_by = None
class UpdatedUserModel(models.Model) :
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Rooms, null=True, on_delete=models.CASCADE)





