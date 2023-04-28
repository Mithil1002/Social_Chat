from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import *
from .forms import RoomForm, RegisterForm
from django.views.decorators.cache import cache_control


# Create your views here.
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def userlogin(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('Home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')
        print(username, password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('Home')
        else:
            messages.error(request, 'Username or password does not match')

    context = {'page': page}
    return render(request, 'baseapp/register.html', context)


def registeruser(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('Home')
        else:
            messages.error(request, 'an error occured during registration')

    return render(request, 'baseapp/register.html', {'form': form})


def userlogout(request):
    logout(request)
    return redirect('Home')


def home(request):
    q = request.GET.get('q') if request.GET.get('q') is not None else ''
    rooms = Room.objects.filter(Q(topic__name__icontains=q) |
                                Q(name__icontains=q)
                                # Q(description__icontains=q)
                                # Q(host__username__icontains=q)
                                )

    topics = Topic.objects.all()
    all_msg = Message.objects.filter(Q(room__topic__name__icontains=q))
    context = {'rooms': rooms, 'topics': topics, 'all_msg': all_msg}
    return render(request, 'baseapp/home.html', context)


def room(request, pk):
    rooms = Room.objects.get(id=pk)
    room_message = rooms.message_set.all().order_by('-created')
    participants = rooms.participants.all()
    if request.method == "POST":
        message = Message.objects.create(
            user=request.user,
            room=rooms,
            body=request.POST.get('body')
        )
        rooms.participants.add(request.user)
        print(request.user)
        return redirect('Room', pk=rooms.id)
    context = {'Room': rooms, 'room_message': room_message, 'participants': participants}

    return render(request, 'baseapp/room.html', context)


def userprofile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    all_msg = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'rooms': rooms,
               'all_msg': all_msg, 'topics': topics}
    return render(request, 'baseapp/profile.html', context)


@login_required(login_url='/login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def create(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host = request.user,
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description')

        )
        return redirect('Home')

    context = {'form': form, 'topics': topics}
    return render(request, 'baseapp/form_r.html', context)


@login_required(login_url='login')
def update(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse('You cannot edit this room')

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('Home')
    context = {'form': form}
    return render(request, 'baseapp/form_r.html', context)


@login_required
def delete(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect("Home")
    return render(request, 'baseapp/delete.html', {'object': room})


@login_required
def delete_message(request, pk):
    message = Message.objects.get(id=pk)
    room = message.room
    if request.user != message.user:
        return HttpResponse('you are not allowed ')
    if request.method == 'POST':
        message.delete()
        return redirect('Room', pk=room.id)
    else:
        return render(request, 'baseapp/delete.html', {'object': message})
