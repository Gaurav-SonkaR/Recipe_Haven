from django.shortcuts import render
from vege.models import Receipe
# Create your views here.

def home(request):
    queryset = Receipe.objects.all()
    
    if request.GET.get('search_reciepe'):
        queryset = Receipe.objects.filter(receipe_name__icontains = request.GET.get('search_reciepe'))

    context = {'receipes': queryset}    
    return render(request,"index.html",context)

