from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps
from portfoly.models import AuthToken
from django.utils import timezone


def admin_login_required(view_func):
    """
    Decorator para verificar se o usuário está autenticado via token.
    Redireciona para login se não estiver autenticado.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        token_value = request.COOKIES.get('admin_token')
        
        if not token_value:
            messages.warning(request, 'Por favor, faça login para acessar esta página.')
            return redirect('portfoly:admin_login')
        
        try:
            token = AuthToken.objects.get(token=token_value, is_active=True)
            
            # Verificar se o token expirou
            if token.is_expired():
                token.is_active = False
                token.save()
                messages.warning(request, 'Sua sessão expirou. Por favor, faça login novamente.')
                return redirect('portfoly:admin_login')
            
            # Adicionar usuário ao request
            request.admin_user = token.user
            
        except AuthToken.DoesNotExist:
            messages.warning(request, 'Sessão inválida. Por favor, faça login novamente.')
            return redirect('portfoly:admin_login')
        
        return view_func(request, *args, **kwargs)
    
    return wrapper


def admin_required(view_func):
    """
    Decorator para verificar se o usuário está autenticado e é staff.
    Redireciona para login se não estiver autenticado ou não for staff.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        token_value = request.COOKIES.get('admin_token')
        
        if not token_value:
            messages.warning(request, 'Por favor, faça login para acessar esta página.')
            return redirect('portfoly:admin_login')
        
        try:
            token = AuthToken.objects.get(token=token_value, is_active=True)
            
            # Verificar se o token expirou
            if token.is_expired():
                token.is_active = False
                token.save()
                messages.warning(request, 'Sua sessão expirou. Por favor, faça login novamente.')
                return redirect('portfoly:admin_login')
            
            # Verificar se é staff
            if not token.user.is_staff:
                messages.error(request, 'Você não tem permissão para acessar esta página.')
                return redirect('portfoly:index')
            
            # Adicionar usuário ao request
            request.admin_user = token.user
            
        except AuthToken.DoesNotExist:
            messages.warning(request, 'Sessão inválida. Por favor, faça login novamente.')
            return redirect('portfoly:admin_login')
        
        return view_func(request, *args, **kwargs)
    
    return wrapper

