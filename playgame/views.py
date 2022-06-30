
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib import messages
from .models import rom, topic,message,coursename,coursedetails
from django.db.models import Q
from .forms import modelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.clickjacking import xframe_options_exempt
# rooms = [
#     {'id':1,'name':'lets learn python'},
#     {'id':2,'name':'design with me'},
#     {'id':3,'name':'frontend'}

# ]


def showcourses(request):
    details=coursename.objects.all()
    return render(request,'playgame/course.html',{'data':details})

@xframe_options_exempt
def details(request,courses_id):
    display_course=coursename.objects.get(id=courses_id)
    return render(request,'playgame/coursed.html',{'display':display_course})

def vp(request):
    product=request.GET.get('prod_id')
    print(product)
    a=coursedetails.objects.all()
    return render(request,'playgame/vp.html',{'a':a})
    
def loginpage(request):
    page= 'login'
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'uusername not valid 404')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'username or password not correct')

    context = {'page':page}
    return render(request, 'playgame/register.html', context)

def registeruser(request):
    
    form = UserCreationForm
    if request.method=='POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username=user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'error')
            
    return render(request,'playgame/register.html',{'form':form})

def logoutpage(request):
    logout(request)
    return redirect('home')



def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = rom.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    topics = topic.objects.all()
    room_count = rooms.count()
    room_messages=message.objects.filter(Q(room__topic__name__icontains=q))
    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count ,'room_messages':room_messages}
    return render(request, 'playgame/home.html', context)


def room(request, pk):
    room = rom.objects.get(id=pk)
    room_messages= room.message_set.all().order_by('-created')
    participants = room.participants.all()

    if request.method =='POST':
        messag = message.objects.create(
            user= request.user,
            room= room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room',pk=room.id)
        
    context = {'room': room,'room_messages':room_messages,'participants':participants}
    return render(request, 'playgame/room.html', context)

def userprofile(request,pk):
    user = User.objects.get(id=pk)
   # rooms= user.room_set.all()
    room_message= user.message_set.all()
    topics=topic.objects.all()
    context={'user':user,'room_message':room_message}
    return render(request,'playgame/profile.html',context)

@login_required(login_url='/login')
def createroom(request):

    form = modelForm
    if request.method == 'POST':
        form = modelForm(request.POST)
        if form.is_valid():
            room=form.save(commit=False)
            room.host=request.user
            room.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'playgame/form.html', context)

@login_required(login_url='/login')
def updateroom(request, pk):
    room = rom.objects.get(id=pk)
    form = modelForm(instance=room)
    if request.user != room.host:
        return HttpResponse('fk of get away from here mf')
    
    if request.method == 'POST':
        form = modelForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'playgame/form.html', context)

@login_required(login_url='/login')
def deleteroom(request, pk):
    room = message.objects.get(id=pk)
    
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'playgame/delete.html', {'obj': room})

@login_required(login_url='/login')
def deletemessage(request, pk):
    messag = message.objects.get(id=pk)
    if request.user != messag.user:
        return HttpResponse('fk of get away from here mf')
    if request.method == 'POST':
        messag.delete()
        return redirect('home')
    return render(request, 'playgame/delete.html', {'obj': messag})
