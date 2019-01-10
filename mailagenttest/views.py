from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .forms import NameForm, KeyForm, SendForm, ReceiveForm
from django.views.decorators.csrf import csrf_protect
from django.urls import reverse
from django.core.mail import EmailMessage, get_connection
from django.core.mail.backends.smtp import EmailBackend
import asyncio

from .sendSecureEmail import *
from .receiveSecureEmail import *
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

@csrf_protect
def actions(request):
	context = {}
	return render(request, 'actions.html', context)

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

			encrypted_msg = loop.run_until_complete(encryptMsg('testFile.json', request.session.get('wallet_handle'), request.session.get('my_vk'), request.session.get('other_key')))
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
			return HttpResponseRedirect(reverse('finished'))
	else:
		forms = SendForm()

	return render(request, 'send.html', {'form': forms})

def recieve(request):
	loop = asyncio.new_event_loop()
	asyncio.set_event_loop(loop)
	if request.method == 'POST':
		form = ReceiveForm(request.POST)
		if form.is_valid():
			securemsg = setUp(request.session.get('my_email'))
			securemsg.my_vk = request.session.get('my_vk')
			securemsg.wallet_handle = request.session.get('wallet_handle')
			securemsg.their_vk = request.session.get('other_key')
			their_email = form.cleaned_data['their_email']
			encrypted_msg = run('imap.gmail.com', '1', request.session['my_email'], request.session['my_password'], their_email)
			decrypted_msg = loop.run_until_complete(decryptMsg(securemsg.wallet_handle, securemsg.my_vk, encrypted_msg))
			print('decrypted_msg is: ', decrypted_msg)
			decrypted_msg_obj = json.loads(decrypted_msg[1].decode("utf-8"))
			print('decrypted_obj is: ', decrypted_msg_obj)

			request.session['decrypted_msg'] = decrypted_msg
			request.session['decrypted_msg_obj'] = decrypted_msg_obj

			return HttpResponseRedirect(reverse('finished'))
	else:
		form = ReceiveForm()

	return render(request, 'receive.html', {'form': form})

def finished(request):
	context = {}
	return render(request, 'finished.html', context)
