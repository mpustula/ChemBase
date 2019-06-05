# -*- coding: utf-8 -*-
"""
Created on Fri Aug  4 08:59:29 2017

@author: marcin
"""
import re
import pandas as pd
import sys
from subprocess import call, getoutput, run
import datetime
sys.path.append('/home/marcin/Dokumenty/programy/indigo-python-1.2.3.r0-linux/')
from indigo import *
from indigo_inchi import *
from indigo_renderer import *
from bingo import *
from chemspipy import ChemSpider
import cirpy
import difflib
import pubchempy as pcp

class Molecule(object):

    def __init__(self, molfile = None, smiles = None, inchi = None):
        self.indigo=Indigo()

        structure_id = molfile or smiles or inchi
        if not structure_id:
            raise Exception('No structure data given!')

        self.mol = self.indigo.loadMolecule(structure_id)
        #self.mol.aromatize()
        self.mol_fp = self.mol.fingerprint('sim')

    def build_query(self, query_id):
        query_mol = self.indigo.loadQueryMolecule(query_id)
        query_mol.aromatize()

        return query_mol

    def structure_similarity(self, molfile = None, smiles = None, inchi = None):
        query_mol = self.build_query(molfile or smiles or inchi)

        query_fp = query_mol.fingerprint('sim')
        similarity = self.indigo.similarity(query_fp, self.mol_fp, 'tanimoto')

        return similarity

    def is_substructure(self, molfile = None, smiles = None, inchi = None):
        query_mol=self.build_query(molfile or smiles or inchi)

        matcher = self.indigo.substructureMatcher(self.mol)
        match = matcher.match(query_mol)

        return bool(match)

    def properties(self):
        formula = self.mol.grossFormula()
        mw = self.mol.molecularWeight()
        smile = self.mol.canonicalSmiles()
        indigoinchi = IndigoInchi(self.indigo)
        inChi = indigoinchi.getInchi(self.mol)

        return {'formula': formula, 'mass': '%0.4f' % mw, 'smiles': smile, 'inchi': inChi}

    def clean_structure(self):
        self.mol.layout()
        new_mol = self.mol.molfile()

        return {'new_mol': new_mol}

    def render_image(self, image_id):

        renderer = IndigoRenderer(self.indigo)

        self.indigo.setOption("render-output-format", "png")
        self.indigo.setOption("render-margins", 50, 50)
        self.indigo.setOption("render-coloring", True)
        self.indigo.setOption("render-relative-thickness", 1.3)
        self.indigo.setOption("render-bond-line-width", 1.5)

        file_name = '/home/marcin/Dokumenty/projekty/production/Chem/chembase/static/chembase/temp/temp' + image_id + '.png'
        # file_name='temp.png'
        renderer.renderToFile(self.mol, file_name)

        image_path = '/static/chembase/temp/temp' + image_id + '.png?timestamp=' + str(datetime.datetime.now())
        return image_path

    def clean_formula(formula):
        i = 0
        j = 0
        el_data = pd.read_csv(
            "/home/marcin/Dokumenty/projekty/production/Chem/chembase/static/chembase/data/elementlist.csv")
        new_df = pd.DataFrame(columns=['Sym', 'Num', 'Order'])

        par = True
        while par:
            try:
                char = formula[i]
            except:
                par = False
                break
            if char.isupper():
                j = j + 1
                new_df.loc[j, 'Sym'] = char
                new_df.loc[j, 'Num'] = ''
            if char.islower():
                new_df.loc[j, 'Sym'] = new_df.loc[j, 'Sym'] + char
            if char.isdigit():
                new_df.loc[j, 'Num'] = new_df.loc[j, 'Num'] + char
            i = i + 1

        for item in new_df.index.tolist():
            symb = new_df.loc[item, 'Sym']
            order = el_data.loc[el_data['Sym'] == symb]['Order']
            order = order.iloc[0]
            new_df.loc[item, 'Order'] = order

        new_df = new_df.sort_values(['Order'])

        new_formula = ''
        for item in new_df.index.tolist():
            symb = new_df.loc[item, 'Sym']
            num = new_df.loc[item, 'Num']
            new_formula = new_formula + symb
            if num != "":
                new_formula = new_formula + '_{' + num + '}'

        return new_formula


class ChemSp(object):
    def __init__(self):
        self.cs = ChemSpider('Aat9Dp8QIdEY0nN12R58GdyzXGezl1MM', api_url='https://api.rsc.org')

    def get_cmpd(self,csid):
        return self.cs.get_compound(csid)

    def search(self,query):
        print('Connected to ChemSpider API')
        print("Searching started")
        print("Searching for: " + query)
        i = 0
        results = []
        for result in self.cs.search(query):
            if i > 5:
                break
            print("Compound " + str(i))
            formula = str(result.molecular_formula)
            csid = str(result.csid)
            inchi = result.inchi
            name = result.common_name
            cas = cirpy.resolve(inchi, 'cas')
            iupac_name = cirpy.resolve(inchi, 'iupac_name')

            if type(cas) is list:
                c_cas = query
                sim_cas = difflib.get_close_matches(str(c_cas), cas, 3, 0)
                print(sim_cas)
                cas_ = sim_cas[0]
            else:
                cas_ = cas
            image = result.image_url
            print(image)
            i = i + 1
            result_line = {'csid': csid, 'name': name, 'iupac_name': iupac_name, 'cas': cas_, 'inchi': inchi, \
                           'formula': formula, 'image': image}
            results.append(result_line)

        print("Searching finished")
        print(results)

        return results

    def render_image(self, csid, image_id):

        image_png = self.get_cmpd(csid).image
        temp_image = '/home/marcin/Dokumenty/projekty/django_projects/Chem/chembase/static/chembase/temp/temp' + image_id + '.png'
        with open(temp_image, 'wb+') as destination:
            destination.write(image_png)
        image_path = '/static/chembase/temp/temp' + image_id + '.png?timestamp=' + str(datetime.datetime.now())
        return image_path




class Sds(object):
    def __init__(self,sdsfile):
        self.sdsfile=sdsfile
        self.file_base='/home/marcin/Dokumenty/projekty/django_projects/Chem/chembase/static/chembase/temp/temp'

    def save_temp(self):
        file_name = self.file_base+'.pdf'
        file_txt = self.file_base+'.txt'
        with open(file_name, 'wb+') as destination:
            for line in self.sdsfile:
                destination.write(line)

    def transform_temp(self):
        command='pdftotext -layout '+self.file_base+'.pdf'+' '+self.file_base+'.txt'
        call(command,shell=True)

    def read_contents(self):
        output=self.transform_sds(self.file_base+'.txt')
        return output

    def delete_temp(self):
        delete_files='rm '+self.file_base+'.pdf'
        getoutput(delete_files)
        delete_files_txt='rm '+self.file_base+'.txt'
        getoutput(delete_files_txt)


    def transform_sds(self,txt_file):
        ghs_codes=pd.read_csv('/home/marcin/Dokumenty/projekty/production/Chem/chembase/static/chembase/data/GHSCodes.csv',sep=';',index_col='Code')
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
                    try:
                        signal_word=item.split()[2]
                    except:
                        pass
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
        clas_extr_dict={'%d'%(x):clas_df.loc[x,'number'] for x in clas_df.index.tolist()}
        #print(clas_extr_dict)
        #print(clas_extr_dict)
        #clas_text_extr=clas_df.to_string(header=False)

        pict_df=pd.DataFrame(index=['1','2','3','4','5','6','7','8','9'],columns=['value'])
        #print pict_df
        #print(H)
        for item in H:
            if item=='H317':
                if not 'H335' in H:
                   pict_df.loc[ghs_codes.loc[item,'Pict_short'],'value']=1
            elif (item=='H315' or item=='H319'):
                if not ('H314' in H or 'H318' in H or 'H335' in H):
                   pict_df.loc[ghs_codes.loc[item,'Pict_short'],'value']=1
            else:
                pict_df.loc[ghs_codes.loc[item,'Pict_short'],'value']=1
        #print(pict_df)
        if pict_df.loc['6','value']==1:
            pict_df.loc['7','value']=0
        pictures=pict_df[pict_df['value']>=1]
        #print pict_df
        #print pictures
        #print(pictures)
        pic_list=['%d'%(x) for x in pictures.index.tolist() if x]
        #print(pic_list)

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
        

