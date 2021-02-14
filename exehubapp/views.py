from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def index(request):
    return render(request, 'index.html')

@csrf_exempt
def addEvent(request):
    return render(request, 'addevent.html')

def viewEvents(request):
    return render(request, 'events.html')