from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from sign.models import Event, Guest
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.

def index(request):
   return render(request, "index.html")

def login_action(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        # if username == 'admin' and password == 'adminadmin':
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            response = HttpResponseRedirect('/event_manager/')
            # response.set_cookie('user',username, 3600)
            request.session['user'] = username
            request.session['password'] = password
            return response
        else:
            return render(request, 'index.html', {'error': 'username or password error!'})

@login_required
def event_manager(request):
    #username = request.COOKIES.get('user', '')
    event_list = Event.objects.all()
    username = request.session.get('user','')
    return render(request, 'event_manager.html', {"user": username, "events": event_list})

@login_required
def search_name(request):
    username = request.session.get('user', '')
    search_name =request.GET.get("name", "")
    event_list = Event.objects.filter(name__contains=search_name)
    return render(request, "event_manager.html", {"user": username, "events": event_list})

@login_required
def guest_manager(request):
    username = request.session.get('user', '')
    guest_list = Guest.objects.order_by('id')
    paginator = Paginator(guest_list, 2)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    return render(request, "guest_manager.html", {"user": username, "guests": contacts})

@login_required
def sign_index(request, eid):
    events = get_object_or_404(Event, id=eid)
    return render(request, 'sign_index.html', {"event": events})

@login_required
def sign_index_action(request, eid):
    events = get_object_or_404(Event, id=eid)
    phone = request.POST.get("phone", "")
    print(phone)
    result = Guest.objects.filter(phone=phone)
    if not result:
        return render(request, 'sign_index.html', {"event": events, "hint": "phone error"})
    result = Guest.objects.filter(phone=phone, event_id=eid)
    if not result:
        return render(request, 'sign_index.html', {"event": events, "hint": "phone or event id error"})
    result = Guest.objects.get(phone=phone, event_id=eid)
    if result.sign:
        return render(request, 'sign_index.html', {"event": events, "hint": "user has signed in"})
    else:
        Guest.objects.filter(phone=phone, event_id=eid).update(sign="1")
        return render(request, "sign_index.html", {"event": events, "hint": "sign in success", "guest": result})

@login_required
def logout(request):
    auth.logout(request)
    response = HttpResponseRedirect("/index/")
    return response

