from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from home.models import Setting, ContactFormMessage, ContactFormu
from place.models import Place, Category, Images


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
    context = {'place': place,
               'category': category,
               'images': images,
               #'slug': slug,
               }
    return render(request,'place_detail.html',context)
