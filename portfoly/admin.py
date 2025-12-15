from django.contrib import admin
from . import models

# Register your models here.

@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "password", "is_staff", "is_active", "created_at")
    ordering = ("-id",)
    list_filter = ["name", "email", "is_staff", "is_active"]
    search_fields = ["name", "email", "is_staff", "is_active"]
    list_per_page = 20
    list_max_show_all = 200
    list_display_links = ["id", "name",]

    def id(self, obj):
        return obj.id
    id.short_description = "ID"

    def name(self, obj):
        return obj.name
    name.short_description = "Nome"

    def email(self, obj):
        return obj.email
    email.short_description = "Email"

    def password(self, obj):
        return obj.password
    password.short_description = "Senha"

    def is_staff(self, obj):
        return obj.is_staff
    is_staff.short_description = "Staff"

    def is_active(self, obj):
        return obj.is_active
    is_active.short_description = "Ativo"

    def created_at(self, obj):
        return obj.created_at
    created_at.short_description = "Data de Criação"    

@admin.register(models.UserDetails)
class UserDetailsAdmin(admin.ModelAdmin):
    list_display = ("id", "user_id", "phone", "linkedin", "github", "created_at")
    ordering = ("-id",)
    list_filter = ["user_id"]
    search_fields = ["user_id", "phone", "linkedin", "github"]
    list_per_page = 20
    list_max_show_all = 200
    list_display_links = ["id", "user_id",]

    def id(self, obj):
        return obj.id
    id.short_description = "ID"

    def user_id(self, obj):
        return obj.user_id
    user_id.short_description = "Usuário"

    def phone(self, obj):
        return obj.phone
    phone.short_description = "Telefone"

    def linkedin(self, obj):
        return obj.linkedin
    linkedin.short_description = "LinkedIn"

    def github(self, obj):
        return obj.github
    github.short_description = "GitHub"

    def created_at(self, obj):
        return obj.created_at
    created_at.short_description = "Data de Criação"


@admin.register(models.Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "user_id", "category", "technologies","created_at")
    ordering = ("-id",)
    list_filter = ["user_id", "category", "technologies"]
    search_fields = ["title", "category", "technologies"]
    list_per_page = 20
    list_max_show_all = 200
    list_display_links = ["id", "title",]

    def id(self, obj):
        return obj.id
    id.short_description = "ID"

    def title(self, obj):
        return obj.title
    title.short_description = "Título"

    def user_id(self, obj):
        return obj.user_id
    user_id.short_description = "Usuário"

    def category(self, obj):
        return obj.category
    category.short_description = "Categoria"

    def technologies(self, obj):
        return obj.technologies
    technologies.short_description = "Tecnologias"

    def created_at(self, obj):
        return obj.created_at
    created_at.short_description = "Data de Criação"


@admin.register(models.Experiment)
class ExperimentAdmin(admin.ModelAdmin):
    list_display = ("id", "position", "company", "description", "range_time", "created_at")
    ordering = ("-id",)
    list_filter = ["user_id", "position", "company", "range_time"]
    search_fields = ["position", "company", "range_time"]
    list_per_page = 20
    list_max_show_all = 200
    list_display_links = ["id", "position",]

    def id(self, obj):
        return obj.id
    id.short_description = "ID"

    def position(self, obj):
        return obj.position
    position.short_description = "Posição"

    def company(self, obj):
        return obj.company
    company.short_description = "Empresa"

    def description(self, obj):
        return obj.description
    description.short_description = "Descrição"

    def range_time(self, obj):
        return obj.range_time
    range_time.short_description = "Tempo"

    def created_at(self, obj):
        return obj.created_at
    created_at.short_description = "Data de Criação"

@admin.register(models.Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "level", "created_at")
    ordering = ("-id",)
    list_filter = ["user_id", "name", "level"]
    search_fields = ["name", "level"]
    list_per_page = 20
    list_max_show_all = 200
    list_display_links = ["id", "name"]

    def id(self, obj):
        return obj.id
    id.short_description = "ID"

    def name(self, obj):
        return obj.name
    name.short_description = "Nome"

    def level(self, obj):
        return obj.level
    level.short_description = "Nível"

    def created_at(self, obj):
        return obj.created_at
    created_at.short_description = "Data de Criação"


@admin.register(models.Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "subject", "read", "created_at")
    ordering = ("-id",)
    list_filter = ["read"]
    search_fields = ["name", "email", "subject", "message"]
    list_per_page = 20
    list_max_show_all = 200
    list_display_links = ["id", "name"]

    def id(self, obj):
        return obj.id
    id.short_description = "ID"

    def name(self, obj):
        return obj.name
    name.short_description = "Nome"

    def email(self, obj):
        return obj.email
    email.short_description = "Email"

    def subject(self, obj):
        return obj.subject
    subject.short_description = "Assunto"

    def read(self, obj):
        return obj.read
    read.short_description = "Lido"

    def created_at(self, obj):
        return obj.created_at
    created_at.short_description = "Data"


@admin.register(models.AuthToken)
class AuthTokenAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "token_preview", "is_active", "remember_me", "created_at", "expires_at")
    ordering = ("-id",)
    list_filter = ["is_active", "remember_me"]
    search_fields = ["user__name", "user__email"]
    list_per_page = 20
    list_display_links = ["id", "user"]

    def token_preview(self, obj):
        return f"{obj.token[:10]}..."
    token_preview.short_description = "Token"


@admin.register(models.PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "token_preview", "used", "created_at", "expires_at")
    ordering = ("-id",)
    list_filter = ["used"]
    search_fields = ["user__name", "user__email"]
    list_per_page = 20
    list_display_links = ["id", "user"]

    def token_preview(self, obj):
        return f"{obj.token[:10]}..."
    token_preview.short_description = "Token"

