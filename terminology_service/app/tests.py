from django.test import TestCase, Client
from django.urls import reverse

from app import (
    models,
    views
)


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
        