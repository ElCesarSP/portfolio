from django.contrib import admin
from . import models

# Register your models here.

@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "email_formatado", "telefone", "linkedin", "github", "created_at")
    ordering = ("-id",)
    list_filter = ["name"]
    search_fields = ["name", "email", "phone"]
    list_per_page = 20
    list_max_show_all = 200
    list_display_links = ["id", "nome",]

    def id(self, obj):
        return obj.id
    id.short_description = "ID"

    def nome(self, obj):
        return obj.name
    nome.short_description = "Nome"

    def email_formatado(self, obj):
        return obj.email
    email_formatado.short_description = "E-mail"

    def telefone(self, obj):
        return obj.phone
    telefone.short_description = "Telefone"

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
    list_filter = ["created_at"]
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
    list_filter = ["created_at"]
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
    list_filter = ["created_at"]
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

