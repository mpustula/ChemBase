from django.shortcuts import get_object_or_404,render,redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.db.models import Q
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth import authenticate, login,logout, update_session_auth_hash
from django.contrib.auth.models import Permission
from django.contrib.auth.forms import PasswordChangeForm
from django.views.decorators.debug import sensitive_post_parameters
from django.shortcuts import resolve_url
from django.template.response import TemplateResponse
from django.utils.translation import ugettext as _
import json
from django.utils import timezone


import cirpy
import re
import os
import datetime

from django.contrib.auth.models import User, Permission
# Create your views here.
from .models import Compound, GHSClass, Cmpd_Class, SystemLog,Item,Group, Annotation,History, ExtraPermissions, UserProfile,OwnershipGroup, ORZForm, ORZExtraFields
from .forms import (SearchForm, CompoundForm, ItemForm, UserForm, UserProfileForm, 
                    ExtraPermForm,GroupForm,GHSClassForm, ORZ_Form, ExpirePasswords, OwnershipGroupForm)
from .utils.functions import ChemSp


def can_add_item(user):
    return ExtraPermissions.check_perm(user,'chembase.add_item')
    
def check_password_valid(request):
    now=timezone.now()
    valid=request.user.userprofile.password_expiry_date
      
    if valid and now>valid:
        request.user.is_active=False
        request.user.save()
        #print('expired')
        #return HttpResponse('chembase/password_expired.html')
        #return TemplateResponse(request,'chembase/password_expired.html')
        #request.user.logout()

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
        



@sensitive_post_parameters()
@csrf_protect
@login_required
def password_change(request,
                    template_name='chembase/change_password.html',
                    post_change_redirect=None,
                    password_change_form=PasswordChangeForm,
                    current_app=None, extra_context=None):
    if post_change_redirect is None:
        post_change_redirect = reverse('chembase:password_change_done')
    else:
        post_change_redirect = resolve_url(post_change_redirect)
    if request.method == "POST":
        form = password_change_form(user=request.user, data=request.POST)
        if form.is_valid():
                form.save()
                # Updating the password logs out all other sessions for the user
                # except the current one if
                # django.contrib.auth.middleware.SessionAuthenticationMiddleware
                # is enabled.
                update_session_auth_hash(request, form.user)
                form.user.userprofile.set_password_expiry(365)
                return HttpResponseRedirect(post_change_redirect)
    else:
        form = password_change_form(user=request.user)
    context = {
        'form': form,
        'title': _('Password change'),
    }
    if extra_context is not None:
        context.update(extra_context)

    if current_app is not None:
        request.current_app = current_app

    return TemplateResponse(request, template_name, context)

@login_required()
def detail(request,cmpd_id):
    check_password_valid(request)
    
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
        
    own_groups=set([x.owner for x in existing_items+deleted_items])
    orz_details=[]
    for item in own_groups:
        orz_fields=ORZExtraFields.objects.filter(compound=compound,owner=item)
        if orz_fields:
            orzdict={'group':item.name,'du':orz_fields[0].dailyused,'ewid':orz_fields[0].ewidencja,'resp':orz_fields[0].respzone}
        else:
            orzdict={'group':item.name,'du':'','ewid':False,'resp':False}
        orz_details.append(orzdict)
        
    #items_log.annotate(extra_field=Value('a'))
    #print(items_log[0].item_loc)
    items_log_list=[{'date':x.date,'author':x.author,'action':x.action,
                     'comment':x.comment,
                     'item_loc':Item.objects.get(pk=x.model_instance_id).local} for x in items_log]
                             

    #loc_list={x.id:Item.objects.get(pk=x.model_instance_id) for x in items_log}

    return render(request,'chembase/detail.html',{'compound':compound,'exist':allowed_existing,
                                                  'del':allowed_deleted,'log_entries':log_items,'item_log_entries':items_log_list,
                                                  'can_add':can_add,'can_add_cmpd':can_add_cmpd,'can_edit':can_edit,'user_staff':user_staff,'orzdet':orz_details})
    

@login_required()
@user_passes_test(can_add_item)
def add(request):
    check_password_valid(request)
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
    check_password_valid(request)
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
        #owner_group_choices=ExtraPermissions.objects.filter(user__exact=request.user,permission__codename__exact='add_item')
        owner_group_choices=ExtraPermissions.permitted_groups(request.user,'chembase.add_item')
        #print(owner_group_choices)
        #choices=((item.owner.id,item.owner.name),((item.group.id,item.group.name) for item in owner_group_choices))
        #choices.append(((item.group.id,item.group.name) for item in owner_group_choices))
        item_form.fields['owner'].choices=((item.id,item.name) for item in owner_group_choices)
        if not ExtraPermissions.check_perm(request.user,'chembase.add_item',item.owner):
            item_form.fields['owner'].choices.append((item.owner.id,item.owner.name))
            
        
    else:
        if not can_add_item(request.user):
            return redirect('/login/?next=%s' % request.path)
            
        item_form=ItemForm()
        item_id='new'
        room_init=''
        place_init=''
        place_num_init=''
        #owner_group_choices=ExtraPermissions.objects.filter(user__exact=request.user,permission__codename__exact='add_item')
        owner_group_choices=ExtraPermissions.permitted_groups(request.user,'chembase.add_item')
        #print(owner_group_choices)
        item_form.fields['owner'].choices=((item.id,item.name) for item in owner_group_choices)

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
@user_passes_test(can_add_item)
def suggest_loc(request):
    cmpd_id=request.GET.get('cmpd_id')
    owner=request.GET.get('owner')
    owner_obj=OwnershipGroup.objects.filter(name__exact=owner)[0]
    ignore_temp=request.GET.get('ignore_temp')
    if ExtraPermissions.check_perm(request.user,'chembase.can_see_item',owner_obj):
        resp_dict=Item.suggest_loc(cmpd_id,request.user,owner,ignore_temp)
    
        return JsonResponse(resp_dict)
    else:
        return HttpResponse('You do not have permission required to see this content!',status=403)
    
    
@login_required()
def get_orz_details(request):
    cmpd_id=request.GET.get('cmpd_id')
    cmpd=Compound.objects.get(pk=cmpd_id)
    owner_id=request.GET.get('owner_id')
    owner=OwnershipGroup.objects.get(pk=owner_id)
    
    fields=ORZExtraFields.objects.filter(compound__exact=cmpd,owner=owner)    
    
    if fields:
        orz_dict={'du':fields[0].dailyused,'ewid':fields[0].ewidencja,'resp':fields[0].respzone}
    else:
        orz_dict={'du':None,'ewid':None,'resp':None}
    
    return JsonResponse(orz_dict)
    
    
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
                if new_item.is_allowed(request.user,'chembase.change_item'):
                    action='edit'
                else:
                    return redirect('/login/?next=%s' % request.path)
                
                
            
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
            
            ###orz_details
            current_details=ORZExtraFields.objects.filter(compound__exact=cmpd,owner__exact=owner_obj)
            print(current_details)
            new_details={'du':request.POST.get('dailyused'),'ewid':request.POST.get('ewid'),'resp':request.POST.get('resp')}
            print(new_details)
            
            if new_details['du'] or new_details['ewid'] or new_details['resp']:
                if current_details:
                    current_details[0].dailyused=new_details['du']
                    current_details[0].ewidencja=bool(new_details['ewid'])
                    current_details[0].respzone=bool(new_details['resp'])
                    current_details[0].save()
                    print(current_details[0])
                    print(current_details)
                else:
                    new_detail=ORZExtraFields(compound=cmpd,owner=owner_obj,dailyused=new_details['du'],ewidencja=bool(new_details['ewid']),respzone=bool(new_details['resp']))
                    new_detail.save()
                    print(new_detail)
            else:
                if current_details:
                    current_details.delete()
            
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
                try:
                    image_data=open('/home/marcin/Dokumenty/projekty/production/Chem/chembase'+image_name,'rb+').read()
                except:
                    pass
                else:
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

            ###paper sds
            paper_sds=data_dict['paper_sds']
            new_cmpd.set_paper(paper_sds)
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
    check_password_valid(request)
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

            paper=Compound.isPaperSDS(compound)
            if paper:
                form.fields['paper_sds'].initial=True
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

            compound=ChemSp().get_compound(cmpd_id)
            formula=str(compound.molecular_formula)
            inchi=compound.inchi
            smiles=compound.smiles
            molfile=compound.mol_2d
            #str_image=compound.image_url
            image_id=request.session.session_key
            str_image=ChemSp().render_image(cmpd_id,image_id)
            name=compound.common_name
            mw=compound.molecular_weight or 0
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
                                         'weight':'%.4f'%mw,
                                         'molfile':molfile})
        else:
            form=CompoundForm()
            group_form=GroupForm()
            str_image=''
            classes_dict={}
            classes_names_dict={}
            sds_name=''
            
    else:
        form=CompoundForm()
        group_form=GroupForm()
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
    check_password_valid(request)
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
    check_password_valid(request)
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
        qa=Q()
        qb=Q()
        qc=Q()
        for item in query.split():
            qa = qa & Q(name__icontains=item)
            qb = qb & Q(all_names__icontains=item)
            qc = qc & Q(pl_name__icontains=item)
            
        q1=qa | qb | qc

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
    
    
    ###moving daily used, registered resp_zone to separate class
#    items=Item.objects.all()
#    for item in items:
#        cmpd=item.compound
#        owner=item.owner
#        extr_fields=ORZExtraFields.objects.filter(compound__exact=cmpd,owner__exact=owner)
#        if not extr_fields:
#            dused=cmpd.dailyused
#            ewid=cmpd.is_registered()
#            rzone=cmpd.inRespZone()
#            new_field=ORZExtraFields(compound=cmpd,owner=owner,dailyused=dused,ewidencja=ewid,respzone=rzone)
#            new_field.save()
#            
    #####end
    
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

    return ChemSp().search(query)
    
def structure_ajax(request):
    if request.method=='POST':
        query_csid=request.POST.get('csid')
        compound=ChemSp().get_cmpd(query_csid)
        molfile=compound.mol_2d
        
        return JsonResponse({'molfile':molfile})
        
def image_ajax(request):
    if request.method=='POST':
        query_csid=request.POST.get('csid')
        mol_file=request.POST.get('mol')
        print(mol_file)
        image_id=request.session.session_key
        if query_csid:
            image_path = ChemSp().render_image(query_csid, image_id)
        elif mol_file:
            image_path = Compound.render_image(mol_file, image_id)
        else:
            image_path = ''

        return JsonResponse({'image':image_path})

        
def formula_ajax(request):
    if request.method=='POST':
        formula=request.POST.get('formula')
        new_formula=Compound.clean_formula(formula)
        
        return JsonResponse({'new_formula':new_formula})
                
def properties_ajax(request):
    if request.method=='POST':
        mol_file=request.POST.get('mol')
        properties=Compound.calculate_properties(mol_file)
        
        if properties:
            return JsonResponse(properties)
        else:
            return HttpResponse('Invalid structure!', status=409)
            
def clean_str_ajax(request):
    if request.method=='POST':
        mol_file=request.POST.get('mol')
        properties=Compound.clean_structure(mol_file)
        
        if properties:
            return JsonResponse(properties)
        else:
            return HttpResponse('Invalid structure!', status=409)
        
def sds_ajax(request):
    
    if request.method=='POST':
        sds=request.FILES['sds_file']
        ans=Compound.save_sds(sds)
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
    check_password_valid(request)
    return render(request,'chembase/account.html')
                
def sds_index(request):
    sds_list=os.listdir('/home/marcin/Dokumenty/projekty/production/Chem/chembase/static/chembase/data/sds/')
    
    pdf_list=[]    
    for item in sds_list:
        if item.endswith('.pdf'):
            pdf_list.append(item)
                
    return render(request,'chembase/sds.html',{'list':sorted(pdf_list)})
    

@login_required()
@user_passes_test(lambda u: u.is_staff)   
def log_file(request,file_type):
    if file_type=="access":
        file_log=open('/var/log/apache2/access.log','r')
        msg='Access log file'
    elif file_type=='error':
        msg='Error log file'
        file_log=open('/var/log/apache2/error.log','r')
        
    file_lines=file_log.readlines()[::-1]
    
    return render(request,'chembase/log_file.html',{'log':file_lines,'msg':msg})

@login_required()        
def admin(request):
    check_password_valid(request)


    return render(request,'chembase/admin.html')
                                                 
@login_required()
@user_passes_test(lambda u: u.is_staff)    
def server(request):
    check_password_valid(request)
    access_log=open('/var/log/apache2/access.log','r')
    access_lines=access_log.readlines()[-15:]
    error_log=open('/var/log/apache2/error.log','r')
    error_lines=error_log.readlines()[-15:]
    
    #access_log=[]
    #error_log=[]

    #####note: access to apache log files requires granting permission (644) to www-data user. 
    #  This can be done by:
    #    sudo chmod 644 /var/log/apache2/access.log /var/log/apache2/error.log
    # and by changing "create 640 root adm" into "create 644 roor adm" in /etc/logrotate.d/apache2 file

    return render(request,'chembase/admin_server.html',{'access_log':access_lines[::-1],
                                                 'error_log':error_lines[::-1],
                                                 })
                                                 

@login_required()
@user_passes_test(lambda u: u.is_staff)    
def settings(request):
    check_password_valid(request)

    
    return render(request,'chembase/admin_settings.html')

@login_required()        
def cmpds_items(request):
    check_password_valid(request)

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
    

    return render(request,'chembase/admin_cmpds_items.html',{'system_log':system_log_list,
                                                 'compounds_number':compounds_number,
                                                 'existing_cmpds':existing_compounds})
                                                 
@login_required() 
def logs(request):
    check_password_valid(request)
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
@permission_required('auth.change_user')
def users_groups(request):
    check_password_valid(request)
    
    users_all=User.objects.all()
    
    users_total=len(users_all)
    users=users_all.order_by('-last_login')[0:5]
    
    now=datetime.datetime.now() 
    
    users_active=users_all.filter(last_login__gte=now-datetime.timedelta(days=30)).order_by('-last_login')
    active_total=len(users_active)
    
    users_inactive=users_all.filter(last_login__lte=now-datetime.timedelta(days=60)).order_by('last_login')
    inactive_total=len(users_inactive)
    
    users_with_permissions=[]
    existing_permissions=[]
    
    for item in users_all:
        permissions=Permission.objects.filter(user=item)
        if permissions:
            users_line={'user':item}
            users_with_permissions.append(users_line)
            for j in permissions:
                existing_permissions.append(j)
        elif item.is_superuser or item.is_staff:
            users_line={'user':item}
            users_with_permissions.append(users_line)
        
    #userperm=list(set(users_with_permissions))
    userperm=users_with_permissions

    permissions=list(set(existing_permissions))

    for user in userperm:
        perms=[]
        for item in permissions:
            perms.append(user['user'].has_perm(item.content_type.app_label+'.'+item.codename))
        user['perms']=perms
    
    items_groups=OwnershipGroup.objects.all()
   
    return render(request,'chembase/admin_users_groups.html',{'users':users,'users_total':users_total,'users_active':users_active[0:10],
                                                              'active_total':active_total,'users_inactive':users_inactive,'inactive_total':inactive_total,
                                                              'groups':items_groups,'perms':permissions,'users_perms':userperm})
    
    
@login_required()
@permission_required('auth.change_user')
def users(request):
    check_password_valid(request)
    
    users=User.objects.all()
      
    return render(request,'chembase/admin_users.html',{'users':users})
    

@login_required()
@permission_required('auth.change_user') 
def edit_user(request,user_id):
    check_password_valid(request)
    
    if int(user_id)!=0:
        user=User.objects.get(pk=user_id)
        if (user.is_superuser and not request.user.is_superuser): 
            return redirect('chembase:admin_users')
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
        user_form.fields['password'].required=False
        user_form.fields['password_commit'].required=False
    
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
@permission_required('auth.change_user')                                                   
def save_user(request):
    
    if request.method=='POST':
        user_id=request.POST.get('user_id')
        if user_id:
            user=User.objects.get(pk=user_id)
            is_su=user.is_superuser
            if (is_su and not request.user.is_superuser):
                return HttpResponse("Permission denied - you cannot edit the Superuser account!")
            is_staff=user.is_staff
            user_form=UserForm(request.POST,instance=user)
            password=None
            if_random_pass=0
        else:
            user_form=UserForm(request.POST)
            is_su=False
            is_staff=False
            password=request.POST.get('password')
            password_commit=request.POST.get('password_commit')
            
            if_random_pass=request.POST.get('if_random_pass')
            
            if if_random_pass:
                password=''
                password_commit=''
            else:        
                if not (password and password==password_commit):
                    return render(request,'chembase/admin_edit_user.html',{'form':user_form,'pr_form':UserProfileForm(request.POST),
                                                                   'perm_form':ExtraPermForm(request.POST),'pass_err':'The passwords do not match!'})
        if user_form.is_valid():
            set_su=user_form.cleaned_data['is_superuser']
            set_staff=user_form.cleaned_data['is_staff']
            
            mail=user_form.cleaned_data['email']
            if if_random_pass and not mail:
                return render(request,'chembase/admin_edit_user.html',{'form':user_form,'pr_form':UserProfileForm(request.POST),
                                                                   'perm_form':ExtraPermForm(request.POST),'pass_err':'E-mail address is required for random password generation!'})

            if ((is_su==set_su and is_staff==set_staff) or request.user.is_superuser):
                new_user=user_form.save()
            else:
                return HttpResponse("Permission denied - you cannot alter 'Staff' and 'Superuser' fields!")
                
            
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
                
            if if_random_pass:
                new_user.userprofile.set_random_password()
                            

        else:
            print(user_form.errors.as_data())
            
            return HttpResponse(user_form.errors.as_data())


        

    
    return redirect('chembase:admin_users')
    
@login_required()
@permission_required('auth.change_user') 
def reset_password(request):

    if request.method=='POST':
        if request.user.is_superuser:
            edited_user_id=request.POST.get('user_id')
            user=User.objects.get(pk=edited_user_id)
            ans=user.userprofile.set_random_password("Reset")
            if ans[0]:
                return HttpResponse(ans[1])
            else:
                return HttpResponse(ans[1],status=400)
        else:
            return HttpResponse('You do not have superuser permission required to reset a password!',status=403)

@login_required()
@user_passes_test(lambda u: u.is_superuser)           
def expire_passwords(request):
    
    if request.method=='POST':
        user_id=request.POST.get('user_id')
        days=int(request.POST.get('date'))
        #date=(datetime.datetime.today()+datetime.timedelta(days=days)).strftime('%Y-%m-%d')
        if_mail=request.POST.get('if_mail')
        #print(if_mail)
        user=User.objects.get(pk=user_id)
        username=user.username
        names=user.get_full_name()
        if user.is_superuser:
            ans='User '+names+' ('+username+') has superuser privileges. Superuser password cannot be forced to expire!'
            return HttpResponse(ans,status=403)
        else:
            if if_mail=="false":
                user.userprofile.set_password_expiry(days)
                ans='Password for user: '+names+' ('+username+') will expire on '+ \
                    user.userprofile.password_expiry_date.strftime('%Y-%m-%d')+'. Notification e-mail has NOT been sent!'
                status=200
            else:
                user_mail=user.email
                if user_mail:
                    user.userprofile.set_password_expiry(days)
                    mail_ans=user.userprofile.sent_expiry_mail()
                    if mail_ans[0]:
                        ans='Password for user: '+names+' ('+username+') will expire on '+ \
                            user.userprofile.password_expiry_date.strftime('%Y-%m-%d')+'. Notification e-mail has been sent to: '+user_mail
                        status=200
                    else:
                        ans='E-mail during sending error.'
                        status=500
                else:
                    ans='No valid e-mail address has been found for user: '+names+' ('+username+'). Request cancelled.'
                    status=409
            return HttpResponse(ans,status=status)
        
    else:
        exp_form=ExpirePasswords()
        return render(request,'chembase/admin_expire_passwords.html',{'form':exp_form})
    

@login_required()
def group_details(request,group_id):
    check_password_valid(request)
    
    group=OwnershipGroup.objects.get(pk=group_id)
    
    items=group.item_set.all()
    items_num=len(items)
    
    active_items=group.item_set(manager='citems').existing()
    active_num=len(active_items)
    
    locations=set([item.room for item in active_items])
    
    loc_occ=[]
    
    for loc in locations:
        count=0
        loc_items=items.filter(room__exact=loc)
        for item in loc_items:
            if not item.is_deleted():
                count=count+1
        loc_occ.append([count,loc])
        
    #locations_occupancy=[{x,len(items.filter(room__exact=x))} for x in locations]
    occupancies=sorted(loc_occ,reverse=True)
    
    orz=ORZForm.objects.filter(owner__exact=group)
    orz_num=len(orz)
    
    if orz:   
        last_orz=orz.order_by('-date')[0]
    else:
        last_orz=None
    
    
    users_permissions=ExtraPermissions.objects.filter(group__exact=group).order_by('user')
    
    perm_users=set([x.user for x in users_permissions])
    
    permissions_dict=[{'id':x.id,'user':x.username,'first_name':x.first_name,'last_name':x.last_name,
                       'see_item':users_permissions.filter(user__exact=x,permission__codename__exact='can_see_item').exists(),
                       'change_item':users_permissions.filter(user__exact=x,permission__codename__exact='change_item').exists(),
                       'all_permissions':[item.permission for item in users_permissions.filter(user__exact=x)]} for x in perm_users]
                       

    
    return render(request,'chembase/admin_groups.html',{'group':group,'permissions':permissions_dict,'items':items_num,'ex_items':active_num,
                                                        'locations':occupancies,'orz':orz_num,'last_orz':last_orz})
    
@login_required()    
def orz_form(request):
    check_password_valid(request)
    
    groups=ExtraPermissions.permitted_groups(request.user,'chembase.can_see_item')
    #orz_permissions=ExtraPermissions.objects.filter(user__exact=request.user,permission__codename__exact='can_see_item')
    #groups=[x.group for x in orz_permissions]
    
    groups_add=ExtraPermissions.permitted_groups(request.user,'chembase.add_orzform')
    #orz_add_permissions=ExtraPermissions.objects.filter(user__exact=request.user,permission__codename__exact='add_orzform')
    #groups_add=[x.group for x in orz_add_permissions]
    
    
    
    if request.method=='POST':
        form=ORZ_Form(request.POST)
        form.fields['owner'].choices=((item.id,item.name) for item in groups_add)
        
        if form.is_valid():
            owner=form.cleaned_data['owner']
            
            perm=ExtraPermissions.check_perm(request.user,'chembase.add_orzform',owner)
            if not perm:
                return HttpResponse('Permission denied - you can not create a form for this group!',status=403)
                
            dfrom=form.cleaned_data['date_from']
            dto=form.cleaned_data['date_to']
            
            stanowisko=form.cleaned_data['stanowisko']
            kod=form.cleaned_data['kod_stanowiska']
            #print(kod)
            
            
            orz_entry=ORZForm.objects.create(owner=owner,author=request.user,date_from=dfrom)
            if dto:
                orz_entry.date_to=dto
                                            
            orz_entry.run(stanowisko,kod)
            
            if orz_entry.date_from:
                from_date=orz_entry.date_from.strftime("%d.%m.%Y")
            else:
                from_date=''
            result={'code':orz_entry.code_name,'author':orz_entry.author.first_name+' '+orz_entry.author.last_name,
                    'owner':orz_entry.owner.name, 'from':from_date,
                    'to':orz_entry.date_to.strftime("%d.%m.%Y"),
                    'created':orz_entry.date.strftime("%Y-%m-%d %H:%M:%S"),
                    'num':orz_entry.num_cmpds,'status':orz_entry.status_text}
            return JsonResponse(result)
        else:
            return HttpResponse('The "Group" field must be chosen. If you cannot see any choices, you do not have permission to create a form!',status=403)
            
            
    else:
        form=ORZ_Form()
        form.fields['owner'].choices=((item.id,item.name) for item in groups_add)

    orz_entries=ORZForm.objects.filter(owner__in=groups)[::-1]
    
    return render(request,'chembase/orz.html',{'form':form,'entries':orz_entries})


@login_required()
@user_passes_test(lambda u: u.is_superuser)
def edit_group(request, group_id):
    check_password_valid(request)

    if int(group_id) != 0:
        own_group = OwnershipGroup.objects.get(pk=group_id)

        group_form = OwnershipGroupForm(instance=own_group)
    else:
        group_form = OwnershipGroupForm()
        own_group = None

    return render(request, 'chembase/admin_group_edit.html', {'form': group_form,'gr_id':group_id,'group':own_group})

@login_required()
@user_passes_test(lambda u: u.is_superuser)
def save_group(request):
    if request.method == 'POST':
        group_id = int(request.POST.get('group_id'))
        if group_id:
            own_group=OwnershipGroup.objects.get(pk=group_id)
            group_form = OwnershipGroupForm(request.POST, instance=own_group)
        else:
            group_form = OwnershipGroupForm(request.POST)

        if group_form.is_valid():
            group = group_form.save()
            return redirect('chembase:admin_group','%d'%group.id)
        else:
            return render(request, 'chembase/admin_group_edit.html',
                          {'form': group_form, 'gr_id': group_id, 'group': own_group})
