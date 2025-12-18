from django.contrib import messages
from django.shortcuts import redirect, render

from portfoly.forms import ContactForm
from portfoly.models import Contact, Experiment, Project, Skill, User

# Create your views here.

def index(request):
    
    # Conexão da page do Home 
    
    return render(
        request, "portfoly/pages/index.html"
    )

def about(request):
    
    # Conexão da page do Sobre 
    
    return render(
        request, "portfoly/pages/about.html"
    )
    
def project(request):
    
    # Conexão da page do Projetos 
    
    projects = Project.objects.all().order_by('-created_at')
    
    return render(
        request, "portfoly/pages/project.html",
        {
            'projects': projects
        }
    )
    
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Mensagem enviada com sucesso! Entrarei em contato em breve.')
            return redirect('portfoly:contact')
        else:
            messages.error(request, 'Erro ao enviar mensagem. Por favor, verifique os campos.')
    else:
        form = ContactForm()
    
    return render(
        request, "portfoly/pages/contact.html",
        {
            'form': form
        }
    ) 