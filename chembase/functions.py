# -*- coding: utf-8 -*-
"""
Created on Fri Aug  4 08:59:29 2017

@author: marcin
"""
import re
import pandas as pd
#from .models import H_Pict_Class

def transform_sds(txt_file):
    ghs_codes=pd.read_csv('chembase/static/chembase/data/GHSCodes.csv',sep=';',index_col='Code')
    ghs_codes=ghs_codes.fillna('')

    f=open(txt_file,'r')  
    lines=f.readlines()
    name='ERROR'
    cas='ERROR'
    for line_i,item in enumerate(lines):
        if ("Nazwa" in item or "name" in item):
            try:
                name=(item.split(':')[1]).strip()
            except:
                pass
        if "CAS" in item:
            try:
                cas=(item.split(':')[1]).strip()
            except:
                pass
            break
    H=[]
    H_text=''
    P=[]
    P_text=''
    H_start=0
    P_start=0
    clas_start=0
    clas_text=''
    signal_word='error'
    for line_,item in enumerate(lines):
        item_=item.strip()
        if item_!="":
            if 'Uzupełniające zwroty' in item:
                break
            if item_[:3]=='2.3':
                break
            if 'Klasyfikacja zgodnie z Rozporządzeniem (WE) nr 1272/2008' in item:
                clas_start=1
                continue
            if 'Pełny tekst zwrotów H' in item:
                clas_start=0
                continue
            if (clas_start==1 and not ('Strona' in item)):
                clas_text=clas_text+item_+'. '
            if 'Hasło ostrzegawcze' in item:
                signal_word=item.split()[2]
            if 'rodzaj zagrożenia' in item:
                H_start=1
                continue
            if 'środki ostrożności' in item:
                H_start=0
                P_start=1
                continue
            if (H_start==1 and not ('Strona' in item)):
                H_text=H_text+re.sub("\s\s+", " ", item_)+' '
            if (P_start==1 and not ('Strona' in item)):
                P_text=P_text+re.sub("\s\s+", " ", item_)+' '
            if item_[0]=='H':
                matchObj=re.findall(r'H\d{3}',item)
                if matchObj:
                    H=H+matchObj
                    #H_text=H_text+re.sub("\s\s+", " ", item_)+' '
            if item_[0]=='P':
                matchObj=re.findall(r'P\d{3}',item)
                if matchObj:
                    P=P+matchObj
                    #P_text=P_text+re.sub("\s\s+", " ", item_)+' '

           
    H_t=', '.join(H)
    P_t=', '.join(P)
    
    
    #clas_text_extr=''
    clas_df=pd.DataFrame()
    clas_list=clas_text.split('.')
    for item in clas_list:
        matchObj=re.search(r'H\d{3}',item)
        if matchObj:
            clas=ghs_codes.loc[matchObj.group(0),'Class_num']
            if clas!="":
                matchObj2=re.search(r'\(Kategoria (.*?)\)',item)
                if matchObj2:
                    #clas_ext_list.append(clas+'='+matchObj2.group(1))
                    try:
                        current_num=clas_df.loc[clas,'number']
                        if int(matchObj2.group(1))<int(current_num):
                            clas_df.loc[clas,'number']=matchObj2.group(1)
                    except:
                        clas_df.loc[clas,'=']='='
                        clas_df.loc[clas,'number']=matchObj2.group(1)
                else:
                    #clas_ext_list.append(clas+'=')
                    clas_df.loc[clas,'=']='='
                    clas_df.loc[clas,'number']=''
    #clas_text_extr=';'.join(clas_ext_list)
    #print(clas_df)
    clas_extr_dict={str(x):clas_df.loc[x,'number'] for x in clas_df.index.tolist()}
    #print(clas_extr_dict)
    #clas_text_extr=clas_df.to_string(header=False)
        
    pict_df=pd.DataFrame(index=['1','2','3','4','5','6','7','8','9'],columns=['value'])
    #print pict_df
    #print H
    for item in H:
        if item=='H317':
            if not 'H335' in H:
               pict_df.loc[ghs_codes.loc[item,'Pict_short'],'value']=1
        elif (item=='H315' or item=='H319'):
            if not ('H314' in H or 'H318' in H or 'H335' in H):
               pict_df.loc[ghs_codes.loc[item,'Pict_short'],'value']=1 
        else:
            pict_df.loc[ghs_codes.loc[item,'Pict_short'],'value']=1
    #print pict_df
    if pict_df.loc['6','value']==1:
        pict_df.loc['7','value']=0
    pictures=pict_df[pict_df['value']>=1]
    #print pict_df
    #print pictures
    #print pictures
    pic_list=[str(x) for x in pictures.index.tolist()]
    print(pic_list)
        
    un_number='ERROR'
    transport_class='ERROR'
    transport_group='ERROR'
    for ind,item in enumerate(lines):
#                if "Gęstość względna" in item:
#                    #print item
#                    matchObj=re.search(r'względna (.*?) g/cm3',item,re.M|re.I)
#                    if matchObj:        
#                        #print matchObj.group(2)
#                        density=matchObj.group(1).strip()
#                        #print matchObj.group(2)
#                    else:
#                        pass            
#                        print 'No match'
        if item.strip()[0:4]=='14.1':
            #print item
            try:
                un_number=lines[ind+1].split()[1]
            except:
                pass
        if item.strip()[0:4]=='14.3':
            #print item
            try:
                transport_class=lines[ind+1].split()[1]
            except:
                pass
        if item.strip()[0:4]=='14.4':
            #print item
            try:
                transport_group=lines[ind+1].split()[1]
            except:
                pass
            break
        
    return {'name':name,'cas':cas,'H':H_t,'H_text':H_text,'P':P_t,'P_text':P_text,
            'clas_text':clas_text,'signal':signal_word,'clas_extr':clas_extr_dict,
            'pict_list':pic_list,'adr_num':un_number,'adr_class':transport_class,
            'adr_group':transport_group}


class Cmpdlist(object):
    
    def __init__(self,qset):
        self.qset=qset
        
        
    def existing(self):
        final_set=[]
        for item in self.qset():
            if item.how_many_items()!=0:
                final_set.append(item)
                
        return final_set
        

