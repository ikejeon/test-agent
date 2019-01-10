from django import forms

class NameForm(forms.Form):
    my_email = forms.EmailField()
    my_password = forms.CharField(max_length=100)

class KeyForm(forms.Form):
    key = forms.CharField(max_length=100)

class SendForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea)
    their_email = forms.EmailField()

class ReceiveForm(forms.Form):
    their_email = forms.EmailField()
