from django.test import TestCase
from .models import Compound
from .utils.functions import Molecule
import os
# Create your tests here.


#class CompoundTestCase(TestCase):
    #
    # def test_compound_ewidencja_true(self):
    #     new_cmpd=Compound(name='hydrazyna')
    #     new_cmpd.save()
    #
    #     new_cmpd.set_registered(True)
    #     self.assertEqual(new_cmpd.is_registered(),True)
    #
    # def test_compound_ewidencja_false(self):
    #     new_cmpd=Compound(name='woda')
    #     new_cmpd.save()
    #     self.assertEqual(new_cmpd.is_registered(),False)
    #
    # def test_compound_ewidencja_true_then_false(self):
    #     new_cmpd=Compound(name='hydrazyna')
    #     new_cmpd.save()
    #
    #     new_cmpd.set_registered(True)
    #     new_cmpd.set_registered(False)
    #     self.assertEqual(new_cmpd.is_registered(),False)
    #
    # def test_compound_ewidencja_true_then_false_then_true_again(self):
    #     new_cmpd=Compound(name='hydrazyna')
    #     new_cmpd.save()
    #
    #     new_cmpd.set_registered(True)
    #     new_cmpd.set_registered(False)
    #     new_cmpd.set_registered(True)
    #     self.assertEqual(new_cmpd.is_registered(),True)

class MoleculeTestCase(TestCase):

    global test_dir
    test_dir = 'chembase/static/chembase/tests/'


    def test_structure_similarity(self):
        aniline = Molecule(molfile=open(os.path.join(test_dir,'aniline.mol'),'r').read())
        rphenylethanol = Molecule(molfile=open(os.path.join(test_dir,'R-1-phenylethanol.mol'),'r').read())
        sphenylethanol = Molecule(molfile=open(os.path.join(test_dir, 'S-1-phenylethanol.mol'), 'r').read())

        self.assertEqual(aniline.structure_similarity(smiles='c1ccc(cc1)N'),1)
        self.assertEqual(aniline.structure_similarity(smiles='[Cu]'), 0)
        self.assertEqual(round(aniline.structure_similarity(smiles='c1ccccc1'),2), 0.46)
        self.assertEqual(round(aniline.structure_similarity(smiles='n'), 2), 0.08)
        self.assertEqual(round(aniline.structure_similarity(molfile=open(os.path.join(test_dir,
                                                                                       'S-1-phenylethanol.mol'),
                                                                          'r').read()), 2), 0.29)
        #self.assertEqual(rphenylethanol.structure_similarity(molfile=open(os.path.join(test_dir,
        #                                                                               'S-1-phenylethanol.mol'), 'r').read()), 0)
        self.assertEqual(aniline.is_substructure(smiles='c1ccccc1'), True)
        self.assertEqual(aniline.is_substructure(smiles='[Cu]'), False)
        #self.assertEqual(aniline.is_substructure(smiles='cn'), True)
        self.assertEqual(aniline.properties()['formula'],'C6 H7 N')
        self.assertEqual(aniline.properties()['mass'], '93.1265')
        self.assertEqual(rphenylethanol.properties()['mass'], '122.1644')
        self.assertEqual(rphenylethanol.properties()['formula'], 'C8 H10 O')
        self.assertEqual(rphenylethanol.properties()['smiles'], 'C[C@@H](O)c1ccccc1 |&1:1|')
        self.assertEqual(Molecule.clean_formula('C6H6'),'C_{6}H_{6}')
        self.assertEqual(Molecule.clean_formula('H6C6'), 'C_{6}H_{6}')
        self.assertEqual(Molecule.clean_formula('C6O2H6'), 'C_{6}H_{6}O_{2}')


