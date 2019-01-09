from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .forms import NameForm, KeyForm, SendForm
from django.views.decorators.csrf import csrf_protect
from django.urls import reverse
from django.core.mail import EmailMessage, get_connection
from django.core.mail.backends.smtp import EmailBackend

import asyncio

from .sendSecureEmail import *
# Create your views here.

def index(request):
	# loop = asyncio.get_event_loop()
	loop = asyncio.new_event_loop()
	asyncio.set_event_loop(loop)
	home = expanduser("~")
	# args = _get_config_from_cmdline()
	context = {}
	if request.method == 'POST':
		form = NameForm(request.POST)
		if form.is_valid():
			my_email = form.cleaned_data['my_email']
			my_password = form.cleaned_data['my_password']
			request.session['my_email'] = my_email
			request.session['my_password'] = my_password
			# securemsg = setUp(name)
			# request.session['securemsg'] = securemsg
			# print(securemsg.my_did)
			return HttpResponseRedirect('keygen/')
	else:
		form = NameForm()
	return render(request, 'index.html',  {'form':form})

@csrf_protect
def generateKey(request):
	# print(request.session.get('user_name'))
	securemsg = setUp(request.session.get('my_email'))
	if request.method == 'POST':
		form = KeyForm(request.POST)
		if form.is_valid():
			key = form.cleaned_data['key'].strip().split(' ')
			request.session['other_key'] = key[1]
			return HttpResponseRedirect(reverse('actions'))
	else:
		loop = asyncio.get_event_loop()
		form = KeyForm()
		context = {
			'did': securemsg.my_did,
			'vkey': securemsg.my_vk
		}
		request.session['my_vk'] = securemsg.my_vk
		request.session['my_did'] = securemsg.my_did
		request.session['wallet_handle'] = securemsg.wallet_handle
		context['form'] = form

	return render(request, 'keygen.html', context)
	# return HttpResponse(template.render(context))
	# return HttpResponse("your did and key are: ")

@csrf_protect
def actions(request):
	context = {}
	return render(request, 'actions.html', context)

	# return HttpResponse(">")

# def vote(request, question_id):
#     return HttpResponse("You're voting on question %s." % question_id)

def sendEmail(request):
	loop = asyncio.new_event_loop()
	asyncio.set_event_loop(loop)
	if request.method == 'POST':
		forms = SendForm(request.POST)
		if forms.is_valid():
			securemsg = setUp(request.session.get('my_email'))
			securemsg.my_vk = request.session.get('my_vk')
			securemsg.wallet_handle = request.session.get('wallet_handle')
			securemsg.their_vk = request.session.get('other_key')
			message = forms.cleaned_data['message']
			their_email = forms.cleaned_data['their_email']
			with open('testFile.json', 'w') as f:
				f.write(message)
			# encrypted_msg = loop.run_until_complete(securemsg.encryptMsg(message))
			encrypted_msg = loop.run_until_complete(encryptMsg('testFile.json', request.session.get('wallet_handle'), request.session.get('my_vk'), request.session.get('other_key')))
			# request.session['encrypted_msg'] = encrypted_msg
			connection = EmailBackend(
				host='smtp.gmail.com',
			    port=587,
			    username=request.session['my_email'],
			    password=request.session['my_password']
			)
			email = EmailMessage(
			'test',
			message,
			request.session['my_email'],
			[their_email],
			connection=connection
			)
			email.attach_file('encrypted.dat')
			email.send(fail_silently=False)
			# send_mail('test', encrypted_msg, my_email, [their_email], fail_silently=False, auth_user=my_email, auth_password=my_password)
			# send(my_email, my_password, 'smtp.gmail.com', 'port', their_email, 'encrypted.dat', 2)
			return HttpResponseRedirect(reverse('finished'))
	else:
		form = SendForm()
	return render(request, 'send.html', {'form': form})

def recieve(request):
	return HttpResponse("recieve")

def finished(request):
	context = {}
	return render(request, 'finished.html', context)
