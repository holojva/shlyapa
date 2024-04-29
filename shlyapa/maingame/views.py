from django.shortcuts import render, redirect
from .models import Rooms, Words, UpdatedUserModel
from random import shuffle
from .tasks import todo_notification
from .forms import LoginForm, RegisterForm, RoomForm, WordForm
from django.contrib.auth.models import User
from django.contrib.auth import logout as logout_function, login as login_function, authenticate
# from .tasks import add
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from datetime import datetime
#Create your views here.
import random

@login_required(login_url='/login/')
def index(request) :
    Rooms.objects.filter()
    upd_user = get_object_or_404(UpdatedUserModel, user=request.user.id)
    upd_user.room = None
    upd_user.save()
    print(request.user)
    # add.delay(2, 2)
    return render(request, "index.html", context={"rooms":Rooms.objects.filter(started=False)})

@login_required(login_url='/login/')
def room(request, pk) :
    model_entity = Rooms.objects.get(id=pk)
    upd_user = UpdatedUserModel.objects.get(user=request.user)
    #Rooms.users.add(request.user)

    if request.user == model_entity.admin_user :
        model_entity.end_room()
        model_entity.save()

    if not model_entity.started :
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
    
    else:
        return render(request, "waiting_screen.html")
    
@login_required(login_url='/login/')
def game(request, pk, pk2) :
    print(request.user)
    model_entity = Rooms.objects.get(id=pk)
    print(model_entity.users)

    if request.user == model_entity.admin_user :
        model_entity.prepare_room()
        

    if model_entity.started :
        list_of_words = [i for i in Words.objects.filter(room=model_entity, used=False)]
        shuffle(list_of_words)

        if request.method == "POST":
            print(request.POST)
            is_completed = request.POST["action"]

            if is_completed :
                word_model = Words.objects.get(id=pk2)
                word_model.guessed_word()

                if is_completed == "Объяснил" :
                    word_model.guessed_by = request.user

                else :
                    word_model.guessed_by = None

                word_model.save()
                list_of_words = [i for i in Words.objects.filter(room=model_entity, used=False)]
                shuffle(list_of_words)
                print(list_of_words)

                if len(list(list_of_words)) < 1 :
                    return redirect("/rooms/"+str(pk)+"/finals/")
                
                if request.user == model_entity.user_playing :
                    return redirect("/rooms/"+str(pk)+"/card/")
                
        if model_entity.started == False :
            redirect("/rooms/"+str(pk))

        model_entity.save()

        return render(request, "cards.html", context={"word":Words.objects.get(id=pk2).word, "user_playing":Rooms.objects.get(id=pk).user_playing})


def card_teleport(request, pk) :
    list_of_words = [i for i in Words.objects.filter(room=Rooms.objects.get(id=pk), used=False)]
    shuffle(list_of_words)

    if len(list(list_of_words)) < 1 :
        return redirect("/rooms/"+str(pk)+"/finals/")
    
    return redirect("/rooms/"+str(pk)+"/card/"+str(list_of_words[0].id))


def finals(request, pk) :
    list_of_words = [i for i in Words.objects.filter(room=Rooms.objects.get(id=pk))]
    return render(request, "finals.html", context={"words": list_of_words, "pk":pk})


def login(request) :
    if request.method == "POST":
    # create a form instance and populate it with data from the request:
        form = LoginForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            username = request.POST["username"]
            password = request.POST["password"]

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login_function(request,user)
            return redirect("/")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = LoginForm()

    return render(request, "login.html", context={"form":LoginForm})


def register(request) :
    if request.method == "POST":
    # create a form instance and populate it with data from the request:
        form = RegisterForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            user = User.objects.create_user(request.POST["username"], "test@test.com", request.POST["password"])
            updated_user = UpdatedUserModel.objects.create(user=user, room=None)
            return redirect("/")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = RegisterForm()
    return render(request, "register.html", context={"form":RegisterForm})


def logout(request) :
    logout_function(request)
    return redirect("/")


@login_required(login_url='/login/')
def room_form(request) :
    if request.method == "POST":
    # create a form instance and populate it with data from the request:
        form = RoomForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            # task = .apply_async(countdown=2)
            # print(task.get())
            room = Rooms.objects.create(name=request.POST["name"],password="password", admin_user=request.user, user_playing=request.user)
            print(room.id)
        return redirect("/rooms/"+str(room.id))

    # if a GET (or any other method) we'll create a blank form
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

        return redirect("/rooms/"+str(room.id))
    
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
            room = Words.objects.create(word=request.POST["word"], room=Rooms.objects.get(id=pk), created_by=request.user)
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
        return redirect(f'/rooms/{room_pk}')
    else :
        return redirect("/")
def test(text) :
    print(text)