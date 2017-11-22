from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth.models import User, Permission
import re
import sys, os
from subprocess import call
import pandas as pd
from difflib import SequenceMatcher
sys.path.append('/home/marcin/Dokumenty/programy/indigo-python-1.2.3.r0-linux/')

#import indigo
from indigo import *
from indigo_inchi import *
from indigo_renderer import *
from bingo import *

from .functions import transform_sds

#from rdkit import Chem
#from rdkit import DataStructs
#from rdkit.Chem.Fingerprints import FingerprintMols
#from rdkit.Chem import rdqueries
# Create your models here.

class OwnershipGroup(models.Model):
    name=models.CharField(max_length=500)
    
    def __str__(self):
        return self.name
        
class UserProfile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    own_groups=models.ManyToManyField(OwnershipGroup,blank=True)
    
    def __str__(self):
        return str(self.user.username)+': '+str(self.own_groups.all())
        
        
class ExtraPermissions(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    group=models.ForeignKey(OwnershipGroup, on_delete=models.CASCADE,blank=True)
    permission=models.ForeignKey(Permission, on_delete=models.PROTECT,blank=True)
    
    def __str__(self):
        return str(self.user.username)+': '+str(self.group.name)+', '+str(self.permission)
        
    def check_perm(user,perm,group=None):
        
        q=Q(user__exact=user,permission__codename__exact=perm.split('.')[1])
        
        if group:
            q=q & Q(group__exact=group)
        
        user_extra_perms=ExtraPermissions.objects.filter(q)

        if user_extra_perms:
            return True
        else:
            return False
            

class Pictogram(models.Model):
    code=models.CharField(max_length=10)
    path=models.FilePathField(max_length=200)
    
    def __str__(self):
        return self.code
    
class GHSClass(models.Model):
    class_text=models.CharField(max_length=100)
    class_full_en=models.CharField(max_length=300,blank=True)
    class_full_pl=models.CharField(max_length=300,blank=True)
    
    def __str__(self):
        return self.class_text
    
class H_Pict_Class(models.Model):
    h_code=models.CharField(max_length=8)
    pictogram=models.ForeignKey(Pictogram,on_delete=models.PROTECT)
    ghs_class=models.ForeignKey(GHSClass,on_delete=models.PROTECT)
    
class ExtraCompoundsManager(models.Manager):
    
    def existing(self,qset):
        final_set=[]
        for compound in qset:
            if compound.how_many_items()!=0:
                final_set.append(compound)
        return final_set
        
    def allowed_cmpds(self,user,qset):
        final_set=[]
        for compound in qset:
            if compound.how_many_allowed(user)!=0:
                final_set.append(compound)
        return final_set
        
    def sort_by_name_simil(self,qset,text,cutoff):
        final_list=[[s,s.name_similarity(text)] for s in qset]
        
        fin_list=[[s[0],s[1]] for s in final_list if s[1]>cutoff]
        fin_list2=sorted(fin_list,key=lambda s: s[1],reverse=True)
        
        return [s[0] for s in fin_list2]
        
    def sort_by_str_simil(self,qset,smiles,cutoff):
        final_list=[[s,s.smiles_similarity(smiles)] for s in qset]
        
        fin_list=[[s[0],s[1]] for s in final_list if s[1]>cutoff]
        
        fin_list2=sorted(fin_list,key=lambda s: s[1],reverse=True)
        
        return [s[0] for s in fin_list2]
        
    def substr_match(self,qset,smiles,cutoff):
        final_set=[]
        for compound in qset:
            match=compound.is_substructure(smiles)
            if match:
                final_set.append((compound,match))

        final_list=sorted(final_set,key=lambda s: s[1],reverse=True)
        
        return [x[0] for x in final_list if x[1]>cutoff]
        
        
    

class Compound(models.Model):
    name=models.CharField('Name (english)',max_length=2000)
    all_names=models.CharField(max_length=5000,blank=True)
    subtitle=models.CharField(max_length=1000,blank=True)
    pl_name=models.CharField('Name (polish)',max_length=2000,blank=True)
    pl_subtitle=models.CharField('Subtitle (polish)',max_length=1000,blank=True)
    cas=models.CharField('CAS',max_length=100,blank=True)
    csid=models.CharField('ChemSpider Id',max_length=15,blank=True)
    
    formula=models.CharField(max_length=100,blank=True)
    weight=models.DecimalField("Molecular weight",max_digits=10,decimal_places=4,null=True,blank=True)
    density=models.CharField(max_length=100,blank=True)
    
    image=models.CharField(max_length=300,blank=True)
    
    inchi=models.CharField('InChi',max_length=1000,blank=True)
    smiles=models.CharField('SMILES',max_length=1000,blank=True)
    molfile=models.TextField(blank=True)
    
    sds=models.CharField('SDS',max_length=300,blank=True)
    sds_name=models.CharField(max_length=2000,blank=True)
    sds_cas=models.CharField(max_length=100,blank=True)
    
    pictograms=models.ManyToManyField(Pictogram,blank=True)
    
    warning=models.CharField(max_length=200,blank=True)
    
    h_numbers=models.CharField(max_length=2000,blank=True)
    h_text=models.TextField(blank=True)
    
    p_numbers=models.CharField(max_length=2000,blank=True)
    p_text=models.TextField(blank=True)
    
    classification=models.TextField(blank=True)
    
    class_extr=models.ManyToManyField(GHSClass,through='Cmpd_Class')
    
    adr_num=models.CharField(max_length=15,blank=True)
    adr_class=models.CharField(max_length=15,blank=True)
    adr_group=models.CharField(max_length=15,blank=True)
    
    dailyused=models.CharField("Daily usage",max_length=15,blank=True)
    
    author=models.ForeignKey(User,on_delete=models.PROTECT,default=1)
    
    extra_methods=ExtraCompoundsManager()
    objects=models.Manager()
        
    def __str__(self):
        return self.name
        
    def formulaHTML(self):
        html_form=re.sub(r'_{(?P<num>.*?)}',r'<sub>\g<num></sub>',self.formula)
        html_form=re.sub(r'\cdot',r'&middot;',html_form)
        html_form=re.sub(r'\.',r'&middot;',html_form)
        return html_form
        
    def name_similarity(self,text):
        
        main=SequenceMatcher(None, text, self.name).ratio()
        pl=SequenceMatcher(None, text, self.pl_name).ratio()
        all_n=SequenceMatcher(None, text, self.all_names).ratio()
        cas_n=SequenceMatcher(None, text, self.cas).ratio()
        
        return max([main,pl,all_n,cas_n])
    
    def smiles_similarity(self,smiles):

        indigo=Indigo()

        query_mol=indigo.loadQueryMolecule(smiles)
        query_mol.aromatize()

        mol=indigo.loadMolecule(self.smiles)
        mol.aromatize()
        query_fp=query_mol.fingerprint('sim')
        mol_fp=mol.fingerprint('sim')
        
        similarity=indigo.similarity(query_fp,mol_fp,'tanimoto')
        
        return similarity
    
    def is_substructure(self,smiles):
        indigo=Indigo()
        mol=indigo.loadMolecule(self.smiles)
        mol.aromatize()
        
        matcher=indigo.substructureMatcher(mol)
        
        query_mol=indigo.loadQueryMolecule(smiles)
        query_mol.aromatize()
        
        match=matcher.match(query_mol)
        #print(match)
        if match:
            return self.smiles_similarity(smiles)
        else:
            return 0
            
    def how_many_items(self):
        return len(self.item_set(manager='citems').existing())
        
    def how_many_allowed(self,user):
        qset=self.item_set.all()
        return len(self.item_set(manager='citems').allowed(user,qset))
        
    def edit_allowed(self,user):
        item_set=self.item_set.all()
        allowed=True
        for item in item_set:
            if not item.is_allowed(user,'chembase.change_item'):
                allowed=False
                break
        
        return allowed
            
        
    def set_registered(self,true_or_false):
        current_state=self.is_registered()
        if current_state!=true_or_false:
            if current_state:
                query_set=Ewidencja.objects.filter(compound=self)
                query_set.delete()
            if true_or_false:
                Ewidencja.objects.create(compound=self,text='ewidencja')
        
    def is_registered(self):
        query_set=Ewidencja.objects.filter(compound=self)
        if query_set:
            ans=True
        else:
            ans=False
            
        return ans
        
    def render_image(molfile,png_data):
        
        if png_data:
            image_png=png_data
            temp_image='/home/marcin/Dokumenty/projekty/production/Chem/chembase/static/chembase/temp/temp.png'
            with open(temp_image, 'wb+') as destination:
                destination.write(image_png)
                #for chunk in image_png.chunks():
                #   destination.write(chunk)
        elif molfile:
            indigo=Indigo()
            mol=indigo.loadMolecule(molfile)
            #mol.aromatize()
            renderer = IndigoRenderer(indigo)
            
            indigo.setOption("render-output-format", "png");
            indigo.setOption("render-margins", 50, 50)
            indigo.setOption("render-coloring", True)
            indigo.setOption("render-relative-thickness", 1.2)
            indigo.setOption("render-bond-line-width", 1.5)
            
            file_name='/home/marcin/Dokumenty/projekty/production/Chem/chembase/static/chembase/temp/temp.png'
            #file_name='temp.png'
            renderer.renderToFile(mol, file_name)

        image_path='/static/chembase/temp/temp.png?timestamp=' + str(timezone.now())
        return image_path
        
    def save_sds(sdsfile):
        file_base='/home/marcin/Dokumenty/projekty/production/Chem/chembase/static/chembase/temp/temp.png'
        file_name=file_base+'.pdf'
        file_txt=file_base+'.txt'
        with open(file_name, 'wb+') as destination:
            for chunk in sdsfile.chunks():
                destination.write(chunk)
        command='pdftotext -layout '+file_name+' '+file_txt
                #print command
        call(command,shell=True)
        output=transform_sds(file_txt)
        
        return output
    


    def clean_formula(formula):
        i=0
        j=0
        el_data=pd.read_csv("/home/marcin/Dokumenty/projekty/production/Chem/chembase/static/chembase/data/elementlist.csv")
        new_df=pd.DataFrame(columns=['Sym','Num','Order'])
        
        par=True
        while par==True:
        	try:
        		char=formula[i]
        	except:
        		par=False
        		break
        	if char.isupper():
        		j=j+1
        		new_df.loc[j,'Sym']=char
        		new_df.loc[j,'Num']=''
        	if char.islower():
        		new_df.loc[j,'Sym']=new_df.loc[j,'Sym']+char
        	if char.isdigit():
        		new_df.loc[j,'Num']=new_df.loc[j,'Num']+char
        	i=i+1
        
        for item in new_df.index.tolist():
            symb=new_df.loc[item,'Sym']
            order=el_data.loc[el_data['Sym']==symb]['Order']
            order=order.iloc[0]
            new_df.loc[item,'Order']=order
        	
        new_df=new_df.sort_values(['Order'])
        
        new_formula=''
        for item in new_df.index.tolist():
            symb=new_df.loc[item,'Sym']
            num=new_df.loc[item,'Num']
            new_formula=new_formula+symb
            if num!="":
                new_formula=new_formula+'_{'+num+'}'
                
        return new_formula        
    
class Cmpd_Class(models.Model):
    compound=models.ForeignKey(Compound,on_delete=models.CASCADE)
    ghs_class=models.ForeignKey(GHSClass,on_delete=models.CASCADE)
    number=models.CharField(max_length=10)

class Group(models.Model):
    group_name=models.CharField(max_length=150)
    
    def __str__(self):
        return self.group_name
    
    

class ItemManager(models.Manager):

    def get_queryset(self):
        return super(ItemManager, self).get_queryset()
        
    def existing(self):
        ex_items=[]
        for item in self.get_queryset():
            if not item.is_deleted():
                ex_items.append(item)              
        return ex_items
        
    def deleted(self):
        del_items=[]
        for item in self.get_queryset():
            if item.is_deleted():
                del_items.append(item)              
        return del_items
        
    def allowed(self,user,qset):
        allowed_items=[]
        for item in qset:
            if item.is_allowed(user,'chembase.can_see_item'):
                if item.is_allowed(user,'chembase.change_item'):
                    allowed_items.append({'a':item,'edit':True})
                else:
                    allowed_items.append({'a':item,'edit':False})
        return allowed_items
        
 
        
        
class Item(models.Model):
    compound=models.ForeignKey(Compound,on_delete=models.PROTECT)
    room=models.CharField(max_length=20)
    place=models.CharField(max_length=20)
    place_num=models.CharField(max_length=20)
            
    local=models.CharField(max_length=65,blank=True)
    
    quantity=models.IntegerField(blank=True,null=True)
    amount=models.DecimalField(max_digits=10,decimal_places=3,blank=True,null=True)
    
    storage_temp=models.CharField(max_length=10,blank=True)
    
    group=models.ForeignKey(Group,on_delete=models.PROTECT,blank=True,null=True)
    hidden=models.BooleanField()
    
    owner=models.ForeignKey(OwnershipGroup,on_delete=models.PROTECT,default=2)
    
    objects = models.Manager()  # Default Manager
    citems = ItemManager()
    
    class Meta:
        ordering = ['group']
          
    def __str__(self):
        return self.compound.__str__()+' - '+self.local
    
    def localize(self):
        return self.room+'-'+self.place+'-'+self.place_num
        
    def delete(self):
        del_item=History(item=self,action='1')
        del_item.save()
        
    def restore(self):
        del_item=History(item=self,action='restored')
        del_item.save()
    
    def is_deleted(self):
        log_entries=self.history_set.all()
        if log_entries:
            last_entry=log_entries.latest()
            if last_entry.action=='1':
                return 1
            else:
                return 0
        else:
            return 0
            
    def is_allowed(self,user,perm):
        item_owner=self.owner         
            
        return ExtraPermissions.check_perm(user,perm,item_owner)

            
                    
class Annotation(models.Model):
    item=models.ForeignKey(Item,on_delete=models.CASCADE)
    annotation=models.TextField(blank=True)
    
    def __str__(self):
        
        return self.item.__str__()+' - '+self.annotation
    
class Ewidencja(models.Model):
    compound=models.ForeignKey(Compound,on_delete=models.CASCADE)
    text=models.CharField(max_length=50)
    
class History(models.Model):
    item=models.ForeignKey(Item,on_delete=models.CASCADE)
    date=models.DateTimeField(auto_now_add=True)
    action=models.CharField(max_length=30)
    
    class Meta:
        get_latest_by = 'date'
        
class SystemLog(models.Model):
    model_name=models.CharField(max_length=50)
    model_instance_id=models.IntegerField()
    author=models.ForeignKey(User,on_delete=models.PROTECT)
    date=models.DateTimeField(auto_now_add=True)
    action=models.CharField(max_length=300)
    comment=models.CharField(max_length=1000,blank=True)
    
    def __str__(self):
        return str(self.date)+' - '+self.model_name+' '+str(self.model_instance_id)
        
    class Meta:
        get_latest_by = 'date'
    

    

    
    