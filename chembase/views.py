from django.shortcuts import get_object_or_404,render,redirect
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth import authenticate, login,logout
import json
from django.utils import timezone

from chemspipy import ChemSpider
import cirpy
import difflib
import re
import os

from django.contrib.auth.models import User, Permission
# Create your views here.
from .models import Compound, GHSClass, Cmpd_Class, SystemLog,Item,Group, Annotation,History, ExtraPermissions, UserProfile,OwnershipGroup
from .forms import SearchForm, CompoundForm, ItemForm, UserForm, UserProfileForm, ExtraPermForm,GroupForm,GHSClassForm



def can_add_item(user):
    return ExtraPermissions.check_perm(user,'chembase.add_item')

def index(request):
    return redirect('chembase:search')
    
def status(request):
    
    if request.user.is_authenticated:
        return HttpResponse(request.user.first_name+' '+request.user.last_name)
    else:
        return HttpResponse('Login error')


def get_groups(request):
    
    if request.user.is_authenticated:
        groups=Group.objects.all()
        
        groups_dict={item.id:item.group_name for item in groups}
        
        return JsonResponse(groups_dict)
    
    else:
        
        return HttpResponse('Login error')   

@login_required()
def detail(request,cmpd_id):
    
    compound=get_object_or_404(Compound,pk=cmpd_id)
    existing_items=compound.item_set(manager='citems').existing()
    deleted_items=compound.item_set(manager='citems').deleted()
    
    user=request.user
    
    allowed_existing=compound.item_set(manager='citems').allowed(user,existing_items)
    
    allowed_deleted=compound.item_set(manager='citems').allowed(user,deleted_items)
    
    items=[x.id for x in existing_items+deleted_items]
    
    log_items=SystemLog.objects.filter(model_name='compound',model_instance_id=cmpd_id)
    
    items_log=SystemLog.objects.filter(model_name='item',model_instance_id__in=items)
    
    if user.is_staff:
        user_staff=True
    else:
        user_staff=False
    
    if can_add_item(user):
        can_add=True
    else:
        can_add=False
    if user.has_perm('chembase.add_compound'):
        can_add_cmpd=True
    else:
        can_add_cmpd=False
    if compound.edit_allowed(user):
        can_edit=True
    else:
        can_edit=False
        
    #items_log.annotate(extra_field=Value('a'))
    #print(items_log[0].item_loc)
    items_log_list=[{'date':x.date,'author':x.author,'action':x.action,
                     'comment':x.comment,
                     'item_loc':Item.objects.get(pk=x.model_instance_id).local} for x in items_log]
                             

    #loc_list={x.id:Item.objects.get(pk=x.model_instance_id) for x in items_log}

    return render(request,'chembase/detail.html',{'compound':compound,'exist':allowed_existing,
                                                  'del':allowed_deleted,'log_entries':log_items,'item_log_entries':items_log_list,
                                                  'can_add':can_add,'can_add_cmpd':can_add_cmpd,'can_edit':can_edit,'user_staff':user_staff})
    

@login_required()
@user_passes_test(can_add_item)
def add(request):
    #form=CompoundForm()
    if request.user.has_perm('chembase.add_compound'):
        can_add_cmpd=True
    else:
        can_add_cmpd=False
    return render(request,'chembase/add.html',{'can_add_cmpd':can_add_cmpd})
    

def add_item_done(request,item_id):
    item=Item.objects.get(pk=item_id)

    cmpd=item.compound

    return render(request,'chembase/add_item_done.html',{'compound':cmpd,'item':item})

@login_required()
def add_item(request,cmpd_id):
    cmpd=Compound.objects.get(pk=cmpd_id)
    rtype=request.POST.get('type')
    if rtype=='edit':
        item_id=request.POST.get('item_id')
        item=Item.objects.get(pk=item_id)
        
        if not item.is_allowed(request.user,'chembase.change_item'):
            return redirect('/login/?next=%s' % request.path)
        
        comment_list=item.annotation_set.all()
        if comment_list:
            comment=comment_list[0].annotation
        else:
            comment=''
        item_form=ItemForm(instance=item)
        item_form.fields['comment'].initial=comment
        room_init=item.room
        place_init=item.place
        place_num_init=item.place_num
        owner_group_choices=ExtraPermissions.objects.filter(user__exact=request.user,permission__codename__exact='add_item')
        #print(owner_group_choices)
        #choices=((item.owner.id,item.owner.name),((item.group.id,item.group.name) for item in owner_group_choices))
        #choices.append(((item.group.id,item.group.name) for item in owner_group_choices))
        item_form.fields['owner'].choices=((item.group.id,item.group.name) for item in owner_group_choices)
        item_form.fields['owner'].choices.append((item.owner.id,item.owner.name))
    else:
        if not can_add_item(request.user):
            return redirect('/login/?next=%s' % request.path)
            
        item_form=ItemForm()
        item_id='new'
        room_init=''
        place_init=''
        place_num_init=''
        owner_group_choices=ExtraPermissions.objects.filter(user__exact=request.user,permission__codename__exact='add_item')
        #print(owner_group_choices)
        item_form.fields['owner'].choices=((item.group.id,item.group.name) for item in owner_group_choices)

    if request.user.has_perm('chembase.add_compound'):
        can_add_cmpd=True
    else:
        can_add_cmpd=False
    if cmpd.edit_allowed(request.user):
        can_edit=True
    else:
        can_edit=False
    return render(request,'chembase/add_item.html',{'compound':cmpd,'form':item_form,'item_id':item_id,
                                                    'room_init':room_init, 'place_init':place_init,
                                                    'place_num_init':place_num_init,
                                                    'can_add_cmpd':can_add_cmpd,
                                                    'can_edit':can_edit})
                                                    
@login_required()
def suggest_loc(request,cmpd_id):
    compound=Compound.objects.get(pk=cmpd_id)
    
    existing_items=compound.item_set(manager='citems').existing()
    deleted_items=compound.item_set(manager='citems').deleted()
    
    existing_loc=[item.local for item in existing_items]
    deleted_loc=[item.local for item in deleted_items]
    
    ###group_loc
    group_items=Item.objects.filter(compound__group__exact=compound.group,compound__storage_temp__exact=compound.storage_temp)
    
    group_loc=[item.local for item in group_items if not item.is_deleted()]
    
    values_dict={'compound':compound.name,'existing':existing_loc,'deleted':deleted_loc,'group':group_loc}
    
    
    return JsonResponse(values_dict)
    
    
@login_required()
def item_save(request):
    if not (ExtraPermissions.check_perm(request.user,'chembase.add_item') or ExtraPermissions.check_perm(request.user,'chembase.change_item')):
            return redirect('/login/?next=%s' % request.path)
    if request.method=='POST':
        cmpd_id=request.POST.get('cmpd_id')
        cmpd=Compound.objects.get(pk=cmpd_id)
        room=request.POST.get('room')
        place=request.POST.get('place')
        place_num=request.POST.get('place_num')
        
        item_id=request.POST.get('item_id')
        
        if (room and place and place_num):
            if item_id=='new':
                new_item=Item()
                action='add'
            else:
                new_item=Item.objects.get(pk=item_id)
                action='edit'
                
                
            
            new_item.compound=cmpd
            new_item.room=room
            new_item.place=place
            new_item.place_num=place_num
            new_item.hidden=False
            new_item.local=room+'-'+place+'-'+place_num
            new_item.save()
            
            quant=request.POST.get('quantity')
            if quant:
                new_item.quantity=quant
            amount=request.POST.get('amount')
            if amount:
                new_item.amount=amount
            stor_temp=request.POST.get('storage_temp')
            if stor_temp:
                new_item.storage_temp=stor_temp
            hidden=request.POST.get('hidden')
            if hidden:
                new_item.hidden=True   
                
            group_id=request.POST.get('group')
            if group_id:
                try:
                    group_obj=Group.objects.get(pk=group_id)
                except:
                    group_obj=Group(group_name=group_id)
                    group_obj.save()
                new_item.group=group_obj
            
            
            owner_id=request.POST.get('owner')
            owner_obj=OwnershipGroup.objects.get(pk=owner_id)
            new_item.owner=owner_obj
            
            
            ###delete old comments
            comments=Annotation.objects.filter(item=new_item)
            comments.delete()
            #### add new comment
            comment=request.POST.get('comment')            
            if comment:
                new_comment=Annotation(item=new_item,annotation=comment)
                new_comment.save()
                
            new_item.save()
            
            
            
            ###log
            user=request.user
            system_log_entry=SystemLog(model_name='Item',model_instance_id=new_item.id,
                                       author=user,action=action,comment='')
            system_log_entry.save()
            
            
            if item_id=='new':
                del_item=History(item=new_item,action='added')
                del_item.save()
                return redirect('chembase:add_item_done',item_id=new_item.id)
            else:
                return redirect('chembase:detail',cmpd_id=cmpd.id)
            
            
        else:
            i=ItemForm(request.POST)
            return render(request,'chembase/add_item.html',{'compound':cmpd,'form':i})
            
            
@login_required()      
def item_delete(request):
    if request.method=='POST':
        action=request.POST.get('action')
        item_id=request.POST.get('item_id')
        item=Item.objects.get(pk=item_id)
        user=request.user
        if item.is_allowed(user,'chembase.change_item'):
            system_log_entry=SystemLog(model_name='Item',model_instance_id=item_id,
                                       author=user,comment='')
            if action=='delete':
                item.delete()
                system_log_entry.action='delete'
            else:
                item.restore()
                system_log_entry.action='restore'
                
            system_log_entry.save()

        #return JsonResponse({'status':'success'})
        return redirect('chembase:detail',cmpd_id=item.compound.id)


@login_required()
def cmpd_save(request):
    
    if request.method=='POST':
        save_as=request.POST.get('save_as')
        redir_url=request.POST.get('redirect')
        if save_as=='new':
            if not request.user.has_perm('chembase.add_compound'):
                return redirect('/login/?next=%s' % request.path)
            c=CompoundForm(request.POST,request.FILES)
            cmpd_action='add'
        else:
            cmpd=Compound.objects.get(pk=save_as)
            if not cmpd.edit_allowed(request.user):
                return redirect('/login/?next=%s' % request.path)
            c=CompoundForm(request.POST,request.FILES,instance=cmpd)
            cmpd_action='edit'
        if c.is_valid():
            new_cmpd=c.save(commit=False)           
            new_cmpd.save()
            data_dict=c.cleaned_data
            #####class_extr field
            ##delete old classes
            old_classes=Cmpd_Class.objects.filter(compound=new_cmpd)
            old_classes.delete()
            ##add new classes
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
                file_base='/home/marcin/Dokumenty/projekty/production/Chem/chembase/static/chembase/data/sds/'
                file_name=file_base+new_sds_name
                print(file_name)
                file_path='/data/sds/'+new_sds_name
                with open(file_name, 'wb+') as destination:
                    for chunk in sds.chunks():
                        destination.write(chunk)
                new_cmpd.sds=file_path
                
            else:
                new_cmpd.sds=request.POST['sds_path']
                print('sds_path')
                print(request.POST['sds_path'])
            ###image file
            csid=request.POST['csid']
            ##remove <<?timestamp=>> ending
            image_name=(request.POST['image']).split('?')[0]
            if image_name:
                if csid!='':
                    final_image_name=csid+'.png'
                else:
                    final_image_name='cmpd_num_'+str(new_cmpd.id)+'.png'
                file_base='/home/marcin/Dokumenty/projekty/production/Chem/chembase/static/chembase/images/'
                image_name_out=file_base+final_image_name
                image_data=open('/home/marcin/Dokumenty/projekty/production/Chem/chembase'+image_name,'rb+').read()
                with open(image_name_out, 'wb+') as destination:
                    destination.write(image_data)
                new_cmpd.image='images/'+final_image_name
                print('image_file:')            
                print(image_name)
                
            ###group
            group_id=request.POST.get('group')
            if group_id:
                try:
                    group_obj=Group.objects.get(pk=group_id)
                except:
                    group_obj=Group(group_name=group_id)
                    group_obj.save()
                new_cmpd.group=group_obj
            ###ewidencja
            is_to_register=data_dict['ewid']
            new_cmpd.set_registered(is_to_register)
                
            ###log
            user=request.user
            new_cmpd.author=user
            new_cmpd.save()
            system_log_entry=SystemLog(model_name='Compound',model_instance_id=new_cmpd.id,
                                       author=user,action=cmpd_action,comment='')
            system_log_entry.save()
            #new_cmpd=c
            #existing_items=new_cmpd.item_set(manager='citems').existing()
            #deleted_items=new_cmpd.item_set(manager='citems').deleted()
        
            #return render(request,'chembase/detail.html',{'compound':new_cmpd})#,'exist':existing_items,'del':deleted_items})
            
            if redir_url=='':
                return redirect('chembase:add_item',cmpd_id=new_cmpd.id)
            else:
                return redirect(redir_url)
        else:
            return render(request,'chembase/add_cmpd.html',{'form':CompoundForm(request.POST,request.FILES),'pr_form':GroupForm(request.POST),'structure_im':'',
                                                    'classes_dict':{},
                                                    'classes_names_dict':{},
                                                    'sds_name':'','save_as':save_as,'redirect':redir_url})
    
@login_required()
def add_cmpd(request):
    save_as='new'
    redir_url=''
    if request.method=='POST':
        rtype=request.POST.get('type')
        group_form=GroupForm()
        if rtype=='new_cmpd':
            if not request.user.has_perm('chembase.add_compound'):
                return redirect('/login/?next=%s' % request.path)
            form=CompoundForm()
            str_image=''
            molfile=''
            classes_dict={}
            classes_names_dict={}
            sds_name=''
        elif rtype=='base':
            cmpd_id=request.POST.get('cmpd_id')
            return redirect('chembase:add_item',cmpd_id=cmpd_id)
        elif rtype=='edit':
            cmpd_id=request.POST.get('cmpd_id')
            output=request.POST.get('output')
            if output=='update':
                save_as=cmpd_id
            redir_url=request.POST.get('redirect')
            compound = Compound.objects.get(pk=cmpd_id)
            if not compound.edit_allowed(request.user):
                return redirect('/login/?next=%s' % request.path)
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
            
            group_form.fields['group'].initial=compound.group            
            
            
        elif rtype=='spider':
            if not request.user.has_perm('chembase.add_compound'):
                return redirect('/login/?next=%s' % request.path)
            cmpd_id=request.POST.get('cmpd_id')
            cas=request.POST.get('cas')
            
            cs=ChemSpider('c36756c7-401d-4097-9496-32ccbe7d876d')
            compound=cs.get_compound(cmpd_id)
            
            formula=str(compound.molecular_formula)
            inchi=compound.inchi
            smiles=compound.smiles
            molfile=compound.mol_2d
            #str_image=compound.image_url
            image_id=request.session.session_key
            str_image=Compound.render_image('',compound.image,image_id)
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
    return render(request,'chembase/add_cmpd.html',{'form':form,'pr_form':group_form,'structure_im':str_image,
                                                    'classes_dict':json.dumps(classes_dict),
                                                    'classes_names_dict':json.dumps(classes_names_dict),
                                                    'sds_name':sds_name,'save_as':save_as,'redirect':redir_url})


@login_required()
def search_view(request):
    if request.method=='GET':
        form=SearchForm(request.GET)
        pr_form=GHSClassForm()
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
            
            ghs_codes=request.GET.getlist('class_code_')
            #print(ghs_codes)
            ghs_classes=[]
            for item in ghs_codes:
                class_id=item.split('-')[0]
                number=item.split('-')[1]
                class_text=GHSClass.objects.get(pk=class_id).class_text
                ghs_classes.append({'id':item,'group':class_text,'number':number})
            
            #print(ghs_classes)
            if smiles!='':
                structure=True
            else:
                structure=False
    else:
        form=SearchForm()
        
    result=search(request.user,query,query_cas,'and',query_place,smiles,dele,stype,cut,group,ghs_codes)
    
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
            
    return render(request,'chembase/search.html',{'form':form,'pr_form':pr_form,'results':cmpds_list,'str':structure,'found':found,'ghs_classes':ghs_classes})

def search_qt(request):
    
    if request.user.is_authenticated:
       
        query=request.GET.get('text')
        query_cas=request.GET.get('cas')
        query_place=request.GET.get('place')
        linker=request.GET.get('linker')
        smiles=request.GET.get('smiles')
        dele=bool(request.GET.get('dele'))

        stype=request.GET.get('stype')
        cut=request.GET.get('cutoff')
        if cut:
            cutoff=float(cut)
        else:
            cutoff=0.6
        group=request.GET.get('group')

        result=search(request.user,query=query,query_cas=query_cas,query_place=query_place,
                      linker=linker,smiles=smiles,dele=dele,stype=stype,cut=cutoff,group=group)
                      
        json_dict={}
        for compound in result:          
            existing_items=compound.item_set(manager='citems').existing()
    
            allowed_existing=compound.item_set(manager='citems').allowed(request.user,existing_items)
            items_list=[(item['a'].local,[x.annotation for x in item['a'].annotation_set.all()]) for item in allowed_existing]
            
            data_dict={'name':compound.name,'cas':compound.cas,'subtitle':compound.subtitle,'image':compound.image,'items':items_list}
            json_dict[compound.id]=data_dict            
        
        return JsonResponse(json_dict)
        
    else:
        return HttpResponse('Login error')

def search_ajax(request):
    
    if request.method=='POST':
        query_=request.POST.get('query')
        cut_=request.POST.get('cutoff')
        result=search(user='abstract_user',query=query_,query_cas=query_,linker='or',cut=float(cut_),dele=True)     
                 
        return JsonResponse({item.id:{'name':item.name,'cas':item.cas,'subtitle':item.subtitle,'image':item.image} for item in result})

def search(user,query='',query_cas='',linker='and',query_place='',smiles='',dele=False,stype='sim',cut=0.6,group=None,ghs_codes=[]):
            
    if (query!='' or query_cas!='' or query_place!='' or smiles!='' or group or ghs_codes):
        q1=Q(name__icontains=query) | Q(all_names__icontains=query) | \
            Q(pl_name__icontains=query)

        q2=Q(cas__icontains=query_cas)
        q3=Q(item__local__icontains=query_place)
        if group:
            q4=Q(group__exact=group)
        else:
            q4=Q()
            
        q5=Q()
        for item in ghs_codes:
            class_id=item.split('-')[0]
            number=item.split('-')[1]
            ghs_class=GHSClass.objects.get(pk=class_id)
            q5 = q5 | Q(class_extr__exact=ghs_class,ghs_class_numbers__number__exact=number)
        
        if linker=='and':
            q=q1 & q2 & q3 & q4 & q5
        elif linker=='or':
            q=q1 | q2
            if query_place!='':
                q=q | q3
            if group:
                q=q | q4
            if ghs_codes:
                q = q | q5

            
        found_cmpds=Compound.objects.filter(q).distinct()
        if user!='abstract_user':
            found_cmpds=Compound.extra_methods.allowed_cmpds(user,found_cmpds)
        if not dele:
            found_cmpds=Compound.extra_methods.existing(found_cmpds)

        if smiles=='':
            if query!='':
                query_to_compare=query
                sorted_cmpds=Compound.extra_methods.sort_by_name_simil(found_cmpds,query_to_compare,0.1)
            elif query_cas!='':
                query_to_compare=query_cas
                sorted_cmpds=Compound.extra_methods.sort_by_name_simil(found_cmpds,query_to_compare,0.1)
            else:
                sorted_cmpds=found_cmpds
            
        else:
            if stype=='sim':
                sorted_cmpds=Compound.extra_methods.sort_by_str_simil(found_cmpds,smiles,cut)
            else:
                sorted_cmpds=Compound.extra_methods.substr_match(found_cmpds,smiles,cut)
        #existing_cmpds=found_cmpds
    else:
        sorted_cmpds=None
        
    return sorted_cmpds

@login_required()
def search_rm(request):
    
    can=GHSClass.objects.get(pk=4)
    mut=GHSClass.objects.get(pk=10)
    q1=Q(number__exact='1A') | Q(number__exact='1B')
    q2=Q(ghs_class__exact=can) | Q(ghs_class__exact=mut) 
    
    rm_cmpds_cl=Cmpd_Class.objects.filter(q1 & q2)
    
    rm_cmpds=set([item.compound for item in rm_cmpds_cl])
    
    return render(request,'chembase/search_rm.html',{'results':rm_cmpds})

@login_required()
def search_groups(request):
    
    compounds=Compound.objects.all()

    compound_groups=[]
    for item in compounds:
        items=item.item_set.all()
        #if len(items)>1:
        groups=[x.storage_temp for x in items]
            #if len(set(groups))>1:
            #    print(groups)
        #groups_set=set(groups)
        #if len(groups_set)==1:
            #print(list(groups_set))
            #item.group=list(groups_set)[0]
            #item.save()
        if not item.storage_temp:
            compound_groups.append({'cmpd':item,'cmpd_group':item.storage_temp,'items':items,'groups':groups})
        
    return render(request,'chembase/search_gr.html',{'results':compound_groups})
        

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
        image_id=request.session.session_key
        if query_csid:
            cs=ChemSpider('c36756c7-401d-4097-9496-32ccbe7d876d')
            compound=cs.get_compound(query_csid)
            #image_path=compound.image_url
            image_path=Compound.render_image('',compound.image,image_id)

        elif mol_file:
            image_path=Compound.render_image(mol_file,'',image_id)
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
        
def item_loc_filter(request):
    
    if request.method=='POST':
        room=request.POST.get('room')
        #print(room)
        place=request.POST.get('place')
        #print(place)
        if (room!='' and place==''):
            place_choices=sorted(set([item.place for item in Item.objects.filter(room__exact=room)]))
            #print(place_choices)
            #ans={x:x for x in place_choices}
            ans=place_choices
            #print(ans)
        elif (room!='' and place!=''):
            place_num_choices=sorted(set([item.place_num for item in Item.objects.filter(room__exact=room,place__exact=place)]),reverse=True)
            #print(place_num_choices)
            #ans=sorted({x:x for x in place_num_choices})
            ans=place_num_choices
            #print(ans)
        return JsonResponse(ans,safe=False)
        
def ghs_classes_transl(request):
    
    if request.method=='POST':
        array=request.POST.get('array')
        result={}
        print(array)
        for item in array.split(','):
            ghs_class = GHSClass.objects.get(pk=item)
            result[item]=ghs_class.class_full_en
            
        return JsonResponse(result)
            
            
def logout_view(request):
    logout(request)
    return redirect('chembase:login')
    
def account_view(request):
    
    return render(request,'chembase/account.html')
                
def sds_index(request):
    sds_list=os.listdir('/home/marcin/Dokumenty/projekty/production/Chem/chembase/static/chembase/data/sds/')
    
    pdf_list=[]    
    for item in sds_list:
        if item.endswith('.pdf'):
            pdf_list.append(item)
                
    return render(request,'chembase/sds.html',{'list':sorted(pdf_list)})

@login_required()    
def admin(request):
    
    #access_log=open('/var/log/apache2/access.log','r').readlines()[-10:]
    #+error_log=open('/var/log/apache2/error.log','r').readlines()[-10:]
    access_log=[]
    error_log=[]
    
    systemLogs=SystemLog.objects.all()[::-1][0:10]
    
    system_log_list=[]
    for x in systemLogs:
        dictionary={'date':x.date,'author':x.author,'action':x.action,
                     'comment':x.comment,'model':x.model_name,'model_inst_id':x.model_instance_id}
        if x.model_name=='Compound':
            dictionary['compound_name']=Compound.objects.get(pk=x.model_instance_id).name
            dictionary['item']=''
            dictionary['compound_id']=x.model_instance_id
        elif x.model_name=='Item':
            dictionary['item']=Item.objects.get(pk=x.model_instance_id).local
            dictionary['compound_name']=Item.objects.get(pk=x.model_instance_id).compound.name
            dictionary['compound_id']=Item.objects.get(pk=x.model_instance_id).compound.id
        system_log_list.append(dictionary)
        
    compounds_all=Compound.objects.all()
    compounds_number=len(compounds_all)
    existing_compounds=len(Compound.extra_methods.existing(compounds_all))
    return render(request,'chembase/admin.html',{'access_log':access_log[::-1],'error_log':error_log[::-1],'system_log':system_log_list,
                                                 'compounds_number':compounds_number,'existing_cmpds':existing_compounds})
@login_required() 
def logs(request):
    
    systemLogs=SystemLog.objects.all()[::-1]
    
    system_log_list=[]
    for x in systemLogs:
        dictionary={'date':x.date,'author':x.author,'action':x.action,
                     'comment':x.comment,'model':x.model_name,'model_inst_id':x.model_instance_id}
        if x.model_name=='Compound':
            try:
                dictionary['compound_name']=Compound.objects.get(pk=x.model_instance_id).name
            except:
                dictionary['compound_name']='unknown'
            dictionary['item']=''
            dictionary['compound_id']=x.model_instance_id
        elif x.model_name=='Item':
            try:
                dictionary['item']=Item.objects.get(pk=x.model_instance_id).local
                dictionary['compound_name']=Item.objects.get(pk=x.model_instance_id).compound.name
                dictionary['compound_id']=Item.objects.get(pk=x.model_instance_id).compound.id
            except:
                dictionary['item']='unknown'
                dictionary['compound_name']='unknown'
                dictionary['compound_id']=0
        system_log_list.append(dictionary)
        
    return render(request,'chembase/admin_logs.html',{'system_log':system_log_list})
    
    
@login_required()
@permission_required('user.change_user')  
def users(request):
    
    users=User.objects.all()
   
    return render(request,'chembase/admin_users.html',{'users':users})
    
    
@login_required()
@permission_required('user.change_user') 
def edit_user(request,user_id):
    
    if int(user_id)!=0:
        user=User.objects.get(pk=user_id)
        user_form=UserForm(instance=user)
        try:
            profile_form=UserProfileForm(instance=user.userprofile)
        except:
            profile_form=UserProfileForm()
        user_permissions=ExtraPermissions.objects.filter(user__exact=user)
        user_form.fields['password'].disabled=True
        user_form.fields['password_commit'].disabled=True
    else:
        user_form=UserForm()
        profile_form=UserProfileForm()
        user_permissions=None
        user=None
        user_form.fields['password'].required=True
        user_form.fields['password_commit'].required=True
    
    perm_form=ExtraPermForm()
    if request.user.is_superuser:
        user_form.fields['is_superuser'].disabled=False
        user_form.fields['is_staff'].disabled=False
    else:
        user_form.fields['is_superuser'].disabled=True
        user_form.fields['is_staff'].disabled=True

    return render(request,'chembase/admin_edit_user.html',{'form':user_form,'pr_form':profile_form,
                                                           'perm_form':perm_form,'user_permissions':user_permissions,
                                                           'user_ed':user})
                                                           
@login_required()
@permission_required('user.change_user')                                                   
def save_user(request):
    
    if request.method=='POST':
        user_id=request.POST.get('user_id')
        if user_id:
            user=User.objects.get(pk=user_id)
            user_form=UserForm(request.POST,instance=user)
            password=None
        else:
            user_form=UserForm(request.POST)
            password=request.POST.get('password')
            password_commit=request.POST.get('password_commit')
            
            if not (password and password==password_commit):
                return render(request,'chembase/admin_edit_user.html',{'form':user_form,'pr_form':UserProfileForm(request.POST),
                                                               'perm_form':ExtraPermForm(request.POST),'pass_err':'The passwords do not match!'})
        if user_form.is_valid():
            new_user=user_form.save()
            print(password)
            if password:
                new_user.set_password(password)
                new_user.save()
            try:
                profile=new_user.userprofile
            except:
                profile=UserProfile(user=new_user)
                profile.save()
                
            user_profile_form=UserProfileForm(request.POST,instance=profile)
            if user_profile_form.is_valid():
                user_profile_form.save()
            else:
                print(user_profile_form.errors.as_data())
                
            permissions_codes=request.POST.getlist('perm_code_')
            ##delete old permissions
            if user_id:
                old_perms=ExtraPermissions.objects.filter(user__exact=new_user)
                old_perms.delete()
            ##add new permissions
            for item in permissions_codes:
                group_code=item.strip().split('-')[0]
                perm_code=item.strip().split('-')[1]
                group=OwnershipGroup.objects.get(pk=group_code)
                perm=Permission.objects.get(pk=perm_code)

                new_perm=ExtraPermissions(user=new_user,group=group,permission=perm)
                new_perm.save()

        else:
            print(user_form.errors.as_data())
            
            return HttpResponse(user_form.errors.as_data())


        

    
    return redirect('chembase:admin_users')
    
    
