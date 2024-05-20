"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from maingame.views import (
    index, 
    room, 
    game, 
    finals, 
    register, 
    login, 
    logout, 
    room_form, 
    word_form, 
    card_teleport,
    room_edit_form,
    delete_room,
    delete_room_permanently,
    delete_word_permanently
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", index),
    path("rooms/<int:pk>/", room, name="room"),
    path("rooms/<int:pk>/edit/", room_edit_form, name="room_edit"),
    path("rooms/<int:room_index>/card/<int:word_index>/", game, name="card"),
    path("rooms/<int:pk>/card/", card_teleport, name="card_tp"),
    path("rooms/<int:pk>/finals/", finals, name="finals"),
    path("rooms/<int:pk>/newword/", word_form, name="newword"),
    path("register/", register, name="register"),
    path("login/", login, name="login"),
    path("logout/", logout, name="logout"),
    path("rooms/create/", room_form, name="newroom"),
    path("rooms/<int:pk>/delete_room/", delete_room, name="delete_room"),
    path("rooms/<int:pk>/delete_permanently/", delete_room_permanently, name="permanently_delete_room"),
    path("rooms/create/", room_form, name="newroom"),
    path("delete_word/<int:pk>/", delete_word_permanently)
]
