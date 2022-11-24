from django.shortcuts import render

# Create your views here.


def index(request):
    context = {
        'title': 'ElectroLib',
        'text':'Main Page'
    }
    return render(request, 'main/index.html', context)

def faq(request):
    context = {
        'title': 'Помощь',
        'text':'FAQs Page'
    }
    return render(request, 'main/faq.html', context)

def about(request):
    context = {
        'title': 'О проекте ElectroLib',
        'text':'About Page'
    }
    return render(request, 'main/about.html', context)
