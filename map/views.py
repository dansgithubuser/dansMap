from django.shortcuts import render
from django.http import HttpResponse
import json
from .models import Note

def note_new(request):
	note=Note(text=request.POST['text'])
	if request.user.is_authenticated: note.user=request.user
	note.save()

def note_get(request):
	return HttpResponse(json.dumps([str(i) for i in Note.objects.all()]))
