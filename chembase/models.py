from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth.models import User, Permission
import re
import sys, os
import datetime
from subprocess import call, getoutput, run
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
    
class Group(models.Model):
    group_name=models.CharField(max_length=150)
    
    def __str__(self):
        return self.group_name
    
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
    
    group=models.ForeignKey(Group,on_delete=models.PROTECT,blank=True,null=True,default=23)
    storage_temp=models.CharField(max_length=10,blank=True,default=None)
    
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
        
    def set_resp(self,true_or_false):
        current_state=self.inRespZone()
        if current_state!=true_or_false:
            if current_state:
                query_set=RespZone.objects.filter(compound=self)
                query_set.delete()
            if true_or_false:
                RespZone.objects.create(compound=self)
        
    def inRespZone(self):
        query_set=RespZone.objects.filter(compound=self)
        ans=bool(query_set)
        
        return ans
        
    def set_paper(self,true_or_false):
        current_state=self.isPaperSDS()
        if current_state!=true_or_false:
            if current_state:
                query_set=PaperSDS.objects.filter(compound=self)
                query_set.delete()
            if true_or_false:
                PaperSDS.objects.create(compound=self)
        
    def isPaperSDS(self):
        query_set=PaperSDS.objects.filter(compound=self)
        ans=bool(query_set)
        
        return ans
        
    def was_active(self,item_owner,date):
        items=self.item_set.filter(owner__exact=item_owner)
        for item in items:
            if item.was_existing(date):
                active=True
                break
        else:
            active=False
        
        return active
        
    def render_image(molfile,png_data,image_id):
        
        if png_data:
            image_png=png_data
            temp_image='/home/marcin/Dokumenty/projekty/production/Chem/chembase/static/chembase/temp/temp'+image_id+'.png'
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
            
            file_name='/home/marcin/Dokumenty/projekty/production/Chem/chembase/static/chembase/temp/temp'+image_id+'.png'
            #file_name='temp.png'
            renderer.renderToFile(mol, file_name)

        image_path='/static/chembase/temp/temp'+image_id+'.png?timestamp=' + str(timezone.now())
        return image_path
        
    def save_sds(sdsfile):
        file_base='/home/marcin/Dokumenty/projekty/production/Chem/chembase/static/chembase/temp/temp'
        file_name=file_base+'.pdf'
        file_txt=file_base+'.txt'
        with open(file_name, 'wb+') as destination:
            for chunk in sdsfile.chunks():
                destination.write(chunk)
        command='pdftotext -layout '+file_name+' '+file_txt
                #print command
        call(command,shell=True)
        output=transform_sds(file_txt)
        delete_files='rm '+file_name
        getoutput(delete_files)
        delete_files_txt='rm '+file_txt
        getoutput(delete_files_txt)
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
    compound=models.ForeignKey(Compound,on_delete=models.CASCADE,related_name='ghs_class_numbers')
    ghs_class=models.ForeignKey(GHSClass,on_delete=models.CASCADE,related_name='ghs_class_numbers')
    number=models.CharField(max_length=10)
  

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
    
    quantity=models.IntegerField(blank=True,null=True,default=1)
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
            
    def was_existing(self,date):
        exists=1
        all_entries=self.history_set.all()
        if all_entries:
            exists=0
            log_entries=self.history_set.filter(date__lte=date)
            if log_entries:
                last_entry=log_entries.latest()
                if last_entry.action=='1':
                    exists=0
                else:
                    exists=1
            else:
                exists=0
            
        return exists
            
    def is_allowed(self,user,perm):
        item_owner=self.owner         
            
        return ExtraPermissions.check_perm(user,perm,item_owner)
        
    def suggest_loc(cmpd_id,user,owner_group,ignore_temp="false"):
        
        compound=Compound.objects.get(pk=cmpd_id)
    
        existing_items=compound.item_set(manager='citems').existing()
        deleted_items=compound.item_set(manager='citems').deleted()
        
        allowed_existing=compound.item_set(manager='citems').allowed(user,existing_items)
    
        allowed_deleted=compound.item_set(manager='citems').allowed(user,deleted_items)
        
        existing_loc=[item['a'].local for item in allowed_existing if (item['a'].owner.name==owner_group or not owner_group)]
        deleted_loc=[item['a'].local for item in allowed_deleted if (item['a'].owner.name==owner_group or not owner_group)]
        
        ###group_loc
        group_items=Item.objects.filter(compound__group__exact=compound.group)
        
        if (compound.storage_temp and ignore_temp=="false"):
            group_items=group_items.filter(compound__storage_temp__exact=compound.storage_temp)
        
        group_df=pd.DataFrame()
        
        group_items_allowed=compound.item_set(manager='citems').allowed(user,group_items)

        for i,item in enumerate(group_items_allowed):
            if not item['a'].is_deleted():
                if (item['a'].owner.name==owner_group or not owner_group):
                    group_df.loc[i,'item_id']=item['a'].id
                    group_df.loc[i,'loc']=item['a'].local
                    group_df.loc[i,'room']=item['a'].room
                    group_df.loc[i,'place']=item['a'].place
                    group_df.loc[i,'place_num']=item['a'].place_num
                    code_search=re.match(r'(\D*)(\d*)',item['a'].place_num)
                    if code_search:
                        group_df.loc[i,'place_code']=code_search.group(1)
                        group_df.loc[i,'place_code_num']=code_search.group(2)
                    else:
                        group_df.loc[i,'place_code']=''
                        group_df.loc[i,'place_code_num']=''
                    group_df.loc[i,'place_id']=group_df.loc[i,'room']+'-'+group_df.loc[i,'place']+'-'+group_df.loc[i,'place_code']
                
        if not group_df.empty:
            grouped=group_df['item_id'].groupby(group_df['place_id']).count()
            group_loc=[[item,'%d'%grouped[item]] for item in grouped.index.tolist()]
        else:
            group_loc=[]
        values_dict={'compound':compound.name,'group_name':compound.group.group_name,"st_temp":compound.storage_temp,'existing':existing_loc,'deleted':deleted_loc,'group':group_loc}
        
        return values_dict

        

            
                    
class Annotation(models.Model):
    item=models.ForeignKey(Item,on_delete=models.CASCADE)
    annotation=models.TextField(blank=True)
    
    def __str__(self):
        
        return self.item.__str__()+' - '+self.annotation
    
class Ewidencja(models.Model):
    compound=models.ForeignKey(Compound,on_delete=models.CASCADE)
    text=models.CharField(max_length=50)
    
class RespZone(models.Model):
    compound=models.ForeignKey(Compound,on_delete=models.CASCADE)

class PaperSDS(models.Model):
    compound=models.ForeignKey(Compound,on_delete=models.CASCADE)

    
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
        
class ORZForm(models.Model):
    code_name=models.CharField(max_length=20)
    author=models.ForeignKey(User,on_delete=models.PROTECT)
    date=models.DateTimeField(auto_now_add=True)
    date_from=models.DateTimeField(blank=True,null=True)
    date_to=models.DateTimeField(blank=True,null=True,default=timezone.now)
    owner=models.ForeignKey(OwnershipGroup,on_delete=models.PROTECT)
    pdf_url=models.CharField(max_length=300,blank=True)
    csv_url=models.CharField(max_length=300,blank=True)
    status_text=models.CharField(max_length=100,blank=True)
    num_cmpds=models.IntegerField(blank=True,null=True,default=1)
    
    class Meta:
        get_latest_by = 'date'
        
    def __str__(self):
        return self.code_name
    
    def run(self,stanowisko,kod):
        cmpds=self.find_compounds()
        self.set_code()
        current_dir=self.create_dir()
        self.create_csv(cmpds,current_dir)
        self.create_tex(current_dir,stanowisko,kod)
        self.run_PdfLaTeX(current_dir)
        self.run_PdfLaTeX(current_dir)
        
        self.pdf_url=current_dir+'ORZaII.pdf'
        self.save()
        
    def create_dir(self):
            
        base_dir='/home/marcin/Dokumenty/projekty/production/Chem/chembase/static/chembase/data/orz/'
        full_dir=base_dir+self.code_name+'/'
        
        if not os.path.exists(full_dir):
            os.makedirs(full_dir)
            
        return full_dir
    
    
    def set_code(self):
        
        self.code_name=('{:04d}'.format(self.owner.id)+'{:04d}'.format(self.author.id)
                    +'{:04d}'.format(self.num_cmpds)+'{:04d}'.format(self.id))
        self.save()
    
    def find_compounds(self):
        
        compounds=Compound.objects.filter(item__owner__exact=self.owner,item__hidden__exact=False,
                                          ghs_class_numbers__ghs_class__isnull=False).distinct()
        compounds_final=compounds                    
        if self.date_from:
            compounds_final=[]
            for item in compounds:
                if not item.was_active(self.owner,self.date_from):
                    if item.was_active(self.owner,self.date_to):
                        compounds_final.append(item)
        else:
            compounds_final=[]
            for item in compounds:
                if item.was_active(self.owner,self.date_to):
                    compounds_final.append(item)
                                          
        self.num_cmpds=len(compounds_final)
        self.save()
        
        return compounds_final
        
        
        
        
    def latex_text(self,text):
        chars=[("\\",r"\textbackslash{}"),(r"{",r"\{"),("}",r"\}"),("%",r'\%'),
               ("#",r"\#"),("$",r"\$"),("^",r"\^{}"),("&",r"\&"),("_",r"\_"),
               ("~",r"\~{}")]
               
        formatted_text=text
        for (x,y) in chars:
            formatted_text=formatted_text.replace(x,y)
            
        return formatted_text
        
    
    
    def create_csv(self,compounds,current_dir):
        
        df_cols=['Name_tex','Name','CAS','amount','Explosives','UnstableExplosives',
                            'Flammable','Self-reactive','Pyrophoric','Self-heating',
                            'Water-emission','Peroxides','Oxidizers','Gas_pressure',
                            'Skin corrosion','Eye damage','AcuteTox123','AcuteTox4',
                            'Skin/eye irritation','Skin_allergy','SpecTargetOrgan3',
                            'Resp_allergy','Mutag','Cancer','ReproductiveTox',
                            'SpecTargetOrgan12','AspirationHazard','ReprLact', 
                            'breathing_zone','sds','sds_tex']
                            
        orz_df=pd.DataFrame(columns=df_cols)
                                          
        for j,cmpd in enumerate(compounds):
            
            i=j+1
            cname=cmpd.name
            csub=cmpd.subtitle
            cpl=cmpd.pl_name
            cpls=cmpd.pl_subtitle
            sub=0
            
            if csub:
                en_name=cname+', '+csub
                sub=1
            else:
                en_name=cname
                
            if cpl:
                pl_name=cpl
                if cpls:
                    pl_name=cpl+', '+cpls
                elif sub:
                    pl_name=''
            else:
                pl_name=''
                
            full_name=pl_name or en_name
                
            orz_df.loc[i,'Name']=full_name
            orz_df.loc[i,'Name_tex']=self.latex_text(full_name)
            orz_df.loc[i,'CAS']=cmpd.cas
            orz_df.loc[i,'amount']=cmpd.dailyused

            for item in Cmpd_Class.objects.filter(compound__exact=cmpd):
                ghs=item.ghs_class.class_text
                num=item.number
                orz_df.loc[i,ghs]=num
            if cmpd.inRespZone():
                orz_df.loc[i,'breathing_zone']='TAK'
            else:
                orz_df.loc[i,'breathing_zone']='NIE'
            if cmpd.isPaperSDS():
                orz_df.loc[i,'sds']='P'
                orz_df.loc[i,'sds_tex']=r'P\\\hline'
            else:
                orz_df.loc[i,'sds']='E'
                orz_df.loc[i,'sds_tex']=r'E\\\hline'
                
        orz_df.fillna('')

        csv_cols=df_cols[1:30]

        tex_cols=df_cols[0:1]+df_cols[2:29]+df_cols[30:31]     
        
        orz_df.to_csv(current_dir+'orz.csv',sep=',',columns=csv_cols)
        orz_df.to_csv(current_dir+'/orz_tex.csv',sep='&',columns=tex_cols,header=False)
        
        self.csv_url=current_dir+'orz.csv'
        self.save()
        
        
    def create_tex(self,current_dir,stanowisko,kod):
        
        templ=open('/home/marcin/Dokumenty/projekty/production/Chem/chembase/static/chembase/data/ORZ_templ.tex','r').read()
        
        contents=open(current_dir+'orz_tex.csv','r').read()
        
        full=templ%({'code':self.code_name,'contents':contents,'date':self.date_to.strftime("%d.%m.%Y"),
                     'user':self.author.first_name+' '+self.author.last_name,
                     'time':self.date.strftime("%Y-%m-%d %H:%M:%S"),'stanowisko':stanowisko,'kod':kod})
        
        full_file=open(current_dir+'ORZaII.tex','w')
        full_file.write(full)
        
    def run_PdfLaTeX(self,current_dir):
        
        run(["pdflatex", "--shell-escape", "-synctex=1", "-interaction=nonstopmode", "ORZaII.tex"],cwd=current_dir)

    
    
    

    

    
    