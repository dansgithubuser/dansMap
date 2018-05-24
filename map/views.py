from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import json
from .models import Note

def index(request):
	return HttpResponse(loader.get_template('map/index.html').render({}, request))

def note_new(request):
	note=Note(text=request.POST['text'])
	if request.user.is_authenticated: note.user=request.user
	note.save()

def note_get(request):
	return HttpResponse(json.dumps([str(i) for i in Note.objects.all()]))
