from django.test import TestCase
from .models import Compound
# Create your tests here.


class CompoundTestCase(TestCase):
    
    def test_compound_ewidencja_true(self):
        new_cmpd=Compound(name='hydrazyna')
        new_cmpd.save()
        
        new_cmpd.set_registered(True)
        self.assertEqual(new_cmpd.is_registered(),True)
        
    def test_compound_ewidencja_false(self):
        new_cmpd=Compound(name='woda')
        new_cmpd.save()
        self.assertEqual(new_cmpd.is_registered(),False)
        
    def test_compound_ewidencja_true_then_false(self):
        new_cmpd=Compound(name='hydrazyna')
        new_cmpd.save()
        
        new_cmpd.set_registered(True)
        new_cmpd.set_registered(False)
        self.assertEqual(new_cmpd.is_registered(),False)
        
    def test_compound_ewidencja_true_then_false_then_true_again(self):
        new_cmpd=Compound(name='hydrazyna')
        new_cmpd.save()
        
        new_cmpd.set_registered(True)
        new_cmpd.set_registered(False)
        new_cmpd.set_registered(True)
        self.assertEqual(new_cmpd.is_registered(),True)