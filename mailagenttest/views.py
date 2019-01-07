from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
# Create your views here.

def index(request):
	template = loader.get_template('index.html')
	context = {}
	return HttpResponse(template.render(context))

def generateKey(request):
    return HttpResponse("your did and key are: ")

def picklist(request):
    return HttpResponse(">")

# def vote(request, question_id):
#     return HttpResponse("You're voting on question %s." % question_id)