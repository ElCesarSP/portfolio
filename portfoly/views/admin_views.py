import hashlib
import secrets
from datetime import timedelta

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from portfoly.admin_forms import (ChangePasswordForm, ExperimentForm,
                                  LoginForm, PasswordResetForm,
                                  PasswordResetRequestForm, ProjectForm,
                                  SkillForm, UserDetailsForm)
from portfoly.decorators import admin_login_required, admin_required
from portfoly.models import (AuthToken, ChatConversation, ChatMessage, Contact,
                             Experiment, PasswordResetToken, Project,
                             ProjectInquiry, Skill, User, UserDetails)

# ============================================
# AUTHENTICATION VIEWS
# ============================================

def admin_login(request):
    """View de login para admin"""
    # Se já está autenticado, redireciona para dashboard
    
    token_value = request.COOKIES.get('admin_token')
    if token_value:
        try:
            token = AuthToken.objects.get(token=token_value, is_active=True)
            if not token.is_expired():
                return redirect('portfoly:admin_dashboard')
        except AuthToken.DoesNotExist:
            pass
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            remember_me = form.cleaned_data.get('remember_me', False)
            
            # Hash da senha para comparação
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            
            try:
                user = User.objects.get(email=email, password=password, is_active=True)
                
                # Criar token de autenticação
                token_value = secrets.token_urlsafe(32)
                
                # Definir tempo de expiração
                if remember_me:
                    expires_at = timezone.now() + timedelta(days=30)
                else:
                    expires_at = timezone.now() + timedelta(hours=12)
                
                # Criar token no banco
                token = AuthToken.objects.create(
                    user=user,
                    token=token_value,
                    expires_at=expires_at,
                    remember_me=remember_me
                )
                
                messages.success(request, f'Bem-vindo, {user.name}!')
                response = redirect('portfoly:admin_dashboard')
                
                # Definir cookie
                max_age = 30 * 24 * 60 * 60 if remember_me else 12 * 60 * 60
                response.set_cookie('admin_token', token_value, max_age=max_age, httponly=True)
                
                return response
                
            except User.DoesNotExist:
                messages.error(request, 'Email ou senha incorretos.')
    else:
        form = LoginForm()
    
    return render(request, 'portfoly/page_admin/login.html', {'form': form})



def admin_logout(request):
    """View de logout para admin"""
    token_value = request.COOKIES.get('admin_token')
    if token_value:
        try:
            token = AuthToken.objects.get(token=token_value)
            token.is_active = False
            token.save()
        except AuthToken.DoesNotExist:
            pass
    
    messages.success(request, 'Logout realizado com sucesso!')
    response = redirect('portfoly:admin_login')
    response.delete_cookie('admin_token')
    return response


def password_reset_request(request):
    """View para solicitar recuperação de senha"""
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            
            try:
                user = User.objects.get(email=email, is_active=True)
                
                # Criar token de recuperação
                token_value = secrets.token_urlsafe(32)
                expires_at = timezone.now() + timedelta(hours=1)
                
                PasswordResetToken.objects.create(
                    user=user,
                    token=token_value,
                    expires_at=expires_at
                )
                
                # Enviar email
                reset_link = f"{request.build_absolute_uri('/admin-panel/password-reset/')}{token_value}/"
                
                try:
                    send_mail(
                        'Recuperação de Senha - Portfolio Admin',
                        f'Olá {user.name},\n\nClique no link abaixo para redefinir sua senha:\n{reset_link}\n\nEste link expira em 1 hora.\n\nSe você não solicitou esta recuperação, ignore este email.',
                        settings.DEFAULT_FROM_EMAIL,
                        [email],
                        fail_silently=False,
                    )
                    messages.success(request, 'Email de recuperação enviado! Verifique sua caixa de entrada.')
                except Exception as e:
                    messages.error(request, f'Erro ao enviar email: {str(e)}')
                    
            except User.DoesNotExist:
                # Por segurança, não revelar se o email existe
                messages.success(request, 'Se o email estiver cadastrado, você receberá um link de recuperação.')
            
            return redirect('portfoly:admin_login')
    else:
        form = PasswordResetRequestForm()
    
    return render(request, 'portfoly/page_admin/password_reset_request.html', {'form': form})


def password_reset(request, token):
    """View para redefinir senha"""
    try:
        reset_token = PasswordResetToken.objects.get(token=token, used=False)
        
        if reset_token.is_expired():
            messages.error(request, 'Este link de recuperação expirou.')
            return redirect('portfoly:admin_login')
        
        if request.method == 'POST':
            form = PasswordResetForm(request.POST)
            if form.is_valid():
                password = form.cleaned_data['password']
                password_hash = hashlib.sha256(password.encode()).hexdigest()
                
                # Atualizar senha
                user = reset_token.user
                user.password = password_hash
                user.save()
                
                # Marcar token como usado
                reset_token.used = True
                reset_token.save()
                
                # Invalidar todos os tokens de autenticação do usuário
                AuthToken.objects.filter(user=user).update(is_active=False)
                
                messages.success(request, 'Senha redefinida com sucesso! Faça login com sua nova senha.')
                return redirect('portfoly:admin_login')
        else:
            form = PasswordResetForm()
        
        return render(request, 'portfoly/page_admin/password_reset.html', {'form': form, 'token': token})
        
    except PasswordResetToken.DoesNotExist:
        messages.error(request, 'Link de recuperação inválido.')
        return redirect('portfoly:admin_login')


# ============================================
# DASHBOARD
# ============================================

@admin_login_required
def admin_dashboard(request):
    """Dashboard principal do admin"""
    user = request.admin_user
    
    # Estatísticas
    stats = {
        'total_projects': Project.objects.filter(user_id=user).count(),
        'total_experiments': Experiment.objects.filter(user_id=user).count(),
        'total_skills': Skill.objects.filter(user_id=user).count(),
        'unread_contacts': Contact.objects.filter(read=False).count(),
        'total_contacts': Contact.objects.count(),
    }
    
    # Projetos recentes
    recent_projects = Project.objects.filter(user_id=user).order_by('-created_at')[:5]
    
    # Mensagens recentes
    recent_contacts = Contact.objects.order_by('-created_at')[:5]
    
    context = {
        'stats': stats,
        'recent_projects': recent_projects,
        'recent_contacts': recent_contacts,
        'user': user
    }
    
    return render(request, 'portfoly/page_admin/dashboard.html', context)


# ============================================
# PROJECTS CRUD
# ============================================

@admin_required
def admin_projects_list(request):
    """Lista todos os projetos"""
    user = request.admin_user
    
    # Busca
    search = request.GET.get('search', '')
    category = request.GET.get('category', '')
    
    projects = Project.objects.filter(user_id=user)
    
    if search:
        projects = projects.filter(
            Q(title__icontains=search) | 
            Q(description__icontains=search) |
            Q(technologies__icontains=search)
        )
    
    if category:
        projects = projects.filter(category=category)
    
    projects = projects.order_by('-created_at')
    
    context = {
        'projects': projects,
        'search': search,
        'category': category,
        'user': user
    }
    
    return render(request, 'portfoly/page_admin/projects/list.html', context)


@admin_required
def admin_project_create(request):
    """Criar novo projeto"""
    user = request.admin_user
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.user_id = user
            project.save()
            messages.success(request, 'Projeto criado com sucesso!')
            return redirect('portfoly:admin_projects_list')
    else:
        form = ProjectForm()
    
    context = {
        'form': form,
        'action': 'Criar',
        'user': user
    }
    
    return render(request, 'portfoly/page_admin/projects/form.html', context)


@admin_required
def admin_project_edit(request, pk):
    """Editar projeto existente"""
    user = request.admin_user
    project = get_object_or_404(Project, pk=pk, user_id=user)
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, 'Projeto atualizado com sucesso!')
            return redirect('portfoly:admin_projects_list')
    else:
        form = ProjectForm(instance=project)
    
    context = {
        'form': form,
        'action': 'Editar',
        'project': project,
        'user': user
    }
    
    return render(request, 'portfoly/page_admin/projects/form.html', context)


@admin_required
def admin_project_delete(request, pk):
    """Deletar projeto"""
    user = request.admin_user
    project = get_object_or_404(Project, pk=pk, user_id=user)
    
    if request.method == 'POST':
        project.delete()
        messages.success(request, 'Projeto deletado com sucesso!')
        return redirect('portfoly:admin_projects_list')
    
    context = {
        'project': project,
        'user': user
    }
    
    return render(request, 'portfoly/page_admin/projects/delete.html', context)


@admin_required
def admin_project_detail(request, pk):
    """Ver detalhes completos do projeto"""
    user = request.admin_user
    project = get_object_or_404(Project, pk=pk, user_id=user)
    
    context = {
        'project': project,
        'user': user
    }
    
    return render(request, 'portfoly/page_admin/projects/detail.html', context)


# ============================================
# EXPERIMENTS CRUD
# ============================================

@admin_required
def admin_experiments_list(request):
    """Lista todas as experiências"""
    user = request.admin_user
    
    search = request.GET.get('search', '')
    experiments = Experiment.objects.filter(user_id=user)
    
    if search:
        experiments = experiments.filter(
            Q(position__icontains=search) | 
            Q(company__icontains=search) |
            Q(description__icontains=search)
        )
    
    experiments = experiments.order_by('-created_at')
    
    context = {
        'experiments': experiments,
        'search': search,
        'user': user
    }
    
    return render(request, 'portfoly/page_admin/experiments/list.html', context)


@admin_required
def admin_experiment_create(request):
    """Criar nova experiência"""
    user = request.admin_user
    
    if request.method == 'POST':
        form = ExperimentForm(request.POST)
        if form.is_valid():
            experiment = form.save(commit=False)
            experiment.user_id = user
            experiment.save()
            messages.success(request, 'Experiência criada com sucesso!')
            return redirect('portfoly:admin_experiments_list')
    else:
        form = ExperimentForm()
    
    context = {
        'form': form,
        'action': 'Criar',
        'user': user
    }
    
    return render(request, 'portfoly/page_admin/experiments/form.html', context)


@admin_required
def admin_experiment_edit(request, pk):
    """Editar experiência existente"""
    user = request.admin_user
    experiment = get_object_or_404(Experiment, pk=pk, user_id=user)
    
    if request.method == 'POST':
        form = ExperimentForm(request.POST, instance=experiment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Experiência atualizada com sucesso!')
            return redirect('portfoly:admin_experiments_list')
    else:
        form = ExperimentForm(instance=experiment)
    
    context = {
        'form': form,
        'action': 'Editar',
        'experiment': experiment,
        'user': user
    }
    
    return render(request, 'portfoly/page_admin/experiments/form.html', context)


@admin_required
def admin_experiment_delete(request, pk):
    """Deletar experiência"""
    user = request.admin_user
    experiment = get_object_or_404(Experiment, pk=pk, user_id=user)
    
    if request.method == 'POST':
        experiment.delete()
        messages.success(request, 'Experiência deletada com sucesso!')
        return redirect('portfoly:admin_experiments_list')
    
    context = {
        'experiment': experiment,
        'user': user
    }
    
    return render(request, 'portfoly/page_admin/experiments/delete.html', context)


@admin_required
def admin_experiment_detail(request, pk):
    """Ver detalhes completos da experiência"""
    user = request.admin_user
    experiment = get_object_or_404(Experiment, pk=pk, user_id=user)
    
    context = {
        'experiment': experiment,
        'user': user
    }
    
    return render(request, 'portfoly/page_admin/experiments/detail.html', context)


# ============================================
# SKILLS CRUD
# ============================================

@admin_required
def admin_skills_list(request):
    """Lista todas as habilidades"""
    user = request.admin_user
    
    search = request.GET.get('search', '')
    level = request.GET.get('level', '')
    
    skills = Skill.objects.filter(user_id=user)
    
    if search:
        skills = skills.filter(name__icontains=search)
    
    if level:
        skills = skills.filter(level=level)
    
    skills = skills.order_by('name')
    
    context = {
        'skills': skills,
        'search': search,
        'level': level,
        'user': user
    }
    
    return render(request, 'portfoly/page_admin/skills/list.html', context)


@admin_required
def admin_skill_create(request):
    """Criar nova habilidade"""
    user = request.admin_user
    
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.user_id = user
            skill.save()
            messages.success(request, 'Habilidade criada com sucesso!')
            return redirect('portfoly:admin_skills_list')
    else:
        form = SkillForm()
    
    context = {
        'form': form,
        'action': 'Criar',
        'user': user
    }
    
    return render(request, 'portfoly/page_admin/skills/form.html', context)


@admin_required
def admin_skill_edit(request, pk):
    """Editar habilidade existente"""
    user = request.admin_user
    skill = get_object_or_404(Skill, pk=pk, user_id=user)
    
    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, 'Habilidade atualizada com sucesso!')
            return redirect('portfoly:admin_skills_list')
    else:
        form = SkillForm(instance=skill)
    
    context = {
        'form': form,
        'action': 'Editar',
        'skill': skill,
        'user': user
    }
    
    return render(request, 'portfoly/page_admin/skills/form.html', context)


@admin_required
def admin_skill_delete(request, pk):
    """Deletar habilidade"""
    user = request.admin_user
    skill = get_object_or_404(Skill, pk=pk, user_id=user)
    
    if request.method == 'POST':
        skill.delete()
        messages.success(request, 'Habilidade deletada com sucesso!')
        return redirect('portfoly:admin_skills_list')
    
    context = {
        'skill': skill,
        'user': user
    }
    
    return render(request, 'portfoly/page_admin/skills/delete.html', context)


@admin_required
def admin_skill_detail(request, pk):
    """Ver detalhes completos da habilidade"""
    user = request.admin_user
    skill = get_object_or_404(Skill, pk=pk, user_id=user)
    
    context = {
        'skill': skill,
        'user': user
    }
    
    return render(request, 'portfoly/page_admin/skills/detail.html', context)


# ============================================
# CONTACTS VIEW
# ============================================

@admin_required
def admin_contacts_list(request):
    """Lista todas as mensagens de contato"""
    user = request.admin_user
    
    filter_type = request.GET.get('filter', 'all')
    search = request.GET.get('search', '')
    
    contacts = Contact.objects.all()
    
    if filter_type == 'unread':
        contacts = contacts.filter(read=False)
    elif filter_type == 'read':
        contacts = contacts.filter(read=True)
    
    if search:
        contacts = contacts.filter(
            Q(name__icontains=search) | 
            Q(email__icontains=search) |
            Q(subject__icontains=search) |
            Q(message__icontains=search)
        )
    
    contacts = contacts.order_by('-created_at')
    
    context = {
        'contacts': contacts,
        'filter_type': filter_type,
        'search': search,
        'user': user
    }
    
    return render(request, 'portfoly/page_admin/contacts/list.html', context)


@admin_required
def admin_contact_mark_read(request, pk):
    """Marcar mensagem como lida"""
    contact = get_object_or_404(Contact, pk=pk)
    contact.read = True
    contact.save()
    messages.success(request, 'Mensagem marcada como lida!')
    return redirect('portfoly:admin_contacts_list')


@admin_required
def admin_contact_mark_unread(request, pk):
    """Marcar mensagem como não lida"""
    contact = get_object_or_404(Contact, pk=pk)
    contact.read = False
    contact.save()
    messages.success(request, 'Mensagem marcada como não lida!')
    return redirect('portfoly:admin_contacts_list')


@admin_required
def admin_contact_detail(request, pk):
    """Ver detalhes completos da mensagem"""
    user = request.admin_user
    contact = get_object_or_404(Contact, pk=pk)
    
    # Marcar como lida automaticamente ao visualizar
    if not contact.read:
        contact.read = True
        contact.save()
    
    context = {
        'contact': contact,
        'user': user
    }
    
    return render(request, 'portfoly/page_admin/contacts/detail.html', context)


# ============================================
# PROFILE MANAGEMENT
# ============================================

@admin_required
def admin_profile(request):
    """Editar perfil do usuário"""
    user = request.admin_user
    
    try:
        user_details = UserDetails.objects.get(user_id=user)
    except UserDetails.DoesNotExist:
        user_details = UserDetails(user_id=user)
    
    if request.method == 'POST':
        form = UserDetailsForm(request.POST, instance=user_details, user=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('portfoly:admin_profile')
    else:
        form = UserDetailsForm(instance=user_details, user=user)
    
    context = {
        'form': form,
        'user': user
    }
    
    return render(request, 'portfoly/page_admin/profile/edit.html', context)


@admin_required
def admin_change_password(request):
    """Mudar senha do usuário no painel admin"""
    user = request.admin_user
    
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST, user=user)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            password_hash = hashlib.sha256(new_password.encode()).hexdigest()
            
            # Atualizar senha
            user.password = password_hash
            user.save()
            
            # Invalidar todos os tokens de autenticação do usuário
            AuthToken.objects.filter(user=user).update(is_active=False)
            
            messages.success(request, 'Senha alterada com sucesso! Por favor, faça login novamente.')
            response = redirect('portfoly:admin_login')
            response.delete_cookie('admin_token')
            return response
    else:
        form = ChangePasswordForm(user=user)
    
    context = {
        'form': form,
        'user': user
    }
    
    return render(request, 'portfoly/page_admin/profile/change_password.html', context)
