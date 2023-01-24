import sqlite3
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Message
from django.utils import timezone
from django.db.models import Q
from pathlib import Path

#Fix to flaw 3: importing logging and creating a logger
'''import logging
logger = logging.getLogger(__name__)'''


def createView(request):
    
    u = request.POST.get('username')
    p = request.POST.get('password')
    
    newuser = User.objects.create_user(username = u, password = p)
    
    return redirect('/')

#Fix to flaw 4: Checking if the password is strong enough and username is not taken
'''def createView(request):
    
    u = request.POST.get('username')
    p = request.POST.get('password')

    if len(p) < 8 or not any(char.isdigit() for char in p) or not any(char.isalpha() for char in p) or not any(not char.isalnum() for char in p):
        return HttpResponse("Password not strong enough!")
    elif User.objects.filter(username=u).exists():
        return HttpResponse("Username already taken!")

    newuser = User.objects.create_user(username = u, password = p)
    
    return redirect('/')'''

@login_required
def index(request):
    
    #Fix to flaw 3: logging users logging in
    '''logger.info("User %s logged in" % (request.user,))'''

    users = User.objects.all().exclude(username=request.user)
    
    return render(request, 'message/index.html', {'users': users})


@login_required
def messagesView(request, other):
    
    otheruser = User.objects.get(username=other)

    messages = Message.objects.filter((Q(receiver=request.user) & Q(sender=otheruser)) | (Q(receiver=otheruser) & Q(sender=request.user)))
    current_user = User.objects.get(username=request.user)
    
    return render(request, 'message/messages.html', {'messages': messages, 'current_user': current_user, 'other': other})

#Fix to flaws 4, 5: Code needed to allow fix to flaw 4 to work (4) and using try/except to not give revealing errors to users (5)
'''@login_required
def messagesView(request):
    
    try:
        other = request.POST.get('other')

        if not User.objects.filter(username=other).exists():
            return HttpResponse("User does not exist!")
        
        if other == request.user:
            return HttpResponse("You cannot message yourself!")
        
        otheruser = User.objects.get(username=other)

        messages = Message.objects.filter((Q(receiver=request.user) & Q(sender=otheruser)) | (Q(receiver=otheruser) & Q(sender=request.user)))
        current_user = User.objects.get(username=request.user)
        
        return render(request, 'message/messages.html', {'messages': messages, 'current_user': current_user, 'other': other})
    except:

        #Fix to flaw 3: warning that someone tried to access messages in an invalid way
        logger.warning("User %s tried to access messages in an invalid way" % (request.user,))

        return redirect('/')'''


@login_required
def sendMessageView(request):
    
    receiver = User.objects.get(username=request.POST.get('receiver'))
    sender = User.objects.get(username=request.POST.get('sender'))
    message = request.POST.get('message')
    time = timezone.now()
    newmessage = Message.objects.create(receiver=receiver, sender=sender, date_sent = time, text=message)

    return redirect('/messages/' + receiver.username)

#Fix to flaws 5, 1: Using try/except to not give revealing errors to users, and checking if the sender of the message is the logged in user.
'''@login_required
def sendMessageView(request):
    
    try:
        receiver = User.objects.get(username=request.POST.get('receiver'))
        sender = User.objects.get(username=request.POST.get('sender'))
        message = request.POST.get('message')
        time = timezone.now()

        if sender != request.user:
            return HttpResponse("You cannot send a message as someone else!")

        newmessage = Message.objects.create(receiver=receiver, sender=sender, date_sent = time, text=message)

        return redirect('/messages/' + receiver.username)
    except:
        
        #Fix to flaw 3: warning that someone tried to send a message in an invalid way
        logger.warning("User %s tried to send a message in an invalid way" % (request.user,))

        return redirect('/')'''



@login_required
def deleteMessageView(request, messageid):
    
    connection = sqlite3.connect(Path(__file__).resolve().parent.parent / "db.sqlite3")
    cursor = connection.cursor()
    cursor.execute("DELETE FROM message_message WHERE id = %s;" % (messageid,))
    connection.commit()
    connection.close()
    
    other = request.POST.get('other')
    
    return redirect('/messages/' + other)

#Fix to flaws 2, 1: Using Django's ORM to delete the message instead of SQL to prevent SQL injection and checking if the logged in user is the sender of the message to be deleted.
'''@login_required
def deleteMessageView(request, messageid):
    if request.method == 'POST':
        
        if request.user == Message.objects.get(id=messageid).sender:
            Message.objects.get(id=messageid).delete()
        
        other = request.POST.get('other')
        
        return redirect('/messages/' + other)
        
    return redirect('/')'''
