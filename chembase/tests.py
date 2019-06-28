from django.test import TestCase
from .models import Compound
from .utils.functions import Molecule, Sds, ChemSp, Numerical
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

    def test_substructure(self):
        aniline = Molecule(molfile=open(os.path.join(test_dir, 'aniline.mol'), 'r').read())
        self.assertEqual(aniline.is_substructure(smiles='c1ccccc1'), True)
        self.assertEqual(aniline.is_substructure(smiles='[Cu]'), False)
        #self.assertEqual(aniline.is_substructure(smiles='cn'), True)

    def test_properties(self):
        aniline = Molecule(molfile=open(os.path.join(test_dir, 'aniline.mol'), 'r').read())
        rphenylethanol = Molecule(molfile=open(os.path.join(test_dir, 'R-1-phenylethanol.mol'), 'r').read())
        sphenylethanol = Molecule(molfile=open(os.path.join(test_dir, 'S-1-phenylethanol.mol'), 'r').read())
        self.assertEqual(aniline.properties()['formula'],'C6 H7 N')
        self.assertEqual(aniline.properties()['mass'], '93.1265')
        self.assertEqual(rphenylethanol.properties()['mass'], '122.1644')
        self.assertEqual(rphenylethanol.properties()['formula'], 'C8 H10 O')
        self.assertEqual(rphenylethanol.properties()['smiles'], 'C[C@@H](O)c1ccccc1 |&1:1|')

    def test_clean_formula(self):
        self.assertEqual(Molecule.clean_formula('C6H6'),'C_{6}H_{6}')
        self.assertEqual(Molecule.clean_formula('H6C6'), 'C_{6}H_{6}')
        self.assertEqual(Molecule.clean_formula('C6O2H6'), 'C_{6}H_{6}O_{2}')

# class ChemspiderTestCase(TestCase):
#
#     def test_chemspider_search(self):
#
#         chemsp=ChemSp()
#         print(chemsp.search('101-11-1'))
#
#
# class SdsTestCase(TestCase):
#
#     global test_dir
#     test_dir = 'chembase/static/chembase/tests/'
#
#     def test_transform_sds(self):
#         sdsfile=open(os.path.join(test_dir, 'Iodine.pdf'), 'rb+')
#         sds=Sds(sdsfile)
#         sds.save_temp()
#         sds.transform_temp()
#         result = sds.read_contents()
#         sds.delete_temp()
#         print(result)
#         self.assertEqual(result['name'], 'Jod')

class NumericalTestCase(TestCase):

    def test_binding_constant_printing(self):
        self.assertEqual(Numerical.print_binding_const(1), '1.000 mol')
        self.assertEqual(Numerical.print_binding_const(0.2), '200.000 mmol')
        self.assertEqual(Numerical.print_binding_const(0.05), '50.000 mmol')
        self.assertEqual(Numerical.print_binding_const(0.008), '8.000 mmol')
        self.assertEqual(Numerical.print_binding_const(0.0006), '600.000 µmol')

