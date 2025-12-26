from django.test import TestCase

# Create your tests here.
"""
TESTES DO PROJETO PORTFOLIO
Testes unitários e de integração para models, views, forms e URLs
"""

import hashlib
from datetime import timedelta

from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone

from portfoly.forms import ContactForm
from portfoly.models import (AuthToken, ChatConversation, ChatMessage, Contact,
                             Experiment, Project, ProjectInquiry, Skill, User,
                             UserDetails)

# ============================================
# TESTES DE MODELS
# ============================================

class UserModelTest(TestCase):
    """Testes para o model User"""
    
    def setUp(self):
        self.user = User.objects.create(
            name="Test User",
            email="test@example.com",
            password=hashlib.sha256("password123".encode()).hexdigest(),
            is_staff=True,
            is_active=True
        )
    
    def test_user_creation(self):
        """Testa criação de usuário"""
        self.assertEqual(self.user.name, "Test User")
        self.assertEqual(self.user.email, "test@example.com")
        self.assertTrue(self.user.is_staff)
        self.assertTrue(self.user.is_active)
    
    def test_user_str(self):
        """Testa representação string do usuário"""
        self.assertEqual(str(self.user), "Test User")
    
    def test_user_password_hashed(self):
        """Testa se senha está hasheada"""
        self.assertNotEqual(self.user.password, "password123")
        self.assertEqual(len(self.user.password), 64)  # SHA256 hash length


class ProjectModelTest(TestCase):
    """Testes para o model Project"""
    
    def setUp(self):
        self.user = User.objects.create(
            name="Test User",
            email="test@example.com",
            password="hashed_password"
        )
        self.project = Project.objects.create(
            user_id=self.user,
            title="Test Project",
            description="Test Description",
            technologies="Python, Django",
            category="Web",
            link_demo="https://demo.com",
            link_github="https://github.com/test"
        )
    
    def test_project_creation(self):
        """Testa criação de projeto"""
        self.assertEqual(self.project.title, "Test Project")
        self.assertEqual(self.project.category, "Web")
        self.assertEqual(self.project.user_id, self.user)
    
    def test_project_str(self):
        """Testa representação string do projeto"""
        self.assertEqual(str(self.project), "Test Project")
    
    def test_project_optional_fields(self):
        """Testa campos opcionais"""
        project = Project.objects.create(
            user_id=self.user,
            title="Minimal Project",
            technologies="Python",
            category="Web"
        )
        self.assertIsNone(project.description)
        self.assertIsNone(project.link_demo)


class SkillModelTest(TestCase):
    """Testes para o model Skill"""
    
    def setUp(self):
        self.user = User.objects.create(
            name="Test User",
            email="test@example.com",
            password="hashed_password"
        )
        self.skill = Skill.objects.create(
            user_id=self.user,
            name="Python",
            level="Advanced"
        )
    
    def test_skill_creation(self):
        """Testa criação de habilidade"""
        self.assertEqual(self.skill.name, "Python")
        self.assertEqual(self.skill.level, "Advanced")
    
    def test_skill_str(self):
        """Testa representação string da habilidade"""
        self.assertEqual(str(self.skill), "Python")


class ContactModelTest(TestCase):
    """Testes para o model Contact"""
    
    def setUp(self):
        self.contact = Contact.objects.create(
            name="John Doe",
            email="john@example.com",
            subject="Test Subject",
            message="Test Message"
        )
    
    def test_contact_creation(self):
        """Testa criação de contato"""
        self.assertEqual(self.contact.name, "John Doe")
        self.assertEqual(self.contact.email, "john@example.com")
        self.assertFalse(self.contact.read)
    
    def test_contact_str(self):
        """Testa representação string do contato"""
        self.assertEqual(str(self.contact), "John Doe - Test Subject")


class AuthTokenModelTest(TestCase):
    """Testes para o model AuthToken"""
    
    def setUp(self):
        self.user = User.objects.create(
            name="Test User",
            email="test@example.com",
            password="hashed_password"
        )
        self.token = AuthToken.objects.create(
            user=self.user,
            token="test_token_123",
            expires_at=timezone.now() + timedelta(days=7)
        )
    
    def test_token_creation(self):
        """Testa criação de token"""
        self.assertEqual(self.token.user, self.user)
        self.assertTrue(self.token.is_active)
    
    def test_token_not_expired(self):
        """Testa se token não está expirado"""
        self.assertFalse(self.token.is_expired())
    
    def test_token_expired(self):
        """Testa se token expirado"""
        expired_token = AuthToken.objects.create(
            user=self.user,
            token="expired_token",
            expires_at=timezone.now() - timedelta(days=1)
        )
        self.assertTrue(expired_token.is_expired())


class ChatConversationModelTest(TestCase):
    """Testes para o model ChatConversation"""
    
    def setUp(self):
        self.conversation = ChatConversation.objects.create(
            session_id="test_session_123",
            visitor_name="Test Visitor",
            visitor_email="visitor@example.com"
        )
    
    def test_conversation_creation(self):
        """Testa criação de conversa"""
        self.assertEqual(self.conversation.session_id, "test_session_123")
        self.assertTrue(self.conversation.is_active)
        self.assertEqual(self.conversation.total_messages, 0)
    
    def test_conversation_str(self):
        """Testa representação string da conversa"""
        self.assertEqual(str(self.conversation), "Conversa com Test Visitor")


# ============================================
# TESTES DE VIEWS
# ============================================

class ViewsTest(TestCase):
    """Testes para as views públicas"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(
            name="Test User",
            email="test@example.com",
            password=hashlib.sha256("password123".encode()).hexdigest()
        )
    
    def test_index_view(self):
        """Testa view da página inicial"""
        response = self.client.get(reverse('portfoly:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'portfoly/pages/index.html')
    
    def test_sobre_view(self):
        """Testa view da página sobre"""
        response = self.client.get(reverse('portfoly:sobre'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'portfoly/pages/sobre.html')
    
    def test_projetos_view(self):
        """Testa view da página de projetos"""
        # Criar alguns projetos
        Project.objects.create(
            user_id=self.user,
            title="Project 1",
            technologies="Python",
            category="Web"
        )
        response = self.client.get(reverse('portfoly:projetos'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'portfoly/pages/projetos.html')
        self.assertIn('projects', response.context)
    
    def test_contato_view_get(self):
        """Testa view GET da página de contato"""
        response = self.client.get(reverse('portfoly:contato'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'portfoly/pages/contato.html')
        self.assertIsInstance(response.context['form'], ContactForm)
    
    def test_contato_view_post_valid(self):
        """Testa envio válido de formulário de contato"""
        data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'subject': 'Test Subject',
            'message': 'Test Message'
        }
        response = self.client.post(reverse('portfoly:contato'), data)
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertEqual(Contact.objects.count(), 1)
        contact = Contact.objects.first()
        self.assertEqual(contact.name, 'Test User')
    
    def test_contato_view_post_invalid(self):
        """Testa envio inválido de formulário de contato"""
        data = {
            'name': '',  # Campo obrigatório vazio
            'email': 'invalid_email',
            'subject': '',
            'message': ''
        }
        response = self.client.post(reverse('portfoly:contato'), data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Contact.objects.count(), 0)


# ============================================
# TESTES DE FORMS
# ============================================

class ContactFormTest(TestCase):
    """Testes para o formulário de contato"""
    
    def test_contact_form_valid(self):
        """Testa formulário válido"""
        form_data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'subject': 'Test Subject',
            'message': 'Test Message'
        }
        form = ContactForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_contact_form_invalid_email(self):
        """Testa formulário com email inválido"""
        form_data = {
            'name': 'Test User',
            'email': 'invalid_email',
            'subject': 'Test Subject',
            'message': 'Test Message'
        }
        form = ContactForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
    
    def test_contact_form_missing_required_fields(self):
        """Testa formulário com campos obrigatórios faltando"""
        form_data = {
            'name': '',
            'email': '',
            'subject': '',
            'message': ''
        }
        form = ContactForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 4)


# ============================================
# TESTES DE URLS
# ============================================

class URLsTest(TestCase):
    """Testes para as URLs do projeto"""
    
    def test_index_url_resolves(self):
        """Testa se URL da home resolve corretamente"""
        url = reverse('portfoly:index')
        self.assertEqual(url, '/')
    
    def test_sobre_url_resolves(self):
        """Testa se URL sobre resolve corretamente"""
        url = reverse('portfoly:sobre')
        self.assertEqual(url, '/sobre/')
    
    def test_projetos_url_resolves(self):
        """Testa se URL projetos resolve corretamente"""
        url = reverse('portfoly:projetos')
        self.assertEqual(url, '/projetos/')
    
    def test_contato_url_resolves(self):
        """Testa se URL contato resolve corretamente"""
        url = reverse('portfoly:contato')
        self.assertEqual(url, '/contato/')


# ============================================
# TESTES DE INTEGRAÇÃO
# ============================================

class IntegrationTest(TestCase):
    """Testes de integração do sistema"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(
            name="Admin User",
            email="admin@example.com",
            password=hashlib.sha256("admin123".encode()).hexdigest(),
            is_staff=True
        )
    
    def test_full_contact_flow(self):
        """Testa fluxo completo de contato"""
        # 1. Acessar página de contato
        response = self.client.get(reverse('portfoly:contato'))
        self.assertEqual(response.status_code, 200)
        
        # 2. Enviar formulário
        data = {
            'name': 'Integration Test',
            'email': 'integration@example.com',
            'subject': 'Integration Test Subject',
            'message': 'Integration Test Message'
        }
        response = self.client.post(reverse('portfoly:contato'), data)
        
        # 3. Verificar criação no banco
        self.assertEqual(Contact.objects.count(), 1)
        contact = Contact.objects.first()
        self.assertEqual(contact.name, 'Integration Test')
        self.assertFalse(contact.read)
    
    def test_project_display_flow(self):
        """Testa fluxo de exibição de projetos"""
        # 1. Criar projetos
        for i in range(5):
            Project.objects.create(
                user_id=self.user,
                title=f"Project {i}",
                technologies="Python, Django",
                category="Web"
            )
        
        # 2. Acessar página de projetos
        response = self.client.get(reverse('portfoly:projetos'))
        self.assertEqual(response.status_code, 200)
        
        # 3. Verificar se todos os projetos estão no contexto
        self.assertEqual(len(response.context['projects']), 5)
