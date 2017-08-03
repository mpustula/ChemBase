from django.shortcuts import get_object_or_404,render
from django.http import HttpResponse
# Create your views here.
from .models import Compound

def index(request):
    return HttpResponse('Start: ChemnBase')
    
    
def detail(request,cmpd_id):
    compound=get_object_or_404(Compound,pk=cmpd_id)

    return render(request,'chembase/detail.html',{'compound':compound})
    
    
def add(request):
    pass


def search(request):
    pass
