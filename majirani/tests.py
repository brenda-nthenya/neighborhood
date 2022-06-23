from django.test import TestCase
from .models import *

# Create your tests here.
class Neighbourhood(TestCase):
    def setup(self):
        self.hood = Neighborhood(name='Neighbourhood', 
        description='my hood', 
        police_number='123', 
        health_number='1337',
        occupants_count='123')

    def test_instance(self):
        self.assertTrue(isinstance(self.hood, Neighbourhood))

    def test_Create_Neighbourhood(self):
        self.assertTrue(isinstance(self.hood, Neighbourhood))

