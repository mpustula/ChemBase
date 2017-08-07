from django.db import models
import re
import sys
from difflib import SequenceMatcher
sys.path.append('/home/marcin/Dokumenty/programy/indigo-python-1.2.3.r0-linux')

from indigo import *
from indigo_inchi import *
from indigo_renderer import *
from bingo import *

#from rdkit import Chem
#from rdkit import DataStructs
#from rdkit.Chem.Fingerprints import FingerprintMols
#from rdkit.Chem import rdqueries
# Create your models here.



class Pictogram(models.Model):
    code=models.CharField(max_length=10)
    path=models.FilePathField(max_length=200)
    
    def __str__(self):
        return self.code
    
class GHSClass(models.Model):
    class_text=models.CharField(max_length=100)
    
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
        
    def sort_by_name_simil(self,qset,text):
        return sorted(qset,key=lambda s: s.name_similarity(text),reverse=True)
        
    def sort_by_str_simil(self,qset,smiles):
        return sorted(qset,key=lambda s: s.smiles_similarity(smiles),reverse=True)
    

class Compound(models.Model):
    name=models.CharField('Name (english)',max_length=2000)
    all_names=models.CharField(max_length=5000,blank=True)
    subtitle=models.CharField(max_length=1000,blank=True)
    pl_name=models.CharField('Name (polish)',max_length=2000,blank=True)
    pl_subtitle=models.CharField('Subtitle (polish)',max_length=1000,blank=True)
    cas=models.CharField('CAS',max_length=100,blank=True)
    csid=models.CharField('ChemSpider Id',max_length=15,blank=True)
    
    formula=models.CharField(max_length=100,blank=True)
    weight=models.DecimalField("Molecular weight",max_digits=10,decimal_places=3,blank=True)
    density=models.CharField(max_length=100,blank=True)
    
    image=models.FilePathField(max_length=200,blank=True)
    
    inchi=models.CharField('InChi',max_length=1000,blank=True)
    smiles=models.CharField('SMILES',max_length=1000,blank=True)
    
    sds=models.FilePathField('SDS',max_length=200,blank=True)
    sds_name=models.CharField(max_length=2000,blank=True)
    sds_cas=models.CharField(max_length=100,blank=True)
    
    pictograms=models.ManyToManyField(Pictogram)
    
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
        
        return max([main,pl,all_n])
    
    def smiles_similarity(self,smiles):

        #smiles=smiles_.replace('[*]','*')

        indigo=Indigo()

        query_mol=indigo.loadQueryMolecule(smiles)

        mol=indigo.loadMolecule(self.smiles)
        
        query_fp=query_mol.fingerprint('sim')
        mol_fp=mol.fingerprint('sim')
        
        similarity=indigo.similarity(query_fp,mol_fp,'tanimoto')
        
        return similarity
    
#        #query_mol=Chem.MolFromSmiles(smiles)
#        
#        qm=self.adjustQuery(query_mol)
#        sma = Chem.MolToSmarts(qm)
#        #print sma
#        query=FingerprintMols.FingerprintMol(query_mol)
#
#        cutoff=float(self.Cutoff.value())
#
#        if self.smiles!="":
#            mol=Chem.MolFromSmiles(self.smiles)
#            if mol:
#                fp=FingerprintMols.FingerprintMol(mol)
#                similarity=DataStructs.FingerprintSimilarity(query,fp)
#            else:
#                similarity=0
#        else:
#            similarity=0
#        
#        return similarity

#        for item in self.df_result.index.tolist():
#            smiles0=self.df_result.loc[item,'smiles']
#            if smiles0<>"":
#                mol=Chem.MolFromSmiles(smiles0)
#                if mol:
#                    fp=FingerprintMols.FingerprintMol(mol)
#                    sim=DataStructs.FingerprintSimilarity(querry,fp)
#                    self.df_result.loc[item,'similarity']=sim
#                    
#                    
#                    if self.radioSub.isChecked():
#                        if '*' in smiles:
#                            sub=mol.HasSubstructMatch(Chem.MolFromSmarts(sma))
#                        else:
#                            sub=mol.HasSubstructMatch(querry_mol)
#                        self.df_result.loc[item,'substr']=sub
#                else:
#                    print item, self.df_result.loc[item,'Name']
#            else:
#                self.df_result.loc[item,'similarity']=0
#                self.df_result.loc[item,'substr']=0
#        if self.radioSim.isChecked():
#            self.df_result=self.df_result[self.df_result['similarity']>=cutoff]
#        if self.radioSub.isChecked():
#            self.df_result=self.df_result[self.df_result['substr']==True]
#        
#        self.df_result=self.df_result.sort_values(['similarity'],ascending=0)
#        self.parent.show_result(self.df_result)
    
    def adjustQuery(self,m,ringsOnly=True,ignoreDummies=True):
        qm =Chem.RWMol(m)
        if ringsOnly:           
            ri = qm.GetRingInfo()
            try:
                ri.NumRings()
            except RuntimeError:
                ri=None
                Chem.FastFindRings(qm)
                ri = qm.GetRingInfo()
        for atom in qm.GetAtoms():
            if ignoreDummies and not atom.GetAtomicNum():
                continue
            if ringsOnly and not ri.NumAtomRings(atom.GetIdx()):
                continue
    
            oa = atom
            if not atom.HasQuery():
                needsReplacement=True
                atom = rdqueries.AtomNumEqualsQueryAtom(oa.GetAtomicNum())
                atom.ExpandQuery(rdqueries.IsAromaticQueryAtom(oa.GetIsAromatic()))
                if(oa.GetIsotope()):
                    atom.ExpandQuery(rdqueries.IsotopeEqualsQueryAtom(oa.GetIsotope()))
                if(oa.GetFormalCharge()):
                    atom.ExpandQuery(rdqueries.FormalChargeEqualsQueryAtom(oa.GetFormalCharge()))
            else:
                needsReplacement=False
            atom.ExpandQuery(rdqueries.ExplicitDegreeEqualsQueryAtom(oa.GetDegree()))
            if needsReplacement:
                qm.ReplaceAtom(oa.GetIdx(),atom)            
        return qm    
        
    def how_many_items(self):
        return len(self.item_set(manager='citems').existing())
        
        
    
    
class Cmpd_Class(models.Model):
    compound=models.ForeignKey(Compound,on_delete=models.PROTECT)
    ghs_class=models.ForeignKey(GHSClass,on_delete=models.PROTECT)
    number=models.CharField(max_length=10)

class Group(models.Model):
    group_name=models.CharField(max_length=150)
    
    

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
            
class Item(models.Model):
    compound=models.ForeignKey(Compound,on_delete=models.PROTECT)
    room=models.CharField(max_length=20)
    place=models.CharField(max_length=20)
    place_num=models.CharField(max_length=20)
    quantity=models.IntegerField(blank=True)
    amount=models.DecimalField(max_digits=10,decimal_places=3,blank=True)
    storage_temp=models.CharField(max_length=10,blank=True)
    group=models.ForeignKey(Group,on_delete=models.PROTECT,blank=True,null=True)
    hidden=models.BooleanField()
    
    objects = models.Manager()  # Default Manager
    citems = ItemManager()
    
    class Meta:
        ordering = ['group']
        
    def localize(self):
        return self.room+'-'+self.place+'-'+self.place_num
    
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
                    
class Annotation(models.Model):
    item=models.ForeignKey(Item,on_delete=models.CASCADE)
    annotation=models.TextField(blank=True)
    
class Ewidencja(models.Model):
    compound=models.ForeignKey(Compound,on_delete=models.CASCADE)
    text=models.CharField(max_length=50)
    
class History(models.Model):
    item=models.ForeignKey(Item,on_delete=models.CASCADE)
    date=models.DateTimeField()
    action=models.CharField(max_length=30)
    
    class Meta:
        get_latest_by = 'date'

    

    
    