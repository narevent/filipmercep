from django import forms
from .models import NewsletterSubscriber, ContactMessage


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscriber
        fields = ['email', 'name']
        widgets = {
            'email': forms.EmailInput(attrs={
                'placeholder': 'Enter your email',
                'class': 'newsletter-input'
            }),
            'name': forms.TextInput(attrs={
                'placeholder': 'Your name (optional)',
                'class': 'newsletter-input'
            }),
        }


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Your name',
                'class': 'contact-input'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Your email',
                'class': 'contact-input'
            }),
            'subject': forms.TextInput(attrs={
                'placeholder': 'Subject',
                'class': 'contact-input'
            }),
            'message': forms.Textarea(attrs={
                'placeholder': 'Your message',
                'class': 'contact-textarea',
                'rows': 6
            }),
        }