from django.db import models
import re

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
    
    def __str__(self):
        return self.name
        
    def formulaHTML(self):
        html_form=re.sub(r'_{(?P<num>.*?)}',r'<sub>\g<num></sub>',self.formula)
        html_form=re.sub(r'\cdot',r'&middot;',html_form)
        html_form=re.sub(r'\.',r'&middot;',html_form)
        print(html_form)
        return html_form
    
    
class Cmpd_Class(models.Model):
    compound=models.ForeignKey(Compound,on_delete=models.PROTECT)
    ghs_class=models.ForeignKey(GHSClass,on_delete=models.PROTECT)
    number=models.CharField(max_length=10)

class Group(models.Model):
    group_name=models.CharField(max_length=150)
    
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
    
    def localize(self):
        return self.room+'-'+self.place+'-'+self.place_num
    
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

    

    
    