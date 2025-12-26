from django.urls import path

from . import views

app_name = "portfoly"

urlpatterns = [

    # Public pages
    path("", views.index, name="index"),
    path("about/", views.about, name="about"),
    path("projects/", views.project, name="projects"),
    path("contact/", views.contact, name="contact"),        

   # Admin authentication
    path("admin-panel/login/", views.admin_login, name="admin_login"),
    path("admin-panel/logout/", views.admin_logout, name="admin_logout"),
    path("admin-panel/password-reset-request/", views.password_reset_request, name="password_reset_request"),
    path("admin-panel/password-reset/<str:token>/", views.password_reset, name="password_reset"),
    
    # Admin dashboard
    path("admin-panel/", views.admin_dashboard, name="admin_dashboard"),
    
    # Projects CRUD
    path("admin-panel/projects/", views.admin_projects_list, name="admin_projects_list"),
    path("admin-panel/projects/create/", views.admin_project_create, name="admin_project_create"),
    path("admin-panel/projects/<int:pk>/", views.admin_project_detail, name="admin_project_detail"),
    path("admin-panel/projects/<int:pk>/edit/", views.admin_project_edit, name="admin_project_edit"),
    path("admin-panel/projects/<int:pk>/delete/", views.admin_project_delete, name="admin_project_delete"),
    
    # Experiments CRUD
    path("admin-panel/experiments/", views.admin_experiments_list, name="admin_experiments_list"),
    path("admin-panel/experiments/create/", views.admin_experiment_create, name="admin_experiment_create"),
    path("admin-panel/experiments/<int:pk>/", views.admin_experiment_detail, name="admin_experiment_detail"),
    path("admin-panel/experiments/<int:pk>/edit/", views.admin_experiment_edit, name="admin_experiment_edit"),
    path("admin-panel/experiments/<int:pk>/delete/", views.admin_experiment_delete, name="admin_experiment_delete"),
    
    # Skills CRUD
    path("admin-panel/skills/", views.admin_skills_list, name="admin_skills_list"),
    path("admin-panel/skills/create/", views.admin_skill_create, name="admin_skill_create"),
    path("admin-panel/skills/<int:pk>/", views.admin_skill_detail, name="admin_skill_detail"),
    path("admin-panel/skills/<int:pk>/edit/", views.admin_skill_edit, name="admin_skill_edit"),
    path("admin-panel/skills/<int:pk>/delete/", views.admin_skill_delete, name="admin_skill_delete"),
    
    # Contacts view
    path("admin-panel/contacts/", views.admin_contacts_list, name="admin_contacts_list"),
    path("admin-panel/contacts/<int:pk>/", views.admin_contact_detail, name="admin_contact_detail"),
    path("admin-panel/contacts/<int:pk>/mark-read/", views.admin_contact_mark_read, name="admin_contact_mark_read"),
    path("admin-panel/contacts/<int:pk>/mark-unread/", views.admin_contact_mark_unread, name="admin_contact_mark_unread"),
    
    # Profile
    path("admin-panel/profile/", views.admin_profile, name="admin_profile"),
    path("admin-panel/profile/change-password/", views.admin_change_password, name="admin_change_password"),
]