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

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

    id = models.AutoField("ID",primary_key=True)
    name = models.CharField("Nome",max_length=100)
    email = models.EmailField("Email")
    phone = models.CharField("Telefone",max_length=15)
    linkedin = models.CharField("LinkedIn",max_length=100)
    github = models.CharField("GitHub",max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


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


