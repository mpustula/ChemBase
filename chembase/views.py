from django.shortcuts import get_object_or_404,render
from django.http import HttpResponse
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
from .models import Compound
from .forms import SearchForm

def index(request):
    return HttpResponse('Start: ChemnBase')
    
    
def detail(request,cmpd_id):
    compound=get_object_or_404(Compound,pk=cmpd_id)
    existing_items=compound.item_set(manager='citems').existing()
    deleted_items=compound.item_set(manager='citems').deleted()

    return render(request,'chembase/detail.html',{'compound':compound,'exist':existing_items,'del':deleted_items})
    
    
def add(request):
    pass


def search(request):
    if request.method=='GET':
        form=SearchForm(request.GET)
        if form.is_valid():
            #print(form.cleaned_data)
            #print(request.GET)
            query=form.cleaned_data['text']
            smiles=form.cleaned_data['smiles']
            dele=form.cleaned_data['deleted']
            stype=form.cleaned_data['stype']
            cut=form.cleaned_data['cutoff']
            
            #smiles=''
            q=Q(name__icontains=query) | Q(all_names__icontains=query) | \
                Q(pl_name__icontains=query) | Q(cas__icontains=query)
                
                
            found_cmpds=Compound.objects.filter(q)
            
            if not dele:
                found_cmpds=Compound.extra_methods.existing(found_cmpds)
            if smiles=='':
                sorted_cmpds=Compound.extra_methods.sort_by_name_simil(found_cmpds,query)
                structure=False
            else:
                structure=True
                if stype=='sim':
                    sorted_cmpds=Compound.extra_methods.sort_by_str_simil(found_cmpds,smiles)
                else:
                    sorted_cmpds=Compound.extra_methods.substr_match(found_cmpds,smiles)
            #existing_cmpds=found_cmpds
            
            paginator=Paginator(sorted_cmpds,20)
            
            page=request.GET.get('page')
            try:
               cmpds_list = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                cmpds_list = paginator.page(1)
            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                cmpds_list = paginator.page(paginator.num_pages)
        
        else:
            form=SearchForm()
            cmpds_list=None
        
    else:
        form=SearchForm()
        cmpds_list=None
    
    return render(request,'chembase/search.html',{'form':form,'results':cmpds_list,'str':structure})


