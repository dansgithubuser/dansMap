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
	body=json.loads(request.body.decode('utf-8'))
	note=Note(**{i: body[i] for i in ['text', 'latitude', 'longitude']})
	if request.user.is_authenticated: note.user=request.user
	note.save()
	return HttpResponse(status=201)

def note_get(request):
	return HttpResponse(json.dumps([i.to_dict() for i in Note.objects.all()]))
