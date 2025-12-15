from django import forms
from portfoly.models import Project, Experiment, Skill, UserDetails, User, Contact
from django.core.exceptions import ValidationError
import hashlib


class LoginForm(forms.Form):
    """Formulário de login para admin"""
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite seu email',
            'required': True
        })
    )
    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite sua senha',
            'required': True
        })
    )
    remember_me = forms.BooleanField(
        label='Lembrar-me',
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )


class PasswordResetRequestForm(forms.Form):
    """Formulário para solicitar recuperação de senha"""
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite seu email cadastrado',
            'required': True
        })
    )


class PasswordResetForm(forms.Form):
    """Formulário para redefinir senha"""
    password = forms.CharField(
        label='Nova Senha',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite a nova senha',
            'required': True,
            'minlength': 6
        })
    )
    password_confirm = forms.CharField(
        label='Confirmar Senha',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirme a nova senha',
            'required': True,
            'minlength': 6
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            raise ValidationError('As senhas não coincidem.')

        return cleaned_data


class ProjectForm(forms.ModelForm):
    """Formulário para criar/editar projetos"""
    class Meta:
        model = Project
        fields = ['title', 'description', 'technologies', 'category', 'link_demo', 'link_github', 'image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Título do projeto'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Descrição do projeto',
                'rows': 4
            }),
            'technologies': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Python, Django, JavaScript'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'link_demo': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://exemplo.com/demo'
            }),
            'link_github': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://github.com/usuario/projeto'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }


class ExperimentForm(forms.ModelForm):
    """Formulário para criar/editar experiências"""
    class Meta:
        model = Experiment
        fields = ['position', 'company', 'description', 'range_time']
        widgets = {
            'position': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Desenvolvedor Full Stack'
            }),
            'company': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome da empresa'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Descrição das atividades',
                'rows': 4
            }),
            'range_time': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Jan 2020 - Dez 2022'
            })
        }


class SkillForm(forms.ModelForm):
    """Formulário para criar/editar habilidades"""
    class Meta:
        model = Skill
        fields = ['name', 'level']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome da habilidade'
            }),
            'level': forms.Select(attrs={
                'class': 'form-select'
            })
        }


class UserDetailsForm(forms.ModelForm):
    """Formulário para editar detalhes do usuário"""
    name = forms.CharField(
        label='Nome',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Seu nome completo'
        })
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'seu@email.com'
        })
    )

    class Meta:
        model = UserDetails
        fields = ['phone', 'linkedin', 'github']
        widgets = {
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(00) 00000-0000'
            }),
            'linkedin': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://linkedin.com/in/seu-perfil'
            }),
            'github': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://github.com/seu-usuario'
            })
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['name'].initial = self.user.name
            self.fields['email'].initial = self.user.email

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user:
            self.user.name = self.cleaned_data['name']
            self.user.email = self.cleaned_data['email']
            if commit:
                self.user.save()
        if commit:
            instance.save()
        return instance


class ChangePasswordForm(forms.Form):
    """Formulário para mudar senha no painel admin"""
    current_password = forms.CharField(
        label='Senha Atual',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite sua senha atual',
            'required': True
        })
    )
    new_password = forms.CharField(
        label='Nova Senha',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite a nova senha',
            'required': True,
            'minlength': 6
        })
    )
    confirm_password = forms.CharField(
        label='Confirmar Nova Senha',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirme a nova senha',
            'required': True,
            'minlength': 6
        })
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_current_password(self):
        current_password = self.cleaned_data.get('current_password')
        if self.user:
            password_hash = hashlib.sha256(current_password.encode()).hexdigest()
            if self.user.password != password_hash:
                raise ValidationError('Senha atual incorreta.')
        return current_password

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password and confirm_password and new_password != confirm_password:
            raise ValidationError('As senhas não coincidem.')

        return cleaned_data
