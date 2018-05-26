from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
import json
from .models import Note

def index(request):
	return HttpResponse(loader.get_template('map/index.html').render({
		'DEBUG': settings.DEBUG,
	}, request))

def note_new(request):
	note=Note(**{i: request.POST[i] for i in ['text', 'latitude', 'longitude']})
	if request.user.is_authenticated: note.user=request.user
	note.save()
	return HttpResponse(status=201)

def note_get(request):
	return HttpResponse(json.dumps([str(i) for i in Note.objects.all()]))
