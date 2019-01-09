from django import forms

class NameForm(forms.Form):
    name = forms.CharField(max_length=100)

class KeyForm(forms.Form):
    key = forms.CharField(max_length=100)

class SendForm(forms.Form):
    my_email = forms.EmailField()
    my_password = forms.CharField(max_length=100)
    their_email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)
    SEND_OPTION=[('attached','send as an attached file'), ('body','send as an email body')]
    send_options = forms.ChoiceField(choices=SEND_OPTION, widget=forms.RadioSelect)
