from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('keygen/', views.generateKey, name='generateKey'),
    path('pick/', views.picklist, name='picklist'),
]