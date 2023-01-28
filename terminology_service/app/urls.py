from django.urls import path
from django.views.generic import TemplateView

from . import views


urlpatterns = [
    path('refbooks/', 
         views.RefbooksApiView.as_view(), 
         name='refbooks'),
    path('refbooks/<int:id>/elements', 
         views.RefbooksElementsApiView.as_view(), 
         name='refbooks_elements'),
    path('refbooks/<int:id>/check_element', 
         views.CheckRefbookElementApiView.as_view(), 
         name='check_refbook_element'),
    path('docs/', TemplateView.as_view(
        template_name='app/swagger.html',
        extra_context={'schema_url':'/app/openapi.yaml'}
        )),
]