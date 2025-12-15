from django import forms
from portfoly.models import Contact


class ContactForm(forms.ModelForm):
    """
    Formulário de contato baseado no modelo Contact
    """
    
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Seu nome completo',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': 'seu@email.com',
                'required': True
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Assunto da mensagem',
                'required': True
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Digite sua mensagem aqui...',
                'rows': 6,
                'required': True
            }),
        }
        labels = {
            'name': 'Nome',
            'email': 'Email',
            'subject': 'Assunto',
            'message': 'Mensagem',
        }
