import datetime as dt

from django.test import TestCase, Client
from django.urls import reverse

from app import models


class BaseTestCase(TestCase):
    
    def setUp(self) -> None:
        self.client = Client()


class TestRefbooksViewGET(BaseTestCase):
    
    def setUp(self) -> None:
        self.refbook_1 = models.Refbook.objects.create(code='1', name='Refbook_1', description='Some descr...')
        self.refbook_2 = models.Refbook.objects.create(code='2', name='Refbook_2')
        self.refbook_1_v1_0 = models.RefbookVersion.objects.create(refbook=self.refbook_1, 
                                                                   version='1.0', 
                                                                   start_date='2023-01-01')
        self.refbook_1_v1_1 = models.RefbookVersion.objects.create(refbook=self.refbook_1, 
                                                                   version='1.1', 
                                                                   start_date='2023-01-02')
        self.refbook_2_v1_0 = models.RefbookVersion.objects.create(refbook=self.refbook_2, 
                                                                   version='1.0', 
                                                                   start_date='2023-01-03')
        super().setUp()
        
    def test_without_date(self):
        url = reverse('refbooks')       
        resp = self.client.get(url)
        
        expected_response = {'refbooks': [
            {
                'id': str(self.refbook_1.pk),
                'code': self.refbook_1.code,
                'name': self.refbook_1.name
            },
            {
                'id': str(self.refbook_2.pk),
                'code': self.refbook_2.code,
                'name': self.refbook_2.name
            }
        ]}
        
        self.assertEquals(resp.status_code, 200)
        self.assertDictEqual(resp.json(), expected_response)
        
    def test_with_date(self):
        url = reverse('refbooks')
        query_string = f'date={self.refbook_1_v1_0.start_date}'
        resp = self.client.get(url, QUERY_STRING=query_string)
        
        expected_response = {'refbooks': [
            {
                'id': str(self.refbook_1.pk),
                'code': self.refbook_1.code,
                'name': self.refbook_1.name
            }
        ]}
        
        self.assertEquals(resp.status_code, 200)
        self.assertDictEqual(resp.json(), expected_response)


class TestRefbooksElementsViewGET(BaseTestCase):
    
    def setUp(self) -> None:
        current_date = dt.datetime.now()
        self.start_date_v1_0 = current_date - dt.timedelta(days=2)
        self.start_date_v1_1 = current_date - dt.timedelta(days=1)
        self.start_date_v1_2 = current_date + dt.timedelta(days=1)
        self.refbook_1 = models.Refbook.objects.create(code='1', name='Refbook_1', description='Some descr...')
        self.refbook_1_v1_0 = models.RefbookVersion.objects.create(refbook=self.refbook_1, 
                                                              version='1.0', 
                                                              start_date=self.start_date_v1_0)
        self.refbook_1_v1_1 = models.RefbookVersion.objects.create(refbook=self.refbook_1, 
                                                              version='1.1', 
                                                              start_date=self.start_date_v1_1)
        self.refbook_1_v1_2 = models.RefbookVersion.objects.create(refbook=self.refbook_1, 
                                                              version='1.2', 
                                                              start_date=self.start_date_v1_2)
        
        # v1.1 - current version
        
        self.element_1 = models.RefbookElement.objects.create(refbook_version=self.refbook_1_v1_0,
                                                         code='1',
                                                         value='el_1')
        self.element_2 = models.RefbookElement.objects.create(refbook_version=self.refbook_1_v1_1,
                                                         code='1',
                                                         value='el_2')
        self.element_3 = models.RefbookElement.objects.create(refbook_version=self.refbook_1_v1_2,
                                                         code='1',
                                                         value='el_3')
        super().setUp()

    def test_without_version(self):
        url = reverse('refbooks_elements', args=[str(self.refbook_1.pk)])
        resp = self.client.get(url)
        
        expected_response = {'elements': [
            {
                'code': self.element_2.code,
                'value': self.element_2.value
            }
        ]}
        
        self.assertEquals(resp.status_code, 200)
        self.assertDictEqual(resp.json(), expected_response)

    def test_with_version(self):
        url = reverse('refbooks_elements', args=[str(self.refbook_1.pk)])
        query_string = f'version={self.refbook_1_v1_0.version}'
        resp = self.client.get(url, QUERY_STRING=query_string)
        
        expected_response = {'elements': [
            {
                'code': self.element_1.code,
                'value': self.element_1.value
            }
        ]}
        
        self.assertEquals(resp.status_code, 200)
        self.assertDictEqual(resp.json(), expected_response)
        
        
class TestRefbooksCheckElementViewGET(BaseTestCase):
    
    def setUp(self) -> None:
        current_date = dt.datetime.now()
        self.start_date_v1_0 = current_date - dt.timedelta(days=2)
        self.start_date_v1_1 = current_date - dt.timedelta(days=1)
        self.start_date_v1_2 = current_date + dt.timedelta(days=1)
        self.refbook_1 = models.Refbook.objects.create(code='1', name='Refbook_1', description='Some descr...')
        self.refbook_1_v1_0 = models.RefbookVersion.objects.create(refbook=self.refbook_1, 
                                                              version='1.0', 
                                                              start_date=self.start_date_v1_0)
        self.refbook_1_v1_1 = models.RefbookVersion.objects.create(refbook=self.refbook_1, 
                                                              version='1.1', 
                                                              start_date=self.start_date_v1_1)
        self.refbook_1_v1_2 = models.RefbookVersion.objects.create(refbook=self.refbook_1, 
                                                              version='1.2', 
                                                              start_date=self.start_date_v1_2)
        
        # v1.1 - current version
        
        self.element_1 = models.RefbookElement.objects.create(refbook_version=self.refbook_1_v1_0,
                                                         code='1',
                                                         value='el_1')
        self.element_2 = models.RefbookElement.objects.create(refbook_version=self.refbook_1_v1_1,
                                                         code='1',
                                                         value='el_2')
        self.element_3 = models.RefbookElement.objects.create(refbook_version=self.refbook_1_v1_2,
                                                         code='1',
                                                         value='el_3')
        super().setUp()
        super().setUp()
        
    def test_without_version(self):
        url = reverse('check_refbook_element', args=[str(self.refbook_1.pk)])
        query_string = f'code={self.element_1.code}&value={self.element_1.value}'
        resp = self.client.get(url, QUERY_STRING=query_string)
        
        expected_response = False
                
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(resp.json(), expected_response)
        
        url = reverse('check_refbook_element', args=[str(self.refbook_1.pk)])
        query_string = f'code={self.element_2.code}&value={self.element_2.value}'
        resp = self.client.get(url, QUERY_STRING=query_string)
        
        expected_response = True
                
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(resp.json(), expected_response)

    def test_with_version(self):
        url = reverse('check_refbook_element', args=[str(self.refbook_1.pk)])
        query_string = f'code={self.element_1.code}&value={self.element_1.value}&version={self.refbook_1_v1_2.version}'
        resp = self.client.get(url, QUERY_STRING=query_string)
        
        expected_response = False
                
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(resp.json(), expected_response)
        
        url = reverse('check_refbook_element', args=[str(self.refbook_1.pk)])
        query_string = f'code={self.element_3.code}&value={self.element_3.value}&version={self.refbook_1_v1_2.version}'
        resp = self.client.get(url, QUERY_STRING='code=1&value=el_3&version=1.2')
        
        expected_response = True
                
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(resp.json(), expected_response)
