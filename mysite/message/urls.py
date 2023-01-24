from django.urls import path

from .views import index, messagesView, sendMessageView, deleteMessageView, createView

urlpatterns = [
    path('', index, name='index'),
    path("messages/<str:other>", messagesView, name = "messages"),
    #path("messages/", messagesView, name = "messages"),
    path("deleteMessage/<messageid>", deleteMessageView, name = "deletemessage"),
    #path("deleteMessage/", deleteMessageView, name = "deletemessage"),
    path("sendMessage/", sendMessageView, name = "sendmessage"),
    path("createUser/", createView, name = "createuser"),

]