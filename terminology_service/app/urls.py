from django.urls import path
from . import views


urlpatterns = [
    path('refbooks/', views.RefbooksApiView.as_view()),
    path('refbooks/<int:id>/elements', views.RefbooksElementsApiView.as_view()),
    path('refbooks/<int:id>/check_element', views.CheckRefbookElementApiView.as_view()),
]
