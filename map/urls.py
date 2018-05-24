from django.urls import path
from . import views

urlpatterns=[
	path('note_new', views.note_new, name='note_new'),
	path('note_get', views.note_get, name='note_get'),
]
