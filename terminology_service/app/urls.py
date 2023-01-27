from django.urls import path
from django.views.generic import TemplateView

from . import views


urlpatterns = [
    path('refbooks/', views.RefbooksApiView.as_view()),
    path('refbooks/<int:id>/elements', views.RefbooksElementsApiView.as_view()),
    path('refbooks/<int:id>/check_element', views.CheckRefbookElementApiView.as_view()),
    path('docs/', TemplateView.as_view(
        template_name='app/swagger.html',
        extra_context={'schema_url':'/app/openapi.yaml'}
        )),
]