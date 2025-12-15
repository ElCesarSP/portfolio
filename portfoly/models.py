from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

# Create your models here.


# Classe Level

class Level():
    basic = 'Basic'
    intermediate = 'Intermediate'
    advanced = 'Advanced'
    expert = 'Expert'
    master = 'Master'
    
    choices = (
        (basic, 'Basic'),
        (intermediate, 'Intermediate'),
        (advanced, 'Advanced'),
        (expert, 'Expert'),
        (master, 'Master'),
    )


# Classe Category

class Category():
    mobile = 'Mobile'
    web = 'Web'
    desktop = 'Desktop'
    android = 'Android'
    ios = 'iOS'
    game = 'Game'
    ia = 'IA'
    
    choices = (
        (mobile, 'Mobile'),
        (web, 'Web'),
        (desktop, 'Desktop'),
        (android, 'Android'),
        (ios, 'iOS'),
        (game, 'Game'),
        (ia, 'IA'),
    )


# Class table User
class User(models.Model):

    id = models.AutoField("ID",primary_key=True)
    name = models.CharField("Nome",max_length=100)
    email = models.EmailField("Email")
    password = models.CharField("Senha",max_length=100)
    is_staff = models.BooleanField("Staff",default=False)
    is_active = models.BooleanField("Ativo",default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name   

    class Meta:
        verbose_name = "Usuário Administrativo"
        verbose_name_plural = "Usuários Administrativos"


class UserDetails(models.Model):

    class Meta:
        verbose_name = "Detalhes do Usuário"
        verbose_name_plural = "Detalhes dos Usuários"

    id = models.AutoField("ID",primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField("Telefone",max_length=15)
    linkedin = models.CharField("LinkedIn",max_length=100)
    github = models.CharField("GitHub",max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user_id.name


# Class table Project

class Project(models.Model):

    class Meta:
        verbose_name = "Projeto"
        verbose_name_plural = "Projetos"

    id = models.AutoField("ID",primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField("Titulo",max_length=100)
    description = models.TextField("Descrição",blank=True, null=True)
    technologies = models.CharField("Tecnologias",max_length=100)
    category = models.CharField("Categoria",max_length=100, choices=Category.choices)
    link_demo = models.CharField("Link Demonstração",max_length=100, blank=True, null=True)
    link_github = models.CharField("Link GitHub",max_length=100, blank=True, null=True)
    image = models.ImageField("Imagem",upload_to='img/projects/%Y/%m/%d', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    

# Class table Experiment

class Experiment(models.Model):

    class Meta:
        verbose_name = "Experiência"
        verbose_name_plural = "Experiências"

    id = models.AutoField("ID",primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    position = models.CharField("Posição",max_length=100)
    company = models.CharField("Empresa",max_length=100, blank=True, null=True)
    description = models.TextField("Descrição",blank=True, null=True)
    range_time = models.CharField("Tempo",max_length=26, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.position
    

# Class table Skill

class Skill(models.Model):

    class Meta:
        verbose_name = "Habilidade"
        verbose_name_plural = "Habilidades"

    id = models.AutoField("ID",primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField("Nome",max_length=100)
    level = models.CharField("Nível",max_length=100, choices=Level.choices, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


# Class table Contact

class Contact(models.Model):

    class Meta:
        verbose_name = "Contato"
        verbose_name_plural = "Contatos"

    id = models.AutoField("ID", primary_key=True)
    name = models.CharField("Nome", max_length=100)
    email = models.EmailField("Email")
    subject = models.CharField("Assunto", max_length=200)
    message = models.TextField("Mensagem")
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField("Lido", default=False)

    def __str__(self):
        return f"{self.name} - {self.subject}"


# Class table AuthToken for admin authentication

class AuthToken(models.Model):

    class Meta:
        verbose_name = "Token de Autenticação"
        verbose_name_plural = "Tokens de Autenticação"

    id = models.AutoField("ID", primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='auth_tokens')
    token = models.CharField("Token", max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField("Expira em")
    is_active = models.BooleanField("Ativo", default=True)
    remember_me = models.BooleanField("Lembrar-me", default=False)

    def __str__(self):
        return f"Token de {self.user.name}"

    def is_expired(self):
        return timezone.now() > self.expires_at


# Class table PasswordResetToken for password recovery

class PasswordResetToken(models.Model):

    class Meta:
        verbose_name = "Token de Recuperação de Senha"
        verbose_name_plural = "Tokens de Recuperação de Senha"

    id = models.AutoField("ID", primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='password_reset_tokens')
    token = models.CharField("Token", max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField("Expira em")
    used = models.BooleanField("Usado", default=False)

    def __str__(self):
        return f"Reset Token de {self.user.name}"

    def is_expired(self):
        return timezone.now() > self.expires_at


# Class table ChatConversation for AI Chatbot

class ChatConversation(models.Model):

    class Meta:
        verbose_name = "Conversa do Chat"
        verbose_name_plural = "Conversas do Chat"
        ordering = ['-last_message_at']

    id = models.AutoField("ID", primary_key=True)
    session_id = models.CharField("ID da Sessão", max_length=255, unique=True)
    visitor_name = models.CharField("Nome do Visitante", max_length=100, blank=True, null=True)
    visitor_email = models.EmailField("Email do Visitante", blank=True, null=True)
    started_at = models.DateTimeField("Iniciada em", auto_now_add=True)
    last_message_at = models.DateTimeField("Última Mensagem", auto_now=True)
    is_active = models.BooleanField("Ativa", default=True)
    total_messages = models.IntegerField("Total de Mensagens", default=0)
    detected_intent = models.CharField(
        "Intenção Detectada",
        max_length=20,
        choices=(
            ('general', 'Geral'),
            ('project', 'Projeto'),
            ('contact', 'Contato'),
        ),
        default='general'
    )

    def __str__(self):
        if self.visitor_name:
            return f"Conversa com {self.visitor_name}"
        return f"Conversa {self.session_id[:8]}"


# Class table ChatMessage for individual chat messages

class ChatMessage(models.Model):

    class Meta:
        verbose_name = "Mensagem do Chat"
        verbose_name_plural = "Mensagens do Chat"
        ordering = ['created_at']

    id = models.AutoField("ID", primary_key=True)
    conversation = models.ForeignKey(
        ChatConversation,
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name="Conversa"
    )
    role = models.CharField(
        "Papel",
        max_length=10,
        choices=(
            ('user', 'Usuário'),
            ('assistant', 'Assistente'),
        )
    )
    content = models.TextField("Conteúdo")
    created_at = models.DateTimeField("Criada em", auto_now_add=True)

    def __str__(self):
        return f"{self.role}: {self.content[:50]}"


# Class table ProjectInquiry for project requests via chat

class ProjectInquiry(models.Model):

    class Meta:
        verbose_name = "Solicitação de Projeto"
        verbose_name_plural = "Solicitações de Projeto"
        ordering = ['-created_at']

    id = models.AutoField("ID", primary_key=True)
    conversation = models.ForeignKey(
        ChatConversation,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='project_inquiries',
        verbose_name="Conversa Relacionada"
    )
    client_name = models.CharField("Nome do Cliente", max_length=100)
    client_email = models.EmailField("Email do Cliente")
    client_phone = models.CharField("Telefone do Cliente", max_length=20, blank=True, null=True)
    project_type = models.CharField(
        "Tipo de Projeto",
        max_length=50,
        choices=Category.choices
    )
    project_description = models.TextField("Descrição do Projeto")
    budget_range = models.CharField("Faixa de Orçamento", max_length=100, blank=True, null=True)
    timeline = models.CharField("Prazo Desejado", max_length=100, blank=True, null=True)
    additional_info = models.TextField("Informações Adicionais", blank=True, null=True)
    status = models.CharField(
        "Status",
        max_length=20,
        choices=(
            ('new', 'Novo'),
            ('reviewing', 'Em Análise'),
            ('contacted', 'Contatado'),
            ('converted', 'Convertido'),
            ('declined', 'Recusado'),
        ),
        default='new'
    )
    admin_notes = models.TextField("Notas do Admin", blank=True, null=True)
    created_at = models.DateTimeField("Criada em", auto_now_add=True)
    updated_at = models.DateTimeField("Atualizada em", auto_now=True)

    def __str__(self):
        return f"Projeto: {self.client_name} - {self.project_type}"
