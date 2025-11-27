from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

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
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    linkedin = models.CharField(max_length=100)
    github = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


# Class table Project

class Project(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    technologies = models.CharField(max_length=100)
    category = models.CharField(max_length=100, choices=Category.choices)
    link_demo = models.CharField(max_length=100, blank=True, null=True)
    link_github = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='projects', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    

# Class table Experiment

class Experiment(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    position = models.CharField(max_length=100)
    company = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    range_time = models.CharField(max_length=26, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.position
    

# Class table Skill

class Skill(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    level = models.CharField(max_length=100, choices=Level.choices, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
