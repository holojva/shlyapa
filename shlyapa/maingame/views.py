from django.shortcuts import render, redirect
from .models import Rooms, Words, UpdatedUserModel
from random import shuffle
from .tasks import todo_notification
from .forms import LoginForm, RegisterForm, RoomForm, WordForm
from django.contrib.auth.models import User
from django.contrib.auth import logout as logout_function, login as login_function, authenticate
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from datetime import datetime
import random
def admin_decorator(view_function) :
    def wrapper(*args, **kwargs) :
        model_entity=Rooms.objects.get(id=kwargs["room_index"])
        if model_entity.admin_user == args[0].user :
            print("I AM THE ADMIN")
        return view_function(*args, **kwargs)
    return wrapper
    
@login_required(login_url='/login/')
def index(request) :
    Rooms.objects.filter()
    upd_user = get_object_or_404(UpdatedUserModel, user=request.user.id)
    upd_user.room = None
    upd_user.save()
    print(request.user)
    return render(request, "index.html", context={"rooms":Rooms.objects.filter(started=False)})

@login_required(login_url='/login/')
def room(request, pk) :
    model_entity = Rooms.objects.get(id=pk)
    upd_user = UpdatedUserModel.objects.get(user=request.user)

    if request.user == model_entity.admin_user :
        model_entity.end_room()
        model_entity.save()

    upd_user.room = model_entity
    upd_user.save()
    list_of_words = [i for i in Words.objects.filter(room=model_entity)]
    print(list_of_words)
    shuffle(list_of_words)
    print(list_of_words)

    if request.user == model_entity.admin_user :
        for i in list_of_words :
            i.used=False
            i.save()
            print(i.used, i.word)

    return render(request, "room.html", context={
        "words":Words.objects.filter(room=model_entity), 
        "users":UpdatedUserModel.objects.filter(room=model_entity)})
@admin_decorator
@login_required(login_url='/login/')
def game(request, room_index, word_index) :
    
    print(request.user)
    model_entity = Rooms.objects.get(id=room_index)
    model_entity.get_player_index
    
    if request.user == model_entity.admin_user and not model_entity.started :
        model_entity.prepare_room()
    model_entity.update_player()
    if model_entity.started :
        list_of_words = [word for word in Words.objects.filter(room=model_entity, used=False, wasted=False)]
        shuffle(list_of_words)
        print(model_entity.get_time_from_start())
        if request.method == "POST":
            is_completed = request.POST["action"]

            if is_completed :
                word_model = Words.objects.get(id=word_index)
                
                if is_completed == "Объяснил" : 
                    word_model.guessed_word(user=request.user)
                else :
                    word_model.wasted_word()
                word_model.save()

                if len(list(list_of_words)) < 1 :
                    return redirect(reverse("finals", args=[room_index]))#redirect("/rooms/"+str(room_index)+"/finals/")
                
                if request.user == model_entity.user_playing :
                    return redirect(reverse("card_tp", args=[room_index]))

        model_entity.save()
        return render(request, "cards.html", context={
            "word":Words.objects.get(id=word_index).word, 
            "room_object":Rooms.objects.get(id=room_index),
            "time_from_start":model_entity.get_seconds_from_start, 
            "player_index":model_entity.get_player_index, 
            "time_left":model_entity.get_time_left, 
            "room_index":room_index
        })
    else :
        return redirect("/rooms/"+str(room_index))

def card_teleport(request, pk) :
    list_of_words = [i for i in Words.objects.filter(room=Rooms.objects.get(id=pk), used=False, wasted=False)]
    shuffle(list_of_words)

    if len(list(list_of_words)) < 1 :
        return redirect(reverse("finals", args=[pk]))
    
    return redirect(reverse("card", args=[pk, list_of_words[0].id])) #redirect("/rooms/"+str(pk)+"/card/"+str(list_of_words[0].id))


def finals(request, pk) :
    list_of_words = [i for i in Words.objects.filter(room=Rooms.objects.get(id=pk))]
    return render(request, "finals.html", context={"words": list_of_words, "pk":pk})


def login(request) :
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST["username"]
            password = request.POST["password"]

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login_function(request,user)
            return redirect("/")

    else:
        form = LoginForm()

    return render(request, "login.html", context={"form":LoginForm})


def register(request) :
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=request.POST["username"], 
                password=request.POST["password"]
            )
            UpdatedUserModel.objects.create(user=user)
            return redirect(reverse("index"))
    else:
        form = RegisterForm()
    return render(request, "register.html", context={"form":RegisterForm})


def logout(request) :
    logout_function(request)
    return redirect(reverse("index"))


@login_required(login_url='/login/')
def room_form(request) :
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            room = Rooms.objects.create(
                name=request.POST["name"],
                password="password", admin_user=request.user, 
                user_playing=request.user, 
                minutes_for_player=request.POST["time"]
            )
            print(room.id)
        return redirect(reverse("room", args=[room.id]))
    else:
        form = RoomForm()
    return render(request, "login.html", context={"form":RoomForm})


@login_required(login_url='/login/')
def room_edit_form(request, pk) :
    room = Rooms.objects.get(id=pk)
    if request.method == "POST":

        form = RoomForm(request.POST)
        if form.is_valid():

            room.name=request.POST["name"]
            room.save()
            print(room.id)

        return redirect(reverse("room", args=[room.id]))
    
    else:
        form = RoomForm({"name":room.name})
    return render(request, "login.html", context={"form":RoomForm})


@login_required(login_url='/login/')
def word_form(request, pk) :
    if request.method == "POST":
    # create a form instance and populate it with data from the request:
        form = WordForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            room = Words.objects.create(
                word=request.POST["word"], 
                room=Rooms.objects.get(id=pk), 
                created_by=request.user
                )
            print(room.id)
        return redirect("/rooms/"+str(pk))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = WordForm()
    return render(request, "login.html", context={"form":WordForm})
def delete_room(request, pk) :
    # TODO make this a POST request
    return render(request, "delete_room.html", context={"pk":pk})


def delete_room_permanently(request, pk) :
    # TODO make this a POST request
    model = Rooms.objects.get(id=pk)
    model.delete()

    return redirect("/")
    
def delete_word(request, pk) :
    # TODO make this a POST request

    return render(request, "delete_word.html", context={"pk":pk})


def delete_word_permanently(request, pk) :
    model_entity = Words.objects.get(id=pk)
    room_pk = model_entity.room.id
    if model_entity.created_by == request.user or model_entity.created_by == None :
        model_entity.delete()
        return redirect(reverse("room", args=[room_pk]))#redirect(f'/rooms/{room_pk}')
    else :
        return redirect("/")
def test(text) :
    print(text)