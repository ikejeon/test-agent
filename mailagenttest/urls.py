from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('keygen/', views.generateKey, name='generateKey'),
    path('actions/', views.actions, name='actions'),
    path('actions/send/', views.sendEmail, name='send'),
    path('actions/recieve/', views.recieve, name='recieve'),
    path('finished/', views.finished, name = 'finished')
]
