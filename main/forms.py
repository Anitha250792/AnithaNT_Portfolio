from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Your name",
        "autocomplete": "name",
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        "class": "form-control",
        "placeholder": "Your email",
        "autocomplete": "email",
    }))
    message = forms.CharField(widget=forms.Textarea(attrs={
        "class": "form-control",
        "placeholder": "Your message",
        "rows": 5,
    }))
    # Honeypot: hidden from people, filled in by simple spam bots.
    website = forms.CharField(required=False, widget=forms.TextInput(attrs={
        "tabindex": "-1",
        "autocomplete": "off",
    }))
