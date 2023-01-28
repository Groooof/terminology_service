import datetime as dt

from django.test import TestCase, Client
from django.urls import reverse

from app import models


class Urls:
    refbooks = reverse('refbooks')
    refbooks_elements = reverse('refbooks_elements', args=[1])
    check_refbook_element = reverse('check_refbook_element', args=['1'])


class TestViews(TestCase):
    
    def setUp(self) -> None:
        self.client = Client()
        
    def test_refbooks_GET_without_date(self):
        refbook_1 = models.Refbook.objects.create(code='1', name='Refbook_1', description='Some descr...')
        refbook_2 = models.Refbook.objects.create(code='2', name='Refbook_2')
        
        expected_response = {'refbooks': [
            {
                'id': str(refbook_1.pk),
                'code': refbook_1.code,
                'name': refbook_1.name
            },
            {
                'id': str(refbook_2.pk),
                'code': refbook_2.code,
                'name': refbook_2.name
            }
        ]}
        
        url = reverse('refbooks')       
        resp = self.client.get(url)
        
        self.assertEquals(resp.status_code, 200)
        self.assertDictEqual(resp.json(), expected_response)

    def test_refbooks_GET_with_date(self):
        refbook_1 = models.Refbook.objects.create(code='1', name='Refbook_1', description='Some descr...')
        refbook_2 = models.Refbook.objects.create(code='2', name='Refbook_2')
        models.RefbookVersion.objects.create(refbook=refbook_1, version='1.0', start_date='2023-01-01')
        models.RefbookVersion.objects.create(refbook=refbook_1, version='1.1', start_date='2023-01-02')
        models.RefbookVersion.objects.create(refbook=refbook_2, version='1.0', start_date='2023-01-03')
        
        expected_response = {'refbooks': [
            {
                'id': str(refbook_1.pk),
                'code': refbook_1.code,
                'name': refbook_1.name
            }
        ]}
        
        url = reverse('refbooks')       
        resp = self.client.get(url, QUERY_STRING='date=2023-01-01')
        
        self.assertEquals(resp.status_code, 200)
        self.assertDictEqual(resp.json(), expected_response)
        
    def test_refbooks_elements_GET_without_version(self):
        current_date = dt.datetime.now()
        start_date_v1_0 = current_date - dt.timedelta(days=2)
        start_date_v1_1 = current_date - dt.timedelta(days=1)
        start_date_v1_2 = current_date + dt.timedelta(days=1)
        refbook_1 = models.Refbook.objects.create(code='1', name='Refbook_1', description='Some descr...')
        refbook_1_v1_0 = models.RefbookVersion.objects.create(refbook=refbook_1, 
                                                              version='1.0', 
                                                              start_date=start_date_v1_0)
        refbook_1_v1_1 = models.RefbookVersion.objects.create(refbook=refbook_1, 
                                                              version='1.1', 
                                                              start_date=start_date_v1_1)
        refbook_1_v1_2 = models.RefbookVersion.objects.create(refbook=refbook_1, 
                                                              version='1.2', 
                                                              start_date=start_date_v1_2)
        
        # v1.1 - current version
        
        element_1 = models.RefbookElement.objects.create(refbook_version=refbook_1_v1_0,
                                                              code='1',
                                                              value='el_1')
        element_2 = models.RefbookElement.objects.create(refbook_version=refbook_1_v1_1,
                                                              code='1',
                                                              value='el_2')
        element_3 = models.RefbookElement.objects.create(refbook_version=refbook_1_v1_2,
                                                              code='1',
                                                              value='el_3')
        
        expected_response = {'elements': [
            {
                'code': element_2.code,
                'value': element_2.value
            }
        ]}

        url = reverse('refbooks_elements', args=['1'])
        resp = self.client.get(url)
        
        self.assertEquals(resp.status_code, 200)
        self.assertDictEqual(resp.json(), expected_response)
        
    def test_refbooks_elements_GET_with_version(self):
        current_date = dt.datetime.now()
        start_date_v1_0 = current_date - dt.timedelta(days=2)
        start_date_v1_1 = current_date - dt.timedelta(days=1)
        start_date_v1_2 = current_date + dt.timedelta(days=1)
        refbook_1 = models.Refbook.objects.create(code='1', name='Refbook_1', description='Some descr...')
        refbook_1_v1_0 = models.RefbookVersion.objects.create(refbook=refbook_1, 
                                                              version='1.0', 
                                                              start_date=start_date_v1_0)
        refbook_1_v1_1 = models.RefbookVersion.objects.create(refbook=refbook_1, 
                                                              version='1.1', 
                                                              start_date=start_date_v1_1)
        refbook_1_v1_2 = models.RefbookVersion.objects.create(refbook=refbook_1, 
                                                              version='1.2', 
                                                              start_date=start_date_v1_2)
        
        element_1 = models.RefbookElement.objects.create(refbook_version=refbook_1_v1_0,
                                                              code='1',
                                                              value='el_1')
        element_2 = models.RefbookElement.objects.create(refbook_version=refbook_1_v1_1,
                                                              code='1',
                                                              value='el_2')
        element_3 = models.RefbookElement.objects.create(refbook_version=refbook_1_v1_2,
                                                              code='1',
                                                              value='el_3')
        
        expected_response = {'elements': [
            {
                'code': element_1.code,
                'value': element_1.value
            }
        ]}

        url = reverse('refbooks_elements', args=['1'])
        resp = self.client.get(url, QUERY_STRING='version=1.0')
        
        self.assertEquals(resp.status_code, 200)
        self.assertDictEqual(resp.json(), expected_response)
        
    def test_refbooks_check_element_GET_without_version(self):
        current_date = dt.datetime.now()
        start_date_v1_0 = current_date - dt.timedelta(days=2)
        start_date_v1_1 = current_date - dt.timedelta(days=1)
        start_date_v1_2 = current_date + dt.timedelta(days=1)
        refbook_1 = models.Refbook.objects.create(code='1', name='Refbook_1', description='Some descr...')
        refbook_1_v1_0 = models.RefbookVersion.objects.create(refbook=refbook_1, 
                                                              version='1.0', 
                                                              start_date=start_date_v1_0)
        refbook_1_v1_1 = models.RefbookVersion.objects.create(refbook=refbook_1, 
                                                              version='1.1', 
                                                              start_date=start_date_v1_1)
        refbook_1_v1_2 = models.RefbookVersion.objects.create(refbook=refbook_1, 
                                                              version='1.2', 
                                                              start_date=start_date_v1_2)
        
        # v1.1 - current version
        
        element_1 = models.RefbookElement.objects.create(refbook_version=refbook_1_v1_0,
                                                         code='1',
                                                         value='el_1')
        element_2 = models.RefbookElement.objects.create(refbook_version=refbook_1_v1_1,
                                                         code='1',
                                                         value='el_2')
        element_3 = models.RefbookElement.objects.create(refbook_version=refbook_1_v1_2,
                                                         code='1',
                                                         value='el_3')
        
        url = reverse('check_refbook_element', args=['1'])
        resp = self.client.get(url, QUERY_STRING='code=1&value=el_1')
        
        expected_response = False
                
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(resp.json(), expected_response)
        
        url = reverse('check_refbook_element', args=['1'])
        resp = self.client.get(url, QUERY_STRING='code=1&value=el_2')
        
        expected_response = True
                
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(resp.json(), expected_response)
        
    def test_refbooks_check_element_GET_with_version(self):
        current_date = dt.datetime.now()
        start_date_v1_0 = current_date - dt.timedelta(days=2)
        start_date_v1_1 = current_date - dt.timedelta(days=1)
        start_date_v1_2 = current_date + dt.timedelta(days=1)
        refbook_1 = models.Refbook.objects.create(code='1', name='Refbook_1', description='Some descr...')
        refbook_1_v1_0 = models.RefbookVersion.objects.create(refbook=refbook_1, 
                                                              version='1.0', 
                                                              start_date=start_date_v1_0)
        refbook_1_v1_1 = models.RefbookVersion.objects.create(refbook=refbook_1, 
                                                              version='1.1', 
                                                              start_date=start_date_v1_1)
        refbook_1_v1_2 = models.RefbookVersion.objects.create(refbook=refbook_1, 
                                                              version='1.2', 
                                                              start_date=start_date_v1_2)
                
        element_1 = models.RefbookElement.objects.create(refbook_version=refbook_1_v1_0,
                                                         code='1',
                                                         value='el_1')
        element_2 = models.RefbookElement.objects.create(refbook_version=refbook_1_v1_1,
                                                         code='1',
                                                         value='el_2')
        element_3 = models.RefbookElement.objects.create(refbook_version=refbook_1_v1_2,
                                                         code='1',
                                                         value='el_3')
        
        url = reverse('check_refbook_element', args=['1'])
        resp = self.client.get(url, QUERY_STRING='code=1&value=el_1&version=1.2')
        
        expected_response = False
                
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(resp.json(), expected_response)
        
        url = reverse('check_refbook_element', args=['1'])
        resp = self.client.get(url, QUERY_STRING='code=1&value=el_3&version=1.2')
        
        expected_response = True
                
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(resp.json(), expected_response)
        
    