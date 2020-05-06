import json

from django.contrib.auth import logout, login, authenticate
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from home.forms import SearchForm, SignUpForm
from home.models import Setting, ContactFormMessage, ContactFormu
from place.models import Place, Category, Images, Comment


def index(request):
    setting = Setting.objects.get(pk=1)
    sliderdata = Place.objects.all()[:4]
    category=Category.objects.all()
    randomplaces = Place.objects.all().order_by('?')[:6]


    context = {'setting': setting,
               'category': category,
               'page': 'home',
               'sliderdata': sliderdata,
               'randomplaces': randomplaces}
    return render(request, 'index.html', context)


def hakkimizda(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    context = {'setting': setting, 'page': 'hakkimizda', 'category': category}
    return render(request, 'hakkimizda.html', context)


def referanslar(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    context = {'setting': setting, 'page': 'referanslar', 'category': category}
    return render(request, 'referanslar.html', context)


def contact(request):

    if request.method == 'POST':  # form post edildiyse
        form = ContactFormu(request.POST)
        if form.is_valid():
            data = ContactFormMessage()  # model ile bağlantı kur
            data.name = form.cleaned_data['name']  # formdan bilgiyi al
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()  # veritabanına kaydet
            messages.success(request, "Mesajınız başarı ile gönderilmiştir. Teşekkür ederiz.")
            return HttpResponseRedirect('/contact')

    setting = Setting.objects.get(pk=1)
    form = ContactFormu()
    category = Category.objects.all()
    context = {'setting': setting, 'form': form, 'category': category}
    return render(request, 'contact.html', context)


def category_places(request, id, slug):
    category = Category.objects.all()
    categorydata = Category.objects.get(pk=id)
    places = Place.objects.filter(category_id=id)
    context = {'places': places,
               'category': category,
               'slug': slug,
               'categorydata': categorydata
               }
    return render(request,'places.html',context)

def place_detail(request,id,slug):
    category = Category.objects.all()
    place = Place.objects.get(pk=id)
    images = Images.objects.filter(place_id=id)
    comments= Comment.objects.filter(place_id=id,status='True')
    context = {'place': place,
               'category': category,
               'images': images,
               'comments': comments,
               }
    return render(request,'place_detail.html',context)

def place_search(request):
    if request.method == 'POST': # check form post
        form = SearchForm(request.POST)
        if form.is_valid():
            category = Category.objects.all()

            query = form.cleaned_data['query'] # get form data
            catid = form.cleaned_data['catid'] # get form data
            # retun HttpResponse(catid)
            if catid == 0:
                places = Place.objects.filter(title__icontains=query) #Select * from place where title like % query %
            else:
                places = Place.objects.filter(title__icontains=query, category_id=catid)

            # retun HttpResponse(place)
            context = {'places': places,
                       'category': category,
                       }
            return  render(request, 'places_search.html', context)

        return HttpResponseRedirect('/')


def place_search_auto(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        place = Place.objects.filter(city__icontains=q)
        results = []
        for rs in place:
            place_json = {}
            place_json = rs.title
            results.append(place_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # redirect to succes page
            return HttpResponseRedirect('/')
        else:
            messages.error(request, "Login hatası ! Kullanıcı adı veya şifre hatalı")
            return HttpResponseRedirect('/login')

    category = Category.objects.all()
    context = {'category': category,
               }
    return render(request, 'login.html', context)

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return HttpResponseRedirect('/')

    form = SignUpForm()
    category = Category.objects.all()
    context = {'category': category,
               'form': form,
               }
    return render(request, 'signup.html', context)
