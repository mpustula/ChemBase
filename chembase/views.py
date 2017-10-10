from django.shortcuts import get_object_or_404,render
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import ensure_csrf_cookie
import json
from django.utils import timezone

from chemspipy import ChemSpider
import cirpy
import difflib
import re

# Create your views here.
from .models import Compound, GHSClass, Cmpd_Class
from .forms import SearchForm, CompoundForm
from .functions import transform_sds

def index(request):
    return HttpResponse('Start: ChemBase')
    
    
def detail(request,cmpd_id):
    
    compound=get_object_or_404(Compound,pk=cmpd_id)
    existing_items=compound.item_set(manager='citems').existing()
    deleted_items=compound.item_set(manager='citems').deleted()

    return render(request,'chembase/detail.html',{'compound':compound,'exist':existing_items,'del':deleted_items})
    
    
def add(request):
    #form=CompoundForm()
    return render(request,'chembase/add.html')
    
    
def cmpd_save(request):
    
    if request.method=='POST':
        c=CompoundForm(request.POST,request.FILES)
        print(request.POST)
        if c.is_valid():
            new_cmpd=c.save(commit=False)           
            new_cmpd.save()
            
            #####class_extr field
            for item in request.POST:
                matchObj=re.match(r'id_class_(\d+$)',item)
                if matchObj:
                    ghs_class_id=matchObj.group(1)
                    ghs_class=GHSClass.objects.get(pk=ghs_class_id)
                    
                    ghs_class_num=request.POST[item]
                    
                    cc=Cmpd_Class(compound=new_cmpd,ghs_class=ghs_class,number=ghs_class_num)
                    
                    cc.save()
            #####pictograms field and other many-to-many
            c.save_m2m()
            
            ####sds_file
            if request.FILES:
                sds=request.FILES['sds_file']
        
                new_sds_name=(sds.name).split('.')[0]+str(new_cmpd.id)+'.pdf'
                print(new_sds_name)
                file_base='chembase/static/chembase/data/sds/'
                file_name=file_base+new_sds_name
                print(file_name)
                file_path='/data/sds/'+new_sds_name
                with open(file_name, 'wb+') as destination:
                    for chunk in sds.chunks():
                        destination.write(chunk)
                new_cmpd.sds=file_path
                
                
            ###image file
            csid=request.POST['csid']
            ##remove <<?timestamp=>> ending
            image_name=(request.POST['image']).split('?')[0]
            if image_name:
                if csid!='':
                    final_image_name=csid+'.png'
                else:
                    final_image_name='cmpd_num_'+str(new_cmpd.id)+'.png'
                file_base='chembase/static/chembase/images/'
                image_name_out=file_base+final_image_name
                with open(image_name_out, 'wb+') as destination:
                    destination.write(open('chembase'+image_name,'rb+').read())
                new_cmpd.image='images/'+final_image_name
                
                
                
            ###ewidencja
                
                
            ###log
                
                
            #new_cmpd=c
            #existing_items=new_cmpd.item_set(manager='citems').existing()
            #deleted_items=new_cmpd.item_set(manager='citems').deleted()
        
            return render(request,'chembase/detail.html',{'compound':new_cmpd})#,'exist':existing_items,'del':deleted_items})
            
        else:
            return HttpResponse(c.errors.as_data())
    

def add_cmpd(request):
    if request.method=='POST':
        print(request)
        rtype=request.POST.get('type')
        if rtype=='new_cmpd':
            form=CompoundForm()
            str_image=''
            molfile=''
            classes_dict={}
            classes_names_dict={}
            sds_name=''
        elif rtype=='base':
            cmpd_id=request.POST.get('cmpd_id')
            
            compound = Compound.objects.get(pk=cmpd_id)
            str_image='/static/chembase/'+compound.image
            form = CompoundForm(instance=compound)
            sds_name=compound.sds
            ewid=Compound.is_registered(compound)
            if ewid:
                form.fields['ewid'].initial=True
            ##risk classes:
            classes_list=Cmpd_Class.objects.filter(compound=compound)
            classes_dict={}
            classes_names_dict={}
            for item in classes_list:
                classes_names_dict[item.ghs_class.id]=item.ghs_class.class_full_en
                classes_dict["id_class_"+str(item.ghs_class.id)]=item.number

            
        elif rtype=='spider':
            cmpd_id=request.POST.get('cmpd_id')
            cas=request.POST.get('cas')
            
            cs=ChemSpider('c36756c7-401d-4097-9496-32ccbe7d876d')
            compound=cs.get_compound(cmpd_id)
            
            formula=str(compound.molecular_formula)
            inchi=compound.inchi
            smiles=compound.smiles
            molfile=compound.mol_2d
            #str_image=compound.image_url
            str_image=Compound.render_image('',compound.image)
            name=compound.common_name
            mw=compound.molecular_weight
            iupac_name=cirpy.resolve(inchi,'iupac_name')
            sds_name=''
            if iupac_name!=name:
                other_name=iupac_name
            else:
                other_name=''
        
            classes_dict={}
            classes_names_dict={}
            form = CompoundForm(initial={'name':name,
                                         'cas':cas,
                                         'formula':formula,
                                         'inchi':inchi,
                                         'all_names':other_name,
                                         'csid':cmpd_id,
                                         'smiles':smiles,
                                         'weight':mw,
                                         'molfile':molfile})
        else:
            form=CompoundForm()
            str_image=''
            classes_dict={}
            classes_names_dict={}
            sds_name=''
            
    else:
        form=CompoundForm()
        str_image=''
        classes_dict={}
        classes_names_dict={}
        sds_name=''
    return render(request,'chembase/add_cmpd.html',{'form':form,'structure_im':str_image,
                                                    'classes_dict':json.dumps(classes_dict),
                                                    'classes_names_dict':json.dumps(classes_names_dict),
                                                    'sds_name':sds_name})



def search_view(request):
    if request.method=='GET':
        form=SearchForm(request.GET)
        if form.is_valid():
            #print(form.cleaned_data)
            #print(request.GET)
            query=form.cleaned_data['text']
            query_cas=form.cleaned_data['cas']
            query_place=form.cleaned_data['place']
            smiles=form.cleaned_data['smiles']
            dele=form.cleaned_data['deleted']
            stype=form.cleaned_data['stype']
            cut=form.cleaned_data['cutoff']
            group=form.cleaned_data['group']
                        
            if smiles!='':
                structure=True
            else:
                structure=False
    else:
        form=SearchForm()
        
    result=search(query,query_cas,'and',query_place,smiles,dele,stype,cut,group)
    
    if result:
        found=len(result)

        paginator=Paginator(result,20)
        
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
        found=0
        cmpds_list=None
            
    return render(request,'chembase/search.html',{'form':form,'results':cmpds_list,'str':structure,'found':found})
    
def search_ajax(request):
    
    if request.method=='POST':
        query_=request.POST.get('query')
        cut_=request.POST.get('cutoff')
        print(cut_)
        result=search(query=query_,query_cas=query_,linker='or',cut=float(cut_),dele=True)     
                 
        return JsonResponse({item.id:{'name':item.name,'cas':item.cas,'subtitle':item.subtitle,'image':item.image} for item in result})

def search(query='',query_cas='',linker='and',query_place='',smiles='',dele=False,stype='sim',cut=0.6,group=None):
            
    if (query!='' or query_cas!='' or query_place!='' or smiles!='' or group):
        q1=Q(name__icontains=query) | Q(all_names__icontains=query) | \
            Q(pl_name__icontains=query)

        q2=Q(cas__icontains=query_cas)
        q3=Q(item__local__icontains=query_place)
        if group:
            q4=Q(item__group__exact=group)
        else:
            q4=Q()
        
        if linker=='and':
            q=q1 & q2 & q3 & q4
        elif linker=='or':
            q=q1 | q2
            if query_place!='':
                q=q | q3
            if group:
                q=q | q4
            
            
        found_cmpds=Compound.objects.filter(q).distinct()
        
        if not dele:
            found_cmpds=Compound.extra_methods.existing(found_cmpds)
        if smiles=='':
            sorted_cmpds=Compound.extra_methods.sort_by_name_simil(found_cmpds,query,cut)
        else:
            if stype=='sim':
                sorted_cmpds=Compound.extra_methods.sort_by_str_simil(found_cmpds,smiles,cut)
            else:
                sorted_cmpds=Compound.extra_methods.substr_match(found_cmpds,smiles,cut)
        #existing_cmpds=found_cmpds

    else:
        sorted_cmpds=None
        
    return sorted_cmpds
    
def chemspy_ajax(request):
    
    if request.method=='POST':
        query=request.POST.get('query')
        
        return JsonResponse({item['csid']:item for item in search_chemspy(query)})
        
      
    
def search_chemspy(query=''):
    cs=ChemSpider('c36756c7-401d-4097-9496-32ccbe7d876d')
    print('Connected to ChemSpider API')
    print("Searching started")
    print("Searching for: "+query)
    i=0
    results=[]
    for result in cs.search(query):
        if i>5:
            break
        print("Compound "+str(i))
        formula=str(result.molecular_formula)
        csid=str(result.csid)
        inchi=result.inchi
        name=result.common_name
        cas=cirpy.resolve(inchi,'cas')
        iupac_name=cirpy.resolve(inchi,'iupac_name')

        if type(cas) is list:
            c_cas=query
            sim_cas=difflib.get_close_matches(str(c_cas),cas,3,0)
            print(sim_cas)
            cas_=sim_cas[0]
        else:
            cas_=cas
        image=result.image_url
        print(image)
        i=i+1
        result_line={'csid':csid,'name':name,'iupac_name':iupac_name,'cas':cas_,'inchi':inchi,\
            'formula':formula,'image':image}
        results.append(result_line)
        
    print("Searching finished")
    print(results)
    
    return results
    
def structure_ajax(request):
    if request.method=='POST':
        query_csid=request.POST.get('csid')
        cs=ChemSpider('c36756c7-401d-4097-9496-32ccbe7d876d')
        compound=cs.get_compound(query_csid)
        molfile=compound.mol_2d
        
        return JsonResponse({'molfile':molfile})
        
def image_ajax(request):
    if request.method=='POST':
        query_csid=request.POST.get('csid')
        mol_file=request.POST.get('mol')
        print(mol_file)
        if query_csid:
            cs=ChemSpider('c36756c7-401d-4097-9496-32ccbe7d876d')
            compound=cs.get_compound(query_csid)
            #image_path=compound.image_url
            image_path=Compound.render_image('',compound.image)

        elif mol_file:
            image_path=Compound.render_image(mol_file,'')
        else:
            image_path=''
                
        return JsonResponse({'image':image_path})
        
def formula_ajax(request):
    if request.method=='POST':
        formula=request.POST.get('formula')
        new_formula=Compound.clean_formula(formula)
        
        return JsonResponse({'new_formula':new_formula})
        
def sds_ajax(request):
    
    if request.method=='POST':
        sds=request.FILES['sds_file']
        ans=Compound.save_sds(sds)
        print(ans)
        return JsonResponse(ans)
        
def ghs_classes_transl(request):
    
    if request.method=='POST':
        array=request.POST.get('array')
        result={}
        for item in array.split(','):
            ghs_class = GHSClass.objects.get(pk=item)
            result[item]=ghs_class.class_full_en
            
        return JsonResponse(result)
            
        

    
    


